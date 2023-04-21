def clean_spacy_tokens(
    txt,
    tokens,
    stop_words=[], 
    stop_pos=['ADV','PRON','CCONJ','PUNCT','PART','DET','ADP','SPACE', 'NUM'],
    min_size=2,
    lowercase=True,
    keep_lemma=True
):
    valid_tokens = []

    for tok in tokens:

        tok_txt = txt[tok['start']:tok['end']]
        tok_txt = tok_txt.lower() if lowercase else tok_txt

        if len(tok_txt) <= min_size:
           continue

        if tok['pos'] in stop_pos:
           continue

        if tok_txt in stop_words:
           continue
           
        valid_tokens.append(tok['lemma'] if keep_lemma else tok_txt)

    return " ".join(valid_tokens)   

from tqdm import tqdm
from src.utils import read_jsonl, write_jsonl
import spacy

MODEL_NAME = 'en_core_web_lg'
INPUT_PATH = 'data/manifest.jsonl'
OUTUT_PATH = f'data/{MODEL_NAME}.jsonl'

nlp = spacy.load(MODEL_NAME)
docs = read_jsonl(INPUT_PATH)

for doc in tqdm(docs):
    doc['abstract'] = nlp(doc['abstract']).to_json()

write_jsonl(OUTUT_PATH, docs)