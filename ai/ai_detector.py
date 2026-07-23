from transformers import pipeline

# Load model once
detector = pipeline(
    "text-classification",
    model="openai-community/roberta-base-openai-detector",
    truncation=True
)

def detect_ai(text):
    """
    Returns AI probability from 0 to 100.
    """

    if not text or len(text.strip()) < 30:
        return 0

    try:
        result = detector(text[:512])[0]

        print("AI Detection:", result)

        label = result["label"]
        score = result["score"]

        if label == "LABEL_1":
            return round(score * 100, 2)
        else:
            return round((1 - score) * 100, 2)

    except Exception as e:
        print("AI Detection Error:", e)
        return 0