# config.py
# This module loads environment variables from a .env file.
# Make sure you have a .env file in the root of your project with the necessary configuration.

import os
from dotenv import load_dotenv

# Load environment variables from the .env file in the project root.
load_dotenv()

# Basic Authentication credentials.
# You can override these values by setting BASIC_AUTH_USERNAME and BASIC_AUTH_PASSWORD in your .env file.
BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME")
BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD")

# Add additional configuration variables below if needed.
