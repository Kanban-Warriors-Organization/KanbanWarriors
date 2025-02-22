# ⚔️ EcoSplore 🛡️

## 🌍 Overview

EcoSplore is a location-based card collecting game developed as part of ECM2434 at the University of Exeter by the "Kanban Warriors" project group. Built with Django, the game encourages exploration and engagement with sustainability topics on campus. Players can discover digital cards by visiting real-world locations, fostering an interactive learning experience about sustainability initiatives and environmental awareness.

The objective of this project is to gamify sustainability education at the University of Exeter, making environmental awareness both engaging and interactive.

## 🎯 Objectives

EcoSplore is designed to achieve the following goals:

- 🌱 **Promote Sustainability Awareness:** Educate users on environmental initiatives and sustainable practices through interactive gameplay.
- 🏛️ **Encourage Campus Exploration:** Motivate players to explore sustainable features and locations across the university campus.
- 📚 **Foster Environmental Education:** Provide valuable insights on sustainability through collectible cards and challenges.
- 🤝 **Enhance Community Engagement:** Build a network of environmentally conscious students through social gameplay features.
- 🏫 **Support University Sustainability Goals:** Align with and promote the University of Exeter's environmental initiatives and targets.
- 🎮 **Gamify Learning:** Transform sustainability education into an engaging and rewarding experience.

## 🔥 Key Features

- 🗺️ **Interactive Map Integration:** Utilizes Leaflet to display card locations and real-time user positioning, enhancing the location-based gameplay. _(JavaScript: static/js/map.js)_
- 🃏 **Comprehensive Card Collection System:** Users can collect, view, and manage their digital card collections within their profiles. _(HTML: cardgame/templates/card_col.html)_
- 🎯 **Location-Based Challenges:** Players can participate in time-sensitive challenges at specific locations to earn exclusive cards and climb the leaderboard. _(HTML: cardgame/templates/cardgame/challenges.html)_
- 🏆 **Global Leaderboard:** Enables competitive play by allowing users to track their rankings in real-time. _(JavaScript: static/js/leaderboard.js)_
- 🆕 **Recent Card Updates:** Keeps players informed about the latest card additions. _(JavaScript: static/js/recent_card.js)_
- 🔒 **Secure User Authentication:** Implements robust authentication mechanisms for user security. _(HTML: cardgame/templates/cardgame/login.html, cardgame/templates/cardgame/signup.html)_
- 🛠️ **Django Admin Panel:** Facilitates efficient management of cards, challenges, user accounts, and game settings.
- ✅ **Automated Testing and Linting:** Ensures code stability and quality through CI workflows, utilizing GitHub Actions. _(CI: .github/workflows/django.yml, .github/workflows/lint_with_flake8.yml)_

## 🚀 Getting Started

Follow the instructions below to set up the project locally.

### ⚙️ Prerequisites

Ensure the following dependencies are installed:

- 🐍 **Python (3.13.2 recommended):** Download from [python.org](https://www.python.org/downloads/).
- 📦 **pip:** Verify installation by running `pip --version`.
- 🌐 **virtualenv:** Install via:
  ```bash
  pip install virtualenv
  ```

### 🛠️ Installation Guide

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Kanban-Warriors-Organization/KanbanWarriors.git
   cd KanbanWarriors
   ```

2. **Create a Virtual Environment:**

   ```bash
   virtualenv .venv
   ```

3. **Activate the Virtual Environment:**

   - **macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```
   - **Windows:**
     ```bash
     .venv\Scripts\activate
     ```

4. **Install Project Dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r .github/requirements.txt
   ```

### 🎮 Running the Application

1. **Navigate to the project root directory.**
2. **Activate the virtual environment.**
3. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```
4. **Start the Django development server:**
   ```bash
   python manage.py runserver
   ```
5. **Access the application:** Open `http://127.0.0.1:8000/` in a web browser.

### 🧪 Running Tests

To verify the application’s functionality, execute the test suite:

```bash
pytest cardgame
```

## 🛠️ Technologies Used

| 🚀 Technology | 📌 Version | 🔍 Purpose                                             |
| ------------- | ---------- | ------------------------------------------------------ |
| **Django**    | 5.1.6      | Web framework for backend logic and database handling. |
| **Pillow**    | 11.1.0     | Image processing for card generation.                  |
| **Leaflet**   | N/A        | Interactive map rendering.                             |
| **SQLite**    | N/A        | Lightweight database for development.                  |
| **pytest**    | N/A        | Automated testing framework.                           |
| **flake8**    | N/A        | Code quality and linting tool.                         |

## 🎯 Features

- 🃏 **Card Collection:** Discover and collect unique digital cards.
- 📍 **GPS Integration:** Locate cards and challenges in real-world locations.
- 📖 **Detailed Card Descriptions:** Rich information and visuals for each card.
- 👤 **User Profiles:** Track game progress and manage collections.
- 🏆 **Leaderboard:** Compete with other players globally.
- 🎯 **Challenges:** Engage in location-based tasks to earn rewards.
- 🔔 **Recent Card Updates:** Stay informed about new card releases.
- 🗂️ **Set Completion:** Cards are categorized into sets to encourage collection. _(Lines 64-65, cardgame/models.py)_

## 🔮 Future Enhancements

The following features are under consideration for future development:

- ⚔️ **Card Battles:** Engage in strategic battles using collected cards.
- 🔄 **Card Trading:** Exchange cards with other players.
- 💰 **In-Game Currency:** Earn and spend virtual currency for enhancements.
- 🕵️ **Scavenger Hunts:** Multi-location challenges for additional rewards.
- 🏅 **Badges for Collections:** Unlock achievements based on progress.
- 📣 **Social Media Integration:** Share progress and achievements.
- 📆 **Daily/Weekly Challenges:** Recurring events with special rewards.
- 🕶️ **Augmented Reality (AR) Features:** Enhance gameplay with AR elements.

## 📜 License

This project is open-source and is available under the [MIT License](LICENSE).
