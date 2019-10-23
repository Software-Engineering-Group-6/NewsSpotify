#!/usr/bin/env python3

import math

class Track:
    artists = []
    duration = 0 # 0-100, 100 being the most popular
    name = ""
    popularity = 0
    preview_url = ""
    external_url = ""

    # Initialize fields with dictionary
    # of fields from JSON
    def __init__(self, d):
        # Artists
        self.artists = []
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

    # This method returns the duration in
    # a human readable form
    def duration_readable(self):
        min = math.floor((self.duration / 1000.0) / 60)
        sec = round((self.duration / 1000.0) % 60.0)
        return str(min) + ":" + "{0:0=2d}".format(sec)
