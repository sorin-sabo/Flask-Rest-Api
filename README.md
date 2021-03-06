# Flask Sample API
    1. Functionalities covered:
    -   Rest API CRUD opertaions;
    -   Oauth2 integration handling both id and access token;
    -   Validation for request data using schemas;
    -   API docs with swagger;
    2. Programming principles covered:
    -   Best practices in Flask;
    -   Geneneric response format;
    -   Custom error handling for all response types;

## Requirements

It is assumed that:
-   You have Python and MySQL installed. If not, then download the latest versions from:
    * [Python](https://www.python.org/downloads/)
    * [MySql](https://dev.mysql.com/downloads/installer/)

## Installation

1. **Clone git repository**:
   ```bash
   git clone git@github.com:sorin-sabo/Flask-Rest-Api.git
   ```

2. **Create virtual environment**
    ```bash
    python -m venv /path/<venv>
    source <venv>/bin/activate
    ```

3. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Add environment variables**
    - Create a file named `.env` in root directory
    - Add and fill next environment variables with your local database config:
        ```.env
        DATABASE_USERNAME=
        DATABASE_PASSWORD=
        DATABASE_NAME=
        DATABASE_PORT=
        DATABASE_HOST=
        OAUTH_DOMAIN=
        OAUTH_GUEST_ID=
        OAUTH_CLIENT_ID=
        ```

## Run

- Application can run directly from cmd using fallowing command:
  ```bash
  python run.py
  ```

## Useful

- Before deploy check package dependencies (since 2020 Dec 01 is no longer done automatically):
  ```bash
  python -m pip check
  ```