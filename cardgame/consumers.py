import json
import random
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Battle, BattleDeck, UserProfile, Card

class BattleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'battle_{self.room_id}'
        self.user = self.scope["user"]
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Set up the battle or join existing one
        if self.user.is_authenticated:
            result = await self.setup_battle()
            
            # Send response to the connecting client
            await self.send(text_data=json.dumps(result))
            
            # If this is player 2 joining, notify the room
            if result.get('notify_room'):
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'battle_message',
                        'message': {
                            'event': 'user_connected',
                            'username': result.get('username')
                        }
                    }
                )
        else:
            await self.send(text_data=json.dumps({
                'event': 'error',
                'message': 'You must be logged in to join a battle.'
            }))
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        # Update battle status if user disconnects
        if self.user.is_authenticated:
            await self.handle_disconnect()
    
    @database_sync_to_async
    def setup_battle(self):
        user_profile = UserProfile.objects.get(user=self.user)
        battle, created = Battle.objects.get_or_create(
            room_id=self.room_id,
            defaults={'player1': user_profile, 'status': 'waiting'}
        )
        
        if created:
            # This user created the battle
            return {'event': 'battle_created', 'is_creator': True}
        else:
            # Battle exists, check if can join as player 2
            if battle.player2 is None and battle.player1.user != self.user:
                battle.player2 = user_profile
                battle.status = 'selecting'
                battle.save()
                
                # Return event for the joining player along with a flag to notify others
                return {
                    'event': 'battle_joined', 
                    'is_creator': False,
                    'notify_room': True,
                    'username': self.user.username
                }
            elif battle.player1.user == self.user or (battle.player2 and battle.player2.user == self.user):
                # User is already in this battle
                return {'event': 'battle_rejoined', 'is_creator': battle.player1.user == self.user}
            else:
                # Battle is full
                return {'event': 'error', 'message': 'Battle room is full'}
    
    @database_sync_to_async
    def handle_disconnect(self):
        try:
            user_profile = UserProfile.objects.get(user=self.user)
            battle = Battle.objects.get(room_id=self.room_id)
            
            # If battle is not completed, handle player leaving
            if battle.status != 'completed':
                # If player 1 leaves, end the battle
                if battle.player1.user == self.user:
                    if battle.player2:
                        battle.winner = battle.player2
                    battle.status = 'completed'
                # If player 2 leaves, player 1 wins
                elif battle.player2 and battle.player2.user == self.user:
                    battle.winner = battle.player1
                    battle.status = 'completed'
                
                battle.save()
                return {'event': 'player_left', 'username': self.user.username}
        except Exception as e:
            return {'event': 'error', 'message': str(e)}
    
    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data.get('event', '')

        if event_type == 'select_cards':
            result = await self.handle_select_cards(data)
        elif event_type == 'ready':
            result = await self.handle_player_ready()
        elif event_type == 'select_stat':
            result = await self.handle_select_stat(data)
        elif event_type == 'request_current_cards':
            result = await self.handle_request_current_cards()
        else:
            result = {'event': 'error', 'message': f'Unknown event type: {event_type}'}

        # Send response to the user
        await self.send(text_data=json.dumps(result))
        
        # If there's a notification for the room, send it
        if result.get('notify_room', False):
            event_to_broadcast = {
                'event': 'user_connected',
                'username': self.user.username
            }
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'battle_message',
                    'message': event_to_broadcast
                }
            )
    
    @database_sync_to_async
    def handle_select_cards(self, data):
        try:
            card_ids = data.get('card_ids', [])
            if len(card_ids) != 4:
                return {'event': 'error', 'message': 'You must select exactly 4 cards'}
            
            user_profile = UserProfile.objects.get(user=self.user)
            battle = Battle.objects.get(room_id=self.room_id)
            
            # Check if player has these cards
            cards = Card.objects.filter(card_name__in=card_ids)
            if cards.count() != 4:
                return {'event': 'error', 'message': 'One or more cards not found'}
            
            # Create or update battle deck
            deck, created = BattleDeck.objects.get_or_create(
                battle=battle,
                player=user_profile,
                defaults={'current_card_index': 0}
            )
            
            # Clear existing cards and add new ones
            deck.cards.clear()
            for card in cards:
                deck.cards.add(card)
            
            # Shuffle the order by creating a list and randomizing it
            card_list = list(deck.cards.all())
            random.shuffle(card_list)
            
            # Need to save the order somehow - could add a through model with order field
            # For now, just notify that cards were selected
            
            return {
                'event': 'cards_selected',
                'username': self.user.username,
                'message': f'{self.user.username} has selected their cards'
            }
            
        except Exception as e:
            return {'event': 'error', 'message': str(e)}
    
    @database_sync_to_async
    def handle_player_ready(self):
        try:
            user_profile = UserProfile.objects.get(user=self.user)
            battle = Battle.objects.get(room_id=self.room_id)
            
            # Mark the player as ready
            if battle.player1.user == self.user:
                battle.player1_ready = True
            elif battle.player2 and battle.player2.user == self.user:
                battle.player2_ready = True
            
            # If both players are ready, start the battle
            if battle.player1_ready and battle.player2_ready and battle.status == 'selecting':
                battle.status = 'in_progress'
                battle.current_turn = 1  # Player 1 goes first
            
            battle.save()
            
            return {
                'event': 'player_ready',
                'username': self.user.username,
                'both_ready': battle.player1_ready and battle.player2_ready,
                'battle_status': battle.status,
                'first_turn': battle.current_turn if battle.player1_ready and battle.player2_ready else None
            }
            
        except Exception as e:
            return {'event': 'error', 'message': str(e)}

    @database_sync_to_async
    def handle_request_current_cards(self):
        try:
            user_profile = UserProfile.objects.get(user=self.user)
            battle = Battle.objects.get(room_id=self.room_id)
            
            # Get current decks for both players
            p1_deck = BattleDeck.objects.get(battle=battle, player=battle.player1)
            p2_deck = BattleDeck.objects.get(battle=battle, player=battle.player2)
            
            p1_cards = list(p1_deck.cards.all())
            p2_cards = list(p2_deck.cards.all())
            
            # Get the current card for each player
            p1_card = p1_cards[p1_deck.current_card_index] if p1_deck.current_card_index < len(p1_cards) else None
            p2_card = p2_cards[p2_deck.current_card_index] if p2_deck.current_card_index < len(p2_cards) else None
            
            # Only include information that should be visible to this player
            is_player1 = battle.player1.user == self.user
            
            result = {
                'event': 'current_cards',
                'current_turn': battle.current_turn,
            }
            
            # Include detailed player card info
            if is_player1:
                result['player_card'] = {
                    'name': p1_card.card_name,
                    'image': p1_card.card_image_link.url if p1_card.card_image_link else None,
                    'environmental_friendliness': p1_card.environmental_friendliness,
                    'beauty': p1_card.beauty,
                    'cost': p1_card.cost
                }
                result['opponent_card'] = {
                    'name': p2_card.card_name,  # Only show name
                    'image': p2_card.card_image_link.url if p2_card.card_image_link else None
                }
            else:
                result['player_card'] = {
                    'name': p2_card.card_name,
                    'image': p2_card.card_image_link.url if p2_card.card_image_link else None,
                    'environmental_friendliness': p2_card.environmental_friendliness,
                    'beauty': p2_card.beauty,
                    'cost': p2_card.cost
                }
                result['opponent_card'] = {
                    'name': p1_card.card_name,  # Only show name 
                    'image': p1_card.card_image_link.url if p1_card.card_image_link else None
                }
            
            return result
        except Exception as e:
            return {'event': 'error', 'message': str(e)}
    
    @database_sync_to_async
    def handle_select_stat(self, data):
        try:
            stat = data.get('stat')
            if stat not in ['environmental_friendliness', 'beauty', 'cost']:
                return {'event': 'error', 'message': 'Invalid stat selected'}
            
            user_profile = UserProfile.objects.get(user=self.user)
            battle = Battle.objects.get(room_id=self.room_id)
            
            # Check if it's this player's turn
            is_player1 = battle.player1.user == self.user
            if (is_player1 and battle.current_turn != 1) or (not is_player1 and battle.current_turn != 2):
                return {'event': 'error', 'message': 'Not your turn'}
            
            # Get current cards for both players
            p1_deck = BattleDeck.objects.get(battle=battle, player=battle.player1)
            p2_deck = BattleDeck.objects.get(battle=battle, player=battle.player2)
            
            # Get the current card for each player
            p1_cards = list(p1_deck.cards.all())
            p2_cards = list(p2_deck.cards.all())
            
            if p1_deck.current_card_index >= len(p1_cards) or p2_deck.current_card_index >= len(p2_cards):
                # Battle is over, determine winner
                if battle.player1_score > battle.player2_score:
                    battle.winner = battle.player1
                elif battle.player2_score > battle.player1_score:
                    battle.winner = battle.player2
                
                battle.status = 'completed'
                battle.save()
                
                # Award points to users
                if battle.winner == battle.player1:
                    battle.player1.user_profile_points += 10  # Winner gets 10 points
                    battle.player2.user_profile_points += 2   # Loser gets 2 points
                else:
                    battle.player2.user_profile_points += 10
                    battle.player1.user_profile_points += 2
                
                battle.player1.save()
                battle.player2.save()
                
                return {
                    'event': 'battle_completed',
                    'winner': battle.winner.user.username,
                    'player1_score': battle.player1_score,
                    'player2_score': battle.player2_score
                }
            
            p1_card = p1_cards[p1_deck.current_card_index]
            p2_card = p2_cards[p2_deck.current_card_index]
            
            # Compare the chosen stat
            p1_value = getattr(p1_card, stat)
            p2_value = getattr(p2_card, stat)
            
            # For cost, lower is better
            if stat == 'cost':
                p1_wins = p1_value < p2_value
                tie = p1_value == p2_value
            else:
                # For other stats, higher is better
                p1_wins = p1_value > p2_value
                tie = p1_value == p2_value
            
            # Update scores
            if tie:
                battle.player1_score += 1
                battle.player2_score += 1
                result = "tie"
            elif p1_wins:
                battle.player1_score += 3
                result = "player1"
            else:
                battle.player2_score += 3
                result = "player2"
            
            # Move to next card
            p1_deck.current_card_index += 1
            p2_deck.current_card_index += 1
            p1_deck.save()
            p2_deck.save()
            
            # Switch turns
            battle.current_turn = 2 if battle.current_turn == 1 else 1
            battle.save()
            
            # Return the comparison result
            return {
                'event': 'round_result',
                'stat': stat,
                'p1_card': {
                    'name': p1_card.card_name,
                    'value': p1_value,
                    'image': p1_card.card_image_link.url if p1_card.card_image_link else None
                },
                'p2_card': {
                    'name': p2_card.card_name,
                    'value': p2_value,
                    'image': p2_card.card_image_link.url if p2_card.card_image_link else None
                },
                'result': result,
                'player1_score': battle.player1_score,
                'player2_score': battle.player2_score,
                'next_turn': battle.current_turn,
                'cards_remaining': len(p1_cards) - p1_deck.current_card_index
            }
            
        except Exception as e:
            return {'event': 'error', 'message': str(e)}
    
    # Send message to WebSocket
    async def battle_message(self, event):
        message = event['message']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))