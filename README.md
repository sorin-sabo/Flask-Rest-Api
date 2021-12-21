# Flask REST API
    1. Functionalities covered:
    -   Rest API CRUD opertaions;
    -   Oauth2 integration handling both id and access token;
    -   Validation for request data using dtos and schemas;
    -   Unit tests with a mixin of unittest & pytest
    -   API docs with swagger;
    -   Code quality assured with pylint;
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
   git clone https://github.com/sorin-sabo/Flask-Rest-Api.git
   ```

2. **Create virtual environment**
    - Windows
    ```bash
    python -m venv $(pwd)/venv
    source venv/bin/activate
    ```
   
    - OS X
    ```bash
    python3 -m venv $(pwd)/venv
    source venv/bin/activate
    ```

3. **Install requirements**:
    - Windows
    ```bash
    pip install -r requirements.txt
    ```
   
    - OS X
    ```bash
    pip3 install -r requirements.txt
    ```

4. **Add environment variables**
    - Create a file named `.env` in project root directory
    - Add and fill next environment variables with your local database config:
        ```.env
        DATABASE_USERNAME=
        DATABASE_PASSWORD=
        DATABASE_NAME=
        DATABASE_PORT=
        DATABASE_HOST=
        OAUTH2_DOMAIN=
        OAUTH2_GUEST=
        OAUTH2_CLIENT=
        ```

## Run

-   Application can run directly from cmd using fallowing commands:
    - Using python run
        - Windows
        ```bash
        python app.py run
        ```
      
        - OS X
        ```bash
        python3 app.py run
        ```
        
    - Using flask run
    ```bash
    flask run
    ```

## Test

- Tests are done with a mixin of unittest & pytest
    - A base class is created for all unit tests to inherit and can be found in `tests/utils/base` - `BaseTestCase`
- Run:
    - Method1:
        - Windows:
        ```bash
        python app.py test
        ```
        
        - OS X:
        ```bash
        python3 app.py test
        ```
    - Method2 - Using pytest:
        - For fallowing options are available:
            - `-v` - to have verbose tests
            - `-s` - to see logging from tests
      
        - Windows:
        ```bash
        pytest tests
        ```
        
        - OS X:
        ```bash
        pytest -q tests
        ```

## Migrate on data model changes
    
- Run fallowing commands
    - Windows
    ```bash
    python app.py db init
    python app.py db migrate
    python app.py db upgrade
    ```
    
    - OS X
    ```bash
    python3 app.py db init
    python3 app.py db migrate
    python3 app.py db upgrade
    ```

### Useful

- Before deploy check package dependencies (since 2020 Dec 01 is no longer done automatically):
  ```bash
  python -m pip check
  ```
  
## Code quality
- Pylint used to maintain code quality;
- Rules for code quality can be consulted in `.pylintrc`
- Current status: `Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)`
- Make sure before deployment that code quality is the same;
