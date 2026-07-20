import json
import numpy as np

# We'll use a globally cached model to avoid reloading on every request
_model = None

def get_sentence_transformer_model():
    global _model
    if _model is not None:
        return _model
    
    try:
        from sentence_transformers import SentenceTransformer
        # Use a lightweight, fast, and high-performance model
        _model = SentenceTransformer('all-MiniLM-L6-v2')
        return _model
    except Exception as e:
        print(f"Failed to load sentence-transformers: {e}. Fallback vector representation will be used.")
        return None

def generate_embedding(text):
    """
    Generates a vector embedding for the input text.
    Returns a numpy array of float32.
    """
    model = get_sentence_transformer_model()
    if model is not None:
        try:
            # Generate embeddings
            embedding = model.encode(text, convert_to_numpy=True)
            return embedding.astype(np.float32)
        except Exception as e:
            print(f"Error generating SentenceTransformer embedding: {e}")
            
    # Fallback: Simple character-n-gram frequency or hash vector representation (128 dimensions)
    # This ensures similarity scores can still be computed in an offline/lightweight mode.
    fallback_dim = 128
    vector = np.zeros(fallback_dim, dtype=np.float32)
    
    # Hash tokens to index positions to populate the vector
    words = text.lower().split()
    if not words:
        return vector
        
    for word in words:
        idx = hash(word) % fallback_dim
        vector[idx] += 1.0
        
    # L2 Normalization
    norm = np.linalg.norm(vector)
    if norm > 0:
        vector = vector / norm
        
    return vector

def serialize_embedding(embedding):
    """Converts numpy array embedding to bytes for database BLOB storage."""
    return embedding.tobytes()

def deserialize_embedding(embedding_bytes):
    """Converts bytes back to a numpy array."""
    return np.frombuffer(embedding_bytes, dtype=np.float32)
