#!/usr/bin/env python3

class News:
    # Initialize fields with dictionary
    # of fields from JSON
    def __init__(self, hl, s):
        self.headline = hl
        self.source = s
