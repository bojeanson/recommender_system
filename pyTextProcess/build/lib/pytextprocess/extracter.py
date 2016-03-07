import string, re
from nltk.corpus import stopwords


comment_pattern = '<!--begin of joke -->(.*)<!--end of joke -->'
tag_pattern = '(<p>)|(<i>)|(</i>)|(<br>)|(</ul>)|(&nbsp;)'
punct_pattern = '[%s]' % re.escape(string.punctuation)

replacement_patterns = [(r'won\'t', 'will not'), (r'can\'t', 'cannot'), (r'i\'m', 'i am'), (r'ain\'t', 'is not'),
                        (r'(\w+)\'ll', '\g<1> will'), (r'(\w+)n\'t', '\g<1> not'), (r'(\w+)\'ve', '\g<1> have'),
                        (r'(\w+)\'s', '\g<1> is'), (r'(\w+)\'re', '\g<1> are'), (r'(\w+)\'d', '\g<1> would')]


class Extracter(object):

    def __init__(self, patterns=replacement_patterns, language='english'):
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]
        self.comment_pattern = re.compile(comment_pattern)
        self.tag_pattern = re.compile(tag_pattern, re.IGNORECASE)
        self.punct_pattern = re.compile(punct_pattern)
        self.english_stops = set(stopwords.words(language))
        
    def extract_joke(self, html_joke):
        return self.replace(self.extract_text(html_joke))

    def extract_text(self, html_text):
        return re.search(self.comment_pattern, html_text.encode('string-escape')).group(1).decode('string-escape').strip().lower()
        
    def replace(self, text):
        s = text
        for (pattern, repl) in self.patterns:
            s = re.sub(pattern, repl, s)
        without_tag = re.sub(self.tag_pattern, '', s)
        without_return = re.sub('\n', ' ', without_tag).strip()
        without_space = re.sub(' +', ' ', without_return)
        return without_space

    def remove_punctuation(self, text):
        return re.sub(self.punct_pattern, '', text)
    
    def remove_stopwords(self, tokened_sentences, punctuation_too=True):
        tk_sentences = []
        for tokened_sentence in tokened_sentences:
            if punctuation_too:
                tk_sentences.append([token for token in tokened_sentence if token not in self.english_stops
                                     and not re.match(self.punct_pattern, token)])
            else:
                tk_sentences.append([token for token in tokened_sentence if token not in self.english_stops])
        return tk_sentences