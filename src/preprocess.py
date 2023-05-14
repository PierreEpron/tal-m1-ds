from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

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

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

def date_to_astral(date, astral_dates=ASTRAL_DATES):
    _, m, d = date.split('-')
    m, d = int(m), int(d)
    for k, v in astral_dates.items():
        s, e = v.values()
        if (m == s[0] and d >= s[1]) or (m == e[0] and d <= e[1]):
            return k

def clean_spacy_tokens(
    stop_words=stopwords.words('english'), 
    stop_pos=['ADV','PRON','CCONJ','PUNCT','PART','DET','ADP','SPACE','NUM','SYM','X'],
    min_size=2,
    lowercase=True,
    is_alpha=True,
    keep_lemma=True,
    remove_month=True # Only work if lowercase == True:
    ):

    if remove_month:
        stop_words += MONTHS

    def wrapped_clean_spacy_tokens(
        doc_json
    ):
        valid_tokens = []

        for tok in doc_json['tokens']:

            tok_txt = doc_json['text'][tok['start']:tok['end']]
            tok_txt = tok_txt.lower() if lowercase else tok_txt

            if is_alpha and not tok_txt.isalpha():
                continue

            if len(tok_txt) <= min_size:
                continue

            if tok['pos'] in stop_pos:
                continue

            if tok_txt in stop_words:
                continue

            valid_tokens.append(tok['lemma'] if keep_lemma else tok_txt)

        return valid_tokens
    
    return wrapped_clean_spacy_tokens


# if __name__ == '__main__':
#     from tqdm import tqdm
#     from src.utils import read_jsonl, write_jsonl
#     import spacy

#     MODEL_NAME = 'en_core_web_lg'
#     INPUT_PATH = 'data/manifest.jsonl'
#     OUTUT_PATH = f'data/{MODEL_NAME}.jsonl'

#     nlp = spacy.load(MODEL_NAME)
#     docs = read_jsonl(INPUT_PATH)

#     for doc in tqdm(docs):
#         doc['abstract'] = nlp(doc['abstract']).to_json()

#     write_jsonl(OUTUT_PATH, docs)