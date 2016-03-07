import pickle
from nltk.tag.sequential import ClassifierBasedPOSTagger
from tag_util import unigram_feature_detector
from nltk.tag import DefaultTagger
from nltk.corpus import treebank, wordnet


class Tagger(object):

    def __init__(self, name='backup/tagger.pickle'):
        self.__train_sents = treebank.tagged_sents()[:3000]
        self.__test_sents = treebank.tagged_sents()[3000:]
        self.__default = DefaultTagger('NN')
        self.tagger = self.load_tagger(name)
        
    def tag_sentences(self, sentences):
        return self.tagger.tag_sents(sentences)
    
    def map_tag(self, tagged_sentences):
        tg_sentences = []
        for tagged_sentence in tagged_sentences:
            tg_sentence = []
            for tagged_word in tagged_sentence:
                tg_sentence.append((tagged_word[0], self.wordnet_pos_code(str(tagged_word[1]))))
            tg_sentences.append(tg_sentence)
        return tg_sentences

    def load_tagger(self, name='backup/tagger.pickle'):
        try:
            with open(name, "rb") as f:
                tagger = pickle.load(f)
            f.close()
            return tagger
        except IOError as e:
            print ("I/O error: {0}".format(e))
            pass
        tagger = ClassifierBasedPOSTagger(train=self.__train_sents, backoff=self.__default, cutoff_prob=0.3)
        print 'Tagger accuracy : {}'.format(tagger.evaluate(self.__test_sents))
        with open(name, 'wb') as f:
            pickle.dump(tagger, f)
        f.close()
        return tagger

    def wordnet_pos_code(self, tag):
        if tag.startswith('NN'):
            return wordnet.NOUN
        elif tag.startswith('VB'):
            return wordnet.VERB
        elif tag.startswith('JJ'):
            return wordnet.ADJ
        elif tag.startswith('RB'):
            return wordnet.ADV
        else:
            return wordnet.NOUN
