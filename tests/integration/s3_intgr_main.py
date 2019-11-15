#!/usr/bin/env python3

# Integration tests for Sprint  - all the functionality we
# have implemented so far we try to test together after it
# has been 'unit tested' and observe the results are consistent
# with what we expect.

import re
import random
import time
import json

import sys
sys.path.append("../../src")
import news_interface as n_int
import watson_nlu_interface as w_int
import spotify_interface as s_int

def main():
    # tracks 
    tracks = []
    si = s_int.spotify_interface("../../data/session_details.csv")
    ni = n_int.news_interface("../../data/session_details.csv")
    wi = w_int.watson_nlu_interface("../../data/session_details.csv")

    # request token from spotify API
    si.request_token()
    
    # load excluded sources from the fixtures
    excl_sources = get_excluded_sources("fixtures/exclusion")
    
    # get 10 breaking news excluding the BBC News source
    news = ni.get_breaking_news(10, excl_sources)
    # check we got news at all
    if len(news) != 0:
        # now, pipe those news descriptions into the watson nlu text analyzer
        for n in news:
            # store it in our list of term lists
            n_terms = wi.query_text_analyzer(n.headline)
            # tokenize it
            tokens = tokenize_terms(n_terms)
            # get best fit
            tracks += get_best_fit_track(si, tokens)
        # now, print out those terms
        pretty_print_tracks(tracks, news)
        # now print the Json
        print("JSON output:")
        print(output_to_json(tracks, news))
    else:
        print("We received no news.")

    # INTEGRATION TEST: make sure the outputted terms make sense in relation
    # to today's news by checking what the top 10 breaking news are today
    # in Great Britain, excepting BBC News articles.

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
