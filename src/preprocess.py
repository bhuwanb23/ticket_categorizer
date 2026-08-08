import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


def clean_text(text: str) -> str:
    """Basic deterministic text cleaning: lowercase, remove URLs/emails/HTML, punctuation, extra spaces, and stopwords.

    Returns a cleaned string suitable for vectorizers.
    """
    if text is None:
        return ''
    # normalize
    s = str(text).lower()
    # remove HTML tags
    s = re.sub(r"<[^>]+>", " ", s)
    # remove urls and emails
    s = re.sub(r"https?://\S+|www\.[^\s]+", " ", s)
    s = re.sub(r"\S+@\S+", " ", s)
    # remove non-word characters (keep spaces)
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    # collapse whitespace
    s = re.sub(r"\s+", " ", s).strip()
    # remove stopwords naively
    tokens = [t for t in s.split() if t not in ENGLISH_STOP_WORDS]
    return " ".join(tokens)


if __name__ == "__main__":
    examples = [
        "Invoice not received for order #12345",
        "Our API returns 500 error when calling /v1/login",
    ]
    for e in examples:
        print(clean_text(e))
