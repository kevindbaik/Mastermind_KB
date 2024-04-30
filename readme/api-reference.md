## API Routes

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

## SPOTS

### Get all Spots

Returns all the spots.

* Require Authentication: false
* Request
  <!--!!START SILENT -->
  * Method: GET
  * URL: /api/spots
  <!--!!END -->
  <!--!!ADD -->
  <!-- * Method: ? -->
  <!-- * URL: ? -->
  <!--!!END_ADD -->
  * Body: none

* Successful Response
  * Status Code: 200
  * Headers:
    * Content-Type: application/json
  * Body:

    ```json
    {
      "Spots": [
        {
          "id": 1,
          "ownerId": 1,
          "address": "123 Disney Lane",
          "city": "San Francisco",
          "state": "California",
          "country": "United States of America",
          "lat": 37.7645358,
          "lng": -122.4730327,
          "name": "App Academy",
          "description": "Place where web developers are created",
          "price": 123,
          "createdAt": "2021-11-19 20:39:36",
          "updatedAt": "2021-11-19 20:39:36",
          "avgRating": 4.5,
          "previewImage": "image url"
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


