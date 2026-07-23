import textstat


def readability_score(text):
    """
    Converts Flesch Reading Ease to 0-100.
    """

    if not text.strip():
        return 0

    try:

        score = textstat.flesch_reading_ease(text)

        score = max(
            0,
            min(
                100,
                score
            )
        )

        return round(score, 2)

    except:

        return 50