from pathlib import Path
import pickle
from tqdm import tqdm
from src.preprocess import get_page_path
from src.utils import read_jsonl, write_jsonl
import stanza

# Name of sample. Used to make all the path
SAMPLE_NAME = 'sm'
# Name of stanza model to use (https://stanfordnlp.github.io/stanza/available_models.html)
MODEL_NAME = 'en' 
# As stanza model is really slow we reduce the number of component.
PROCESSORS = 'tokenize,pos,lemma,depparse'
# Path of abstracts to parse. Should be a jsonl.  
ABSTRACTS_PATH = Path(f'data/{SAMPLE_NAME}/abstracts.jsonl')
# Path of pages to parse. Should be a folder.
PAGES_PATH = Path(f'data/{SAMPLE_NAME}/pages/')
# Path to save parser ouput. Should be a jsonl.
OUTUT_PATH = Path(f'data/{SAMPLE_NAME}/stanza.pkl')

if __name__ == '__main__':
    
    # Load spacy pipeline
    nlp = stanza.Pipeline(MODEL_NAME, processors=PROCESSORS)

    # Load abstracts
    docs = read_jsonl(ABSTRACTS_PATH)

    for doc in tqdm(docs):

        # Parse abstract        
        doc['abstract'] = nlp(doc['abstract'])

        # Compute page path.
        page_path = get_page_path(PAGES_PATH, doc)

        # Parse page if found.
        if page_path.is_file():
            doc['page'] = nlp(page_path.read_text(encoding='utf-8'))

    OUTUT_PATH.write_bytes(pickle.dumps(docs))