import sys
import os

# Ensure project root is on sys.path when running this demo from the project root or from inside the notebooks/ folder.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.predict import predict_ticket


SAMPLES = [
    ("Invoice missing", "I did not receive my invoice for order 8765, please send asap."),
    ("App crashes on save", "When I try to save a document the app crashes with error 500."),
    ("Leave balance query", "How many paid leaves do I have left this year?"),
    ("Refund status", "I requested a refund last week and haven't received it."),
    ("Password reset", "I cannot login and forgot my password, please help."),
]


def run_demo():
    for subj, body in SAMPLES:
        out = predict_ticket(subj, body)
        print(f"SUBJECT: {subj}")
        print(
            f" -> label={out['label']}, confidence={out['confidence']:.2f}, "
            f"review={out['needs_human_review']}, priority={out['priority']}"
        )
        print('-' * 60)


if __name__ == '__main__':
    run_demo()
