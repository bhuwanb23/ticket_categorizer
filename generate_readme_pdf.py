"""Generate a polished PDF from the project README content."""
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "Auto_Email_Ticket_Categorizer.pdf"

BLUE = (44, 95, 219)
BLUE_DEEP = (28, 63, 153)
TEAL = (14, 165, 160)
INK = (16, 32, 61)
INK_SOFT = (75, 90, 120)
LINE = (220, 226, 237)
SURFACE = (245, 247, 250)

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


def code_block(pdf: DocPDF, lines: str):
    pdf.ln(1)
    pdf.set_font("Mono", "", 8.2)
    row_h = 4.2
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
        # fpdf truncates long lines; keep as-is for mono blocks
        pdf.cell(w - 8, row_h, line.replace("\t", "  "), new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(y + box_h + 3)


def draw_table(pdf: DocPDF, headers, rows):
    col_w = [34, pdf.w - 36 - 34]
    header_h = 8

    if pdf.get_y() + 30 > pdf.h - 22:
        pdf.add_page()

    x0 = 18
    y0 = pdf.get_y()
    pdf.set_fill_color(*BLUE)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Sans", "B", 9.5)
    pdf.set_xy(x0, y0)
    pdf.cell(col_w[0], header_h, f"  {headers[0]}", fill=True)
    pdf.cell(col_w[1], header_h, f"  {headers[1]}", fill=True, new_x="LMARGIN", new_y="NEXT")

    for ri, (step, impl) in enumerate(rows):
        pdf.set_font("Sans", "", 9)
        # estimate height for wrapped implementation text
        impl_w = col_w[1] - 4
        n_lines = max(1, int(pdf.get_string_width(impl) / impl_w) + 1)
        # more accurate wrap count
        words = impl.split()
        lines = []
        cur = ""
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
        n_lines = max(1, len(lines))
        row_h = max(9, n_lines * 4.6 + 3)

        if pdf.get_y() + row_h > pdf.h - 22:
            pdf.add_page()
            # reprint header
            y0 = pdf.get_y()
            pdf.set_fill_color(*BLUE)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Sans", "B", 9.5)
            pdf.set_xy(18, y0)
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
        pdf.multi_cell(col_w[1] - 4, 4.5, impl)
        pdf.set_y(y + row_h)

    pdf.ln(3)


def build():
    pdf = DocPDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(18, 16, 18)

    pdf.add_font("Sans", "", FONT_REG)
    pdf.add_font("Sans", "B", FONT_BOLD)
    pdf.add_font("Mono", "", FONT_MONO)

    # Cover banner
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
    pdf.ln(2)
    pdf.set_font("Sans", "", 10.5)
    pdf.set_text_color(*INK_SOFT)
    pdf.multi_cell(
        0,
        5.5,
        "Lightweight NLP classifier that reads an incoming support ticket "
        "(subject + body) and routes it to Billing, Technical, HR, or General — "
        "with confidence scores, a human-review threshold, and simple priority tagging.",
    )
    pdf.ln(5)

    # Meta pills — fixed Y so they never overlap following content
    pills = [
        ("STACK", "Python · scikit-learn"),
        ("FEATURES", "TF-IDF + Logistic Regression"),
        ("BONUS", "Confidence · Review · Priority · CLI"),
    ]
    pill_y = pdf.get_y()
    pill_h = 14
    pill_w = 56
    gap = 4
    x = 18
    for label, value in pills:
        pdf.set_fill_color(*SURFACE)
        pdf.set_draw_color(*LINE)
        pdf.set_line_width(0.3)
        pdf.rect(x, pill_y, pill_w, pill_h, style="DF")
        pdf.set_xy(x + 3, pill_y + 2)
        pdf.set_font("Sans", "", 7)
        pdf.set_text_color(*INK_SOFT)
        pdf.cell(pill_w - 6, 4, label)
        pdf.set_xy(x + 3, pill_y + 6.5)
        pdf.set_font("Sans", "B", 8)
        pdf.set_text_color(*INK)
        pdf.cell(pill_w - 6, 5, value)
        x += pill_w + gap
    pdf.set_y(pill_y + pill_h + 8)

    # Quick start
    section_title(pdf, "1. Quick start")
    body(pdf, "From the project root, create a virtualenv and run:")
    code_block(
        pdf,
        """# create / use a virtualenv
python -m venv venv

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
    body(
        pdf,
        "train.py prints holdout accuracy, a classification report, and a confusion matrix, "
        "then saves a full-data model to models/.",
    )

    # What it does
    section_title(pdf, "2. What it does")
    draw_table(
        pdf,
        ["Step", "Implementation"],
        [
            ("Clean text", "Lowercase, strip HTML/URLs/emails/punctuation/stopwords (src/preprocess.py)"),
            ("Features", "TF-IDF unigrams + bigrams on combined subject + body"),
            ("Model", "Logistic Regression (sklearn)"),
            ("Evaluate", "Stratified holdout → accuracy, precision/recall/F1, confusion matrix"),
            ("Infer", "predict_ticket(subject, body) for one ticket on demand"),
            ("Bonus", "Confidence %, review if confidence < 60%, urgent/normal keywords, live CLI"),
        ],
    )
    body(pdf, "Categories:  #billing   #technical   #hr   #general")

    # Layout
    section_title(pdf, "3. Project layout")
    code_block(
        pdf,
        """├── data/tickets.csv                 # labeled training tickets
├── src/
│   ├── preprocess.py                # text cleaning
│   ├── train.py                     # train + evaluate + save model
│   └── predict.py                   # inference API + interactive CLI
├── notebooks/
│   └── ticket_categorizer_demo.py   # 5 sample predictions
├── models/                          # created by train.py (gitignored)
├── requirements.txt
└── README.md""",
    )

    # Example output
    section_title(pdf, "4. Example output")
    code_block(
        pdf,
        """SUBJECT: Invoice missing
 -> label=Billing, confidence=0.70, review=False, priority=urgent
------------------------------------------------------------
SUBJECT: App crashes on save
 -> label=Technical, confidence=0.73, review=False, priority=normal
------------------------------------------------------------
SUBJECT: Leave balance query
 -> label=HR, confidence=0.67, review=False, priority=normal
------------------------------------------------------------
SUBJECT: Refund status
 -> label=Billing, confidence=0.52, review=True, priority=normal
------------------------------------------------------------
SUBJECT: Password reset
 -> label=Technical, confidence=0.73, review=False, priority=normal""",
    )
    body(
        pdf,
        "Ambiguous or low-confidence tickets stay labeled with the model’s best guess "
        "but are flagged needs_human_review=True so they can go to a manual queue "
        "instead of auto-assign.",
    )
    body(pdf, "Interactive CLI:")
    code_block(pdf, "python src/predict.py --interactive")
    code_block(
        pdf,
        """Subject: Production outage
Body   : Service is down and not working — urgent
  category : Technical
  confidence: 76.1%
  human review: no (auto-assign)
  priority : urgent""",
    )

    # Approach
    section_title(pdf, "5. Approach summary")
    body(
        pdf,
        "Cleaned subject+body text, vectorized with TF-IDF (1–2 grams), and trained "
        "Logistic Regression for fast short-text classification with usable probability "
        "estimates. Predictions return the category plus a confidence score; below ~60% "
        "confidence the ticket is flagged for human review rather than auto-routed. "
        "Priority (urgent / normal) is a lightweight keyword layer (urgent, down, asap, "
        "not working, critical, outage).",
    )

    # Reflection
    section_title(pdf, "6. Reflection")
    body(
        pdf,
        "With more real helpdesk data I would expand coverage of ambiguous General vs "
        "Technical tickets and rare failure phrases. Next I’d calibrate probabilities, "
        "compare linear SVM / Multinomial Naive Bayes, and learn priority instead of "
        "hard-coded keywords. A human-in-the-loop queue for low-confidence tickets, plus "
        "periodic retraining on reviewed labels, would make routing more reliable in production.",
    )

    # Requirements
    section_title(pdf, "7. Requirements")
    bullet(pdf, "Python 3.9+")
    bullet(pdf, "scikit-learn, pandas, joblib  (see requirements.txt)")

    pdf.ln(8)
    pdf.set_draw_color(*LINE)
    pdf.line(18, pdf.get_y(), pdf.w - 18, pdf.get_y())
    pdf.ln(4)
    pdf.set_font("Sans", "", 8.5)
    pdf.set_text_color(*INK_SOFT)
    pdf.multi_cell(
        0,
        4.5,
        "Fobes Skill Itech Pvt Ltd — AI/ML Internship Program · Technical Assessment\n"
        "Document generated from project README.",
    )

    pdf.output(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
