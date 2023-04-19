import random
from SPARQLWrapper import SPARQLWrapper, JSON
from src.utils import read_jsonl, write_jsonl
from pathlib import Path

MANIFEST_PATH = Path('data/manifest.jsonl')
BIOS_PATH = Path('data/bios/')

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)

manifest = []  

if MANIFEST_PATH.is_file():
    manifest = read_jsonl(MANIFEST_PATH)



query_str = """
    SELECT DISTINCT ?s ?n ?bd ?bp ?dd ?abs WHERE {{
        ?s a wikidata:Q5;
            dbp:name ?n;
            dbo:birthDate ?bd;
            dbo:birthPlace ?bp;
            dbo:abstract ?abs.
        OPTIONAL {{ ?s dbo:deathDate ?dd. }}
        FILTER (lang(?abs) = "en" && lang(?n) = "en")
        BIND(RAND()*{c} AS ?sortKey)
    }} ORDER BY ?sortKey LIMIT 20
"""

while True:
    # Used for random sampling
    c = random.random()
    sparql.setQuery(query_str.format(c=c))
    try:
        ret = sparql.queryAndConvert()
        for r in ret["results"]["bindings"]:
            abs = r['abs']['value']
            
            if len(list(filter(lambda x: x['path'] == r['s']['value'], manifest))) != 0:
                continue
            
            manifest.append({
                'path': r['s']['value'],
                'birthDate': r['bd']['value'],
                'birthPlace': r['bp']['value'],
                'deathDate': r['dd']['value'] if 'dd' in r else None,
                'abstract': r['abs']['value']
            })

        write_jsonl(MANIFEST_PATH, manifest)
        print(f'Request succeed ! manifest have now {len(manifest)} items !')
    except Exception as e:
        print(type(e), e)