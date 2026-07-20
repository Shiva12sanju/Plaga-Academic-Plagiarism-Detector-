import re

# Standard English stopwords fallback
ENGLISH_STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
    'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
    'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
    'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
    "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
    'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
}

def clean_text(text):
    """
    Cleans raw text by removing punctuation, special characters, and converting to lowercase.
    """
    if not text:
        return ""
    # Lowercase
    text = text.lower()
    # Remove special characters/punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Remove multiple spaces/newlines
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_text(text):
    """
    Tokenizes, removes stopwords, and performs basic word normalization (lemmatization).
    Falls back to custom python parsing if spaCy/NLTK are not configured.
    """
    cleaned = clean_text(text)
    
    # Try spaCy
    try:
        import spacy
        # Load small English model (disable parser and ner for speed)
        nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
        doc = nlp(cleaned)
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_space]
        if tokens:
            return tokens
    except Exception:
        pass

    # Try NLTK
    try:
        import nltk
        from nltk.tokenize import word_tokenize
        from nltk.corpus import stopwords
        from nltk.stem import WordNetLemmatizer
        
        # Ensure packages are downloaded (in real apps, these are preloaded)
        # nltk.download('punkt', quiet=True)
        # nltk.download('stopwords', quiet=True)
        # nltk.download('wordnet', quiet=True)
        
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))
        
        tokens = word_tokenize(cleaned)
        filtered = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words]
        if filtered:
            return filtered
    except Exception:
        pass

    # Fallback: Simple string tokenization and stopword removal
    tokens = cleaned.split()
    filtered = [w for w in tokens if w not in ENGLISH_STOPWORDS]
    return filtered
