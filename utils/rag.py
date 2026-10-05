import re
import math
from collections import Counter


def tokenize(text):

    return re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower()
    )


def term_frequency(tokens):

    counter = Counter(tokens)

    total = len(tokens)

    if total == 0:

        return {}

    return {
        word: count / total
        for word, count in counter.items()
    }


def cosine_similarity(
    vector_a,
    vector_b
):

    common = set(vector_a) & set(vector_b)

    numerator = sum(
        vector_a[x] * vector_b[x]
        for x in common
    )

    magnitude_a = math.sqrt(
        sum(
            value * value
            for value in vector_a.values()
        )
    )

    magnitude_b = math.sqrt(
        sum(
            value * value
            for value in vector_b.values()
        )
    )

    if magnitude_a == 0 or magnitude_b == 0:

        return 0

    return numerator / (
        magnitude_a * magnitude_b
    )


def retrieve_chunks(
    question,
    chunks,
    top_k=5
):

    question_tokens = tokenize(
        question
    )

    question_vector = term_frequency(
        question_tokens
    )

    scored = []

    for chunk in chunks:

        chunk_tokens = tokenize(
            chunk
        )

        chunk_vector = term_frequency(
            chunk_tokens
        )

        score = cosine_similarity(
            question_vector,
            chunk_vector
        )

        scored.append(
            (
                score,
                chunk
            )
        )

    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        chunk
        for score, chunk
        in scored[:top_k]
        if score > 0
    ]


def build_context(
    question,
    chunks,
    top_k=5
):

    results = retrieve_chunks(
        question,
        chunks,
        top_k
    )

    if not results:

        return "No relevant context was found."

    return "\n\n".join(
        f"[Source {i + 1}]\n{chunk}"
        for i, chunk
        in enumerate(results)
    )