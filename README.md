# ⚔️ KanbanWarriors 🛡️

## Overview

KanbanWarriors is a location-based card collecting game built with Django, designed to encourage exploration and engagement with the real world. Players discover digital cards by visiting real-world locations, building a unique collection, and participating in exciting challenges. Compete on leaderboards, uncover new cards, and become the ultimate KanbanWarrior!

## Goals

The primary goals of KanbanWarriors are to:

- **Gamify Real-World Exploration:** Encourage users to explore their surroundings by linking gameplay to physical locations.
- **Create a Collectible Card System:** Implement a fun and engaging system for collecting digital cards with rich information and visual appeal.
- **Develop Location-Based Challenges:** Offer interactive challenges at specific locations to drive user engagement and reward exploration.
- **Foster Competition and Community:** Incorporate leaderboards and social features to encourage friendly competition and community building (future development).
- **Provide a User-Friendly Experience:** Design an intuitive and enjoyable game experience across all user interfaces.

## ✨ Highlights ✨

- **Interactive Map with Leaflet:** A dynamic map powered by Leaflet displays card locations and the user's real-time position, enhancing location-based gameplay. (javascript:static/js/map.js)
- **Comprehensive Card Collection System:** Users can seamlessly collect, view, and manage their growing card collections within their profiles. (html:cardgame/templates/card_col.html)
- **Engaging Location-Based Challenges:** Participate in time-sensitive challenges at real locations to earn exclusive cards and climb the leaderboard. (html:cardgame/templates/cardgame/challenges.html)
- **Global Leaderboard:** Compete against other players worldwide and track your ranking on the real-time leaderboard. (javascript:static/js/leaderboard.js)
- **"Recent Card" Feature:** Stay informed about the newest card additions to the game, ensuring you never miss out on exciting content. (javascript:static/js/recent_card.js)
- **Secure User Authentication:** Robust user accounts with secure login and signup functionality protect player progress and personal information. (html:cardgame/templates/cardgame/login.html, html:cardgame/templates/cardgame/signup.html)
- **Django Admin Panel:** A powerful Django admin interface allows administrators to efficiently manage cards, challenges, user accounts, and game settings.
- **Automated Testing and Linting:** Implemented CI workflows for automated testing and code quality checks using GitHub Actions, ensuring a stable and reliable game. (.github/workflows/django.yml, .github/workflows/lint_with_flake8.yml)

## 🚀 Getting Started

Embark on your KanbanWarriors adventure by setting up the project locally!

### 🛠️ Requirements

Ensure the following prerequisites are installed on your system:

- **Python:** Version 3.13.2 is highly recommended for optimal compatibility. Download from [python.org](https://www.python.org/downloads/).
- **pip:** Python package installer, typically included with Python installations. Verify installation by running `pip --version` in your terminal.
- **virtualenv:** Tool for creating isolated Python environments. Install using:
  ```bash
  pip install virtualenv
  ```

### ⚙️ Installation Guide

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Kanban-Warriors-Organization/KanbanWarriors.git
   cd KanbanWarriors
   ```

2. **Create a Virtual Environment:**
   Isolate project dependencies within a virtual environment:

   ```bash
   virtualenv .venv
   ```

3. **Activate the Virtual Environment:**
   Activate the environment to use project-specific dependencies:

   - **macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```
   - **Windows:**
     ```bash
     .venv\Scripts\activate
     ```

4. **Install Project Dependencies:**
   Install required Python packages from `requirements.txt`:
   ```bash
   pip install --upgrade pip # Ensure pip is up-to-date
   pip install -r .github/requirements.txt
   ```

### 🎮 Usage Instructions

#### 🏃 Running the Development Server

1. **Navigate to the project root directory** in your terminal.
2. **Activate the virtual environment** (if not already active).
3. **Apply Database Migrations:**
   Initialize the database schema:
   ```bash
   python manage.py migrate
   ```
4. **Start the Django Development Server:**
   Launch the server to run the game locally:
   ```bash
   python manage.py runserver
   ```
5. **Access KanbanWarriors:** Open your web browser and navigate to `http://127.0.0.1:8000/` to start playing!

#### 🧪 Running Tests

1. **Ensure the virtual environment is activated.**
2. **Execute the Test Suite:**
   Run tests to verify application functionality using pytest:
   ```bash
   pytest cardgame
   ```
   A successful test run ensures the application is functioning as expected.

## 🧰 Technologies Used

| Library     | Version | Purpose                                                                                                 |
| :---------- | :------ | :------------------------------------------------------------------------------------------------------ |
| **Django**  | 5.1.6   | The robust web framework powering the game. Handles backend logic, database interactions, and routing.  |
| **Pillow**  | 11.1.0  | Image processing library used for card image generation and manipulation.                               |
| **Leaflet** | N/A     | JavaScript library for creating interactive maps, used for displaying card locations and user position. |
| **SQLite**  | N/A     | Lightweight, file-based database used for development.                                                  |
| **pytest**  | N/A     | Testing framework used for writing and running tests.                                                   |
| **flake8**  | N/A     | Linting tool for code style checking and quality assurance.                                             |

## ✅ Features

KanbanWarriors is packed with features to provide an engaging gameplay experience:

- [x] **Collect Cards:** Discover and collect a variety of unique digital cards.
- [x] **GPS Location Integration:** Utilize your device's GPS to find cards and challenges at real-world locations.
- [x] **Detailed Card Information:** Learn about each card with rich descriptions, subtitles, and vibrant images.
- [x] **User Profiles:** Create and customize your player profile to track your card collection and game progress.
- [x] **Leaderboard:** Compete with friends and other players for the top spot on the global leaderboard.
- [x] **Challenges:** Participate in location-based challenges to earn exclusive rewards and cards.
- [x] **Card Sets:** Cards are organized into sets, encouraging collection completion. (lines: 64-65, cardgame/models.py)
- [x] **Recent Card Display:** Stay updated with the latest card releases directly on the homepage. (lines: 72-79, html:cardgame/templates/cardgame/home.html)
- [ ] **Battles:** Engage in strategic battles with other players or AI opponents using your card collections.
- [ ] **Trading Cards:** Trade cards with other players to complete your sets and acquire rare cards.
- [ ] **In-Game Currency:** Earn and use in-game currency for various game enhancements and items.
- [ ] **Scavenger Hunts:** Participate in complex, multi-location scavenger hunts for valuable rewards.

## 🔮 Potential Future Features

These are features that could be added to KanbanWarriors in the future:

- Badges for Collections
- Social Media Sharing
- Daily/Weekly Challenges & Combos
- Wagers on Battles
- Bot Battles
- Staff Challenges
- Augmented Reality (AR) Features

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
