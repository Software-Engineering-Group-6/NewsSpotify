import requests
import base64
import csv_reader
import text_attributes as ta

# This class implements an interface
# to IBM Watson's Natural Language Understanding
# interface. We use it to break down news headlines
# and user defined sentences into key terms and
# to analyze the overall sentiment.
class watson_nlu_interface:
    # _api_user is used as the username
    _api_user = "apikey"
    # we get the API key from the session details file
    _api_key = ""
    # Name of the API key field in session details file
    _watson_api_key_field = "watson_nlu_api_key"
    # Location and name of session details CSV file
    _session_details_file_location = "../data/session_details.csv"
    # URL of Watson NLU interface endpoint
    _watson_nlu_endpoint = "https://gateway-syd.watsonplatform.net/natural-language-understanding/api"
    # suffix for the watson nlu endpoint which
    # allows us to point to the right API (and right version of it)
    _watson_nlu_endpoint_suffix = "/v1/analyze?version=2019-07-12"
    
    # initialize the watson nlu interface with the correct API key
    def __init__(self):
        (self._api_key,) = csv_reader.get_csv_prop(self._session_details_file_location, [self._watson_api_key_field])
        
    # this method takes a sentence defined by the user
    # or given by news headlines, breaks it down into
    # key terms and figures out the overall sentiment
    # thanks to Watson's NLU API. We then build
    # a TextAttributes object from the text_attributes
    # module with the key terms and overall sentiment
    # and return that
    def query_text_analyzer(self, text):
        x = base64.urlsafe_b64encode((self._api_user + ":" + self._api_key).encode()).decode()
        headers = {"Content-Type" : "application/json", "Authorization" : "Basic " + x }
        #payload = {"text" : text, "features" : {"sentiment" : {}, "categories" : {}, "concepts" : {}, "entities" : {}, "keywords" : {} }}
        payload = { "text": text, "features": { "sentiment": {}, "concepts" : {}, "entities" : {}, "keywords" : {} } }

        # Make the POST request
        res = requests.post(self._watson_nlu_endpoint + self._watson_nlu_endpoint_suffix, headers = headers, json = payload)
        if res.status_code == 200:
            # good
            # get key terms
            terms = []
            keywords = res.json()["keywords"]
            for k in keywords:
                terms.append(k["text"])
            # get overall sentiment
            sentiment = res.json()["sentiment"]["document"]["score"]
            # build object and return it
            return ta.TextAttributes(terms, sentiment)
        else:
            # not good
            print (f"Error trying to connect with {self._watson_nlu_endpoint} for text analysis...")
            # return None since we can't build a
            # TextAttributes object
            return None
