# ⚔️ KanbanWarriors 🛡️

## Overview

KanbanWarriors is a location-based card collecting game built with Django. Explore your surroundings, collect digital cards at real-world locations, and build your ultimate card collection! Engage in challenges, compete on leaderboards, and discover the world around you in a fun, interactive way.

## Goals

This project aims to create an engaging and interactive mobile game experience centered around card collecting and location-based challenges. The core goals are to:

- **Collect Cards:** Allow users to discover and collect digital cards at various locations.
- **GPS Location Integration:** Utilize GPS to enable location-based gameplay and card discovery.
- **Card Information:** Provide detailed information and descriptions for each collectible card.
- **Challenges:** Implement location-based challenges for users to participate in and earn rewards.
- **User Profiles:** Create personalized user profiles to track progress and card collections.

## ✨ Highlights ✨

- **Dynamic Map Integration:** Uses Leaflet to display an interactive map with card locations and user position.
- **Card Collection System:** Users can collect and view their acquired cards.
- **Location-Based Challenges:** Participate in challenges at real-world locations to earn cards and points.
- **Leaderboard:** Compete with other players and climb the ranks on the global leaderboard.
- **Recent Card Feature:** Stay updated with the latest card additions to the game.
- **User Authentication:** Secure user accounts with login and signup functionality.
- **Admin Panel:** Django admin interface for managing cards, challenges, and users.

## 🚀 Getting Started

Get ready to embark on your KanbanWarriors journey! Follow these steps to set up the project on your local machine.

### 🛠️ Requirements

Before you begin, ensure you have the following installed:

- **Python:** Version 3.13.2 is recommended. You can download it from [python.org](https://www.python.org/downloads/).
- **pip:** Python package installer (usually included with Python installations).
- **virtualenv:** For creating isolated Python environments. Install it using:
  ```bash
  pip install virtualenv
  ```

### ⚙️ How to Install

1. **Clone the repository:**

   ```bash
   git clone [repository URL] # Replace with your repository URL
   cd KanbanWarriors
   ```

2. **Create a virtual environment:**

   ```bash
   virtualenv .venv
   ```

3. **Activate the virtual environment:**

   - **On macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```
   - **On Windows:**
     ```bash
     .venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r .github/requirements.txt
   ```

### 🎮 How to Use

#### 🏃 Run the Project

1. **Navigate to the project directory** if you are not already there.
2. **Activate the virtual environment** (see installation step 3 if not already activated).
3. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```
4. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
5. **Access the game:** Open your web browser and go to `http://127.0.0.1:8000/`.

#### 🧪 Run Tests

1. **Ensure the virtual environment is activated.**
2. **Run the test suite:**
   ```bash
   python manage.py test cardgame/tests
   ```
   All tests should pass, indicating a healthy application state.

## 📚 Libraries Used

| Library     | Version | Purpose                                                                                                 |
| :---------- | :------ | :------------------------------------------------------------------------------------------------------ |
| **Django**  | 5.1.6   | The robust web framework powering the game. Handles backend logic, database interactions, and routing.  |
| **Pillow**  | 11.1.0  | Image processing library used for card image generation and manipulation.                               |
| **Leaflet** | N/A     | JavaScript library for creating interactive maps, used for displaying card locations and user position. |

## ✅ Features

Here's a breakdown of the features in KanbanWarriors:

- [x] Collect Cards
- [x] GPS Location Integration (for card locations and user tracking)
- [x] Information on Cards (name, subtitle, description, image)
- [x] User Profiles (basic profile functionality)
- [x] Leaderboard (tracks top players)
- [x] Challenges (location-based events)
- [ ] Battles (Player vs Player or Player vs Bot battles)
- [ ] Trading Cards
- [ ] Currency (in-game currency system)
- [ ] Scavenger Hunt (more complex location-based tasks)
- [ ] Badges for Collections
- [ ] Sharing on Social Media
- [ ] Daily/Weekly Challenges/Combos
- [ ] Wagers on Battles
- [ ] Bot Battles
- [ ] Staff Challenges
- [ ] Augmented Reality (AR) Features

## 📜 License

This project is currently unlicensed. Consider adding a license such as MIT License for open-source distribution.
