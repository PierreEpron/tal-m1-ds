import functools
from pathlib import Path
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

# Mapping for atral date parsing
ASTRAL_DATES = {
    'Aries' : {'start':(3,21), 'end':(4,20)},
    'Taurus' : {'start':(4,21), 'end':(5,20)},
    'Gemini' : {'start':(5,21), 'end':(6,21)},
    'Cancer' : {'start':(6,22), 'end':(7,22)},
    'Leo' : {'start':(7,23), 'end':(8,22)},
    'Virgo' : {'start':(8,23), 'end':(9,22)},
    'Libra' : {'start':(9,23), 'end':(10,22)},
    'Scorpio' : {'start':(10,23), 'end':(11,22)},
    'Sagittarius' : {'start':(11,23), 'end':(12,21)},
    'Capricorn' : {'start':(12,22), 'end':(1,20)},
    'Aquarius' : {'start':(1,21), 'end':(2,19)},
    'Pisces' : {'start':(2,20), 'end':(3,20)},
}

# List of the months used in token cleaning
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']


def date_to_astral(date, astral_dates=ASTRAL_DATES):
    """
        Convert a yyyy-mm-dd date into astral sign.

        Parameters
        ----------
        date : str, valid_pos to format.
        astral_dates : Dict, mapping to use for conversion.

        Returns
        ---------
        astral_sign : str, the astral sign corresponding to the date. 
    """
    _, m, d = date.split('-')
    m, d = int(m), int(d)
    for k, v in astral_dates.items():
        s, e = v.values()
        if (m == s[0] and d >= s[1]) or (m == e[0] and d <= e[1]):
            return k


def get_page_path(root, doc):
    ''' Helper to format page path to requested name: "path/PersonName_AstralSign.txt" '''
    return (root / f"{Path(doc['path']).name.replace('_', '')}_{date_to_astral(doc['birthDate'])}.txt")


def get_spacy_tokens(doc):
    ''' Helper to iterate over spacy token text, pos and lemma for the given doc'''
    return map(
        lambda t: (t.text, t.pos_, t.lemma_), 
        doc
    )


def get_stanza_tokens(doc):
    ''' Helper to iterate over stanza token text, pos and lemma for the given doc'''
    return map(
        lambda t:(t.text, t.words[0].upos, t.words[0].lemma) , 
        functools.reduce(lambda a, b: a + b.sentences, doc, [])
    )


PARSERS = {
    'spacy':get_spacy_tokens, 
    'stanza':get_stanza_tokens
}


def clean_tokens(
    parser='spacy',
    stop_words=stopwords.words('english'), 
    stop_pos=['ADV','PRON','CCONJ','PUNCT','PART','DET','ADP','SPACE','NUM','SYM','X'],
    min_size=2,
    lowercase=True,
    is_alpha=True,
    keep_lemma=True,
    remove_month=True
    ):
    """
        Wrapper to create a clean_tokens function that take a spacy or a stanza doc and clean it tokens.
        We use a wrapper here to avoid stop_word merging multiple times.

        Parameters
        ----------
        parser : str, default='spacy', from which parser is the doc (spacy, stanza).
        stop_words : Iterable[str], default=nlt.stopwords.words('english'), words to skip during cleaning.
        stop_pos : Iterable[str], default=['ADV','PRON','CCONJ','PUNCT','PART','DET','ADP','SPACE','NUM','SYM','X'], POS to skip during cleaning.
        min_size : int, default=2, minimum size of a token to be kept during cleaning.
        lowercase : bool, default=True, if True the function lower the output tokens.
        is_alpha : bool, default=True, if True non alpha token will be skip during cleaning.
        keep_lemma : bool, default=True, if True the function return lemma of output tokens.
        remove_month : bool, default=True, if True month will be added to stopwords.
        Returns
        ---------
        astral_sign : List[str], List of cleaned tokens. 
    """

    if remove_month:
        stop_words += MONTHS

    def wrapped_clean_tokens(
        doc
    ):
        valid_tokens = []

        for text, pos, lemma in PARSERS[parser](doc):

            text = text.lower() if lowercase else text

            if is_alpha and not text.isalpha():
                continue

            if len(text) <= min_size:
                continue

            if pos in stop_pos:
                continue

            if text.lower() in stop_words:
                continue    

            valid_tokens.append(lemma if keep_lemma else text)

        return valid_tokens
    
    return wrapped_clean_tokens