# 🌱 EcoSplore 🌿

## 🔗Links

Use these links to try the deployed version:

[EcoSplore - ecosplore.xyz](https://ecosplore.xyz/)

[EcoSplore - direct connect via ip](http://45.141.151.64:8000/login)

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

- 🗺️ **Interactive Map Integration:** Utilizes Leaflet to display card locations and real-time user positioning, enhancing the location-based gameplay.
- 🃏 **Comprehensive Card Collection System:** Users can collect, view, and manage their digital card collections within their profiles.
- 🎯 **Location-Based Challenges:** Players can participate in time-sensitive challenges at specific locations to earn exclusive cards and climb the leaderboard.
- 🏆 **Global Leaderboard:** Enables competitive play by allowing users to track their rankings in real-time.
- 🆕 **Recent Card Updates:** Keeps players informed about the latest card additions.
- 🔒 **Secure User Authentication:** Implements robust authentication mechanisms for user security.
- 🛠️ **Django Admin Panel:** Facilitates efficient management of cards, challenges, user accounts, and game settings.
- ✅ **Automated Testing and Linting:** Ensures code stability and quality through CI workflows, utilizing GitHub Actions.

## 🚀 Getting Started

Follow the instructions below to set up the project locally.

### ⚙️ Prerequisites

Ensure the following dependencies are installed:

- **Python (3.13.2 recommended):** Download from [python.org](https://www.python.org/downloads/).
- **pip:** Verify installation by running `pip --version`.
- **virtualenv:** Install via:
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
   pip install -r requirements.txt
   ```

### 🎮 Running the Application

1. **Navigate to the project root directory.**
2. **Activate the virtual environment.**
3. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```
4. **Prepare static files**
   ```bash
   python manage.py collectstatic
   ```
5. **Run the server using uvicorn:**
   ```bash
   uvicorn cards.asgi:application
   ```
6. **Access the application:** Open `http://127.0.0.1:8000/` in a web browser.

### 🧪 Running Tests

To verify the application’s functionality, execute the test suite:

```bash
pytest cardgame
```

or via Django

```bash
python manage.py test
```

## 🛠️ Technologies Used

| 🚀 Technology  | 🔍 Purpose                                             |
| -------------- | ------------------------------------------------------ |
| **Django**     | Web framework for backend logic and database handling. |
| **Pillow**     | Image processing for card generation.                  |
| **Leaflet**    | Interactive map rendering.                             |
| **SQLite**     | Lightweight database for development.                  |
| **pytest**     | Automated testing framework.                           |
| **flake8**     | Code quality and linting tool.                         |
| **uvicorn**    | Asynchronous server to handle websockets in django     |
| **websockets** | Real-time aspect of battles                            |
| **whitenoise** | Middleware to handle Django static files with uvicorn  |

## 🎯 Features

EcoSplore is packed with features to provide an engaging gameplay experience:

- [x] **Collect Cards:** Discover and collect a variety of unique digital cards.
- [x] **GPS Location Integration:** Utilize your device's GPS to find cards and challenges at real-world locations.
- [x] **Detailed Card Information:** Learn about each card with rich descriptions, subtitles, and vibrant images.
- [x] **User Profiles:** Create and customize your player profile to track your card collection and game progress.
- [x] **Leaderboard:** Compete with friends and other players for the top spot on the global leaderboard.
- [x] **Challenges:** Participate in location-based challenges to earn exclusive rewards and cards.
- [x] **Card Sets:** Cards are organized into sets, encouraging collection completion. (lines: 64-65, cardgame/models.py)
- [x] **Recent Card Display:** Stay updated with the latest card releases directly on the homepage. (lines: 72-79, html:cardgame/templates/cardgame/home.html)
- [x] **Battles:** Engage in strategic battles with other players or AI opponents using your card collections.
- [x] **Trading Cards:** Trade cards with other players to complete your sets and acquire rare cards.

## 🔮 Future Enhancements

The following features are under consideration for future development:

- 💰 **In-Game Currency:** Earn and spend virtual currency for enhancements.
- 🕵️ **Scavenger Hunts:** Multi-location challenges for additional rewards.
- 🏅 **Badges for Collections:** Unlock achievements based on progress.
- 📣 **Social Media Integration:** Share progress and achievements.
- 📆 **Daily/Weekly Challenges:** Recurring events with special rewards.

## 📜 License

This project is open-source and is available under the [MIT License](LICENSE).
