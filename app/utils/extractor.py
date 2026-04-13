import re

def extract_stipend(title):
    # Match patterns like "$50k - $70k", "$50/hr", "50 USD", "₹50,000", "$45 / hr", "$90k-$130k"
    pattern = r'(\$|₹|€)?\s?\d+(?:,\d+)?(?:\.\d+)?\s?(?:[kK])?(?:\s?-\s?(?:\$|₹|€)?\s?\d+(?:,\d+)?(?:\.\d+)?\s?(?:[kK])?)?(?:\s?(?:USD|EUR|GBP))?(?:\s?\/?\s?(?:hr|hour|yr|year|month|mo))?'
    
    match = re.search(pattern, title, re.IGNORECASE)
    
    if match:
        extracted = match.group(0).strip()
        # Further refine if it's just a lonely number, maybe we only want ones with currency/rate signs
        if any(c in extracted.lower() for c in ['$', '₹', '€', 'usd', 'eur', 'gbp', 'hr', 'year', 'month', 'k']):
            return extracted
    return None

def clean_description(text: str) -> str:
    if not text:
        return ""
    
    # 1. Strip Markdown links [text](url) -> text
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    
    # 2. Strip standard Markdown symbols (*, #, _, >)
    text = re.sub(r'[*#_>]', '', text)
    
    # 3. Clean up the "scattered" whitespace
    # Replace multiple newlines with a double newline for paragraph separation
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    
    # 4. Strip excessive "Reddit meta" (footers like "not a bot", "thanks", etc.)
    meta_patterns = [
        r'i am a bot.*', r'thanks for reading.*', r'send me a dm.*', 
        r'click here to apply.*', r'view my portfolio.*'
    ]
    for pattern in meta_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    return text.strip()

def is_specialized_role(title: str) -> bool:
    """Helper to catch high-intent roles for accuracy."""
    keywords = [
        # Creative
        "motion graphics", "vfx", "video editor", "animator", "after effects", 
        "cinema 4d", "blender", "colorist",
        # Tech & Data
        "data scientist", "machine learning", "ai engineer", "data analyst",
        "computer vision", "nlp", "deep learning", "researcher"
    ]
    return any(kw in title.lower() for kw in keywords)