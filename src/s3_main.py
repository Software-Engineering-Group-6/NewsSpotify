#!/usr/bin/env python3

import sys
import spotify_interface as s_int
import news_interface as n_int
import watson_nlu_interface as w_int
import track
import news
import re
import random
import time
import json

# This is our shippable product for Sprint 3
# It will by default take the given command
# line terms except options given and pipe
# those through into Spotify search,
# returning a playlist.
#
# However, if the option --news is specified,
# it will return a defined number of songs
# relating to the top breaking news
# of the day.
#
# To exclude news, the option --exclude=filename
# should be given where filename is the name
# of a file where each line is the name of a source
# to be excluded if found. Otherwise, no sources
# will be excluded.
#
#
# Options:
# --max=n        a maximum of n songs is returned
# --news         the tracks returned are a function of today's top news
# --exclude=file sources appearing in file (one per line) are excluded
# --json	 output results to stdout in JSON format

def main():
    # maximum number of songs to return, 10 by default
    max_songs = 10
    # non-option collected terms from the command line
    # interface input
    # ignored if the --news option is set
    terms = []
    # use news, off by default, to turn on, use --news
    use_news = False
    # output JSON?
    output_json = False
    # excluded sources, empty by default
    excl_sources = []

    # if there are no arguments, tell user how to use
    # our application
    if len(sys.argv) == 1:
        print("Please, provide terms for search in Spotify.")
        print("Note: no terms starting with '--' are allowed.")
        print("options available:")
        print("\t--max=n\twhere n is the maximum number of songs you want, 10 by default")
        print("\t--news\tuse today's top news to return songs, given terms ignored")
        print("\t--exclude=file\tsources appearing one per line in file are excluded")
        print("\t--json\toutput to stdout in JSON format")
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
                elif toks[0] == "news":
                    # turn on the use_news flag
                    use_news = True
                elif toks[0] == "exclude":
                    try:
                        excl_sources = get_excluded_sources(toks[1])
                    except:
                        print("Error trying to get excluded sources from file...")
                        print("Fatal error, exiting.")
                        return
                elif toks[0] == "json":
                    output_json = True
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
            # we are okay to continue
            # initialize our Spotify interface
            si = s_int.spotify_interface()
            # request our communication token
            res = si.request_token()
            if res == False:
                print("Error trying to request a token from Spotify.")
                print("Fatal error, exiting.")
                return
            # just do a simple search?
            if use_news == False:
                # search for the tracks
                tracks = si.search_tracks(terms, max_songs)
                if tracks == None:
                    # no tracks were returned for the terms
                    # the user has given us, tell user and
                    # exit
                    print("No tracks returned for given terms.")
                    return
                else:
                    # output to json?
                    if output_json:
                        print(output_to_json(tracks))
                    else:
                        # otherwise just do a pretty
                        # print
                        pretty_print_tracks(tracks)
                    # exit
                    return
            else:
                ni = n_int.news_interface()
                wi = w_int.watson_nlu_interface()
                tracks = []
                # get max_songs top news, excluding indicated sources
                top_news = ni.get_breaking_news(max_songs, excl_sources)
                # pass those news' headlines into Watson NLU
                # and get their fundamental terms
                # then tokenize those fundamental terms
                # and pass them to get_best_fit_track(...)
                # which will give us a song with good fit given
                # the headline, and append it to our output tracks
                for n in top_news:
                    n_terms = wi.query_text_analyzer(n.headline)
                    tokens = tokenize_terms(n_terms)
                    tracks += get_best_fit_track(si, tokens)
                # now that we have the tracks,
                # output to json?
                if output_json:
                    print(output_to_json(tracks, top_news))
                else:
                    # otherwise just do a pretty print
                    pretty_print_tracks(tracks, top_news)
                return

# this method takes a list of strings which may be sentences
# or may have characters such as commas, dots, exclamation marks
# and so on, and it returns a list of words without those characters
# as 'tokens'
def tokenize_terms(terms):
    tokens = []
    delims = " |\-|,|\.|:|!|\?|;"
    for t in terms:
        tokens += list(filter(None, re.split(delims, t)))
    # return tokens, but make sure they are unique (no duplicates)
    return list(dict.fromkeys(tokens))

# this method returns a track which matches a token, or n
# combination of tokens from Spotify
# this assumes the Spotify Interface passed has already
# requested a token
def get_best_fit_track(si, tokens):
    used = []
    # if the given tokens are None or of length 0,
    # return None
    if tokens is None or len(tokens) < 1:
        return None
    elif si is None:
        # if the spotify interface is None, return None
        return None
    # make sure we get a random seed
    random.seed(time.time())
    # progressively add terms from the tokens and stop where
    # we stop receiving tracks    
    while True:
        # token we picked for this iteration
        curr = tokens[random.randint(0, len(tokens) - 1)]
        # remove the token we picked for this iteration
        tokens.remove(curr)
        # search with our previous tokens + new one
        track = si.search_tracks(used + [curr], 1)
        if len(track) != 0:
            # at least 1 track matches
            # incorporate our current token
            # to our set and remove it from tokens
            used.append(curr)
        if len(tokens) < 1:
            # we have no more tokens to try
            # so we quit
            break
    # the final answer will be a search with our 'used'
    # tokens
    return si.search_tracks(used, 1)

# this method takes a list of Track objects
# and prints their contents in an orderly
# manner
def pretty_print_tracks(tracks, news = []):
    do_news = False
    if len(news) > 0:
        do_news = True
    for t in tracks:
        print("==============================================")
        if do_news:
            art = news[tracks.index(t)]
            print("News used:\nSource: {0}\nHeadline: {1}\n".format(art.source, art.headline))
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

# this method gets each line item for
# a given filename and returns that line stripped.
# this is used to get the excluded sources
# from a file, where each source to be excluded
# from the news result is written in its own
# line in a file
def get_excluded_sources(filename):
    out = []
    try:
        # try to open the file
        # reach each line and append
        # it to our list
        with open(filename) as f:
            for line in f:
                out.append(line.strip())
    except IOError:
        # there was an issue with I/O
        # report this to the user
        print(f"Error trying to open file at {filename}")
    # return our list, empty if there was an
    # issue with I/O
    return out
# this method takes the tracks we
# generated from the news headlines
# or terms given by the user, along
# with the news (if we used any)
# and outputs all the data in JSON
# format so the UX application
# can better parse it and show
# it in its interface
#
# this gets called only if the --json
# option is activated by the caller
def output_to_json(tracks, news = []):
    # items which contain news used
    items = []
    # (if any) and track
    # did we get news?
    no_news = False
    if news == []:
        # no news
        no_news = True
    # go through each track
    for t in tracks:
        it = {}
        # if we do have news
        if not no_news:
            # get the corresponding news
            n = news[tracks.index(t)]
            it['news'] = news_to_dict(n)
        else:
            it['news'] = {}
        # now do the track
        it['track'] = track_to_dict(t)
        # add this item to our list
        # of items
        items.append(it)
    # once we are done with all tracks
    # and news, return the result
    # as json
    try:
        # build json string
        json_data = json.dumps(items)
        # all good, return json data
        return json_data
    except:
        # if anything went wrong
        return None

# this method takes a track object and
# turns it in to a dictionary
# where each object data member
# is a key:value pair. The
# duration_readable(...) method from
# the Track object is called and the
# outputted string is put into another
# key:value pair
def track_to_dict(track):
    if track is None:
        return None
    else:
        d = {"artists" : track.artists,
             "duration" : track.duration_readable(),
             "name" : track.name,
             "popularity" : track.popularity,
             "preview_url" : track.preview_url,
             "external_url" : track.external_url}
        return d

# this method takes a News object
# and returns a dictionary where
# its object data members are
# key:value pairs
def news_to_dict(_news):
    if _news is None:
        return None
    else:
        d = {"headline" : _news.headline,
             "source" : _news.source}
        return d
 
if __name__ == "__main__":
    main()
