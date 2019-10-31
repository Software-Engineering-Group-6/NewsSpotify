#!/usr/bin/env python3

import math
import sys

class Track:
    # Initialize fields with dictionary
    # of fields from JSON
    def __init__(self, d):
        self.artists = []
        self.duration = 0
        self.name = ""
        self.popularity = 0 # 0-100, 100 being the most popular
        self.preview_url = ""
        self.external_url = ""
        
        try:
            # Artists
            for a in d["artists"]:
                self.artists.append(a["name"])
                # Duration
                self.duration = d["duration_ms"]
                # Name of the track
                self.name = d["name"]
                # Popularity
                self.popularity = d["popularity"]
                # Preview URL
                self.preview_url = d["preview_url"]
                # External URL
                self.external_url = d["external_urls"]["spotify"]
        except TypeError as te:
            errno, errstr = te.args
            print("Type error {0}: {1}".format(errno, errstr))
        except KeyError as ke:
            errno, errstr = ke.args
            print("Key error {0}: {1}".format(errno, errstr))
        except:
            print("Unexpected error:", sys.exc_info()[0])

    # This method returns the duration in
    # a human readable form
    def duration_readable(self):
        min = math.floor((self.duration / 1000.0) / 60)
        sec = round((self.duration / 1000.0) % 60.0)
        return str(min) + ":" + "{0:0=2d}".format(sec)
