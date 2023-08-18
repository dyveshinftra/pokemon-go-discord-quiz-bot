# access to environment variables

import os

# load .env
import dotenv
dotenv.load_dotenv()

# wrapper around os.getenv() makes sure .env is loaded
def get(key):
    return os.getenv(key)
