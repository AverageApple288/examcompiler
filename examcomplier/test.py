from xml.dom.minidom import Document
import pymupdf
from PIL import Image

pdf = pymupdf.open("../pdf/physics_past_paper.pdf")

DPI = 400  # Dots per inch
SCALE = DPI / 72  # PDFS use 72 points per inch

for i, page in enumerate(pdf):
    page: pymupdf.Page
    text_instances = page.search_for("1. ")
    if not text_instances:
        continue

    print(text_instances)
    pix: pymupdf.Pixmap = page.get_pixmap(dpi=DPI)
    img = pix.pil_image()

    text: pymupdf.Rect = text_instances[0]

    img.crop((text.x0 * SCALE,
              text.y0 * SCALE,
              text.x1 * SCALE,
              text.y1 * SCALE)
             ).save(f"test{i}.png")
