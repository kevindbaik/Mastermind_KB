# Mastermind_KB

## ✏️ Journal ✏️
### ⛅ Day 1: April 23, 2024 ⛅
#### <ins>What I Accomplished Today</ins>:
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
#### <ins>Todays Blockers</ins>:
- Deciding which of my attributes should have getters/setters, which attributes and methods should be "private" (python doesn't have a real private option)
  - I know this doesn't really matter since the only person who will ever work in this repo is me, but I'd like to practice good habits.
- I'm still not sure if I like what my give_hint method returns. I will adjust based on what I do in UI.
  - It's currently a tuple returning the last_answer string and a string message about the hint.
- My give_feedback method is not the most optimized (uses for loop)
  - Since I know that the input will always have a length of 5 (at most), I think it's acceptable in this situation.
#### <ins>What I Plan To-Do Tomorrow</ins>:
- Finish coding Game model for MVP features
  - Add method that validates users guess, since I have a difficulty setting that changes the number of digits and range of each digit.
- Start and finish coding Player model
- Test Player model
- Start UI/interface

### ⛅ Day 2: April 24, 2024 ⛅
#### <ins>What I Accomplished Today</ins>:
- Finished Game model:
  - Created a validate_answer method that validates whether user answer is correct (based on the game difficulty).
  - I wrote a lot more unit tests today to confirm my methods were working, in the long run this saved me a lot of time!
  - I rewrote the algorithm for my give_feedback method after doing more testing and accounting for all edge cases. I can't imagine doing this without testing!   
- Finished Player model (for MVP features it's pretty barebones, will interact more with this for next feature)
- Almost finished coding the UI files
  - I'm using two different classes for the user interface, one class that handles all interactions between the models (controller) and one class that displays information to the user and gets inputs
  - After MVP, I will put more of my focus on implementing features than spending time on the UI since that's whats recommended.
- Overall progress has been great, I'm having fun and because from the start I kept a sharp focus on following good programming principles (encapsulation, abstraction, SRP, testing) I feel confident about being able to implement new features later this week. 

#### <ins>Todays Blockers</ins>:
- My original algorithm for give_feedback didn't account for all the different edge cases (combinations).
  - I should have done this sooner, but I decided to write a bunch of unit tests that accounted for all combinations of answers. Coding the algo was much easier after this.  
  - My solution was to make a list from the user and game answers, mutate them as i check for correct locations and numbers.
  - This solution is only acceptable because our input size is relatively small. 
- I think I have too many while loops in my controller class. Will look to optimize after getting fully functioning MVP
- I really want to spend some time and make a nice fun UI... but I can't! My focus will be all things related to backend!

 #### <ins>What I Plan To-Do Tomorrow</ins>:
- Finish MVP. I will test for bugs also but by mid-afternoon tomorrow I will have the bare minimum project finished.
- Start and make good progress on next feature - scoring system. 

### ⛅ Day 3: April 25, 2024 ⛅
#### <ins>What I Accomplished Today</ins>:
- Finished core features and user interface for MVP
- Added type annotations on most of my methods
  - I was thinking about adding these for my variables as well... but after doing some research decided it could seem a bit excessive. 
- Cleaned up code, wrote additional methods, changed existing methods to follow good code principles
  - My controller class is now only responsible for "controlling" the game by managing the interaction between models
  - My console class is now only responsible for taking inputs from user, showing outputs to user
- Started and made good progress on new feature: scores
  - Created the rules of how scoring will be calculated
  - Finished the score calculating method and unit tested for different scenarios

#### <ins>Todays Blockers</ins>:
- Understanding the game flow and making sure it's perfect took me some time to figure out. 
  - Since my game flows synchronously where it waits for user input, processes it, updates the game state, and loops back.... managing how these steps were handled took some trial and error.
  - I've been looking to see if improvements to game flow can be made by applying asynchronous code, but I can't find a reason too right now. Maybe as the application gets more complex or when I implement multiplayer.
- Creating an engaging scoring system and thinking about a creative way to implement the feature. 
  - Currently I have the bare minimum, a method that calculates the score based on the games remaining attributes when the game is won (attempts remaining, difficulty, and hints remaining).
- I'm looking for more ways to incorporate the Player class. It's empty at the moment. 

 #### <ins>What I Plan To-Do Tomorrow</ins>:
- Finish score feature including implementing a high score leaderboard. 
  - Tomorrow I'll start working with a database! I'm choosing SQLite since it's lightweight and part of Pythons standard library. It's perfect for a small application like this.
- Begin next feature after score.... multiplayer! :D
