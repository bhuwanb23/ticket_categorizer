# Auto Email / Ticket Categorizer

TF‑IDF + Logistic Regression baseline for routing support tickets to **Billing**, **Technical**, **HR**, or **General**, with confidence thresholding and simple priority tags.

## Quick start

```bash
# from project root, using the existing venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe src\train.py
.\venv\Scripts\python.exe notebooks\ticket_categorizer_demo.py
.\venv\Scripts\python.exe src\predict.py --interactive
```

## Files

- `data/tickets.csv` — labeled support tickets (subject, body, label)
- `src/preprocess.py` — lowercase, strip noise/stopwords
- `src/train.py` — TF‑IDF + Naive Bayes train/eval; saves full-data model
- `src/predict.py` — `predict_ticket()` + optional live CLI
- `notebooks/ticket_categorizer_demo.py` — five sample predictions

## Approach

Used TF‑IDF on cleaned subject+body text and Logistic Regression for short-text classification (fast, and better-calibrated confidence than Naive Bayes on this tiny dataset). Predictions include a confidence score; if confidence &lt; 60%, the ticket is flagged `needs_human_review` instead of auto-assigning. Priority is a keyword rule layer (`urgent`, `down`, `not working`, etc.).

## Reflection

With more data I would collect real helpdesk tickets (especially ambiguous General vs Technical cases) and rebalance rare phrases. I would also try Logistic Regression / linear SVM, calibrate probabilities, and learn priority instead of hard-coded keywords. A small human-in-the-loop queue for low-confidence tickets would improve routing quality over time.
