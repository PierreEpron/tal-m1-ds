from functools import reduce
from pathlib import Path
import numpy as np

# List and mapping of upos tags
POS_TAGS = ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X']
TAG_TO_ID = {t:i for i, t in enumerate(POS_TAGS)}
ID_TO_TAG = {i:t for t, i in TAG_TO_ID.items()}

def create_textset(src, n = None, encoding='utf-8'):
    """
        Recover text from n files in an src folder.

        Parameters
        ----------
        src : str or Path, path of the folder containing the files where text will be extract.
        n : int or None, default=None, number of documents to return. If None return all documents from src.
        encoding : str, default='utf-8', encoding format to use when reading text.

        Returns
        ---------
        output : List, the list of retrieved texts.
    """
    # Convert src path if needed.
    src = Path(src) if isinstance(src, str) else src
    # Compute file paths.
    paths = list(src.glob('*.txt'))
    # If n is None set n as len of paths.
    n = len(paths) if n == None else n
    # Return list containing text from each file.
    return [p.read_text(encoding=encoding) for p in paths[:n]]


def compute_sent_len(sp, st):
    """
        Compute and output the respective number of sentences produced by spacy (sp) and stanza (st) document.

        Parameters
        ----------
        sp : spacy.Doc, spacy document to use.
        st : stanza.Document, stanza document to use.

        Returns
        ---------
        output : Tuple[int], (len of sentences produced by spacy, len of sentences produced by stanza).
    """
    return len(list(sp.sents)), len(st.sentences)


def compute_shared_sentences(sp, st):
    """
        Return the set of shared sentences recognized by spacy (sp) and stanza (st).

        Parameters
        ----------
        sp : spacy.Doc, spacy document to use.
        st : stanza.Document, stanza document to use.

        Returns
        ---------
        output : List[str], shared sentences recognize by both library.
    """

    return list(set([sent.text for sent in sp.sents]) & set([sent.text for sent in st.sentences]))


def get_spacy_tokens(docs):
    """
        Return a generator to iterate over all tokens inside the given spacy documents.

        Parameters
        ----------
        docs : List[spacy.Doc], documents to iterate over.

        Returns
        ---------
        output : generator, A generator over all tokens of the given documents.
    """

    for doc in docs:
        for token in doc:
            yield token

def get_stanza_tokens(docs):
    """
        Return a generator to iterate over all tokens inside the given stanza documents.

        Parameters
        ----------
        docs : List[stanza.Document], documents to iterate over.

        Returns
        ---------
        output : generator, A generator over all tokens of the given documents.
    """
        
    for doc in docs:
        for sentence in doc.sentences:
            for token in sentence.tokens:
                yield token


def compute_spacy_vocabulary(docs):
    """
        Return the vocabulary of the given spacy documents.

        Parameters
        ----------
        docs : List[stanza.Document], documents to used to compute vocabulary.

        Returns
        ---------
        output : Set[str], The vocabulary of the given documents.
    """ 
    return set([t.text for t in get_spacy_tokens(docs)])


def compute_stanza_vocabulary(docs):
    """
        Return the vocabulary of the given stanza documents.

        Parameters
        ----------
        docs : List[spacy.Doc], documents to used to compute vocabulary.

        Returns
        ---------
        output : Set[str], The vocabulary of the given documents.
    """ 
    return set(t.text for t in get_stanza_tokens(docs))


def compute_token_by_doc(sp, st):
    """
        Return the tokens that are identified by spacy (sp) and stanza (st) for the given documents without sentence segmentation.

        Parameters
        ----------
        sp : Iterable[spacy.Doc], spacy documents to use.
        st : Iterable[stanza.Document], stanza documents to use.

        Returns
        ---------
        output : List[Tuple[spacy.Token, stanza.Tokan]], List of tuple containing tokens identified by spacy and stanza
    """
    tokens = []

    # Iterate over documents
    for sp_doc, st_doc in zip(sp, st):

        # Compute spacy and stanza tokens.
        sp_tokens = list(get_spacy_tokens([sp_doc]))
        st_tokens = list(get_stanza_tokens([st_doc]))
 
        # Compute maximum len between spacy and stanza tokens.
        min_len = min(len(sp), len(st))

        # Iterate over tokens until minimum len.
        # Keep only equivalent tokens.
        for sp_token, st_token in zip(sp_tokens[:min_len], st_tokens[:min_len]):
            if sp_token.text == st_token.text:
                tokens.append((sp_token, st_token))
    
    return tokens

def compute_token_by_sentence(sp, st):
    """
        Return the tokens that are identified by spacy (sp) and stanza (st) for the given documents with sentence segmentation.

        Parameters
        ----------
        sp : Iterable[spacy.Doc], spacy sentences to use.
        st : Iterable[stanza.Document], stanza sentences to use.

        Returns
        ---------
        output : List[Tuple[spacy.Token, stanza.Tokan]], List of tuple containing tokens identified by spacy and stanza 
    """

    tokens = []
    
    # Iterate over documents
    for sp_doc, st_doc in zip(sp, st):

        # Compute minimum len between spacy sentences and stanza sentences.
        min_len = min(len(list(sp_doc.sents)), len(st_doc.sentences))

        # Iterate over sentences until minimum len.
        for sp_sent, st_sent in zip(list(sp_doc.sents)[:min_len], st_doc.sentences[:min_len]):

            # Compute minimum len between spacy and stanza sentence tokens.
            min_len = min(len(sp_sent), len(st_sent.tokens))

            # Iterate over tokens until minimum len.
            # Keep only equivalent tokens.
            for sp_token, st_token in zip(sp_sent[:min_len], st_sent.tokens[:min_len]):
                if sp_token.text == st_token.text:
                    tokens.append((sp_token, st_token))
        
    return tokens


def format_valid_pos(valid_pos, round_digits=2, scale_factor=100):
    """
        Used to format spacy and stanza valid pos from compute_valid_pos.
        First, valid_pos is normalize as : (valid_pos / valid_pos.sum(1)) * scale_factor
        Second, valid_pos is round to have round_digits digits.
        Finaly, valid_pos is transform and return as dict like {'ADJ':{'ADJ':x, 'ADP':y, ...}, ...}

        Parameters
        ----------
        valid_pos : np.array, valid_pos to format.
        round_digits : int, how many digits to keep when round results.
        scale_factor : int, default = 100, value used to scale results. 
        If 1 results will be unchanged. If 100 results will be in %.

        Returns
        ---------
        output : Dict[Dict[str, float]], formated valid pos. 
    """

    # Normalize and round valid_pos
    valid_pos = ((valid_pos / valid_pos.sum(1)[..., np.newaxis]) * scale_factor).round(round_digits)

    # Transform valid_pos in dict and return it.
    return {ID_TO_TAG[i]: {ID_TO_TAG[j]: valid_pos[i, j] for j in range(len(ID_TO_TAG))} for i in range(len(ID_TO_TAG))}


def compute_valid_pos(tokens, round_digits=2, scale_factor=100):
    """
        Compute valid pos from a given list of spacy and stanza tokens.
        Return valid pos count, valid pos ratio and a pos frequency dict for spacy and stanza.
        The valid pos ratio is rounded and scaled as: round(valid_pos_ration * scale_factor, round_digits) 

        Parameters
        ----------
        tokens : List[Tuple[spacy.Token, stanza.Tokan]], List of tuple containing tokens identified by spacy and stanza.
        round_digits : int, how many digits to keep when round results.
        scale_factor : int, default = 100, value used to scale results. 
        If 1 results will be unchanged. If 100 results will be in %.

        Returns
        ---------
        valid_pos_count : float, rount of valid pos from both libraries.
        valid_pos_ratio : float, ratio of valid pos from both libraries.
        spacy_pos : Dict[Dict[str, float]], formated spacy valid pos.
        stanza_pos : Dict[Dict[str, float]], formated stanza valid pos.
    """

    all_pos = []

    pos_tags_len = len(POS_TAGS)
    spacy_pos = np.zeros((pos_tags_len, pos_tags_len))
    stanza_pos = np.zeros((pos_tags_len, pos_tags_len))

    for sp_token, st_token in tokens:
        sp_pos, st_pos = sp_token.pos_, st_token.words[0].pos
        if sp_pos == st_pos:
            all_pos.append(sp_pos)
        spacy_pos[TAG_TO_ID[sp_pos], TAG_TO_ID[st_pos]] += 1
        stanza_pos[TAG_TO_ID[st_pos], TAG_TO_ID[sp_pos]] += 1

    valid_pos_count = spacy_pos.trace()
    valid_pos_ratio = round((valid_pos_count / spacy_pos.sum()) * scale_factor, round_digits)

    return (
        valid_pos_count, valid_pos_ratio, 
        format_valid_pos(spacy_pos, round_digits, scale_factor), 
        format_valid_pos(stanza_pos, round_digits, scale_factor)
    )
