# Flask Sample API

## Requirements

It is assumed that:
-   You have Python and MySQL installed. If not, then download the latest versions from:
    * [Python](https://www.python.org/downloads/)
    * [MySql](https://dev.mysql.com/downloads/installer/)

## Installation

1.  **Clone git repository**:
    ```bash
    git clone git@github.com:sorin-sabo/Flask-Rest-Api.git
    ```

2.  **Install requirements**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Add environment variables**
    - Create a file named `.env` in root directory
    - Add and fill next environment variables with your local database config:
        ```.dotenv
        DATABASE_USERNAME=
        DATABASE_PASSWORD=
        DATABASE_NAME=
        DATABASE_PORT=
        DATABASE_HOST=
        ```
    
## Run

-   Application can run directly from cmd using fallowing command:
    ```bash
    python run.py
    ```