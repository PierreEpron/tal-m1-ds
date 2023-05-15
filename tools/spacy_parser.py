from pathlib import Path
from tqdm import tqdm
from src.preprocess import get_page_path
from src.utils import read_jsonl, write_jsonl
import spacy


# Name of sample. Used to make all the path
SAMPLE_NAME = 'lg'
# Name of spacy model to use (https://spacy.io/models)
MODEL_NAME = 'en_core_web_lg'
# Path of abstracts to par  se. Should be a jsonl.  
ABSTRACTS_PATH = Path(f'data/{SAMPLE_NAME}/abstracts.jsonl')
# Path of pages to parse. Should be a folder.
PAGES_PATH = Path(f'data/{SAMPLE_NAME}/pages/')
# Path to save parser ouput. Should be a jsonl.
OUTUT_PATH = Path(f'data/{SAMPLE_NAME}/spacy.jsonl')

if __name__ == '__main__':
    
    # Load spacy pipeline
    nlp = spacy.load(MODEL_NAME)

    # Load abstracts
    docs = read_jsonl(ABSTRACTS_PATH)

    for doc in tqdm(docs):

        # Parse abstract        
        doc['abstract'] = nlp(doc['abstract']).to_json()

        # Compute page path.
        page_path = get_page_path(PAGES_PATH, doc)
        
        # Parse page if found.
        if page_path.is_file():
            doc['page'] = nlp(page_path.read_text(encoding='utf-8')).to_json()
        else:
            doc['page'] = ''

    # Write output
    write_jsonl(OUTUT_PATH, docs)