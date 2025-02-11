# auth.py
# This module handles Basic Authentication.
# Yes, credentials are hardcoded because apparently we don’t have a full-blown authentication system.

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from .config import BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD

security = HTTPBasic()

# Hardcoded credentials – you can change these if you actually care about security.
USERNAME = BASIC_AUTH_USERNAME
PASSWORD = BASIC_AUTH_PASSWORD


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Verifies the provided credentials.
    If they are not correct, you'll get a 401, because we don't have time for slackers.
    """
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password. Try harder next time!",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
