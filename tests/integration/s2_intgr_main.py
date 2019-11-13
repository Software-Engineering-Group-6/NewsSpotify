#!/usr/bin/env python3

# Integration tests for Sprint 2 - all the functionality we
# have implemented so far we try to test together after it
# has been 'unit tested' and observe the results are consistent
# with what we expect.

import sys
sys.path.append("../../src")
import news_interface as n_int
import watson_nlu_interface as w_int

def main():
    ni = n_int.news_interface("../../data/session_details.csv")
    wi = w_int.watson_nlu_interface("../../data/session_details.csv")

    # get 10 breaking news excluding the BBC News source
    news = ni.get_breaking_news(10, ["BBC News"])
    # check we got news at all
    if len(news) != 0:
        # now, pipe those news descriptions into the watson nlu text analyzer
        term_set = []
        for n in news:
            # store it in our list of term lists
            term_set.append(wi.query_text_analyzer(n.headline))
        # now, print out those terms
        print("Fundamental terms from today's headlines:")
        for tl in term_set:
            print(tl)
    else:
        print("We received no news.")

    # INTEGRATION TEST: make sure the outputted terms make sense in relation
    # to today's news by checking what the top 10 breaking news are today
    # in Great Britain, excepting BBC News articles
    
if __name__ == "__main__":
    main()
