from PyPDF2 import PdfReader


def extract_pdf_text(uploaded_file):

    reader = PdfReader(
        uploaded_file
    )

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = page.extract_text()

        if text:

            pages.append(
                f"""
--- Page {page_number} ---

{text}
"""
            )

    return "\n".join(pages)


def clean_text(text):

    text = text.replace(
        "\x00",
        ""
    )

    return text.strip()


def split_text(
    text,
    chunk_size=1500,
    overlap=250
):

    text = clean_text(text)

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():

            chunks.append(
                chunk.strip()
            )

        start += (
            chunk_size - overlap
        )

    return chunks