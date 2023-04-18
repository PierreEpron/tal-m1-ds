import random
from SPARQLWrapper import SPARQLWrapper, JSON
from src.utils import read_jsonl, write_jsonl
from pathlib import Path

MANIFEST_PATH = Path('data/manifest.jsonl')
BIOS_PATH = Path('data/bios/')

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

def date_to_astral(date, astral_dates=ASTRAL_DATES):
    _, m, d = date.split('-')
    m, d = int(m), int(d)
    for k, v in astral_dates.items():
        s, e = v.values()
        if (m == s[0] and d > s[1]) or (m == e[0] and d < e[1]):
            return k

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
            dbo:deathDate ?dd;
            dbo:abstract ?abs.
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
                'deathDate': r['dd']['value'],
                'abstract': r['abs']['value']
            })

        write_jsonl(MANIFEST_PATH, manifest)
        print(f'Request succeed ! manifest have now {len(manifest)} items !')
    except Exception as e:
        print(type(e), e)