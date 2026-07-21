from difflib import SequenceMatcher
import re


def split_sentences(text):
    """
    Split text into sentences.
    """

    if not text:
        return []

    sentences = re.split(r'(?<=[.!?])\s+', text)

    return [s.strip() for s in sentences if s.strip()]


def compare_sentences(text1, text2, threshold=0.80):
    """
    Compare every sentence from text1 with every sentence in text2.
    """

    s1 = split_sentences(text1)
    s2 = split_sentences(text2)

    matches = []

    for sentence1 in s1:

        best_score = 0
        best_sentence = ""

        for sentence2 in s2:

            score = SequenceMatcher(
                None,
                sentence1.lower(),
                sentence2.lower()
            ).ratio()

            if score > best_score:

                best_score = score
                best_sentence = sentence2

        if best_score >= threshold:

            matches.append({

                "sentence": sentence1,

                "matched_sentence": best_sentence,

                "similarity": round(best_score * 100, 2)

            })

    return matches