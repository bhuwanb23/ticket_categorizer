import os
import sys
from typing import Dict

# Ensure project root is on sys.path when running this module as a script.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import joblib
from src.preprocess import clean_text

_vect = None
_clf = None

PRIORITY_KEYWORDS = (
    'urgent',
    'down',
    'asap',
    'immediately',
    'not working',
    'critical',
    'outage',
)


def _load():
    global _vect, _clf
    if _vect is None or _clf is None:
        models_dir = os.path.join(ROOT, 'models')
        vectorizer_path = os.path.join(models_dir, 'vectorizer.joblib')
        model_path = os.path.join(models_dir, 'model.joblib')
        if not os.path.exists(vectorizer_path) or not os.path.exists(model_path):
            raise FileNotFoundError(
                "Trained model not found. Run `python src/train.py` from the project root first."
            )
        _vect = joblib.load(vectorizer_path)
        _clf = joblib.load(model_path)
    return _vect, _clf


def predict_ticket(subject: str, body: str, threshold: float = 0.6) -> Dict:
    """Return prediction dictionary: label, confidence, needs_human_review, priority."""
    vect, clf = _load()
    raw = f"{subject or ''} {body or ''}"
    text = clean_text(raw)
    X = vect.transform([text])
    probs = clf.predict_proba(X)[0]
    idx = int(probs.argmax())
    label = clf.classes_[idx]
    confidence = float(probs[idx])
    needs_human_review = confidence < threshold
    lowtext = raw.lower()
    priority = 'urgent' if any(k in lowtext for k in PRIORITY_KEYWORDS) else 'normal'
    final_label = 'NEEDS_HUMAN_REVIEW' if needs_human_review else str(label)
    return {
        'label': str(label),
        'routed_to': final_label,
        'confidence': confidence,
        'needs_human_review': needs_human_review,
        'priority': priority,
    }


def _print_result(out: Dict) -> None:
    review = 'YES -> manual queue' if out['needs_human_review'] else 'no (auto-assign)'
    print(
        f"  category : {out['label']}\n"
        f"  confidence: {out['confidence']:.1%}\n"
        f"  human review: {review}\n"
        f"  priority : {out['priority']}"
    )


def interactive_cli():
    print("Ticket Categorizer — type subject and body (empty subject to quit)")
    while True:
        try:
            subject = input("\nSubject: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break
        if not subject:
            print("Bye.")
            break
        body = input("Body   : ").strip()
        out = predict_ticket(subject, body)
        _print_result(out)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in {'-i', '--interactive', 'cli'}:
        interactive_cli()
    else:
        s = 'Invoice not received for July invoice'
        b = 'I have not received invoice for July, please resend.'
        print('Prediction:', predict_ticket(s, b))
        print("\nTip: run with --interactive for a live demo CLI.")
