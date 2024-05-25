"""Utilsy używane w ramach usługi"""

import re
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

from app.models import EndpointInputModel

# load data from .env file
load_dotenv()

api_key = os.getenv("API_KEY")
sentence_transformer_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


def validate_input(input_: EndpointInputModel):
    """
    Funkcja sprawdzająca czy input do enpointa ma poprawną strukturę

    Args:
        input_ (EndpointInputModel): JSON stanowiący request body

    Returns:
        (bool): wartość logiczna mówiąca o tym czy podany JSON jest poprawny
    """
    if input_:
        return True
    else:
        return False


def convert_to_markdown(text):
    markdown = text

    # Convert headings
    markdown = re.sub(r'^(#+)(.*)', r'\1 \2', markdown, flags=re.MULTILINE)

    # Convert unordered lists
    markdown = re.sub(r'^\*\s+(.*)', r'- \1', markdown, flags=re.MULTILINE)

    # Convert ordered lists
    markdown = re.sub(r'^\d+\.\s+(.*)', r'1. \1', markdown, flags=re.MULTILINE)

    # Convert blockquotes
    markdown = re.sub(r'^>\s+(.*)', r'> \1', markdown, flags=re.MULTILINE)

    return markdown


def generate_vector(text: str) -> np.ndarray:
    return sentence_transformer_model.encode(text).tolist()
