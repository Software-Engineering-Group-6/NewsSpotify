#!/usr/bin/env python3

import unittest
import sys
sys.path.append("../../src")
import csv_reader

class test_basic(unittest.TestCase):
    def test_get_csv_prop(self):
        # "../../data/session_details.csv"
        # first test with a nonexistent file
        print("Test #1.1 for get_csv_prop(...) with non existent file:")
        print("Expected 'Error trying to open file at ...' from exception:")
        out = csv_reader.get_csv_prop("non_existent_file.extension", [])
        # check we got an empty tuple
        self.assertEqual(out, ())

        # secondly, test with values that are in the
        # csv and with values that are not in the csv
        # only those in the csv should be returned to us, and
        # they should be correct
        print("Test #1.1 Done.\n")
        print("Test #1.2 for get_csv_prop(...) with a valid file, with existing and non-existing properties in it:")
        out = csv_reader.get_csv_prop("fixtures/good.csv", ["property_one",
                                                            "property_two",
                                                            "property_three",
                                                            "propert_four"])
        # test the values are correct, assuming order:
        # 1) property_one 2) property_two 3) property_three
        self.assertEqual(out[0], "value_one")
        self.assertEqual(out[1], "value_two")
        self.assertEqual(out[2], "value_three")
        self.assertEqual(len(out), 3)
        
        print("Test #1.2 Done.\n")

        # thirdly, test with a badly formatted CSV file
        print("Test #1.3 for get_csv_prop(...) with a badly formatted CSV file, output should be empty")
        out = csv_reader.get_csv_prop("fixtures/bad.csv", ["really", "is"])
        # out should be an empty tuple
        self.assertEqual(out, ())
        print("Test #1.3 Done.\n")

if __name__ == "__main__":
    unittest.main()
