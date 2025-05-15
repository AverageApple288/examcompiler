# Imports
from openai import OpenAI
from enum import Enum
from pathlib import Path
import base64

class PastPaper:
    def __init__(self, questions):
        self.questions = questions
        self.client = OpenAI(api_key="YOUR_API_KEY")

    def initialise_topic(self, question):
        prompt = f"Analyze the image and decide what topic it is in"
        image_path = Path(question.question)

        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")

        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        try:
            response = self.client.responses.create(
                model="gpt-4o-mini",
                instructions="You are an expert in deciding what topic an exam question is about. Please answer with only the topic name, selecting from these following topics: ",
                input=[
                    {
                        "role": "system",
                        "content": [
                            {"type": "input_text", "text": prompt},
                            {"type": "input_image", "image_url": f"data:image/png;base64,{base64_image}"},
                        ],
                    }
                ],
            )
            question.topic = response.choices[0].message.content
        except Exception as e:
            return f"Error analyzing image: {str(e)}"