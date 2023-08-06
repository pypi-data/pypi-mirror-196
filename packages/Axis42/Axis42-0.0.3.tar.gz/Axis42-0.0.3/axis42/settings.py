
from dotenv import load_dotenv
load_dotenv()

import os

def print_help():
    print("You should create a.env file in the same directory as this script like this\n")
    print(".env:")
    print('    UID42="API_UID"')
    print('    SECRET42="API SECRET"')
    print('    SCOPE42="public project"')
    print('    CAMPUS_ID="38"')
    print('    AXIS_USER="username"')
    print('    AXIS_PASSWORD="password"')
    exit(1)

CAMPUS_ID: str = os.getenv("CAMPUS_ID")
if CAMPUS_ID is None:
    print_help()

AXIS_USER: str = os.getenv("AXIS_USER")
if AXIS_USER is None:
    print_help()

AXIS_PASSWORD: str = os.getenv("AXIS_PASSWORD")
if AXIS_PASSWORD is None:
    print_help()

LOG_FILE_PATH: str = os.getenv("LOG_FILE_PATH")
if LOG_FILE_PATH is None:
    LOG_FILE_PATH = "axis.log"