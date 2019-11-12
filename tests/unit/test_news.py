#!/usr/bin/env python3

import unittest
import sys

sys.path.append("../../src")
import news

class test_basic(unittest.TestCase):
    # Initialize by calling unittest.TestCase __init__ and
    # then initializing a couple of instance variables
    def __init__(self, *args, **kwargs):
        super(test_basic, self).__init__(*args, **kwargs)
        print("Creating mock News API replies")
        self.mock_api_answer = [{"source": "BBC News", "description": "Astros win world series"},
                                {"source": "Sky News", "description": "Israel new PM"},
                                {"source": "Fox News", "description": "France has protests"},
                                {"source": "CNBC", "description": "New Arab Spring?"},
                                {"source": "Bloomberg", "description": "Interest Rates Go Negative"},
                                {"source": "Bloomberg", "description": "Interest Rates Go Sideways"},
                                {"source": "Bloomberg", "description": "The cake is a lie"},
                                {"source": "CNN News", "description": "Primaries incoming"},
                                {"source": "CNN News", "description": "Sanders drops the ball"},
                                {"source": "Fox News", "description": "Trump leads in the polls"},
                                {"source": "Fox News", "description": "Tulsi Gabbard leads the polls"}]
    # runs test on the initialization function of the News object from the news module
    def test_1_news_init(self):
        print("Test #1 for news.__init__(...) with mock News API replies:")
        news_out = []

        # go through each mock API answer and initialize a News object
        for a in self.mock_api_answer:
            news_out.append(news.News(a["description"], a["source"]))
            # run the check through the news_tester function defined below
            self.news_tester(news_out[-1], a)
        print("Done.")

    # this method takes the mock News API answer and checks it against the values of the
    # correspondingly constructed News object
    def news_tester(self, n, m):
        self.assertEqual(n.headline, m["description"])
        self.assertEqual(n.source, m["source"])

if __name__ == "__main__":
    unittest.main()
