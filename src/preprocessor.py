"""
Reusable preprocessing functions.
All notebooks and the Streamlit app import from here.
"""

import re
from src.pidgin_dict import PIDGIN_DICT

# Pre-sort by token length descending so multi-word phrases
# are matched before single-word tokens
PIDGIN_PAIRS = sorted(PIDGIN_DICT.items(), key=lambda x: len(x[0]), reverse=True)

# ── Stop words ────────────────────────────────────────────────────────────────
# Standard English stop words with fraud-signal words deliberately retained
_BASE_STOPS = {
    'i','me','my','myself','we','our','ours','ourselves','yourself','yourselves',
    'he','him','his','himself','she','her','hers','herself','it','its','itself',
    'they','them','their','theirs','themselves','what','which','who','whom',
    'this','that','these','those','am','is','are','was','were','be','been',
    'being','have','has','had','having','do','does','did','doing','a','an',
    'the','and','but','if','or','because','as','until','while','of','at','by',
    'for','with','about','against','between','into','through','during','before',
    'after','above','below','to','from','up','down','in','out','on','off',
    'over','under','again','further','then','once','here','there','when',
    'where','why','how','all','both','each','few','more','most','other','some',
    'such','nor','only','own','same','so','than','too','very','s','t','d',
    'll','m','o','re','ve','y','ain','also','us','any','just'
}

# These stay in even though they appear in the base list —
# they are strong fraud-signal words in the Nigerian admission context
_KEEP = {
    'you', 'your', 'call', 'free', 'now', 'click', 'account', 'no', 'not',
    'pay', 'send', 'confirm', 'verify', 'urgent', 'win', 'won', 'link',
    'portal', 'admission', 'jamb', 'caps', 'result', 'offer', 'congratulations'
}

STOP_WORDS = _BASE_STOPS - _KEEP


# ── Pipeline functions ────────────────────────────────────────────────────────

def to_lowercase(text: str) -> str:
    """Step 1: Convert all text to lowercase."""
    return str(text).lower()


import re

def normalise_pidgin(text: str) -> str:
    """
    Step 2: Replace Nigerian Pidgin tokens with Standard English equivalents.
    Uses whole-word regex matching to prevent substring corruption.
    Multi-word phrases are matched before single tokens.
    """
    for pidgin, english in PIDGIN_PAIRS:
        # \b = word boundary — only matches whole words, not substrings
        pattern = r'\b' + re.escape(pidgin) + r'\b'
        text = re.sub(pattern, english, text)
    return text


def remove_punctuation(text: str) -> str:
    """
    Step 3: Remove punctuation and special characters.
    Digits are retained — phone numbers and account numbers
    are meaningful fraud signals.
    """
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def remove_stopwords(text: str) -> str:
    """
    Step 4: Remove stop words.
    Fraud-signal words are retained regardless of stop word list membership.
    """
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOP_WORDS and len(t) > 1]
    return " ".join(tokens)


def preprocess(text: str) -> str:
    """
    Full preprocessing pipeline — applies all four steps in sequence:
      1. Lowercase
      2. Pidgin normalisation
      3. Punctuation removal (digits retained)
      4. Stop word removal
    Returns a cleaned string ready for TF-IDF vectorisation.
    """
    text = to_lowercase(text)
    text = normalise_pidgin(text)
    text = remove_punctuation(text)
    text = remove_stopwords(text)
    return text


def preprocess_batch(series):
    """
    Apply preprocess() to a pandas Series.
    Returns a new Series of cleaned strings.
    """
    return series.apply(preprocess)