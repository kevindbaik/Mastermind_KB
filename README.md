# Welcome to Mastermind! 
<div align="center"> <img src="readme/Mastermind_KB_Logo.png" alt="logo"> </div>

## 📚 Table of Contents 📚
  - WIP

## 🖥️ Setup and Run Locally 🖥️
 Prerequisites:
   - **Python 3.12**: You may download and install Python 3.12 from [python.org](https://www.python.org/downloads/release/python-3120/)
   - **Pip**: Pip is automatically installed with Python 3.12, but you can ensure it is up to date by following the instructions [here](https://pip.pypa.io/en/stable/installation/).
     
### 1.  Clone Repo:
```bash
git clone https://github.com/kevindbaik/Mastermind_KB.git
```
### 2. Navigate to Project Directory:
```bash
cd Mastermind_KB
```
### 3. Environment Setup:
If you do NOT have 'pipenv' installed, run one of the following commands:
```bash
pip install pipenv

    or 

pip3 install pipenv
```

After installing `pipenv`, run this command to create a virtual environment and install all required dependencies (including Flask):

```bash
pipenv install
```

### 4. Database Setup
Mastermind includes two pre-seeded SQLite database files located in the 'db' directory. If they are missing or need to be reset, navigate to the 'db' directory and run the setup scripts:
```bash
cd db
python local_setup.py
python online_setup.py
```

### 5. Starting Server:
To play in online mode, Mastermind requires the Flask server running on port 5000. Open a second terminal and navigate to the 'server' directory:
```bash
cd server
```
Start the Flask server by running:
```bash
pipenv run flask run
```

### 6. Running Mastermind
To start the game, from the root directory of Mastermind run:
```bash
python main.py
```

## 🎦 Demo Walkthrough 🎦
### Local Play
- You can play Mastermind with no internet connection through the (Play Local) option!
- All scores played in local mode are saved in the local leaderboard. <br><br>
<img src="readme/demo_local.gif" alt="local"> <br><br>


### Online Play
- If you have an internet connection and the Flask server running, you can play Mastermind Online!
- Register an account or login using the demo user credentials (demouser@demo.com, demouser)
  - Once you log in, you will not be asked to login again until you exit the game. <br><br>
<img src="readme/demo_login.gif" alt="login"> <br><br>

- You can start a new game or continue one of your games in progress!
- During a game session, you may enter 'return' to return back to the menu. <br><br>
<img src="readme/demo_resume.gif" alt="resume"> <br><br>
- You can also view the results of your past games! <br><br>
<img src="readme/demo_history.gif" alt="history"> <br><br>

### Leaderboard
- View the top 10 players with the highest scores both locally and online! <br><br>
<img src="readme/demo_leaderboard.gif" alt="leaderboard"> <br><br>

## 🏁 Features 🏁
  - WIP

## ⚙️ API Reference ⚙️
**_Click [here](/readme/api-reference.md) for more information about the API routes and database schema!_**

## ✏️ My Journal ✏️
**_Click [here](/readme/journal.md) to read my journal where I documented my daily progress!_**
