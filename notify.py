from threading import get_native_id
import firebase_admin
from firebase_admin import credentials, messaging
from pkg_resources import require
import requests

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)


def send_to_token():
    # [START send_to_token]
    # This registration token comes from the client FCM SDKs.
    registration_token = 'YOUR_REGISTRATION_TOKEN'

    # See documentation on defining a message payload.
    message = messaging.Message(
        data={
            'score': '850',
            'time': '2:45',
        },
        token=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)