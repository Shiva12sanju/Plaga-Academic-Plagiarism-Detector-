import re

STOPWORDS = {
    "the","a","an","is","are","was","were",
    "of","to","in","on","for","with","at",
    "by","and","or","that","this","it",
    "as","from","be","been","being","has",
    "have","had","do","does","did","will",
    "would","can","could","shall","should"
}


def clean_text(text):
    """
    Basic preprocessing before similarity comparison.
    """

    if not text:
        return ""

    text = text.lower()

    text = re.sub(r"\n+", " ", text)

    text = re.sub(r"[^a-z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def split_sentences(text):

    if not text:
        return []

    sentences = re.split(r"[.!?]+", text)

    return [
        s.strip()
        for s in sentences
        if len(s.strip()) > 10
    ]


def tokenize(text):

    text = clean_text(text)

    return text.split()


def remove_stopwords(words):

    return [
        w
        for w in words
        if w not in STOPWORDS
    ]


def extract_keywords(text):

    words = tokenize(text)

    words = remove_stopwords(words)

    freq = {}

    for word in words:

        freq[word] = freq.get(word, 0) + 1

    keywords = sorted(
        freq.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [k for k, v in keywords[:40]]
