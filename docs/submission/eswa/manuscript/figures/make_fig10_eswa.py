"""Build Fig10 for the ESWA paper: composite of 8 portal screenshots.

Layout: 4 columns x 2 rows. Each cell is lettered (a)-(h) to match
the IUI paper's Fig10 for cross-reference consistency. The two
single-direction screenshots already in the paper (fig1_application =
c, fig2_employer_view = g) are reproduced here so all 8 portal states
are visible in a single figure.

Mapping (mirrors the IUI paper convention):
  (a) candidate resume upload and review       ui-candidate-onboarding.png
  (b) candidate parsed-fields confirmation     ui-candidate-profile.png
  (c) candidate match list with explanation    ui-candidate-matches.png
  (d) candidate counterfactual view            ui-score-breakdown.png
  (e) employer job-description upload/review   ui-employer-jobs.png
  (f) employer parsed-requirements confirm     ui-admin-match-run.png
  (g) employer reverse match list              ui-employer-matches.png
  (h) employer shortlist panel                 ui-admin-console.png
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

SOURCE = Path("../../../jaamas/figures/screenshots")
OUTPUT = Path("Fig10.png")

MAPPING = [
    ("ui-candidate-onboarding.png", "a"),
    ("ui-candidate-profile.png", "b"),
    ("ui-candidate-matches.png", "c"),
    ("ui-score-breakdown.png", "d"),
    ("ui-employer-jobs.png", "e"),
    ("ui-admin-match-run.png", "f"),
    ("ui-employer-matches.png", "g"),
    ("ui-admin-console.png", "h"),
]

COLS = 4
ROWS = 2
CELL_W = 720
CELL_H = 450
PADDING = 16
LABEL_H = 40

GRID_W = COLS * CELL_W + (COLS + 1) * PADDING
GRID_H = ROWS * CELL_H + (ROWS + 1) * PADDING + ROWS * LABEL_H

canvas = Image.new("RGB", (GRID_W, GRID_H), "white")
draw = ImageDraw.Draw(canvas)

try:
    font_label = ImageFont.truetype("/System/Library/Fonts/Helvetica-Bold.ttc", 32)
except OSError:
    font_label = ImageFont.load_default()

for idx, (fname, letter) in enumerate(MAPPING):
    row = idx // COLS
    col = idx % COLS

    src = Image.open(SOURCE / fname).convert("RGB")
    src.thumbnail((CELL_W, CELL_H), Image.LANCZOS)

    x0 = PADDING + col * (CELL_W + PADDING)
    y0 = PADDING + row * (CELL_H + PADDING + LABEL_H)
    paste_x = x0 + (CELL_W - src.width) // 2
    paste_y = y0 + (CELL_H - src.height) // 2

    draw.rectangle(
        [x0, y0, x0 + CELL_W, y0 + CELL_H],
        outline=(180, 180, 180),
        width=1,
    )
    canvas.paste(src, (paste_x, paste_y))

    draw.text(
        (x0 + 8, y0 + CELL_H + 4),
        f"({letter})",
        fill=(40, 40, 40),
        font=font_label,
    )

canvas.save(OUTPUT, optimize=True)
print(f"Wrote {OUTPUT} ({canvas.size[0]}x{canvas.size[1]})")
