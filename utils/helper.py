import re

def format_percentage(value):
    """Formats a float/integer as a percentage string."""
    try:
        return f"{float(value):.2f}%"
    except (ValueError, TypeError):
        return "0.00%"

def clean_text_simple(text):
    """Performs a simple cleanup of whitespace in text."""
    if not text:
        return ""
    # Replace multiple newlines/whitespaces with a single space
    return re.sub(r'\s+', ' ', text).strip()

def split_into_paragraphs(text):
    """Splits a document's text into logical paragraphs."""
    if not text:
        return []
    # Split by double newline or carriage returns
    paras = re.split(r'\n\s*\n', text)
    # Filter empty or very short paragraphs
    return [p.strip() for p in paras if len(p.strip()) > 10]

def highlight_text(original_text, matches):
    """
    Highlights words or sentences in the original_text that match elements in matches.
    matches is a list of strings/phrases.
    Returns HTML formatted text.
    """
    if not original_text or not matches:
        return original_text or ""
        
    highlighted = original_text
    # Order matches by length descending to avoid highlighting substrings first
    sorted_matches = sorted(matches, key=len, reverse=True)
    
    for match in sorted_matches:
        if not match.strip():
            continue
        # Escaping regex characters
        escaped_match = re.escape(match.strip())
        # Use regex to replace case-insensitively with a span class for marking
        pattern = re.compile(escaped_match, re.IGNORECASE)
        highlighted = pattern.sub(r'<mark class="plagiarized-highlight">\g<0></mark>', highlighted)
        
    return highlighted
