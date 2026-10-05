import os
import json
import base64

from dotenv import load_dotenv
from groq import Groq

from .prompts import (
    SYSTEM_PROMPT,
    RAG_PROMPT,
    QUIZ_PROMPT,
    EXAM_PROMPT,
    SUMMARY_PROMPT
)


# =========================================================
# LOAD GROQ API KEY
# =========================================================

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing from .env"
    )


# =========================================================
# GROQ CLIENT
# =========================================================

client = Groq(
    api_key=API_KEY
)


# =========================================================
# TEXT MODEL
# =========================================================

MODEL = "openai/gpt-oss-120b"


# =========================================================
# BASIC AI ASSISTANT
# =========================================================

def ask_ai(question):

    response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]
)
    return response.choices[0].message.content


# =========================================================
# PDF RAG
# =========================================================

def answer_from_document(question, context):

    prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )

    return ask_ai(prompt)


# =========================================================
# SUMMARIZER
# =========================================================

def summarize(text):

    prompt = SUMMARY_PROMPT.format(
        text=text
    )

    return ask_ai(prompt)


# =========================================================
# EXAM ANSWER GENERATOR
# =========================================================

def generate_exam_answer(topic, marks):

    prompt = EXAM_PROMPT.format(
        topic=topic,
        marks=marks
    )

    return ask_ai(prompt)


# =========================================================
# QUIZ GENERATOR
# =========================================================

def generate_quiz(topic, number):

    prompt = QUIZ_PROMPT.format(
        topic=topic,
        number=number
    )

    response = client.chat.completions.create(

        model=MODEL,

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.7
    )

    result = response.choices[0].message.content

    # Remove markdown code fences if AI adds them
    result = result.strip()

    if result.startswith("```json"):
        result = result[7:]

    elif result.startswith("```"):
        result = result[3:]

    if result.endswith("```"):
        result = result[:-3]

    result = result.strip()

    try:

        return json.loads(result)

    except json.JSONDecodeError:

        # Try to find JSON array
        start = result.find("[")
        end = result.rfind("]")

        if start != -1 and end != -1:

            json_text = result[start:end + 1]

            return json.loads(json_text)

        raise ValueError(
            "AI did not return valid quiz JSON."
        )


# =========================================================
# MULTIMODAL IMAGE ANALYSIS
# =========================================================

def analyze_image(
    question,
    image_bytes,
    mime_type
):

    encoded_image = base64.b64encode(
        image_bytes
    ).decode("utf-8")


    image_url = (
        f"data:{mime_type};base64,{encoded_image}"
    )


    response = client.chat.completions.create(

        model="meta-llama/llama-4-scout-17b-16e-instruct",

        messages=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",

                "content": [

                    {
                        "type": "text",
                        "text": question
                    },

                    {
                        "type": "image_url",

                        "image_url": {
                            "url": image_url
                        }
                    }

                ]
            }

        ],

        temperature=0.5
    )


    return response.choices[0].message.content