#!/usr/bin/env python3

import unittest
import sys
sys.path.append("../../src")
import watson_nlu_interface as w_int
import csv_reader

class test_basic(unittest.TestCase):
    # Initialize by calling unittest.TestCase __init__ and
    # then initializing a couple of instance variables
    def __init__(self, *args, **kwargs):
        super(test_basic, self).__init__(*args, **kwargs)
        self.wint = w_int.watson_nlu_interface("../../data/session_details.csv")

    # test initialization sets correct values to object
    def test_1_w_int_init(self):
        print("Test #1.1 Checking all class attributes are correct:")
        # check class attributes
        self.assertEqual(self.wint._api_user, "apikey")
        self.assertEqual(self.wint._watson_api_key_field, "watson_nlu_api_key")
        self.assertEqual(self.wint._session_details_file_location, "../data/session_details.csv")
        self.assertEqual(self.wint._watson_nlu_endpoint, "https://gateway-syd.watsonplatform.net/natural-language-understanding/api")
        self.assertEqual(self.wint._watson_nlu_endpoint_suffix, "/v1/analyze?version=2019-07-12")
        print ("Done.\n")

        # check object attributes are correct
        print("Test #1.2 Checking all object attributes are correct:")
        # get the Watson NLU API key
        (apikey,) = csv_reader.get_csv_prop("../../data/session_details.csv", ["watson_nlu_api_key"])
        # check they are the same
        self.assertEqual(self.wint._api_key, apikey)
        print("Done.\n")

    # test the request token functionality
    def test_2_query_text_analyzer(self):
        print("Test #2 Check the Watson NLU text analyzer returns reasonable terms:")
        # two test sentences
        t_sent_1 = "I really like red herrings, especially those that come gift wrapped."
        t_sent_2 = "The mysterious flurry of the mechanical arm spread fear over the building."

        # get terms
        terms_1 = self.wint.query_text_analyzer(t_sent_1)
        terms_2 = self.wint.query_text_analyzer(t_sent_2)

        # check that the length of terms is lessser than the length of words in each test
        # sentence, and check that the returned terms are members of the set of words
        # from its corresponding test sentence
        simple_terms_1 = t_sent_1.split()
        simple_terms_2 = t_sent_2.split()

        self.assertTrue(len(simple_terms_1) > len(terms_1))
        self.assertTrue(len(simple_terms_2) > len(terms_2))

        # check the terms are part of the sentence
        for t1, t2 in zip(terms_1, terms_2):
            self.assertTrue(t1 in t_sent_1)
            self.assertTrue(t2 in t_sent_2)
        print("Done.\n")

if __name__ == "__main__":
    unittest.main()
