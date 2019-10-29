# Holds the key terms of a headline or sentence, along
# with its overall sentiment.
class TextAttributes:
    key_terms = []
    overall_sentiment = 0.0
    
    def __init__(self, terms, sent):
        self.key_terms = terms
        if sent < -1.0:
            self.overall_sentiment = -1.0
        elif sent > 1.0:
            self.overall_sentiment = 1.0
        else:
            self.overall_sentiment = sent
