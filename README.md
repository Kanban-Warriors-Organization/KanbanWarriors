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

or via Django

```bash
python manage.py test
```

## 🛠️ Technologies Used

| 🚀 Technology  | 📌 Version | 🔍 Purpose                                             |
| -------------- | ---------- | ------------------------------------------------------ |
| **Django**     | 5.1.6      | Web framework for backend logic and database handling. |
| **Pillow**     | 11.1.0     | Image processing for card generation.                  |
| **Leaflet**    | N/A        | Interactive map rendering.                             |
| **PostgreSQL** | N/A        | Lightweight database for development.                  |
| **pytest**     | N/A        | Automated testing framework.                           |
| **flake8**     | N/A        | Code quality and linting tool.                         |

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
- [ ] **Battles:** Engage in strategic battles with other players or AI opponents using your card collections.
- [ ] **Trading Cards:** Trade cards with other players to complete your sets and acquire rare cards.
- [ ] **In-Game Currency:** Earn and use in-game currency for various game enhancements and items.
- [ ] **Scavenger Hunts:** Participate in complex, multi-location scavenger hunts for valuable rewards.

## 🚀 Migrating from SQLite3 to PostgreSQL

Our project has migrated from **SQLite3** to **PostgreSQL**. Follow these steps to update your local environment.

### 📌 Step 1: Install PostgreSQL

Make sure PostgreSQL is installed on your system.

- **Windows**: [Download PostgreSQL](https://www.postgresql.org/download/)
- **Mac (Homebrew)**:
  ```sh
  brew install postgresql
  ```

**Important**: You may need to manually add PostgreSQL to your PATH, to do that look up "how to add to PATH".

### 📌 Step 2: Install Depedencies

Ensure `psycopg2-binary` is installed.

```sh
pip install psycopg2-binary
```

### 📌 Step 3: Setting up PostgreSQL Database

When going through setup, make sure you remember the **password** that you set up, this will be required down the line.

For the additional tools download menu, check all the boxes aside from "stack builder".

You may use the shell, however, I found this quite tedious and annoying. Once installation is complete, I recommend you use the GUI named "pgAdmin 4".

From pgAdmin 4, you can create new databases, change user settings etc. Keep in mind that this database, while connected to the codebase, is unique to you. This means all changes you make are local.

## 📌 Step 5: Update settings.py

Assuming all is well at this point, we need to change some settings.

First: Create a new file `.env` in the root directory of the project. This will store your credentials.

```ini
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_secure_password # This is the password you have set during intallation
DB_HOST=localhost
DB_PORT=5432
```

Next, update `settings.py`

```python
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

## 📌 Step 6: Add the .env file to gitignore

```bash
echo ".env" >> .gitignore
```

Doing so will not push your database credentials to GitHub. This is important down the line when we eventually need to host the DB securely on a remote server.

## 📌 Step 6: Migrating the Relations

I had some issues when migrating the relations initially. Hopefully, following these instructions will avoid all that.

While in the directory of the project, use the terminal to execute the command:

```bash
manage.py migrate --run-syncdb
```

This should force the initialisation of all relations and models that do not exist currently in PSQL

## 📌 Step 7: Loading the data into the new DB

I have already extracted and re-encoded the data from our original DB. It is in the root directory of the project called "data.json".

In the working directory's terminal, execute:

```bash
py manage.py loaddata data.json
```

This will populate the new DB with the data we had in the original DB.

If you have made it this far, congratulations! you have successfully migrated from Sqlite3 to PostgreSQL!

## 🔮 Future Enhancements

The following features are under consideration for future development:

- ⚔️ **Card Battles:** Engage in strategic battles using collected cards.
- 🔄 **Card Trading:** Exchange cards with other players.
- 💰 **In-Game Currency:** Earn and spend virtual currency for enhancements.
- 🕵️ **Scavenger Hunts:** Multi-location challenges for additional rewards.
- 🏅 **Badges for Collections:** Unlock achievements based on progress.
- 📣 **Social Media Integration:** Share progress and achievements.
- 📆 **Daily/Weekly Challenges:** Recurring events with special rewards.

## 📜 License

This project is open-source and is available under the [MIT License](LICENSE).
