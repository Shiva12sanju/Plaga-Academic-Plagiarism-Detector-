import re
import textstat

from collections import Counter


def readability_score(text):
    if not text:
        return 0

    return round(textstat.flesch_reading_ease(text), 2)


def word_count(text):
    return len(text.split())


def sentence_count(text):
    return max(len(re.split(r"[.!?]+", text)), 1)


def vocabulary_richness(text):

    words = re.findall(r"\b\w+\b", text.lower())

    if not words:
        return 0

    unique = len(set(words))

    return round(unique / len(words), 2)


def average_sentence_length(text):

    words = word_count(text)

    sentences = sentence_count(text)

    return round(words / sentences, 2)


def ai_probability(text):
    """
    Simple heuristic AI detector.
    Returns probability (0–100).
    """

    score = 0

    avg_sentence = average_sentence_length(text)

    vocab = vocabulary_richness(text)

    readability = readability_score(text)

    if avg_sentence > 25:
        score += 25

    if vocab > 0.55:
        score += 25

    if readability > 70:
        score += 20

    repeated = Counter(text.lower().split())

    common = repeated.most_common(5)

    repetition = sum(c for _, c in common)

    if repetition < 15:
        score += 30

    return min(score, 100)


def writing_quality(text):

    return {

        "word_count": word_count(text),

        "sentence_count": sentence_count(text),

        "average_sentence_length": average_sentence_length(text),

        "readability": readability_score(text),

        "vocabulary": vocabulary_richness(text),

        "ai_probability": ai_probability(text)

    }