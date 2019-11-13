#!/usr/bin/env python3

import sys
import spotify_interface as s_int
import track

# This is our shippable product for Sprint 1
# It simply emulates a Spotify search since at this point,
# what we have implemented is the Spotify interface and
# the Track object.
#
# This is a command line tool that allows you to give it
# terms through the command line, and it will by default
# return a maximum of 10 songs.
#
# There is an option where you can define the maximum number
# of songs you want through the --max=n option.

def main():
    # maximum number of songs to return, 10 by default
    max_songs = 10
    # non-option collected terms from the command line
    # interface input
    terms = []

    # if there are no arguments, tell user how to use
    # our application
    if len(sys.argv) == 1:
        print("Please, provide terms for search in Spotify.")
        print("Note: no terms starting with '--' are allowed.")
        print("options available:")
        print("\t--max=n\twhere n is the maximum number of songs you want, 10 by default")
    else:
        # look for options
        for arg in sys.argv[1:]:
            # is it an option argument?
            if arg[:2] == "--":
                # this is an option argument
                toks = arg[2:].split('=')
                # which option is it?
                if toks[0] == "max":
                    # try to convert to integer
                    try:
                        max_songs = int(toks[1])
                    except:
                        # if we cannot, tell user why we cannot keep on
                        # going and exit
                        print("Error trying to convert '{0}' to integer...".format(toks[1]))
                        print("Fatal error, exiting.")
                        return
                else:
                    # if an unknown option has been given to us,
                    # tell the user and exit
                    print("Unknown option {0}".format(toks[0]))
                    print("Fatal error, exiting.")
                    return
            else:
                # it is a Spotify seach term
                terms.append(arg)
        # Check the maximum number of songs is greater than 1 and no bigger than 20
        if max_songs < 1 or max_songs > 20:
            print("Maximum number of songs to be outputted cannot be bigger than 20 or less than 1.")
            print("Fatal error, exiting.")
        else:
            # we are okay to continue, simply search for the songs with the given terms
            # initialize our Spotify interface
            si = s_int.spotify_interface()
            # request our communication token
            res = si.request_token()
            if res == False:
                print("Error trying to request a token from Spotify.")
                print("Fatal error, exiting.")
                return
            # search for the tracks
            tracks = si.search_tracks(terms, max_songs)
            if tracks == None:
                # no tracks were returned for the terms
                # the user has given us, tell user and
                # exit
                print("No tracks returned for given terms.")
                return
            else:
                # print the song data
                pretty_print_tracks(tracks)
                # exit
                return

# this method takes a list of Track objects
# and prints their contents in an orderly
# manner
def pretty_print_tracks(tracks):
    for t in tracks:
        print("==============================================")
        print("Title:\t\t", t.name)
        print("Artists:\t", ", ".join(t.artists))
        print("Duration:\t", t.duration_readable())
        print("Popularity:\t", "{:02d}/100".format(t.popularity))
        print("External URL:\t", t.external_url)
        prev_url = "N/A"
        if t.preview_url != "":
            prev_url = t.preview_url
        print("Preview URL:\t", prev_url)
    print("==============================================")

if __name__ == "__main__":
    main()
