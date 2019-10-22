#!/usr/bin/env python3

# We do a client credentials flow authentication:
# https://developer.spotify.com/documentation/general/guides/authorization-guide/
#
# Therefore, we cannot access user data but we can easily authenticate
# our application.

import csv
import base64
import requests
from enum import Enum

# Spotify token request address
sp_token_address = "https://accounts.spotify.com/api/token"

# Session details enumeration:
class s_details(Enum):
    CLIENT_ID = "spotify_client_id"
    CLIENT_SECRET = "spotify_client_secret"
    FILE_LOCATION = "../data/session_details.csv"

class spotify_interface:
    # The credentials used to authenticate ourselves
    # to Spotify:
    _client_id = ""
    _client_secret = ""
    
    def __init__(self):
        # Get the credentials from the csv file
        try:
            with open(s_details.FILE_LOCATION.value) as f:
                r = csv.reader(f, delimiter = ',')
                for line in r:
                    if line[0] == s_details.CLIENT_ID.value:
                        self._client_id = line[1].strip()
                    elif line[0] == s_details.CLIENT_SECRET.value:
                        self._client_secret = line[1].strip()
        except IOError:
            print(f"Error trying to open file at {s_details.FILE_LOCATION.value}")
                
    def request_token(self):
        # We need to send a POST request to
        # https://accounts.spotify.com/api/token
        # with header "Authorization" : "Basic x"
        # where x = base64('client_id:client_secret')
        # as well as body parameter grant_type='client_credentials'
        x = base64.urlsafe_b64encode((self._client_id + ":" + self._client_secret).encode()).decode()
        headers = {"Authorization" : "Basic " + x}
        payload = {"grant_type" : "client_credentials"}

        # Make the POST request
        res = requests.post(sp_token_address, headers = headers, data = payload)
        print(res.status_code)
        print(res.json())
