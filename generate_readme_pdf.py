"""Generate a polished PDF report for the ticket categorizer assessment."""
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "Auto_Email_Ticket_Categorizer.pdf"
REPO_URL = "https://github.com/Padmanaban29072004/ticket_categorizer"
REPO_NAME = "Padmanaban29072004/ticket_categorizer"

BLUE = (44, 95, 219)
BLUE_DEEP = (28, 63, 153)
TEAL = (14, 165, 160)
INK = (16, 32, 61)
INK_SOFT = (75, 90, 120)
LINE = (220, 226, 237)
SURFACE = (245, 247, 250)
AMBER_BG = (255, 249, 230)
AMBER = (138, 100, 8)

FONT_REG = "C:/Windows/Fonts/segoeui.ttf"
FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_MONO = "C:/Windows/Fonts/consola.ttf"


class DocPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_draw_color(*LINE)
        self.set_line_width(0.3)
        self.line(18, 12, self.w - 18, 12)
        self.set_xy(18, 4)
        self.set_font("Sans", "", 8)
        self.set_text_color(*INK_SOFT)
        self.cell(0, 6, "Auto Email / Ticket Categorizer  ·  Fobes Skill Itech", align="L")
        self.set_y(16)

    def footer(self):
        self.set_y(-14)
        self.set_draw_color(*LINE)
        self.line(18, self.get_y(), self.w - 18, self.get_y())
        self.set_y(-12)
        self.set_font("Sans", "", 8)
        self.set_text_color(*INK_SOFT)
        self.cell(0, 8, f"Page {self.page_no()}/{{nb}}", align="C")


def section_title(pdf: DocPDF, text: str):
    pdf.ln(3)
    if pdf.get_y() > pdf.h - 40:
        pdf.add_page()
    pdf.set_font("Sans", "B", 13)
    pdf.set_text_color(*BLUE_DEEP)
    pdf.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT")
    y = pdf.get_y()
    pdf.set_draw_color(*TEAL)
    pdf.set_line_width(0.8)
    pdf.line(18, y, 48, y)
    pdf.ln(4)


def body(pdf: DocPDF, text: str, size: float = 10.5):
    pdf.set_font("Sans", "", size)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 5.5, text)
    pdf.ln(1.5)


def bullet(pdf: DocPDF, text: str):
    pdf.set_font("Sans", "", 10.5)
    pdf.set_x(18)
    pdf.set_text_color(*TEAL)
    pdf.cell(5, 5.5, "•")
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 5.5, text)
    pdf.ln(0.5)


def insight_box(pdf: DocPDF, title: str, text: str):
    pdf.ln(1)
    pdf.set_font("Sans", "", 9.5)
    # rough height
    avail = pdf.w - 44
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if pdf.get_string_width(trial) <= avail:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    box_h = 8 + 5 * len(lines) + 4
    if pdf.get_y() + box_h > pdf.h - 22:
        pdf.add_page()
    x, y = 18, pdf.get_y()
    w = pdf.w - 36
    pdf.set_fill_color(*AMBER_BG)
    pdf.set_draw_color(240, 223, 168)
    pdf.set_line_width(0.4)
    pdf.rect(x, y, w, box_h, style="DF")
    pdf.set_xy(x + 4, y + 2.5)
    pdf.set_font("Sans", "B", 9)
    pdf.set_text_color(*AMBER)
    pdf.cell(0, 5, title.upper())
    pdf.set_xy(x + 4, y + 8)
    pdf.set_font("Sans", "", 9.5)
    pdf.set_text_color(*INK)
    pdf.multi_cell(w - 8, 5, text)
    pdf.set_y(y + box_h + 3)


def code_block(pdf: DocPDF, lines: str):
    pdf.ln(1)
    pdf.set_font("Mono", "", 8.0)
    row_h = 4.1
    text_lines = lines.strip("\n").split("\n")
    box_h = row_h * len(text_lines) + 6
    if pdf.get_y() + box_h > pdf.h - 22:
        pdf.add_page()
    x, y = 18, pdf.get_y()
    w = pdf.w - 36
    pdf.set_fill_color(*SURFACE)
    pdf.set_draw_color(*LINE)
    pdf.set_line_width(0.3)
    pdf.rect(x, y, w, box_h, style="DF")
    pdf.set_xy(x + 4, y + 3)
    pdf.set_text_color(*INK)
    for line in text_lines:
        pdf.set_x(x + 4)
        pdf.cell(w - 8, row_h, line.replace("\t", "  "), new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(y + box_h + 3)


def draw_table(pdf: DocPDF, headers, rows, col0_w=34):
    col_w = [col0_w, pdf.w - 36 - col0_w]
    header_h = 8

    if pdf.get_y() + 30 > pdf.h - 22:
        pdf.add_page()

    pdf.set_fill_color(*BLUE)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Sans", "B", 9.5)
    pdf.set_x(18)
    pdf.cell(col_w[0], header_h, f"  {headers[0]}", fill=True)
    pdf.cell(col_w[1], header_h, f"  {headers[1]}", fill=True, new_x="LMARGIN", new_y="NEXT")

    for ri, (step, impl) in enumerate(rows):
        pdf.set_font("Sans", "", 9)
        impl_w = col_w[1] - 4
        words = str(impl).split()
        lines, cur = [], ""
        for w in words:
            trial = f"{cur} {w}".strip()
            if pdf.get_string_width(trial) <= impl_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        row_h = max(9, len(lines) * 4.6 + 3)

        if pdf.get_y() + row_h > pdf.h - 22:
            pdf.add_page()
            pdf.set_fill_color(*BLUE)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Sans", "B", 9.5)
            pdf.set_x(18)
            pdf.cell(col_w[0], header_h, f"  {headers[0]}", fill=True)
            pdf.cell(col_w[1], header_h, f"  {headers[1]}", fill=True, new_x="LMARGIN", new_y="NEXT")

        y = pdf.get_y()
        fill = SURFACE if ri % 2 else (255, 255, 255)
        pdf.set_fill_color(*fill)
        pdf.rect(18, y, sum(col_w), row_h, style="F")
        pdf.set_draw_color(*LINE)
        pdf.line(18, y + row_h, 18 + sum(col_w), y + row_h)

        pdf.set_xy(18, y + (row_h - 4.5) / 2)
        pdf.set_font("Sans", "B", 9)
        pdf.set_text_color(*BLUE_DEEP)
        pdf.cell(col_w[0], 4.5, f"  {step}")

        pdf.set_xy(18 + col_w[0] + 2, y + 2)
        pdf.set_font("Sans", "", 9)
        pdf.set_text_color(*INK)
        pdf.multi_cell(col_w[1] - 4, 4.5, str(impl))
        pdf.set_y(y + row_h)

    pdf.ln(3)


def metric_pills(pdf: DocPDF, items):
    """items: list of (label, value)"""
    n = len(items)
    gap = 4
    total_w = pdf.w - 36
    pill_w = (total_w - gap * (n - 1)) / n
    pill_h = 16
    y = pdf.get_y()
    if y + pill_h + 6 > pdf.h - 22:
        pdf.add_page()
        y = pdf.get_y()
    x = 18
    for label, value in items:
        pdf.set_fill_color(*SURFACE)
        pdf.set_draw_color(*LINE)
        pdf.set_line_width(0.3)
        pdf.rect(x, y, pill_w, pill_h, style="DF")
        pdf.set_xy(x + 3, y + 2)
        pdf.set_font("Sans", "", 7)
        pdf.set_text_color(*INK_SOFT)
        pdf.cell(pill_w - 6, 4, label.upper())
        pdf.set_xy(x + 3, y + 7)
        pdf.set_font("Sans", "B", 11)
        pdf.set_text_color(*BLUE_DEEP)
        pdf.cell(pill_w - 6, 6, value)
        x += pill_w + gap
    pdf.set_y(y + pill_h + 6)


def build():
    pdf = DocPDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(18, 16, 18)

    pdf.add_font("Sans", "", FONT_REG)
    pdf.add_font("Sans", "B", FONT_BOLD)
    pdf.add_font("Mono", "", FONT_MONO)

    # ---------- Cover ----------
    pdf.add_page()
    pdf.set_fill_color(*BLUE)
    pdf.rect(0, 0, pdf.w, 38, style="F")
    pdf.set_fill_color(*TEAL)
    pdf.rect(0, 38, pdf.w, 3, style="F")

    pdf.set_xy(18, 12)
    pdf.set_font("Sans", "B", 11)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 6, "FOBES SKILL ITECH PVT LTD", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(18)
    pdf.set_font("Sans", "", 9)
    pdf.set_text_color(220, 230, 255)
    pdf.cell(0, 5, "AI / ML Intern Assessment  ·  Technical Submission", new_x="LMARGIN", new_y="NEXT")

    pdf.set_y(48)
    pdf.set_font("Sans", "B", 22)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 9, "Auto Email / Ticket Categorizer")
    pdf.ln(1)

    repo_y = pdf.get_y()
    pdf.set_fill_color(*SURFACE)
    pdf.set_draw_color(*TEAL)
    pdf.set_line_width(0.6)
    pdf.rect(18, repo_y, pdf.w - 36, 16, style="DF")
    pdf.set_xy(22, repo_y + 2)
    pdf.set_font("Sans", "", 7.5)
    pdf.set_text_color(*INK_SOFT)
    pdf.cell(0, 4, "GITHUB REPOSITORY")
    pdf.set_xy(22, repo_y + 6.5)
    pdf.set_font("Sans", "B", 10)
    pdf.set_text_color(*BLUE_DEEP)
    pdf.cell(0, 4.5, REPO_NAME, link=REPO_URL)
    pdf.set_xy(22, repo_y + 11)
    pdf.set_font("Sans", "", 8)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 3.5, REPO_URL, link=REPO_URL)
    pdf.set_y(repo_y + 20)

    pdf.set_font("Sans", "", 10.5)
    pdf.set_text_color(*INK_SOFT)
    pdf.multi_cell(
        0,
        5.5,
        "Lightweight NLP classifier that reads an incoming support ticket "
        "(subject + body) and routes it to Billing, Technical, HR, or General — "
        "with confidence scores, a human-review threshold, and simple priority tagging.",
    )
    pdf.ln(4)

    metric_pills(
        pdf,
        [
            ("STACK", "Python · sklearn"),
            ("MODEL", "TF-IDF + LogReg"),
            ("HOLDOUT ACC.", "62.5%"),
            ("DEMO HITS", "5 / 5 labels"),
        ],
    )

    # ---------- Problem ----------
    section_title(pdf, "1. Problem & goal")
    body(
        pdf,
        "Enterprise helpdesks receive a mixed stream of tickets every day. Manual triage "
        "is slow and inconsistent. This project builds a lightweight routing layer that "
        "reads new ticket text and assigns a department automatically — the same pattern "
        "used in front of live ticket queues.",
    )
    bullet(pdf, "Input: ticket subject + body text")
    bullet(pdf, "Output: category (Billing / Technical / HR / General)")
    bullet(pdf, "Also return confidence %, human-review flag, and urgent/normal priority")
    bullet(pdf, "Must classify one ticket on demand (not only a static test set)")

    # ---------- What we did ----------
    section_title(pdf, "2. What we built (how)")
    body(
        pdf,
        "End-to-end pipeline: clean text → TF-IDF features → Logistic Regression → "
        "evaluate on a stratified holdout → retrain on all labeled data → serve predictions "
        "via API helper and an interactive CLI.",
    )
    draw_table(
        pdf,
        ["Stage", "What happens"],
        [
            ("1. Data", "32 labeled tickets in data/tickets.csv (8 per class: Billing, Technical, HR, General)"),
            ("2. Clean", "Lowercase; strip HTML, URLs, emails, punctuation, stopwords (src/preprocess.py)"),
            ("3. Features", "Combine subject+body; TF-IDF unigrams + bigrams"),
            ("4. Model", "Logistic Regression (C=8, max_iter=2000) — sharper probs than Naive Bayes here"),
            ("5. Evaluate", "25% stratified holdout → accuracy, precision/recall/F1, confusion matrix"),
            ("6. Ship", "Retrain on 100% of labels; save models/vectorizer.joblib + model.joblib"),
            ("7. Infer", "predict_ticket() cleans text the same way as training, then scores one ticket"),
            ("8. Bonuses", "Confidence %; review if < 60%; keyword priority; live CLI (--interactive)"),
        ],
        col0_w=28,
    )

    insight_box(
        pdf,
        "Design choice",
        "Training and inference share the same clean_text() path so the vectorizer "
        "sees the same token distribution. After reporting holdout metrics, the final "
        "saved model is fit on all labeled rows so production inference uses every example.",
    )

    # ---------- Outcomes / metrics ----------
    section_title(pdf, "3. Evaluation outcomes")
    body(
        pdf,
        "Holdout set: 8 tickets (2 per class), stratified, random_state=42. "
        "With only 32 total samples, holdout numbers are noisy — they are a sanity check, "
        "not a production SLA. The live demo on clear tickets is the stronger usability signal.",
    )
    metric_pills(
        pdf,
        [
            ("ACCURACY", "62.5%"),
            ("MACRO F1", "~0.64"),
            ("BILLING", "P1.00 R1.00"),
            ("TECHNICAL", "P1.00 R0.50"),
        ],
    )
    code_block(
        pdf,
        """Confusion matrix  (rows = true, cols = pred)
Labels: [Billing, General, HR, Technical]

 [[2 0 0 0]     Billing: both correct
  [0 1 1 0]     General: 1 correct, 1 → HR
  [0 1 1 0]     HR:      1 correct, 1 → General
  [0 0 1 1]]    Technical: 1 correct, 1 → HR""",
    )
    insight_box(
        pdf,
        "Insight from the matrix",
        "Billing is cleanly separable (invoice/refund/payment language). Most errors are "
        "General ↔ HR swaps — short, polite questions that share vocabulary (\"how\", "
        "\"policy\", \"account\"). Technical recall dipped when wording overlapped HR/General. "
        "More real tickets in those grey zones would help most.",
    )

    # ---------- Live demo outcomes ----------
    section_title(pdf, "4. Live prediction outcomes")
    body(
        pdf,
        "Five unseen sample tickets (assessment requirement). Labels match intent; "
        "confidence drives auto-assign vs human review.",
    )
    code_block(
        pdf,
        """SUBJECT: Invoice missing
 -> Billing   conf=0.70  review=False  priority=urgent   (\"asap\")
SUBJECT: App crashes on save
 -> Technical conf=0.73  review=False  priority=normal
SUBJECT: Leave balance query
 -> HR        conf=0.67  review=False  priority=normal
SUBJECT: Refund status
 -> Billing   conf=0.52  review=True   priority=normal   (borderline)
SUBJECT: Password reset
 -> Technical conf=0.73  review=False  priority=normal""",
    )
    draw_table(
        pdf,
        ["Outcome", "Meaning"],
        [
            ("4 / 5 auto-assign", "Clear tickets cleared the ~60% confidence bar and route automatically"),
            ("1 human review", "\"Refund status\" stayed Billing but flagged for a person (conf 52%)"),
            ("Priority layer", "\"asap\" / \"down\" / \"urgent\" / \"outage\" mark urgent without changing category"),
            ("CLI demo", "python src/predict.py --interactive types a ticket and routes instantly"),
        ],
        col0_w=40,
    )

    # ---------- Key insights ----------
    section_title(pdf, "5. Key insights")
    bullet(
        pdf,
        "TF-IDF + linear models are enough for short support text — fast to train, easy to explain.",
    )
    bullet(
        pdf,
        "Logistic Regression beat Multinomial Naive Bayes here on usable confidence scores "
        "(NB stayed ~0.4–0.5 even on clear tickets, so almost everything hit human review).",
    )
    bullet(
        pdf,
        "A 60% threshold is conservative on tiny multiclass data; that is desirable for a "
        "triage tool — wrong auto-routes are costlier than an extra human look.",
    )
    bullet(
        pdf,
        "Edge cases (gibberish / vague text) get low confidence → needs_human_review=True "
        "instead of forcing a department.",
    )
    bullet(
        pdf,
        "Keyword priority is a cheap second signal; it should eventually be learned from labeled urgency.",
    )

    # ---------- Quick start ----------
    section_title(pdf, "6. Quick start")
    body(pdf, "From the project root:")
    code_block(
        pdf,
        """python -m venv venv
# Windows
venv\\Scripts\\python.exe -m pip install -r requirements.txt
venv\\Scripts\\python.exe src\\train.py
venv\\Scripts\\python.exe notebooks\\ticket_categorizer_demo.py
venv\\Scripts\\python.exe src\\predict.py --interactive

# macOS / Linux
venv/bin/python -m pip install -r requirements.txt
venv/bin/python src/train.py
venv/bin/python notebooks/ticket_categorizer_demo.py
venv/bin/python src/predict.py --interactive""",
    )

    # ---------- Layout ----------
    section_title(pdf, "7. Project layout")
    code_block(
        pdf,
        """├── data/tickets.csv                 # 32 labeled tickets
├── src/preprocess.py                # text cleaning
├── src/train.py                     # train + evaluate + save
├── src/predict.py                   # API + interactive CLI
├── notebooks/ticket_categorizer_demo.py
├── models/                          # gitignored artifacts
├── requirements.txt
└── README.md""",
    )

    # ---------- Approach ----------
    section_title(pdf, "8. Approach summary")
    body(
        pdf,
        "Cleaned subject+body text, vectorized with TF-IDF (1–2 grams), and trained "
        "Logistic Regression for fast short-text classification with usable probability "
        "estimates. Predictions return the category plus a confidence score; below ~60% "
        "confidence the ticket is flagged for human review rather than auto-routed. "
        "Priority (urgent / normal) is a lightweight keyword layer (urgent, down, asap, "
        "not working, critical, outage).",
    )

    # ---------- Reflection ----------
    section_title(pdf, "9. Reflection — what next")
    body(
        pdf,
        "With more real helpdesk data I would expand coverage of ambiguous General vs "
        "Technical tickets and rare failure phrases. Next I’d calibrate probabilities, "
        "compare linear SVM / Multinomial Naive Bayes on a larger set, and learn priority "
        "instead of hard-coded keywords. A human-in-the-loop queue for low-confidence "
        "tickets, plus periodic retraining on reviewed labels, would make routing more "
        "reliable in production.",
    )

    # ---------- Requirements ----------
    section_title(pdf, "10. Requirements")
    bullet(pdf, "Python 3.9+")
    bullet(pdf, "scikit-learn, pandas, joblib  (see requirements.txt)")

    pdf.ln(6)
    pdf.set_draw_color(*LINE)
    pdf.line(18, pdf.get_y(), pdf.w - 18, pdf.get_y())
    pdf.ln(4)
    pdf.set_font("Sans", "", 8.5)
    pdf.set_text_color(*INK_SOFT)
    pdf.multi_cell(
        0,
        4.5,
        "Fobes Skill Itech Pvt Ltd — AI/ML Internship Program · Technical Assessment\n"
        f"Repository: {REPO_URL}\n"
        "Document generated from project results + README.",
    )

    pdf.output(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
