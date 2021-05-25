# Documentation

## Table of Contents

* [Technologies Used](#technologies-used)
* [Database](#database)
* [Deployment](#deployment)
* [Schemas](#schemas)
* [Views](#views)

## Technologies Used

- `FastAPI 0.63.0` - Web Framework for building APIs
- `SQLAlchemy 1.4.13` - Object Relational Mapper
- `Uvicorn 0.13.4` - ASGI server implementation

## Database

The database consists of two tables:

- `messages` - table to store messages with their contents and counters:
    - `MessageID` auto incremented primary key integer
    - `Content` not nullable varchar(160) with constraint on it (length(Content) > 0)
    - `Counter` not nullable integer with default value 0

- `accounts` - table to store all the logins and hashed passwords of database users:
    - `AccountID` auto incremented primary key integer
    - `Login`  not nullable varchar(30)
    - `PasswordHash` not nullable varchar(128)

## Deployment

The API is deployed on Heroku using Heroku Postgresql to store its database. It is
available  [here](https://evox-wsek.herokuapp.com
).

## Schemas

- **Message**:
    - MessageID: PositiveInt
    - Content: constr(max_length=160)
    - Counter: NonNegativeInt


- **MessageOnlyContent**:
    - Content: constr(max_length=160)


- **MessageNoCounter**:
    - MessageID: PositiveInt
    - Content: constr(max_length=160)


- **MessageNoID**:
    - Content: constr(max_length=160)
    - Counter: NonNegativeInt

- **Account**:
    - AccountID: PositiveInt
    - Login: constr(max_length=30)
    - PasswordHash: constr(max_length=128)

## Views

- `/login`
    - **HTTP Method**: GET
    - **Required parameters**:
        - `login`: string
        - `password`: string
    - **Successful response**:
        - `{"message": "welcome"}` with Status Code 202
    - **Error responses**:
        - `{"detail": "Unauthorized"}` with Status Code 401
        - `{"detail": [{"loc": ["string"], "msg": "string", "type": "string"}]}` with Status Code 422
    - **Description**:

      This method checks if there is a row with given login and sha512 hash value of the given password in the table
      accounts of our database.

      If any parameter is not provided, it raises exception with status code 422.

      If there is such row it generates a random token, adds it to the collection of currently used session tokens and
      sets a cookie with key "session_token" and the value of generated token.

    - **Final Remarks**:
        - The only user existing currently in the database is `admin` and the password is `evox`.


- `/logout`
    - **HTTP Method**: DELETE
    - **Required parameters**:
        - `session_token`: string
    - **Successful response**:
        - `{"message": "goodbye"}` with Status Code 202
    - **Error responses**:
        - `{"detail": "Bad Request"}` with Status Code 401
        - `{"detail": [{"loc": ["string"], "msg": "string", "type": "string"}]}` with Status Code 422
    - **Description**:

      This method finds the `session_token` saved in a cookie and tries to delete it from the app's session tokens.

      If any parameter is not provided, it raises exception with status code 422.

      If it does not exist or is not in the session tokens of the app it returns `{"detail": "Bad Request"}`.


- `/messages`
    - **HTTP Method**: POST
    - **Required parameters**:
        - `session_token`: string
        - `new_message`: MessageOnlyContent
        - `db`: Session
    - **Successful response**:
        - `{"id": message_id}` with Status Code 201
    - **Error responses**:
        - `{"detail": "Unauthorised"}` with Status Code 401
        - `{"detail": [{"loc": ["string"], "msg": "string", "type": "string"}]}` with Status Code 422
    - **Description**:

      This method creates a new message and saves it in the database.

      It requires the content of the message and requires the user to be authorised (logged in).

      The counter is always set to 0 and id is auto generated.

      If the user is not logged, it raises exception with status code 401.

      If any parameter is not provided, it raises exception with status code 422.

      The correct return value is a dictionary with the id of the created message.


- `/messages`
    - **HTTP Method**: PUT
    - **Required parameters**:
        - `session_token`: string
        - `new_message`: MessageNoCounter
        - `db`: Session
    - **Successful response**:
        - `{"Result": "Updated successfully"}` with Status Code 202
    - **Error responses**:
        - `{"detail": "Unauthorised"}` with Status Code 401
        - `{"detail": "Not Found"}` with Status Code 404
        - `{"detail": [{"loc": ["string"], "msg": "string", "type": "string"}]}` with Status Code 422
    - **Description**:

      This method updates a message with given `Messageid` and new `Content`.
    
      It changes the `Counter` value to 0.

      It requires the content and id of the message and requires the user to be authorised (logged in).

      If the user is not logged, it raises exception with status code 401.

      If the MessageID does not exist in the database, it raises exception with status code 404.

      If any parameter is not provided, it raises exception with status code 422.

      The correct return value is `{"Result": "Updated successfully"}`.


- `/messages/{message_id}`
    - **HTTP Method**: DELETE
    - **Required parameters**:
        - `session_token`: string
        - `message_id`: PositiveInt
        - `db`: Session
    - **Successful response**:
        - `{"Result": "Updated successfully"}` with Status Code 202
    - **Error responses**:
        - `{"detail": "Unauthorised"}` with Status Code 401
        - `{"detail": "Not Found"}` with Status Code 404
        - `{"detail": [{"loc": ["string"], "msg": "string", "type": "string"}]}` with Status Code 422
    - **Description**:

      This method deletes a message with given `Messageid`.

      It requires the id of the message and requires the user to be authorised (logged in).

      If the user is not logged, it raises exception with status code 401.

      If the MessageID does not exist in the database, it raises exception with status code 404.

      If any parameter is not provided, it raises exception with status code 422.

      The correct return value is `{"Result": "Deleted successfully"}`.


- `/messages/{message_id}`
    - **HTTP Method**: GET
    - **Required parameters**:
        - `message_id`: PositiveInt
        - `db`: Session
    - **Successful response**:
        - `{"Content": "string", "Counter": 0 }` with Status Code 200
    - **Error responses**:
        - `{"detail": "Unauthorised"}` with Status Code 401
        - `{"detail": "Not Found"}` with Status Code 404
        - `{"detail": [{"loc": ["string"], "msg": "string", "type": "string"}]}` with Status Code 422
    - **Description**:

      This method returns `Content` and `Counter` of the message with given `Messageid`. It also increments
      the `Counter`.

      It requires the id of the message.

      If the MessageID does not exist in the database, it raises exception with status code 404.

      If any parameter is not provided, it raises exception with status code 422.

      The correct return value is a json with the message's content and counter.