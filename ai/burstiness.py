import numpy as np

from ai.text_processing import split_sentences


def burstiness_score(text):

    sentences = split_sentences(text)

    if len(sentences) < 2:
        return 0

    lengths = [len(x.split()) for x in sentences]

    std = np.std(lengths)

    mean = np.mean(lengths)

    if mean == 0:
        return 0

    score = std / mean

    return round(score*100,2)
