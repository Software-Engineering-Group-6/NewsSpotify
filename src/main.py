#!/usr/bin/env python3

import spotify_interface, json

def main():
    si = spotify_interface.spotify_interface()
    si.request_token()
    data = si.search_tracks(["sharing", "the", "night", "together"], 1)
    if data != False:
        print("Number of tracks {0}".format(len(data)))
        print(data)

if __name__ == "__main__":
    main()
