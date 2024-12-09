import os
from dotenv import load_dotenv


def check_env_variables_exist():
    load_dotenv()
    if os.getenv("SECRET_KEY") is None or os.getenv("DATABASE_URI") is None:
        raise ValueError(
            "No environment variables found. Please create a .env file in the root directory. Travel-Metric-Dashboard/.env and add the following variables: SECRET_KEY, DATABASE_URI"
        )
    else:
        print("Continuing with app initialization...")
