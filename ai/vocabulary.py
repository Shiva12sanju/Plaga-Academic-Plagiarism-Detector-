import re


def vocabulary_score(text):

    words = re.findall(r"\w+", text.lower())

    if not words:
        return 0

    unique = len(set(words))

    score = unique / len(words)

    return round(score*100,2)