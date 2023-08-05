
from dotenv import load_dotenv
load_dotenv()

import os
from getpass import getpass

CAMPUS_ID: str = os.getenv("CAMPUS_ID")
if CAMPUS_ID is None:
    CAMPUS_ID = input("Please enter your campus id: ")

AXIS_USER: str = os.getenv("AXIS_USER")
if AXIS_USER is None:
    AXIS_USER = input("Please enter your AXIS user: ")

AXIS_PASSWORD: str = os.getenv("AXIS_PASSWORD")
if AXIS_PASSWORD is None:
    AXIS_PASSWORD = getpass("Please enter your AXIS password: ")

LOG_FILE_PATH: str = os.getenv("LOG_FILE_PATH")
if LOG_FILE_PATH is None:
    LOG_FILE_PATH = "axis.log"