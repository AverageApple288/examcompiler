import pymupdf
from PIL import Image

pdf = pymupdf.open("../pdf/physics_past_paper.pdf")

DPI = 400  # Dots per inch
SCALE = DPI / 72  # PDFS use 72 points per inch

MARGIN_TOP = 10
MARGIN_LEFT = 10
MARGIN_BOTTOM = -10

# Loop through questions instead of pages
for q_num in range(1, 50):
    print(f"Searching for question {q_num}...")
    question_image_parts = []
    is_in_question = False

    # Loop through pages to find all parts of a question
    for i, page in enumerate(pdf):
        page: pymupdf.Page

        question_start_instances = page.search_for(f"{q_num}. ")
        question_end_instances = page.search_for(f"{q_num + 1}. ")
        end_of_paper = page.search_for("END OF QUESTION PAPER")
        end_of_page = page.search_for("page")
        turn_page = page.search_for("Turn over")

        x0, y0, x1, y1 = 0, 0, page.rect.width, page.rect.height

        if not is_in_question and question_start_instances:
            # This is the first page of the question
            is_in_question = True
            q_start_rect: pymupdf.Rect = question_start_instances[0]
            y0 = q_start_rect.y0 - MARGIN_TOP
            x0 = q_start_rect.x0 - MARGIN_LEFT

        if is_in_question:
            # Determine the bottom boundary for the crop
            if question_end_instances:
                q_end_rect: pymupdf.Rect = question_end_instances[0]
                y1 = q_end_rect.y0 + MARGIN_BOTTOM
            elif end_of_paper:
                q_end_rect: pymupdf.Rect = end_of_paper[0]
                y1 = q_end_rect.y0 + MARGIN_BOTTOM
            elif turn_page:
                q_end_rect: pymupdf.Rect = turn_page[0]
                y1 = q_end_rect.y0 + MARGIN_BOTTOM
            elif end_of_page:
                q_end_rect: pymupdf.Rect = end_of_page[0]
                y1 = q_end_rect.y0 + MARGIN_BOTTOM

            # Define the crop area for the current page
            crop_rect = pymupdf.Rect(x0, y0, x1, y1)

            # Crop the page and add the image to our list
            pix: pymupdf.Pixmap = page.get_pixmap(dpi=DPI, clip=crop_rect)
            question_image_parts.append(pix.pil_image())

            # If the question ends on this page, stop searching
            if question_end_instances or end_of_paper:
                break

            # If question continues, reset for next page (top-to-bottom crop)
            is_in_question = True
            x0, y0 = 0, 0

    # Stitch the image parts together if any were found
    if question_image_parts:
        print(f"Processing and saving question {q_num}...")
        widths, heights = zip(*(i.size for i in question_image_parts))
        total_height = sum(heights)
        max_width = max(widths)

        combined_image = Image.new('RGB', (max_width, total_height), (255, 255, 255))

        y_offset = 0
        for im in question_image_parts:
            combined_image.paste(im, (0, y_offset))
            y_offset += im.size[1]

        combined_image.save(f"../images/question{q_num}.png")