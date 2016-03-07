from nltk.stem import WordNetLemmatizer


class Lemmatizer(object):
    
    def __init__(self, language='english'):
        self.lemmatizer = WordNetLemmatizer()
        
    def lemmatize_sentences(self, sentences):
        lemmatized_sentences = []
        for sentence in sentences:
            lemmatized_sentence = []
            for tagged_word in sentence:
                lemmatized_sentence.append(self.lemmatizer.lemmatize(tagged_word[0], pos=tagged_word[1]))
            lemmatized_sentences.append(lemmatized_sentence)
        return lemmatized_sentences