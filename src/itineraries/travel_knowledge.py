import sys

from unstructured.documents.elements import Element
from unstructured.partition.html import partition_html
from unstructured.partition.pdf import partition_pdf
from pathlib import Path

faq_url = "https://teaspoonofadventure.com/75-questions-for-travellers/"


def partition_article(url: str) -> list[Element]:
    return partition_html(url=url, content_type="text/html")


from pathlib import Path

from unstructured.documents.elements import Element, NarrativeText, Title, ListItem
from unstructured.partition.pdf import partition_pdf
from unstructured.cleaners.core import (
    clean,
    clean_extra_whitespace,
    replace_unicode_quotes,
)

DATA_DIR = Path("src/itineraries/data")


def partition_pdf_file(pdf_path: str, strategy: str = "hi-res") -> list[Element]:
    return partition_pdf(filename=pdf_path, strategy=strategy)


def normalize_text(text: str) -> str:
    text = replace_unicode_quotes(text)
    text = clean_extra_whitespace(text)
    text = clean(text, bullets=True, extra_whitespace=True, dashes=True)
    return text


def normalize_elements(elements: list[Element]) -> list[Element]:
    """Filter noise and clean text in-place."""
    keep_types = (Title, NarrativeText, ListItem)
    filtered = [el for el in elements if isinstance(el, keep_types)]
    for el in filtered:
        el.text = normalize_text(el.text)
    return [el for el in filtered if el.text.strip()]


def preprocess_pdf(pdf_path: str) -> list[Element]:
    raw_elements = partition_pdf_file(pdf_path, strategy="hi-res")
    return normalize_elements(raw_elements)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")

    elements = partition_article(faq_url)
    for element in elements:
        print(f"[{element.category}] {element.text}")
