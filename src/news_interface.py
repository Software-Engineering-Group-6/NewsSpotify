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
        try:
            (self._api_key,) = csv_reader.get_csv_prop(file_loc, [news_interface.api_property])
        except:
            # it failed
            print("Error: cannot find News API's API Key.")
            print("\nPlease make sure your session_details.csv file has all the connection details")
            raise Exception
            
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
                    # if there is no description, try to use the title
                    title_art = self.get_news_object(a, use_description = False)
                    if title_art != None:
                        # is it not None, so it is valid, add it
                        news_out.append(title_art)
                    else:
                        continue
                else:
                    descr_art = self.get_news_object(a)
                    if descr_art != None:
                        # it is long enough, add it
                        news_out.append(descr_art)
                    else:
                        # it is not long enough, pass on this one
                        continue
            return news_out
        else:
            # bad
            # report the error and report None
            print("HTTP error {0} in News search operation...".format(res.status_code))
            return None

    # this method returns a News object for a given article
    # returned by the News API
    def get_news_object(self, art, use_description = True):
        # check the news headline is long enough, otherwise
        # Watson NLU won't be able to analyze it
        if use_description:
            key = "description"
        else:
            key = "title"
            # also try to clean the title
            art[key] = self.clean_news_title(art[key])
        hl = art[key]
        if len(hl.split()) > 3 and len(hl) > 15:
            # it is long enough, use it
            return news.News(art[key], art["source"]["name"])
        else:
            # it is not long enough, pass on this one
            return None

    # this method tries to cleanse an article title by trying to
    # remove the name of the source contained in the title
    # if we are using the article's description this is not
    # necessary
    def clean_news_title(self, title):
        # try to find the first instance of the character '-'
        # from the back
        for i in range(len(title) - 1, -1, -1):
            if title[i] == '-':
                # we found the point at which the news
                # title begins
                # slice it and return it
                return title[:i]
        # otherwise, if we found nothing, return the
        # title as is
        return title
