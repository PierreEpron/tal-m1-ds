from pathlib import Path
import json

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

def read_jsonl(path, encoding='utf-8'):
    """
        Shortcut for read jsonl file

        Parameters
        ----------
        path : str or Path, path of file to read.
        encoding : str, default='utf-8', encoding format to use.
    """
    path = Path(path) if isinstance(path, str) else path
    return [json.loads(line) for line in path.read_text(encoding=encoding).strip().split('\n')]

def write_jsonl(path, data, encoding='utf-8'):
    """
        Shortcut for write jsonl file

        Parameters
        ----------
        path : str or Path, path of file to write.
        data : List, list of json data to write.
        encoding : str, default='utf-8', encoding format to use.
    """
    path = Path(path) if isinstance(path, str) else path
    path.write_text('\n'.join([json.dumps(item) for item in data]), encoding=encoding)

def date_to_astral(date, astral_dates=ASTRAL_DATES):
    _, m, d = date.split('-')
    m, d = int(m), int(d)
    for k, v in astral_dates.items():
        s, e = v.values()
        if (m == s[0] and d >= s[1]) or (m == e[0] and d <= e[1]):
            return k