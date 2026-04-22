import re

def clean_text(text):
    if not text:
        return ""
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Remove weird characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)

    return text.strip()