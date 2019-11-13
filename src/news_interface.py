#!/usr/bin/env python3

import requests
import json
import time
import datetime
import requests

import csv_reader
import news

class news_interface:
    # News API search endpoint
    news_search_endpoint = "https://newsapi.org/v2/top-headlines"

    # session_details.csv location
    session_details_location = "../data/session_details.csv"

    # name of the property in the session_details.csv file for our API key
    api_property = "news_api_key"

    # the country where we search for the top headlines
    news_country = "gb"

    def __init__(self, file_loc = session_details_location):
        # retrieve the API key from the session_details.csv file
        (self._api_key,) = csv_reader.get_csv_prop(file_loc, [news_interface.api_property])
        
    # this method returns n News objects with their corresponding headlines
    # and source. if excluded_sources are defined, those news headlines from
    # the specified sources will be excluded from the output
    # return None if there is an error
    def get_breaking_news(self, n, excluded_sources = []):
        # build the payload to be sent to the news API service
        payload = {"country" : news_interface.news_country, "apiKey" : self._api_key}
        # make the request
        res = requests.get(news_interface.news_search_endpoint, headers = {}, params = payload)
        # check the return status is good
        if res.status_code == 200:
            # good
            # input articles from News API
            inp_articles = res.json()["articles"]
            # News we return
            news_out = []
            for a in inp_articles:
                if len(news_out) >= n:
                    break
                elif a["source"]["name"] in excluded_sources:
                    # we excluded this article
                    continue
                elif a["description"] == "" or a["description"] == None:
                    # if there is no description, exclude it
                    continue
                else:
                    # check the news headline is long enough, otherwise
                    # Watson NLU won't be able to analyze it
                    hl = a["description"]
                    if len(hl.split()) > 3 and len(hl) > 15:
                        # it is long enough, add it
                        news_out.append(news.News(a["description"], a["source"]["name"]))
                    else:
                        # it is not long enough, pass on this one
                        continue
            return news_out
        else:
            # bad
            # report the error and report None
            print("HTTP error {0} in News search operation...".format(res.status_code))
            return None
