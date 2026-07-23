import re
import numpy as np

from ai.text_processing import split_sentences


def stylometry_score(text):
    """
    Returns a writing-style consistency score (0-100)
    """

    if not text.strip():
        return 0

    sentences = split_sentences(text)

    if len(sentences) < 3:
        return 50

    sentence_lengths = [
        len(s.split())
        for s in sentences
    ]

    avg = np.mean(sentence_lengths)
    std = np.std(sentence_lengths)

    if avg == 0:
        return 0

    variation = std / avg

    score = max(
        0,
        min(
            100,
            (1 - variation) * 100
        )
    )

    return round(score, 2)