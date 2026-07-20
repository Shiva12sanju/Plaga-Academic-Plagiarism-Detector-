import re

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

def allowed_file(filename):
    """Checks if a file extension is in the allowed list."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_user_input(name, email, password):
    """
    Validates registration inputs.
    Returns (is_valid: bool, message: str)
    """
    if not name or len(name.strip()) < 2:
        return False, "Name must be at least 2 characters long."
        
    if not email:
        return False, "Email address is required."
        
    # Email regex check
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, email):
        return False, "Invalid email address format."
        
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long."
        
    return True, "Input is valid."
