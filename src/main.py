#!/usr/bin/env python3

import spotify_interface

def main():
    si = spotify_interface.spotify_interface()
    si.request_token()

if __name__ == "__main__":
    main()
