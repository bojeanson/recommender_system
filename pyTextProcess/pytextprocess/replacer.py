from nltk.corpus import wordnet


class AntonymReplacer(object):
    def replace(self, word, pos=None):
        """ Returns the antonym of a word, but only if there is no ambiguity.
        >>> replacer = AntonymReplacer()
        >>> replacer.replace('good')
        >>> replacer.replace('uglify')
        'beautify'
        >>> replacer.replace('beautify')
        'uglify'
        """
        antonyms = set()
        
        for syn in wordnet.synsets(word, pos=pos):
            for lemma in syn.lemmas():
                for antonym in lemma.antonyms():
                    antonyms.add(antonym.name())

        if len(antonyms) == 1:
            return antonyms.pop()
        else:
            return None

    def replace_negations(self, sent):
        """ Try to replace negations with antonyms in the tokenized sentence.
        >>> replacer = AntonymReplacer()
        >>> replacer.replace_negations(['do', 'not', 'uglify', 'our', 'code'])
        ['do', 'beautify', 'our', 'code']
        >>> replacer.replace_negations(['good', 'is', 'not', 'evil'])
        ['good', 'is', 'not', 'evil']
        """
        i, l = 0, len(sent)
        words = []
    
        while i < l:
            word = sent[i]
        
            if word == 'not' and i+1 < l:
                ant = self.replace(sent[i+1])
            
                if ant:
                    words.append(ant)
                    i += 2
                    continue
        
            words.append(word)
            i += 1
    
        return words