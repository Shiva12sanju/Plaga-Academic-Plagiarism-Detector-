from ai.ai_detector import detect_ai

from ai.perplexity import calculate_perplexity
from ai.burstiness import burstiness_score
from ai.stylometry import stylometry_score
from ai.vocabulary import vocabulary_score
from ai.repetition import repetition_score
from ai.readability import readability_score


def hybrid_ai_analysis(text):

    if not text.strip():

        return {

            "overall_score": 0,

            "confidence": "Low"

        }

    roberta = detect_ai(text)

    perplexity = calculate_perplexity(text)

    burstiness = burstiness_score(text)

    vocabulary = vocabulary_score(text)

    repetition = repetition_score(text)

    readability = readability_score(text)

    stylometry = stylometry_score(text)

    # Convert perplexity into AI score

    if perplexity < 20:
        perplexity_score = 95

    elif perplexity < 40:
        perplexity_score = 80

    elif perplexity < 60:
        perplexity_score = 65

    elif perplexity < 100:
        perplexity_score = 45

    else:
        perplexity_score = 20

    overall = (

        roberta * 0.35 +

        perplexity_score * 0.20 +

        stylometry * 0.10 +

        vocabulary * 0.10 +

        repetition * 0.10 +

        readability * 0.05 +

        burstiness * 0.10

    )

    overall = round(overall, 2)

    if overall >= 80:

        confidence = "High"

    elif overall >= 60:

        confidence = "Medium"

    else:

        confidence = "Low"

    return {

        "overall_score": overall,

        "confidence": confidence,

        "roberta": roberta,

        "perplexity": perplexity,

        "burstiness": burstiness,

        "stylometry": stylometry,

        "vocabulary": vocabulary,

        "repetition": repetition,

        "readability": readability

    }
