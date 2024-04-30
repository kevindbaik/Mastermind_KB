# API Routes

## Player
### Sign Up Player
Creates a new player, logs them in as the current player, and returns the current player's information.

* Request
  <!--!!START SILENT -->
  * Method: POST
  * URL: http://localhost:5000/api/player
  <!--!!END -->
  <!--!!ADD -->
  <!-- * Method: ? -->
  <!-- * URL: ? -->
  <!--!!END_ADD -->
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "name": "John",
      "email": "john.smith@gmail.com",
      "password": "secretpassword"
    }
    ```

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "success": {
        "id": 1,
        "firstName": "John",
        "email": "john.smith@gmail.com"
      }
    }
    ```

* Error Response: User Exists
  * Status Code: 409
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      'error': 'This email already exists for a player'
    }
    ```

* Error Response: Already Logged In
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      'error': 'You are already logged in'
    }
    ```

* Error Response: Missing Body 
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
     'error': 'Missing username, password, or email'
    }
    ```

### LOG IN Player
Logs in a current player with valid credentials and returns the current player's
information.

* Request
  <!--!!START SILENT -->
  * Method: POST
  * URL: http://localhost:5000/api/player/login
  <!--!!END -->
  <!--!!ADD -->
  <!-- * Method: ? -->
  <!-- * URL: ? -->
  <!--!!END_ADD -->
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "email": "john.smith@gmail.com",
      "password": "secret password"
    }
    ```

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "success": {
        "id": 1,
        "email": "John",
        "name": "Smith",
      }
    }
    ```

* Error Response: Wrong Password
  * Status Code: 401
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      'error': 'User password is incorrect'
    }
    ```

* Error Response: Email Does Not Exist
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      'error': 'User email does not exist in database'
    }
    ```
* Error response: Invalid Email (no @)
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      'error': 'Invalid email address'
    }
    ```

* Error Response: Empty Body
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
     'error': 'Missing email or password'
    }
    ```


### Log Out Player 
Logs out a player

* Request
  <!--!!START SILENT -->
  * Method: GET
  * URL: http://localhost:5000/api/player/logout
  <!--!!END -->
  <!--!!ADD -->
  <!-- * Method: ? -->
  <!-- * URL: ? -->
  <!--!!END_ADD -->
  * Body: None

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "success" : "You have been logged out"
    }
    ```

* Error Response: No Logged In Player
  * Status Code: 403
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      'error': 'No user is currently logged in'
    }
    ```

### Get Player Games (Active)
Retrieves a list of dictionaries that each represent the players games that have not ended.

* Request
  <!--!!START SILENT -->
  * Method: GET
  * URL: http://localhost:5000/api/player/{player_id}/games/ongoing
  <!--!!END -->
  <!--!!ADD -->
  <!-- * Method: ? -->
  <!-- * URL: ? -->
  <!--!!END_ADD -->
  * Body: None

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
      {
        "success": [
            {
                "answer": "5678",
                "attempts": 9,
                "difficulty": 2,
                "game_over": 0,
                "hints": 1,
                "history": [
                    "1111"
                ],
                "id": 2,
                "player_id": 1,
                "score": 0,
                "win": 0
            }
        ]
    }
    ```


### Get Player Games (Ended)
Retrieves a list of dictionaries that each represent the players games that have ended.

* Request
  <!--!!START SILENT -->
  * Method: GET
  * URL: http://localhost:5000/api/player/{player_id}/games/ended
  <!--!!END -->
  <!--!!ADD -->
  <!-- * Method: ? -->
  <!-- * URL: ? -->
  <!--!!END_ADD -->
  * Body: None

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
        "success": [
            {
                "answer": "1234",
                "attempts": 1,
                "difficulty": 3,
                "game_over": 1,
                "hints": 2,
                "history": [
                    "1111",
                    "2222",
                    "1234",
                    "1111",
                    "1111",
                    "1111",
                    "2222",
                    "2222",
                    "4444"
                ],
                "id": 1,
                "player_id": 1,
                "score": 300,
                "win": 1
            }
        ]
    }
    ```
    
## Game
### Start Game
Starts a game session for the player

* Request
  <!--!!START SILENT -->
  * Method: POST
  * URL: http://localhost:5000/api/start_game
  <!--!!END -->
  <!--!!ADD -->
  <!-- * Method: ? -->
  <!-- * URL: ? -->
  <!--!!END_ADD -->
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "difficulty": 1
    }
    ```

* Successful Response
  * Status Code: 201
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "game_id": 8,
      "message": "Game started successfully",
      "player_id": 2
    }
    ```

* Error Response: Player Not Logged In
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      'error': 'You must be logged in to play'
    }
    ```

### Get Status Game
Gets current status of a game in session by player based on game id

* Request
  <!--!!START SILENT -->
  * Method: GET
  * URL: http://localhost:5000/api/game/{game_id}
  <!--!!END -->
  <!--!!ADD -->
  <!-- * Method: ? -->
  <!-- * URL: ? -->
  <!--!!END_ADD -->
  * Headers:
    * Content-Type: application/json
  * Body: None

* Successful Response
  * Status Code: 201
  * Headers:
    * Content-Type: application/json
  * Body:
    ```json
       {
        "success": {
            "attempts_left": 9,
            "difficulty": 2,
            "game_id": 2,
            "game_over": 0,
            "hints_left": 1,
            "history": [
                "1111"
            ],
            "player_id": 1,
            "win": 0
        }
    }
    ```

* Error Response: Game already ended
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      'error': 'Game has already ended'
    }
    ```
* Error Response: Game Doesn't Belong to Player
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      'error': 'Game does not belong to user'
    }
    ```

* Error Response: Invalid Game Id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      'error': 'Game not found'
    }
    ```

### Make Guess
Player makes a guess for an active game in session

* Request
  <!--!!START SILENT -->
  * Method: POST
  * URL: http://localhost:5000/api/game/{game_id}/guess
  <!--!!END -->
  <!--!!ADD -->
  <!-- * Method: ? -->
  <!-- * URL: ? -->
  <!--!!END_ADD -->
  * Headers:
    * Content-Type: application/json
  * Body:
    ```json
    {
      "guess": "4234"
    }
    ```

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:
    ```json
      {
          "success": {
              "attempts": 8,
              "difficulty": 2,
              "feedback": {
                  "correct_locations": 0,
                  "correct_numbers": 0
              },
              "guess": "4234",
              "history": [
                  "1111",
                  "4234"
              ]
          }
      }
    ```

  * Successful Response (If Game Won)
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:
    ```json
      {
        "game_over" : { 
              "result": 1,
             "score": 1500
          }
      }
    ```

  * Successful Response (If Game Lost)
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:
    ```json
      {
        "game_over" : { 
              "result": 0,
             "score": 0
          }
      }
    ```
    
* Error Response: Missing Body
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      'error': 'Missing guess'
    }
    
* Error Response: Player not logged in
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
     'error' : 'Player must be logged in'
    }

* Error Response: Game already ended
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      'error': 'Game has already ended'
    }
    ```
* Error Response: Game Doesn't Belong to Player
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      'error': 'Game does not belong to player'
    }
    ```
    
* Error Response: Invalid Game Id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      'error': 'Game not found'
    }
    ```

### Get Hint
Get a hint from current game in session

* Request
  <!--!!START SILENT -->
  * Method: POST
  * URL: http://localhost:5000/api/game/{game_id}/hint
  <!--!!END -->
  <!--!!ADD -->
  <!-- * Method: ? -->
  <!-- * URL: ? -->
  <!--!!END_ADD -->
  * Headers:
    * Content-Type: application/json
  * Body: None
    
* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:
    ```json
      {
          "success": {
              "hint": "The number 2 in position 2 is not in the secret code.",
              "hints_left": 0
          }
      }
    ```
    
  * Error Response: No Attempt Taken
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
     'error': 'You must take a guess first'
    }

  * Error Response: No Hints Remaining
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
     'error': 'You have no more hints'
    }

  * Error Response: Game Not Found
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
     'error': 'Game not found'
    }

* Error Response: Game Already Ended
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      'error': 'Game has already ended'
    }
    ```
* Error Response: Game Does Not Belong to Player
  * Status Code: 400
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      'error': 'Game does not belong to player'
    }
    ```
    
* Error Response: Invalid Game Id
  * Status Code: 404
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      'error': 'Game not found'
    }
    ```

### Get Online Leaderboard
Retrieves a list of dictionaries that each represent highest scores 

* Request
  <!--!!START SILENT -->
  * Method: GET
  * URL: http://localhost:5000/api/leaderboard
  <!--!!END -->
  <!--!!ADD -->
  <!-- * Method: ? -->
  <!-- * URL: ? -->
  <!--!!END_ADD -->
  * Body: None

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
     {
        "success": [
            {
                "difficulty": 3,
                "name": "Hermione",
                "score": 1700
            },
            {
                "difficulty": 3,
                "name": "Frodo",
                "score": 1600
            },
            {
                "difficulty": 3,
                "name": "Sam",
                "score": 1599
            },
            {
                "difficulty": 2,
                "name": "Harry",
                "score": 1200
            },
            {
                "difficulty": 1,
                "name": "Voldemort",
                "score": 1000
            },
            {
                "difficulty": 2,
                "name": "Merry",
                "score": 900
            },
            {
                "difficulty": 1,
                "name": "Luna",
                "score": 600
            },
            {
                "difficulty": 2,
                "name": "Pippin",
                "score": 500
            },
            {
                "difficulty": 1,
                "name": "Malfoy",
                "score": 200
            },
            {
                "difficulty": 1,
                "name": "Ron",
                "score": 100
            }
        ]
    }
    ```

## Database Schema

### User

| `Key`        | `Type` | `Required` | `Default`  | `Unique` | 
| :----------- | :----- | :--------- | :--------- | :------- |
| `id`      | Integer | primary_key      | autoincrement         | true    |
| `name`   | String | true       | none         | false   |
| `email`       | String | true      | none   | true    |  |
| `password` | String   | true      | none | false    |

### Game

| `Key`        | `Type`   | `Required` | `Default`  | `Unique` | 
| :----------- | :------- | :--------- | :--------- | :------- |
| `id`       | Integer | primary_key       | autoincrement         | true    |     
| `player_id`  | Integer     | true       | none | false    |
| `difficulty`    | Integer     | true      | none         | false    |
| `attempts`      | Integer   | false      | 10          | false    |
| `history`      | String | false      | no         | no       |
| `hints` | Integer   | false      | no         | no       |
| `win`       | Boolean | false       | false         | false    |
| `game_over`  | Boolean     | false       | false | false    |
| `score`    | Integer     | false      | 0         | false    |

### Leaderboard

| `Key`             | `Type`   | `Required` | `Default` | `Unique` |
| :---------------- | :------- | :--------- | :-------- | :-------  
| `id`            | Integer | primary_key       | autoincrement        | true    |
| `name`           | String   | true      | no       | false    | 
| `score`        | Integer   | true      | no       | false    | 
| `difficulty`        |  Integer | true      | no      | false    | 


