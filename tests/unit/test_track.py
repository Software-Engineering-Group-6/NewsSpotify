#!/usr/bin/env python3

import unittest
import json

import sys
sys.path.append("../../src/")
import track

# track_normal_1.json =>
#       artists = ["The Killers"]
#       duration = 222200
#       name = "Mr. Brightside"
#       popularity = 76
#       preview_url = ""
#       external_url = "https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp"
#       duration_readable() = "3:42"
    
# track_normal_2.json =>
#       artists = ["Carly Rae Jepsen"]
#       duration = 207959
#       name = "Cut To The Feeling"
#       popularity = 7
#       preview_url = ""
#       external_url = "https://open.spotify.com/track/11dFghVXANMlKmJXsNCbNl"
#       duration_readable() = "3:27"
    
# track_corrupt_1.json and track_corrupt_2.json =>
#       artists = [""]
#       duration = 0
#       name = ""
#       popularity = 0
#       preview_url = ""
#       external_url = ""
#       duration_readable() = "0"

class test_basic(unittest.TestCase):
    # Initialize by calling unittest.TestCase __init__ and
    # then initializing a couple of instance variables
    def __init__(self, *args, **kwargs):
        super(test_basic, self).__init__(*args, **kwargs)
        self.f_norm_1 = None
        self.f_norm_2 = None
        self.f_corr_1 = None
        self.f_corr_2 = None
        
        # Load test fixture data
        # Normal and valid JSON first
        try:
            f = open("fixtures/track_normal_1.json", "r")
            self.f_norm_1 = json.load(f)
            f.close()
            f = open("fixtures/track_normal_2.json", "r")
            self.f_norm_2 = json.load(f)
            f.close()
        except IOError as ioe:
            print("I/O error: {0}".format(ioe))
        except json.JSONDecodeError as jde:
            print("JSON decode error: {0}".format(jde))
        
        # Now corrupt JSON 1 - this one should not yield JSONDecodeError
        try:
            f = open("fixtures/track_corrupt_1.json", "r")
            self.f_corr_1 = json.load(f)
        except IOError as ioe:
            print("I/O error: {01}".format(ioe))
        except json.JSONDecodeError as jde:
            print("JSON decode error: {0}".format(jde))
        finally:
            f.close()
        # And corrupt JSON 2 - this one should yield JSONDecodeError
        try:
            f = open("fixtures/track_corrupt_2.json", "r")
            self.f_corr_2 = json.load(f)
        except IOError as ioe:
            print("I/O error: {0}".format(ioe))
        except json.JSONDecodeError:
            print("Passing JSONDecodeError for a corrupt JSON...")
            pass
        finally:
            f.close()
    
    def test_track_init(self):
        # build expected data objects
        # track_normal_1.json
        exp_norm_1 = {}
        exp_norm_1["artists"] = ["The Killers"]
        exp_norm_1["duration"] = 222200
        exp_norm_1["name"] = "Mr. Brightside"
        exp_norm_1["popularity"] = 76
        exp_norm_1["preview_url"] = ""
        exp_norm_1["external_url"] = "https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp"
        exp_norm_1["duration_readable"] = "3:42"
        
        # track_normal_2.json
        exp_norm_2 = {}
        exp_norm_2["artists"] = ["Carly Rae Jepsen"]
        exp_norm_2["duration"] = 207959
        exp_norm_2["name"] = "Cut To The Feeling"
        exp_norm_2["popularity"] = 7
        exp_norm_2["preview_url"] = ""
        exp_norm_2["external_url"] = "https://open.spotify.com/track/11dFghVXANMlKmJXsNCbNl"
        exp_norm_2["duration_readable"] = "3:27"
        
        # track_corrupt_1.json
        exp_corr_1 = {}
        exp_corr_1["artists"] = []
        exp_corr_1["duration"] = 0
        exp_corr_1["name"] = ""
        exp_corr_1["popularity"] = 0
        exp_corr_1["preview_url"] = ""
        exp_corr_1["external_url"] = ""
        exp_corr_1["duration_readable"] = "0:00"
        
        # track_corrupt_2.json - we expect the same output as with
        # track_corrupt_1.json
        exp_corr_2 = exp_corr_1 
        
        # Build normal tracks first
        t_norm_1 = track.Track(self.f_norm_1)
        t_norm_2 = track.Track(self.f_norm_2)
        # Now corrupt ones
        t_corr_1 = track.Track(self.f_corr_1)
        t_corr_2 = track.Track(self.f_corr_2)
        
        # Testing loaded JSON
        # Good ones
        self.assertTrue(isinstance(self.f_norm_1, dict))
        self.assertTrue(isinstance(self.f_norm_2, dict))
        # Bad ones
        self.assertTrue(isinstance(self.f_corr_1, dict))
        self.assertIs(self.f_corr_2, None)
        
        # Testing Track objects
        self.assertTrue(isinstance(t_norm_1, track.Track))
        self.assertTrue(isinstance(t_norm_2, track.Track))
        self.assertTrue(isinstance(t_corr_1, track.Track))
        self.assertTrue(isinstance(t_corr_2, track.Track))
        
        # Checking correct field values for t_norm_1, t_norm_2 and t_corr_1

        # t_norm_1
        self.track_tester(t_norm_1, exp_norm_1)
        # t_norm_2
        self.track_tester(t_norm_2, exp_norm_2)
        # t_corr_1
        self.track_tester(t_corr_1, exp_corr_1)
        # t_corr_2
        self.track_tester(t_corr_2, exp_corr_2)

    def track_tester(self, t, d):
        self.assertEqual(t.artists, d["artists"])
        self.assertEqual(t.duration, d["duration"])
        self.assertEqual(t.name, d["name"])
        self.assertEqual(t.popularity, d["popularity"])
        self.assertEqual(t.preview_url, d["preview_url"])
        self.assertEqual(t.external_url, d["external_url"])
        self.assertEqual(t.duration_readable(), d["duration_readable"])
        
if __name__ == "__main__":
    unittest.main()
