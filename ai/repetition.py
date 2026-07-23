import re
from collections import Counter


def repetition_score(text):

    words = re.findall(r"\w+", text.lower())

    if not words:
        return 0

    counter = Counter(words)

    repeated = sum(v for v in counter.values() if v>1)

    return round(repeated/len(words)*100,2)