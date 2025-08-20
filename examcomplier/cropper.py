import pymupdf

pdf = pymupdf.open("../pdf/physics_past_paper.pdf")

DPI = 400  # Dots per inch
SCALE = DPI / 72  # PDFS use 72 points per inch

MARGIN_TOP = 10
MARGIN_LEFT = 10
MARGIN_BOTTOM = -10

completed_questions = [0]

for i, page in enumerate(pdf):
    print(f"Processing page {i + 1}...")
    page: pymupdf.Page
    pix: pymupdf.Pixmap = page.get_pixmap(dpi=DPI)
    img = pix.pil_image

    for q_num in range(completed_questions[-1]+1, 50):
        question_1_instances = page.search_for(f"{q_num}. ")
        if question_1_instances:
            completed_questions.append(q_num)
        else:
            continue  # Skip if the current question number isn't on the page

        print(f"Processing question {q_num}...")

        question_2_instances = page.search_for(f"{q_num + 1}. ")
        end_of_paper = page.search_for("END OF QUESTION PAPER")
        end_of_page = page.search_for("page")
        turn_page = page.search_for("Turn over")

        # Define the crop area
        q1_rect: pymupdf.Rect = question_1_instances[0]
        x0 = q1_rect.x0 - MARGIN_LEFT
        y0 = q1_rect.y0 - MARGIN_TOP
        x1 = page.rect.width  # Use the full page width

        if question_2_instances:
            # If the next question is on the same page, crop to its top
            q2_rect: pymupdf.Rect = question_2_instances[0]
            y1 = q2_rect.y0 + MARGIN_BOTTOM
        elif end_of_paper:
            q2_rect: pymupdf.Rect = end_of_paper[0]
            y1 = q2_rect.y0 + MARGIN_BOTTOM
        elif turn_page:
            q2_rect: pymupdf.Rect = turn_page[0]
            y1 = q2_rect.y0 + MARGIN_BOTTOM
        elif end_of_page:
            q2_rect: pymupdf.Rect = end_of_page[0]
            y1 = q2_rect.y0 + MARGIN_BOTTOM
        else:
            # Otherwise, crop to the bottom of the page
            y1 = page.rect.height

        # Crop the image using scaled coordinates
        img().crop((
            x0 * SCALE,
            y0 * SCALE,
            x1 * SCALE,
            y1 * SCALE
        )).save(f"../images/question{q_num}.png")