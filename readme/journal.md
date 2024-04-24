# Mastermind_KB

## Journal
### Day 1: April 23, 2024
#### What I Accomplished Today:
- Set up project: created repository, established file structure, installed pipenv, installed requests package, confirmed unittest module works
- Created an initial plan for features and UI:
  - MVP features: singleplayer, hints, difficulty
    - Additional features: score counter, high score leaderboard, multiplayer
  - Console based UI
    - I'll be focusing most of my time on backend logic, testing, and implementing features.
  - Coded in Python and following OOP principles
    - Classes and encapsulation will make debugging, making changes, and adding new features a much smoother process.
    - I'll be testing w/ unittest every step of the way to avoid bugs and save time in the long run.
- Built Game model (attributes and methods)
  - Created a getter and setter for difficulty attribute.
    - Since the user will be choosing the difficulty, it's important I validate it first to make sure its a valid choice.
  - The games history attribute will be a list that I append attempts to after every wrong guess.
  - I gave the game a game_over attribute which is how I plan to let the UI know when to stop the game.
  - give_feedback returns a dictionary with two key/values of correct counts, i used a set to check for duplicates
  - generate_answer method uses the random.org API
    - Based on difficulty I send in different params to the request
  - I didn't want to make hint feature too powerful, so the give_hint method will randomly select an index, find that digit from the users last attempt and give a statement about it.
- Testing Game model methods went well, no major issues.
#### Todays Blockers:
- Deciding which of my attributes should have getters/setters, which attributes and methods should be "private" (python doesn't have a real private option)
  - I know this doesn't really matter since the only person who will ever work in this repo is me, but I'd like to practice good habits.
- I'm still not sure if I like what my give_hint method returns. I will adjust based on what I do in UI.
  - It's currently a tuple returning the last_answer string and a string message about the hint.
- My give_feedback method is not the most optimized (uses for loop)
  - Since I know that the input will always have a length of 5 (at most), I think it's acceptable in this situation.
#### What I Plan To-Do Tomorrow:
- Finish coding Game model for MVP features
  - Add method that validates users guess, since I have a difficulty setting that changes the number of digits and range of each digit.
- Start and finish coding Player model
- Test Player model
- Start UI/interface
