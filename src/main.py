#!/usr/bin/env python3

import spotify_interface as s_int
import watson_nlu_interface as w_int
import news_interface as n_int

def main():
    si = s_int.spotify_interface()
    wi = w_int.watson_nlu_interface()
    ni = n_int.news_interface()
    
    si.request_token()
    tracks = si.search_tracks(["circles", "post", "malone"], 10)
    for i in tracks:
        print("Name: ", i.name, "  Artists: ", i.artists, "  Duration: ", i.duration_readable())
    news = ni.get_breaking_news(10, ["BBC News"])
    for n in news:
        print("Source: {0}, Headline: {1}".format(n.source, n.headline))
    
if __name__ == "__main__":
    main()
