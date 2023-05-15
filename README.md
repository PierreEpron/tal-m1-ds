# tal-m1-ds

## Installation

## Tools

Several tools are required before you can run the notebooks. If you do not want to collect more data. Just run Spacy Parser and Stanza Parser.

### Collector

```
python -m tools.collector
```

It's an infinite loop that collects information about people in two ways:
    - Request dbpedia with sparql to collect people's information.
    - Based on dbpedia results, ask wikipedia to collect full biography.

You can stop the loop at any time by doing Ctrl+C (this may take a little time). The script is made for, it will not create a shadow file.

### Spacy Parser

```
python -m tools.spacy_parser
```

Use spacy to parse a sample abstract and page.
The default configuration is:
- SAMPLE_NAME: 'sm', the name of the sample to be parsed
- MODEL_NAME: 'en_core_web_lg', the name of the Spacy model used

The results are saved in "data/{SAMPLE_NAME}/spacy.jsonl".

The configuration can be modified by changing the constants defined at the top of the file "tools/spacy_parser.py"

### Stanza Parser

```
python -m tools.stanza_parser
```

Use stanza to parse a sample abstract and page.
The default configuration is:
- SAMPLE_NAME: 'sm', the name of the sample to be parsed
- MODEL_NAME: 'en', the name of the Spacy model used
- PROCESSORS = 'tokenize,pos,lemma,depparse', the processors used by the model. We reduced them because stanza but much more time than spacy to execute.

The results are saved in "data/{SAMPLE_NAME}/stanza.jsonl".

The configuration can be modified by changing the constants defined at the top of the file "tools/stanza_parser.py"