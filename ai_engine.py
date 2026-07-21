from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text):
    """
    Convert text into a semantic vector.
    """
    if not text:
        return None

    embedding = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embedding


def semantic_similarity(text1, text2):
    """
    Compare two documents using AI embeddings.
    """

    emb1 = create_embedding(text1)
    emb2 = create_embedding(text2)

    if emb1 is None or emb2 is None:
        return 0

    score = cosine_similarity(
        [emb1],
        [emb2]
    )[0][0]

    return float(score)