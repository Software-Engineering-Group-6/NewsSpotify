#!/usr/bin/env python3

import unittest
import sys
import time
sys.path.append("../../src")
import spotify_interface as s_int
import csv_reader
import track

class test_basic(unittest.TestCase):
    # Initialize by calling unittest.TestCase __init__ and
    # then initializing a couple of instance variables
    def __init__(self, *args, **kwargs):
        super(test_basic, self).__init__(*args, **kwargs)
        self.sint = s_int.spotify_interface("../../data/session_details.csv")

    # test initialization sets correct values to object
    def test_1_s_int_init(self):
        print("Test #1.1 Checking all class attributes are correct:")
        # check class attributes
        self.assertEqual(self.sint.sp_token_endpoint, "https://accounts.spotify.com/api/token")
        self.assertEqual(self.sint.sp_search_endpoint, "https://api.spotify.com/v1/search")
        
        # token
        self.assertEqual(self.sint._token, "");
        # token expiry
        self.assertEqual(self.sint._token_expiry, None)
        print("Done.\n")

        print("Test #1.2 Checking we correctly load auth. properties into Spotify interface:")
        # extract spotify_client_id and spotify_client_secret
        # then compare the values with the concents of the
        # initialized spotify interface
        (client_id, client_secret) = csv_reader.get_csv_prop("../../data/session_details.csv",
                                                             ["spotify_client_id", "spotify_client_secret"])

        # check with spotify interface values
        self.assertEqual(self.sint._client_id, client_id)
        self.assertEqual(self.sint._client_secret, client_secret)
        print("Done.\n")

    # test the request token functionality
    def test_2_request_token(self):
        # request token, inspect the changed values
        # and observe return status of function
        print("Test #2.1 Check we store token related data:")
        status = self.sint.request_token()
        self.assertEqual(status, True)
        self.assertNotEqual(self.sint._token, "")
        self.assertNotEqual(self.sint._token_expiry, None)
        self.assertTrue(self.sint._token_expiry > time.time())
        print("Done.\n")

        # corrupt client_id and client_secret on purpose
        print("Test #2.2 Check expected state of Spotify interface with incorrect auth. details:")
        print("Expected 'Error trying to connect with ...'")
        self.sint._client_id = "abcdefghijklmnopqrstuvwxyz1234567890"
        self.sint._client_secret = "abcdefghijklmnopqrstuvwxyz1234567890"
        # try to request token again, expect to fail
        status = self.sint.request_token()
        self.assertEqual(status, False)
        self.assertEqual(self.sint._token, "")
        self.assertEqual(self.sint._token_expiry, 0.0)
        print("Done.\n")

    # test the search tracks functionality
    def test_3_search_tracks(self):
        # send various terms and various limits and inspect outputs
        # note we are almost certainly within expiry time, if this
        # fails check the expiry time against request timing

        print("Test #3.1 Check we get expected results for 'ABBA' query:")
        status = self.sint.request_token()
        self.assertEqual(status, True)
        # terms 'ABBA'; limit 10
        self.check_search_results(["ABBA"], 10)
        print("Done.\n")
        # terms 'Daft Punk'; limit 20
        print("Test #3.2 Check we get expected results for 'Daft Punk' query:")
        self.check_search_results(["Daft Punk"], 20)
        print("Done.\n")
        # terms "Paint", "It", "Black", 5
        print("Test #3.3 Check we get expected results for 'Paint It Black' query:")
        self.check_search_results(["Paint", "It", "Black"], 5)
        print("Done.\n")

    # test the keepalive function
    def test_4_keep_alive(self):
        print("Test #4.1 Check keep alive function triggers when we go beyond token expiry:")
        # first request a token
        status = self.sint.request_token()
        self.assertEqual(status, True)
        # now mock time has passed by advancing beyond the expiry time
        self.sint._token_expiry = time.time() - 1
        # try to perform a search, keepalive should request a new
        # token and we should get terms back
        # if we do, keepalive has worked
        # note this function below asserts the results are good,
        # so it will communicate whether keepalive worked
        self.check_search_results(["Wu-Tang", "Clan"], 10)
        print("Done.\n")

    # this method checks the terms searched for
    # appear in the artists and name fields of the returned
    # track objects. it also checks the number of returned tracks
    # is within 1 and given limit
    def check_search_results(self, terms, limit):
        # request tracks with given parameters
        req = self.sint.search_tracks(terms, limit)
        # check size of returned playlist is within bounds
        self.assertTrue(limit > 0);
        self.assertTrue(len(req) > 0 and len(req) <= limit)
        # check some of the songs have terms in the artists field
        # or terms in the name field
        good_artist = False
        good_name = False
        for s in req:
            for t in terms:
                if t in s.artists:
                    good_artist = True
                if t in s.name:
                    good_name = True

        # make sure at least one of artists or name field contain
        # some of the search terms
        self.assertTrue(good_artist or good_name)

if __name__ == "__main__":
    unittest.main()
