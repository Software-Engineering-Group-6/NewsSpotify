#!/usr/bin/env python3

import unittest
import sys
sys.path.append("../../src")
import news_interface as n_int
import csv_reader

class test_basic(unittest.TestCase):
    # Initialize by calling unittest.TestCase __init__ and
    # then initializing a couple of instance variables
    def __init__(self, *args, **kwargs):
        super(test_basic, self).__init__(*args, **kwargs)
        self.nint = n_int.news_interface("../../data/session_details.csv")

    # test initialization sets correct values to object
    def test_1_n_int_init(self):
        print("Test #1.1 Checking all class attributes are correct:")
        # check class attributes
        self.assertEqual(n_int.news_interface.news_search_endpoint, "https://newsapi.org/v2/top-headlines")
        self.assertEqual(n_int.news_interface.session_details_location, "../data/session_details.csv")
        self.assertEqual(n_int.news_interface.api_property, "news_api_key")
        self.assertEqual(n_int.news_interface.news_country, "gb")
        print("Done.\n")

        print("Test #1.2 Checking the loaded API key is correct:")
        
        # get API key from the file
        (apikey, ) = csv_reader.get_csv_prop("../../data/session_details.csv", ["news_api_key"])

        # check the api keys are the same for our initialized News interface
        self.assertEqual(self.nint._api_key, apikey)
        
        print("Done.\n")

    def test_2_breaking_news(self):
        print("Test #2 Checking the breaking_news(...) method returns n news and excludes the sources we indicate:")

        # Perform 2 tests in total with different expected number of news and different excluded sources

        # first no exclusions, 10 headlines:
        ar = self.nint.get_breaking_news(10)
        self.assertEqual(len(ar), 10)

        # get a news source
        ex_ns = ar[-1].source

        # make a request with 10 headlines
        # excluding our found source
        ar2 = self.nint.get_breaking_news(10, [ex_ns])
        self.assertTrue(len(ar2) <= 10)
        # check our excluded source is not
        # among the responses
        self.assertTrue(ex_ns not in [a.source for a in ar2])

        print("Done.\n")
        
if __name__ == "__main__":
    unittest.main()
