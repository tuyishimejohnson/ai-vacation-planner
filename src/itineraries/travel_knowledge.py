import sys

from unstructured.chunking.title import chunk_by_title
from unstructured.cleaners.core import clean_extra_whitespace, clean_non_ascii_chars
from unstructured.documents.elements import Element
from unstructured.partition.auto import partition
from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import (
    Element,
    Header,
    Footer,
)

faq_urls = [
    "https://teaspoonofadventure.com/75-questions-for-travellers/",
    "https://www.adventure-life.com/rwanda/articles/rwanda-faqs",
]


pdf_paths = [
    "src/itineraries/data/The-Best-100-Travel-Tips-and-Hacks-by-Jessica-Ufuoma-1.pdf",
    "src/itineraries/data/TravelTips-Oct2008.PDF",
]


# Partition articles urls
def partition_article(urls):
    results = {}

    for url in urls:
        results[url] = partition(url=url)

    return results


# Partition pdf documents
def partition_pdf_documents(pdf_paths):
    results = {}

    for pdf_path in pdf_paths:
        results[pdf_path] = partition_pdf(filename=pdf_path)

    return results


# Clean the elements by removing empty
def clean_elements(elements):
    cleaned = []

    for element in elements:
        if not element.text:
            continue

        text = clean_extra_whitespace(element.text)
        text = clean_non_ascii_chars(text)

        if not text.strip():
            continue

        element.text = text
        cleaned.append(element)

    return cleaned


articles = partition_article(faq_urls)
documents = partition_pdf_documents(pdf_paths)

for source, elements in articles.items():
    articles[source] = clean_elements(elements)

for source, elements in documents.items():
    documents[source] = clean_elements(elements)


# Filter unecessary elements from the documents and articles
def filter_elements(elements):
    filtered = []

    for element in elements:
        if not element.text:
            continue

        text = element.text.strip()

        if not text:
            continue

        # Remove very short fragments
        if len(text) < 50:
            continue

        # Remove headers and footers
        if isinstance(element, (Header, Footer)):
            continue

        filtered.append(element)

    return filtered
