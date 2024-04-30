# Welcome to Mastermind! 

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


## 🏁 Features 🏁
  - WIP
    
## ✏️ My Journal ✏️
**_Click [here](/readme/journal.md) to read my journal where I documented my daily progress!_**
