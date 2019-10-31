#!/usr/bin/env python3

import spotify_interface as s_int
import watson_nlu_interface as w_int

def main():
    si = s_int.spotify_interface()
    wi = w_int.watson_nlu_interface()
    phrase = "This phrase is very positive."
    
    si.request_token()
    tracks = si.search_tracks(["circles", "post", "malone"], 10)
    for i in tracks:
        print("Name: ", i.name, "  Artists: ", i.artists, "  Duration: ", i.duration_readable())
    txt_att = wi.query_text_analyzer(phrase)
    print("For phrase: '{0}' the key terms are: {1} and the overall sentiment is ~{2:.2f}".format(phrase, txt_att.key_terms, txt_att.overall_sentiment))
    
if __name__ == "__main__":
    main()
