# To use this function, you need to install the Twilio Python library:
# pip install twilio
#
# You also need to set the following environment variables:
# TWILIO_ACCOUNT_SID: Your Twilio Account SID
# TWILIO_AUTH_TOKEN: Your Twilio Auth Token
# TWILIO_PHONE_NUMBER: Your Twilio phone number

import os
from twilio.rest import Client
from decouple import config



def send_sms(to_number, message):
    """
    Sends an SMS message using Twilio.

    Args:
        to_number (str): The recipient's phone number in E.164 format.
        message (str): The message to send.

    Returns:
        bool: True if the message was sent successfully, False otherwise.
    """
    account_sid = config("TWILIO_ACCOUNT_SID")
    auth_token = config("TWILIO_AUTH_TOKEN")
    from_number = config("TWILIO_PHONE_NUMBER")

    if not all([account_sid, auth_token, from_number]):
        print("Twilio credentials are not configured. Please set the environment variables.")
        return False

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to=to_number,
            from_=from_number,
            body=message
        )
        print(f"Message sent successfully with SID: {message.sid}")
        return True
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False
