# Holds the key terms of a headline or sentence, along
# with its overall sentiment. Sentiment is a float
# with range -1.0 to 1.0 where 1.0 is the most positive
# a sentence can be and -1.0 the most negative a sentence
# can be; 0 means neutral sentiment.
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
