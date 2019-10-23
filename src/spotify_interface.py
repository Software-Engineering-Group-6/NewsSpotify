#!/usr/bin/env python3

# We do a client credentials flow authentication:
# https://developer.spotify.com/documentation/general/guides/authorization-guide/
#
# Therefore, we cannot access user data but we can easily authenticate
# our application.

import base64
import time
import requests
import csv_reader
import track
from enum import Enum

# Session details enumeration:
class s_details(Enum):
    CLIENT_ID = "spotify_client_id"
    CLIENT_SECRET = "spotify_client_secret"
    FILE_LOCATION = "../data/session_details.csv"

class spotify_interface:
    # Spotify token request endpoint
    sp_token_endpoint = "https://accounts.spotify.com/api/token"
    # Spotify search endpoint
    sp_search_endpoint = "https://api.spotify.com/v1/search"
    
    # The credentials used to authenticate ourselves
    # to Spotify:
    _client_id = ""
    _client_secret = ""
    # The token for subsequent communication:
    _token = ""
    _token_expiry = None
    
    def __init__(self):
        # Get the credentials from the csv file
        (self._client_id, self._client_secret) = csv_reader.get_csv_prop(s_details.FILE_LOCATION.value,
                                                                         [s_details.CLIENT_ID.value,
                                                                          s_details.CLIENT_SECRET.value])

    # This method requests an access token from Spotify
    # If things are good, return True, otherwise return False
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
        res = requests.post(self.sp_token_endpoint, headers = headers, data = payload)
        if res.status_code == 200:
            # good
            # store the token
            self._token = res.json()["access_token"]
            # store the expiry time of the token
            self._token_expiry = float(res.json()["expires_in"]) + time.time()
        else:
            # not good
            print (f"Error trying to connect with {self.sp_token_endpoint} for token request...")
            self._token = ""
            self._token_expiry = 0.0
            return

    # This method checks whether the token we currently
    # hold has expired. If it has, request a new one
    # Return True if it has not expired, or if it
    # expired but we were able to renew it
    # False if it expired and we were not able
    # to renew it
    def keepalive_token(self):
        if time.time() + 1 > self._token_expiry:
            # it has expired, or is near to expiring
            if self.request_token():
                return True
            else:
                # we could not properly renew the token...
                return False
        else:
            # It has not expired
            return True

    # This method retrieves a set of tracks from Spotify
    # according to given search terms in a list
    # Returns tracks of type Track class,
    # returns False if unsuccessful
    def search_tracks(self, terms, limit):
        headers = {"Authorization" : "Bearer {0}".format(self._token)}
        payload = {"q" : "", "type" : "track", "limit" : str(limit)}
        space = "+" # used to separate search terms
        for t in terms:
            if payload["q"] == "":
                payload["q"] = t
            else:
                payload["q"] += space + t
        # before a request, always make sure the token is
        # kept alive
        self.keepalive_token()
        res = requests.get(self.sp_search_endpoint, headers = headers, params = payload)
        if res.status_code == 200:
            # good
            # now build a list of tracks
            items = res.json()["tracks"]["items"]
            out = []
            for i in items:
                out.append(track.Track(i))
            return out
        else:
            # bad
            print("HTTP error {0} in Spotify search operation...".format(res.status_code))
            return False
                
        
