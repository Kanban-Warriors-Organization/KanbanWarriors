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
        try:
            user_profile = UserProfile.objects.get(user=self.user)
            
            try:
                battle = Battle.objects.get(room_id=self.room_id)
                
                # If battle exists, try to join it
                if battle.status == 'completed':
                    return {'event': 'error', 'message': 'This battle has ended'}
                    
                if battle.player1.user == self.user:
                    # Reconnecting as player 1
                    if battle.player2:
                        # If player 2 exists, return battle state
                        return {
                            'event': 'battle_state',
                            'is_player1': True,
                            'opponent_name': battle.player2.user.username,
                            'status': battle.status,
                            'both_ready': battle.both_ready(),
                            'current_turn': battle.current_turn if battle.status == 'in_progress' else None
                        }
                    else:
                        # Still waiting for player 2
                        return {
                            'event': 'battle_created',
                            'is_player1': True,
                            'status': 'waiting'
                        }
                elif battle.player2 and battle.player2.user == self.user:
                    # Reconnecting as player 2
                    return {
                        'event': 'battle_state',
                        'is_player1': False,
                        'opponent_name': battle.player1.user.username,
                        'status': battle.status,
                        'both_ready': battle.both_ready(),
                        'current_turn': battle.current_turn if battle.status == 'in_progress' else None
                    }
                elif not battle.player2:
                    # Join as player 2
                    battle.player2 = user_profile
                    battle.status = 'selecting'
                    battle.save()
                    
                    # Notify both players with the same event
                    return {
                        'event': 'battle_joined',
                        'notify_room': True,  # This will send to both players
                        'username': self.user.username,
                        'is_player1': False,  # This player is player 2
                        'opponent_name': battle.player1.user.username,
                        'status': 'selecting'
                    }
                else:
                    return {'event': 'error', 'message': 'Battle room is full'}
                    
            except Battle.DoesNotExist:
                # Create new battle if it doesn't exist
                battle = Battle.objects.create(
                    room_id=self.room_id,
                    player1=user_profile,
                    status='selecting'  # Changed from 'waiting' to 'selecting'
                )
                return {
                    'event': 'battle_created',
                    'is_player1': True,
                    'status': 'selecting'  # Add status to signal the creator should select cards
                }
                
        except Exception as e:
            return {'event': 'error', 'message': str(e)}

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
        event = data.get('event', '')
        
        if event == 'request_state':
            result = await self.get_current_state()
            
            # If we need to fetch cards, do it here in the async function
            if result.get('needs_cards'):
                cards_result = await self.handle_request_current_cards()
                if 'player_card' in cards_result:
                    result['player_card'] = cards_result['player_card']
                    result['opponent_card'] = cards_result['opponent_card']
                    result['is_my_turn'] = cards_result['is_my_turn']
                # Remove the needs_cards flag
                if 'needs_cards' in result:
                    del result['needs_cards']
                    
        elif event == 'select_cards':
            result = await self.handle_select_cards(data)
        elif event == 'ready':
            result = await self.handle_player_ready()
        elif event == 'select_stat':
            result = await self.handle_select_stat(data)
        elif event == 'request_current_cards':
            result = await self.handle_request_current_cards()
        else:
            result = {'event': 'error', 'message': f'Unknown event type: {event}'}

        # Send response to the requesting client
        await self.send(text_data=json.dumps(result))
        
        # If the event should be broadcast, send to the room
        if result.get('notify_room'):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'battle_message',
                    'message': {k: v for k, v in result.items() if k != 'notify_room'}
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
                defaults={
                    'current_card_index': 0,
                    'shuffle_seed': random.randint(1, 1000000)  # Add unique seed
                }
            )
            
            # Clear existing cards and add new ones
            deck.cards.clear()
            
            for card in cards:
                deck.cards.add(card)
                
            deck.current_card_index = 0
            deck.save()
            
            return {
                'event': 'cards_selected',
                'username': self.user.username,
                'message': f'{self.user.username} has selected their cards'
            }
            
        except Exception as e:
            return {'event': 'error', 'message': str(e)}
    
    @database_sync_to_async
    def handle_player_ready(self):
        """
        Handles a player indicating they are ready to battle.
        Broadcasts the state change to all players.
        """
        try:
            user_profile = UserProfile.objects.get(user=self.user)
            battle = Battle.objects.get(room_id=self.room_id)
            
            # Mark the player as ready
            if battle.player1.user == self.user:
                battle.player1_ready = True
            elif battle.player2 and battle.player2.user == self.user:
                battle.player2_ready = True
            
            both_ready = battle.player1_ready and battle.player2_ready 
            
            # Start battle if both players are ready
            if both_ready and battle.status == 'selecting':
                battle.status = 'in_progress'
                battle.current_turn = 1
                
            battle.save()
            
            return {
                'event': 'player_ready',
                'notify_room': True,
                'username': self.user.username,
                'both_ready': both_ready,
                'battle_status': battle.status,
                'first_turn': battle.current_turn if both_ready else None
            }
                
        except Exception as e:
            return {'event': 'error', 'message': str(e)}

    @database_sync_to_async
    def handle_request_current_cards(self):
        try:
            battle = Battle.objects.get(room_id=self.room_id)
            is_player1 = battle.player1.user == self.user
            
            # Get current decks for both players
            p1_deck = BattleDeck.objects.get(battle=battle, player=battle.player1)
            p2_deck = BattleDeck.objects.get(battle=battle, player=battle.player2)
            
            p1_cards = list(p1_deck.cards.all())
            p2_cards = list(p2_deck.cards.all())

            # Use the stored seeds to shuffle consistently but differently
            random.Random(p1_deck.shuffle_seed).shuffle(p1_cards)
            random.Random(p2_deck.shuffle_seed).shuffle(p2_cards)
            
            # Check if we've reached the end of the cards
            if p1_deck.current_card_index >= len(p1_cards) or p2_deck.current_card_index >= len(p2_cards):
                return self.end_battle(battle)
            
            # Get the current card for each player
            p1_card = p1_cards[p1_deck.current_card_index] if p1_deck.current_card_index < len(p1_cards) else None
            p2_card = p2_cards[p2_deck.current_card_index] if p2_deck.current_card_index < len(p2_cards) else None
            
            # If either card is None, we can't continue
            if not p1_card or not p2_card:
                return {'event': 'error', 'message': 'Cards not available'}
            
            # Create the result with common data for both players
            result = {
                'event': 'current_cards',
                'current_turn': battle.current_turn,
                'player1_score': battle.player1_score,
                'player2_score': battle.player2_score,
                'cards_remaining': min(len(p1_cards) - p1_deck.current_card_index, len(p2_cards) - p2_deck.current_card_index)
            }
            
            # Add player-specific data
            if is_player1:
                result['player_card'] = self.card_to_dict(p1_card)
                result['opponent_card'] = {
                    'name': p2_card.card_name,
                    'image': p2_card.card_image_link.url if p2_card.card_image_link else None
                }
                result['is_my_turn'] = battle.current_turn == 1
            else:
                result['player_card'] = self.card_to_dict(p2_card)
                result['opponent_card'] = {
                    'name': p1_card.card_name,
                    'image': p1_card.card_image_link.url if p1_card.card_image_link else None
                }
                result['is_my_turn'] = battle.current_turn == 2
            
            return result
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'event': 'error', 'message': str(e)}
    
    @database_sync_to_async
    def handle_select_stat(self, data):
        try:
            stat = data.get('stat')
            if stat not in ['environmental_friendliness', 'beauty', 'cost']:
                return {'event': 'error', 'message': 'Invalid stat selected'}
            
            battle = Battle.objects.get(room_id=self.room_id)
            is_player1 = battle.player1.user == self.user
            
            # Verify it's this player's turn
            if (is_player1 and battle.current_turn != 1) or (not is_player1 and battle.current_turn != 2):
                return {'event': 'error', 'message': 'Not your turn'}
            
            # Get current decks and cards
            p1_deck = BattleDeck.objects.get(battle=battle, player=battle.player1)
            p2_deck = BattleDeck.objects.get(battle=battle, player=battle.player2)
            
            p1_cards = list(p1_deck.cards.all())
            p2_cards = list(p2_deck.cards.all())
            
            # Check if we've reached the end of the battle
            if p1_deck.current_card_index >= len(p1_cards) or p2_deck.current_card_index >= len(p2_cards):
                return self.end_battle(battle)
            
            # Get current cards
            p1_card = p1_cards[p1_deck.current_card_index]
            p2_card = p2_cards[p2_deck.current_card_index]
            
            # Compare stats and determine winner
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
            
            # Move to next cards
            p1_deck.current_card_index += 1
            p2_deck.current_card_index += 1
            p1_deck.save()
            p2_deck.save()
            
            # Switch turns
            battle.current_turn = 2 if battle.current_turn == 1 else 1
            battle.save()
            
            # Create full response with all card details visible to both players
            response = {
                'event': 'round_result',
                'notify_room': True,  # Send to both players
                'stat': stat,
                'p1_card': self.card_to_dict(p1_card, p1_value),
                'p2_card': self.card_to_dict(p2_card, p2_value),
                'result': result,
                'player1_score': battle.player1_score,
                'player2_score': battle.player2_score,
                'next_turn': battle.current_turn,
                'cards_remaining': min(len(p1_cards) - p1_deck.current_card_index, len(p2_cards) - p2_deck.current_card_index)
            }
            
            # If this was the last card, end the battle
            if response['cards_remaining'] <= 0:
                end_result = self.end_battle(battle)
                if end_result:
                    return end_result
            
            return response
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'event': 'error', 'message': str(e)}

    def card_to_dict(self, card, value=None):
        """Helper method to convert a card to a dictionary"""
        result = {
            'name': card.card_name,
            'image': card.card_image_link.url if card.card_image_link else None,
            'environmental_friendliness': card.environmental_friendliness,
            'beauty': card.beauty,
            'cost': card.cost
        }
        if value is not None:
            result['value'] = value
        return result

    def end_battle(self, battle):
        """Helper method to end the battle and award points"""
        # Determine winner
        if battle.player1_score > battle.player2_score:
            battle.winner = battle.player1
        elif battle.player2_score > battle.player1_score:
            battle.winner = battle.player2
        # if tie, winner remains null
        
        battle.status = 'completed'
        battle.save()
        
        # Award points to users
        if battle.winner:
            if battle.winner == battle.player1:
                battle.player1.user_profile_points += 10  # Winner gets 10 points
                battle.player2.user_profile_points += 2   # Loser gets 2 points
            else:
                battle.player2.user_profile_points += 10
                battle.player1.user_profile_points += 2
            
            battle.player1.save()
            battle.player2.save()
        else:
            # In case of a tie, both get 5 points
            battle.player1.user_profile_points += 5
            battle.player2.user_profile_points += 5
            battle.player1.save()
            battle.player2.save()
        
        return {
            'event': 'battle_completed',
            'notify_room': True,  # Send to both players
            'winner': battle.winner.user.username if battle.winner else None,
            'is_tie': battle.winner is None,
            'player1_score': battle.player1_score,
            'player2_score': battle.player2_score,
            'player1_name': battle.player1.user.username,
            'player2_name': battle.player2.user.username
        }
    
    @database_sync_to_async
    def get_current_state(self):
        try:
            battle = Battle.objects.get(room_id=self.room_id)
            is_player1 = battle.player1.user == self.user
            opponent = battle.player2 if is_player1 else battle.player1
            
            state = {
                'event': 'battle_state',
                'status': battle.status,
                'is_player1': is_player1,
                'opponent_name': opponent.user.username if opponent else None,
                'both_ready': battle.both_ready(),
                'current_turn': battle.current_turn if battle.status == 'in_progress' else None,
                'player1_score': battle.player1_score,
                'player2_score': battle.player2_score
            }
            
            # If battle is in progress, include current cards
            if battle.status == 'in_progress':
                # We can't use await inside a sync function
                # Instead, return a flag indicating we need cards
                state['needs_cards'] = True
            
            return state
            
        except Battle.DoesNotExist:
            return {'event': 'error', 'message': 'Battle not found'}
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'event': 'error', 'message': str(e)}
    
    # Send message to WebSocket
    async def battle_message(self, event):
        message = event['message']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))