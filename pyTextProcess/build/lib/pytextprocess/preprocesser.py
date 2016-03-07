from extracter import *
from tokenizer import *
from tagger import *
from lemmatizer import *
from time import time
from replacer import AntonymReplacer
from time import time


class Preprocesser(object):

    def __init__(self, tagger_backup):
        t0 = time()
        print 'Initialisation ...'
        self.extracter = Extracter()
        self.tokenizer = Tokenizer()
        self.tagger = Tagger(name=tagger_backup)
        self.replacer = AntonymReplacer()
        self.lemmatizer = Lemmatizer()
        print 'Initialisation done in %0.3fs.' % (time() - t0)
    
    def preprocess(self, text):
        t0 = time()
        preprocessed_jokes = []
        for joke in text:
            # Jokes tokenization...
            tokenized_joke = self.tokenizer.tokenize(joke, remove_stopwords=False)
            # Jokes tokenization done!
            # Jokes POS Tagging...
            tagged_sentences = self.tagger.tag_sentences(tokenized_joke)
            tagged_joke = self.tagger.map_tag(tagged_sentences)
            # Jokes POS Tagging done!
            # Jokes negation replacement...
            tagged_joke2 = []
            for sentence in tagged_joke:
                tagged_joke2.append(self.replacer.replace_negations(sentence))
            # Jokes negation replacement done!
            # Jokes lemmatization...
            lemmatized_joke = self.lemmatizer.lemmatize_sentences(tagged_joke2)
            # Jokes lemmatization done!
            # Jokes removing stopwords and punctuation...
            normalized_joke = self.extracter.remove_stopwords(lemmatized_joke)
            # Jokes removing stopwords and punctuation!
            # Jokes transformation from list of tokens into concatenation of tokens...
            preprocessed_joke = ''
            for normalized_sentence in normalized_joke:
                preprocessed_joke = preprocessed_joke +' '+' '.join(normalized_sentence)
            preprocessed_jokes.append(preprocessed_joke.strip())
            # Jokes transformation from list of tokens into concatenation of tokens!
        print 'Preprocessing done in %0.3fs.' % (time() - t0)
        return preprocessed_jokes
#    def preprocess(self, path='data/jokes/'):
#        #path = 'data/jokes/'
#        html_jokes = self.retriever.read_from_directory(path)
#        # Jokes extraction from HTML documents
#        jokes = []
#        for html_joke in html_jokes:
#            jokes.append(extracter.extract_joke(html_joke))
#            #jokes.append(extracter.replace(extracter.extract_text(html_joke)))
#        # Jokes tokenization
#        tokenized_jokes = []
#        for joke in jokes:
#            #without_punc = extracter.remove_punctuation(joke)
#            tokenized_jokes.append(tokenizer.tokenize(joke, remove_stopwords=False))
#        # Jokes POS Tagging
#        tagged_jokes = []
#        for sentences in tokenized_jokes:
#            tagged_sentences = tagger.tag_sentences(sentences)
#            tagged_jokes.append(tagger.map_tag(tagged_sentences))
#        # Jokes negation replacement
#        tagged_jokes_2 = []
#        for sentences in tagged_jokes:
#            tg_sentences = []
#            for sentence in sentences:
#                tg_sentences.append(replacer.replace_negations(sentence))
#            tagged_jokes_2.append(tg_sentences)
#        # Jokes lemmatization
#        lemmatized_jokes = []
#        for sentences in tagged_jokes_2:
#            lemmatized_jokes.append(lemmatizer.lemmatize_sentences(sentences))
#        # Jokes removing stopwords and punctuation
#        normalized_jokes = []
#        for lemmatized_joke in lemmatized_jokes:
#            normalized_jokes.append(extracter.remove_stopwords(lemmatized_joke))
#        # Jokes transformation from list of tokens into concatenation of tokens
#        preprocessed_jokes = []
#        for normalized_joke in normalized_jokes:
#            preprocessed_joke = ''
#            for normalized_sentence in normalized_joke:
#                preprocessed_joke = preprocessed_joke +' '+' '.join(normalized_sentence)
#            preprocessed_jokes.append(preprocessed_joke.strip()) 
#
#        return preprocessed_jokes