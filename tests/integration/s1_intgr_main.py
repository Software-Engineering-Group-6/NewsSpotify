#!/usr/bin/env python3

# Integration tests for Sprint 1 - all the functionality we
# have implemented so far we try to test together after it
# has been 'unit tested' and observe the results are consistent
# with what we expect.

import sys
sys.path.append("../../src")
import spotify_interface as s_int
import track

def main():
    si = s_int.spotify_interface("../../data/session_details.csv")

    # request token from Spotify
    si.request_token()
    # request tracks from the spotify API
    tracks = si.search_tracks(["circles", "post", "malone"], 10)
    # print the track attributes, one per line
    for i in tracks:
        print("Name: ", i.name, "  Artists: ", i.artists, "  Duration: ", i.duration_readable())

    # INTEGRATION TEST: compare the output of our application to that of the
    # Spotify client, any differences must be resolved.
    
if __name__ == "__main__":
    main()
