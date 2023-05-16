from pathlib import Path
from tqdm import tqdm
from src.preprocess import get_page_path
from src.utils import read_jsonl, write_jsonl
from spacy.tokens.doc import Doc
import spacy
import pickle

# Name of sample. Used to make all the path
SAMPLE_NAME = 'sm'
# Name of spacy model to use (https://spacy.io/models)
MODEL_NAME = 'en_core_web_sm'
# Path of abstracts to par  se. Should be a jsonl.  
ABSTRACTS_PATH = Path(f'data/{SAMPLE_NAME}/abstracts.jsonl')
# Path of pages to parse. Should be a folder.
PAGES_PATH = Path(f'data/{SAMPLE_NAME}/pages/')
# Path to save parser ouput. Should be a jsonl.
OUTUT_PATH = Path(f'data/{SAMPLE_NAME}/spacy.pkl')

def remove_vectors(doc):
    '''Remove vecor and tensor for a given spacy doc'''
    return Doc(doc.vocab).from_bytes(doc.to_bytes(exclude=['vector', 'tensor'])) 

if __name__ == '__main__':
    
    # Load spacy pipeline
    nlp = spacy.load(MODEL_NAME)
    nlp.remove_pipe('ner')
    # Load abstracts
    docs = read_jsonl(ABSTRACTS_PATH)

    for doc in tqdm(docs):

        # Parse abstract. Remove vectors for lowering size of result file.
        doc['abstract'] = remove_vectors(nlp(doc['abstract']))

        # Compute page path.
        page_path = get_page_path(PAGES_PATH, doc)
        
        # Parse page if found. Remove vectors for lowering size of result file.
        if page_path.is_file():
            doc['page'] = remove_vectors(nlp(page_path.read_text(encoding='utf-8')))
        else:
            doc['page'] = ''

    OUTUT_PATH.write_bytes(pickle.dumps(docs))