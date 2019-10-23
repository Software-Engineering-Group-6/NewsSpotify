#!/usr/bin/env python3

import spotify_interface
import track

def main():
    si = spotify_interface.spotify_interface()
    si.request_token()
    tracks = si.search_tracks(["circles", "post", "malone"], 10)
    for i in tracks:
        print("Name: ", i.name, "  Artists: ", i.artists, "  Duration: ", i.duration_readable())
    
if __name__ == "__main__":
    main()
