import nltk.data
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords


class Tokenizer(object):
    
    def __init__(self, language='english'):
        self.paragraph_tokenizer = nltk.data.load('tokenizers/punkt/%s.pickle' % language)
        self.sentence_tokenizer = TreebankWordTokenizer()
        self.english_stops = set(stopwords.words(language))
        
    def tokenize(self, text, remove_stopwords=False):
        sentences = self.paragraph_tokenizer.tokenize(text)
        token = []
        for sentence in sentences:
            words = self.sentence_tokenizer.tokenize(sentence)
            if remove_stopwords:
                token.append([word for word in words if word not in self.english_stops])
            else:
                token.append(words)
        return token