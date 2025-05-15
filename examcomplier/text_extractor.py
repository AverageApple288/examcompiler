from pymupdf import Document

DPI = 400
SCALE = DPI / 72

class QuestionExtractor:
    def __init__(self, pdf: Document):
        self.pdf = pdf

    

