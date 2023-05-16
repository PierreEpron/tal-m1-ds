from SPARQLWrapper import SPARQLWrapper, JSON
from src.utils import read_jsonl, write_jsonl
from src.preprocess import get_page_path
from pathlib import Path
import wikipedia
import random

# Query is explained in the report.
DBPEDIA_QUERIES = {
    'all':"""
        SELECT DISTINCT ?s ?n ?bd ?bp ?dd ?abs WHERE {{
            ?s a wikidata:Q5;
                dbp:name ?n;
                dbo:birthDate ?bd;
                dbo:birthPlace ?bp;
                dbo:abstract ?abs.
            OPTIONAL {{ ?s dbo:deathDate ?dd. }}
            FILTER (lang(?abs) = "en" && lang(?n) = "en")
            BIND(RAND()*{r} AS ?sortKey)
        }} ORDER BY ?sortKey LIMIT 20
    """
}

# Path of the file used to store abstracts and metadata.
# Should be a jsonl.
# If the file already exist, the script will load it and add items (if not duplicate) to it.
ABSTRACTS_PATH = Path('data/lg/abstracts.jsonl')

# Path of the folder to store pages.
PAGES_PATH = Path('data/lg/pages/')

# Key of the sparql query to use.
QUERY = 'all'

if __name__ == '__main__':

    # Load sparql wrapper
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    # Select sparql query
    query_str = DBPEDIA_QUERIES[QUERY]

    # Load abstracts file if exist.
    abstracts = []  
    if ABSTRACTS_PATH.is_file():
        abstracts = read_jsonl(ABSTRACTS_PATH)

    # Create pages dir if not exist.
    if not PAGES_PATH.is_dir():
        PAGES_PATH.mkdir()

    # Start collect loop
    while True:

        # Format sparql query (r is used for random sampling)
        r = random.random()
        sparql.setQuery(query_str.format(r=r))
        
        # Try to execute query, if succeed:
        #   store new abstracts in new_abstracts
        new_abstracts = []
        try:            
            # Execute sparl query
            res = sparql.queryAndConvert()
            
            # For each binding results
            for r in res["results"]["bindings"]:
                
                # If abstract is a duplicate continue
                if len(list(filter(lambda x: x['path'] == r['s']['value'], abstracts))) != 0:
                    continue
                
                # Store new_abstract
                new_abstracts.append({
                    'path': r['s']['value'],
                    'birthDate': r['bd']['value'],
                    'birthPlace': r['bp']['value'],
                    'deathDate': r['dd']['value'] if 'dd' in r else None,
                    'abstract': r['abs']['value']
                })

        except Exception as e:
            print('Error on sparql query', type(e), e)

        # For each new abstract
        for abstract in new_abstracts:

            # Try to request wikipedia page, if succeed:
            #   Save wikipedia page and add new abstract into abstracts.
            try:

                page_name = Path(abstract['path']).name
                page = wikipedia.page(page_name.replace('_', ' '), auto_suggest=False).content

                page_path = get_page_path(PAGES_PATH, abstract)
                page_path.write_text(page, encoding='utf-8')
                abstracts.append(abstract) 

            except Exception as e:
                print('Error on wikipedia request', type(e), e)

        write_jsonl(ABSTRACTS_PATH, abstracts)
        print(f'Request succeed ! Abstracts have now {len(abstracts)} items !')

        
    