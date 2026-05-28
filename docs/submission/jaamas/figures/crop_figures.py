#!/usr/bin/env python3
"""Trim white margins from Mermaid PNG/PDF figure exports."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def ensure_deps() -> None:
    for pkg, import_name in (("Pillow", "PIL"), ("pymupdf", "fitz")):
        try:
            __import__(import_name)
        except ImportError:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--quiet", pkg],
            )


def _is_white(r: int, g: int, b: int, tolerance: int) -> bool:
    return r >= 255 - tolerance and g >= 255 - tolerance and b >= 255 - tolerance


def trim_png(path: Path, margin: int, tolerance: int) -> None:
    from PIL import Image

    im = Image.open(path).convert("RGB")
    w, h = im.size
    px = im.load()
    min_x, min_y, max_x, max_y = w, h, -1, -1

    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if not _is_white(r, g, b, tolerance):
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)

    if max_x < 0:
        return

    left = max(0, min_x - margin)
    top = max(0, min_y - margin)
    right = min(w, max_x + margin + 1)
    bottom = min(h, max_y + margin + 1)
    cropped = im.crop((left, top, right, bottom))
    cropped.save(path, optimize=True)


# Match draw.io pageframe stroke (#94a3b8)
BORDER_RGB = (148, 163, 184)


def add_border_png(path: Path, width: int = 2) -> None:
    from PIL import Image, ImageDraw

    im = Image.open(path).convert("RGB")
    w, h = im.size
    canvas = Image.new("RGB", (w + 2 * width, h + 2 * width), (255, 255, 255))
    canvas.paste(im, (width, width))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle(
        (0, 0, w + 2 * width - 1, h + 2 * width - 1),
        outline=BORDER_RGB,
        width=width,
    )
    canvas.save(path, optimize=True)


def add_border_pdf(path: Path, width_pt: float = 1.5) -> None:
    import fitz

    doc = fitz.open(path)
    page = doc[0]
    rect = page.rect
    color = tuple(c / 255.0 for c in BORDER_RGB)
    shape = page.new_shape()
    shape.draw_rect(rect)
    shape.finish(color=color, width=width_pt)
    shape.commit()
    tmp = path.with_suffix(".border.tmp.pdf")
    doc.save(str(tmp), garbage=4, deflate=True)
    doc.close()
    tmp.replace(path)


def pad_png_square(path: Path, margin: int) -> None:
    from PIL import Image

    im = Image.open(path).convert("RGB")
    w, h = im.size
    side = max(w, h) + margin * 2
    if w == h and margin == 0:
        return
    canvas = Image.new("RGB", (side, side), (255, 255, 255))
    canvas.paste(im, ((side - w) // 2, (side - h) // 2))
    canvas.save(path, optimize=True)


def trim_pdf(path: Path, margin: int, tolerance: int, dpi: int) -> None:
    import fitz

    doc = fitz.open(path)
    page = doc[0]
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    w, h = pix.width, pix.height
    data = pix.samples

    min_x, min_y, max_x, max_y = w, h, -1, -1
    for y in range(h):
        row = y * w * 3
        for x in range(w):
            i = row + x * 3
            r, g, b = data[i], data[i + 1], data[i + 2]
            if not _is_white(r, g, b, tolerance):
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)

    if max_x < 0:
        doc.close()
        return

    scale = 72 / dpi
    rect = fitz.Rect(
        max(0, min_x * scale - margin),
        max(0, min_y * scale - margin),
        min(page.rect.width, (max_x + 1) * scale + margin),
        min(page.rect.height, (max_y + 1) * scale + margin),
    )
    page.set_cropbox(rect)
    page.set_mediabox(rect)
    tmp = path.with_suffix(".crop.tmp.pdf")
    doc.save(str(tmp), garbage=4, deflate=True)
    doc.close()
    tmp.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("figures_dir", type=Path, help="Directory containing FigN.png/pdf")
    parser.add_argument("--margin", type=int, default=10, help="Pixels/points to keep around content")
    parser.add_argument("--tolerance", type=int, default=18, help="Near-white threshold")
    parser.add_argument("--dpi", type=int, default=180, help="Raster DPI for PDF crop detection")
    parser.add_argument(
        "--fig-margins",
        default="1:36",
        help="Per-figure crop margins, e.g. '1:36,9:16'",
    )
    parser.add_argument(
        "--fig-square",
        default="",
        help="Comma-separated figure numbers to pad to a square canvas after crop",
    )
    parser.add_argument(
        "--border",
        action="store_true",
        help="Add neutral #94a3b8 frame to figure PNG/PDF exports and screenshots",
    )
    parser.add_argument(
        "--border-screenshots-only",
        action="store_true",
        help="Border only figures/screenshots/*.png (skip diagram PDF/PNG)",
    )
    parser.add_argument(
        "--border-figure-png-only",
        action="store_true",
        help="Border only Fig1-9.png (for IDE preview; manuscript PDFs use LaTeX frame)",
    )
    parser.add_argument(
        "--borders-only",
        action="store_true",
        help="Skip crop/pad; only apply --border* passes",
    )
    parser.add_argument("--border-px", type=int, default=2, help="PNG border width in pixels")
    parser.add_argument("--border-pt", type=float, default=1.5, help="PDF border width in points")
    args = parser.parse_args()

    fig_margins: dict[int, int] = {}
    if args.fig_margins:
        for part in args.fig_margins.split(","):
            if not part.strip():
                continue
            fig_s, margin_s = part.split(":", 1)
            fig_margins[int(fig_s.strip())] = int(margin_s.strip())

    fig_square = {
        int(part.strip())
        for part in args.fig_square.split(",")
        if part.strip()
    }

    ensure_deps()

    if not args.borders_only:
        for n in range(1, 10):
            png = args.figures_dir / f"Fig{n}.png"
            pdf = args.figures_dir / f"Fig{n}.pdf"
            margin = fig_margins.get(n, args.margin)
            if png.is_file():
                trim_png(png, margin, args.tolerance)
                print(f"Cropped {png.name} (margin={margin})")
                if n in fig_square:
                    pad_png_square(png, margin)
                    print(f"Padded {png.name} to square")
            if pdf.is_file():
                trim_pdf(pdf, margin, args.tolerance, args.dpi)
                print(f"Cropped {pdf.name} (margin={margin})")

    if args.border or args.border_screenshots_only or args.border_figure_png_only:
        border_figures = args.border and not args.border_screenshots_only
        border_figure_png = args.border or args.border_figure_png_only
        border_screenshots = args.border or args.border_screenshots_only

        if border_figure_png or border_figures:
            for n in range(1, 10):
                png = args.figures_dir / f"Fig{n}.png"
                pdf = args.figures_dir / f"Fig{n}.pdf"
                if border_figure_png and png.is_file():
                    add_border_png(png, args.border_px)
                    print(f"Bordered {png.name}")
                if border_figures and pdf.is_file():
                    add_border_pdf(pdf, args.border_pt)
                    print(f"Bordered {pdf.name}")

        if border_screenshots:
            shots = args.figures_dir / "screenshots"
            if shots.is_dir():
                for png in sorted(shots.glob("*.png")):
                    add_border_png(png, args.border_px)
                    print(f"Bordered {png.name}")


if __name__ == "__main__":
    main()
