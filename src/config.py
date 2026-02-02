from dotenv import load_dotenv
from os import getenv

load_dotenv()

def get_env(name: str):
    return getenv(name)