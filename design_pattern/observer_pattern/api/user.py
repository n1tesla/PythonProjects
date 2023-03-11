from ..lib.email import send_email
from ..lib.db import create_user, find_user
from ..lib.log import log
from ..lib.slack import post_slack_message
from ..lib.stringtools import get_random_string
from .event import post_event
def register_new_user(name: str, password: str, email: str):
    # create an entry in the database
    user = create_user(name, password, email)
    
    post_event(f"user registered {user}")

def password_forgotten(email: str):
    # retrieve the user
    user = find_user(email)

    # generate a password reset code
    user.reset_code = get_random_string(16)

    # send a password reset message
    send_email(user.name, user.email, "Reset your password",
        f"To reset your password, use this very secure code: {user.reset_code}.\nRegards, The DevNotes team")

    # write server log
    log(f"User with email address {user.email} requested a password reset")
