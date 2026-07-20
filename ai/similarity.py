import numpy as np

def cosine_similarity(vec1, vec2):
    """
    Computes the cosine similarity between two vectors.
    Vectors must be numpy arrays.
    Returns a float between -1.0 and 1.0 (typically 0.0 to 1.0 for positive space).
    """
    if vec1 is None or vec2 is None:
        return 0.0
        
    # Ensure they are numpy arrays
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    # Calculate dot product
    dot_product = np.dot(vec1, vec2)
    
    # Calculate magnitudes
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    
    if norm_vec1 == 0.0 or norm_vec2 == 0.0:
        return 0.0
        
    similarity = dot_product / (norm_vec1 * norm_vec2)
    
    # Clamp value between -1.0 and 1.0 to avoid floating point anomalies
    return float(np.clip(similarity, -1.0, 1.0))

def jaccard_similarity(tokens1, tokens2):
    """
    Computes Jaccard similarity between two lists of preprocessed tokens.
    Returns a float between 0.0 and 1.0.
    """
    if not tokens1 or not tokens2:
        return 0.0
        
    set1 = set(tokens1)
    set2 = set(tokens2)
    
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    
    if not union:
        return 0.0
        
    return len(intersection) / len(union)
