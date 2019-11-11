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
                if a["name"] != "":
                    self.artists.append(a["name"])
            # Duration
            self.duration = d["duration_ms"]
            # Name of the track
            self.name = d["name"]
            # Popularity
            self.popularity = d["popularity"]
            # Preview URL
            if d["preview_url"] != None:
                self.preview_url = d["preview_url"]
            # External URL
            if d["external_urls"]["spotify"] != None:
                self.external_url = d["external_urls"]["spotify"]
        except TypeError as te:
            print("Type error: {0}".format(te))
        except KeyError as ke:
            print("Key error: {0}".format(ke))
        except:
            print("Unexpected error:", sys.exc_info()[0])

    # This method returns the duration in
    # a human readable form
    def duration_readable(self):
        min = math.floor((self.duration / 1000.0) / 60)
        sec = (self.duration / 1000.0) % 60.0
        if math.floor(sec) + 0.5 > sec:
            sec = math.floor(sec)
        else:
            sec = math.ceil(sec)
        return str(min) + ":" + "{0:0=2d}".format(sec)
