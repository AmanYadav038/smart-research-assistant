import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

# --- General Gemini Call ---
def generate_response(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[Error from Gemini API: {str(e)}]"

# --- Generate Summary ---
def generate_summary(doc_text: str) -> str:
    prompt = f"""
Summarize the following document in less than 150 words:
"""
    full_prompt = prompt + doc_text[:6000]  # truncate to avoid overflow
    return generate_response(full_prompt)

# --- Generate Questions ---
def generate_questions_prompt(doc_text):
    return f"""
You are a helpful AI assistant.
Instruction: Read the document and generate exactly 3 logical, inference-based questions.

Example:
Document: Apples are red fruits. They contain vitamins. They're grown in orchards.
Questions:
1. What nutrients do apples provide?
2. Where are apples usually grown?
3. What is the color of apples?

Now do the same for this:
Document: {doc_text}
Questions:
1."""

def generate_logic_questions(text):
    prompt = generate_questions_prompt(text)
    result = generate_response(prompt)

    # Extract numbered questions using regex
    matches = re.findall(r"\d+[\)\.\-\:]\s*(.+?)(?=\d+[\)\.\-\:]|$)", result, re.DOTALL)

    questions = []
    for q in matches:
        cleaned = q.strip().replace("\n", " ")
        if cleaned not in questions:
            questions.append(cleaned)
        if len(questions) >= 3:
            break
    return questions

# --- Evaluate Answer ---
def evaluate_answer_prompt(question, user_answer, doc_text):
    return f"""
Instruction:
Evaluate the user's answer based on the document. Respond whether the answer is correct, incorrect, or partially correct. Justify your verdict using the document. Also, mention what would be a correct or expected answer based on the document.

Positive Example:
Question: Where are apples usually grown?
User's Answer: In orchards.
Document: Apples are red fruits. They contain vitamins. They're grown in orchards.
Response:
✅ Likely Correct
Justification: The answer matches the document, which states that apples are grown in orchards.
Correct Answer: In orchards.

Negative Example:
Question: Where are apples usually grown?
User's Answer: In gardens.
Document: Apples are red fruits. They contain vitamins. They're grown in orchards.
Response:
❌ Needs Review
Justification: The document says apples are grown in orchards, not gardens.
Correct Answer: In orchards.

Now evaluate:
Question: {question}
User's Answer: {user_answer}
Document: {doc_text}
Response:
"""

def evaluate_user_answer(question, user_answer, document):
    prompt = evaluate_answer_prompt(question, user_answer, document)
    result = generate_response(prompt)
    support = get_supporting_snippet(question, document)

    return {
        "justification": result.strip(),
        "support": support
    }


def ask_question_prompt(question, document):
    return f"""
You are a helpful assistant. Answer the question based on the document provided. Be precise, and include justification with reference to the document content.

Question: {question}

Document:
{document}

Response:
"""

def get_supporting_snippet(question: str, document: str) -> str:
    prompt = f"""
    You are a helpful assistant. Your task is to find the exact sentence or paragraph from the document that best supports the following question:

    Question: {question}

    Document:
    {document[:6000]}

    Only return the most relevant sentence or paragraph from the document that supports answering this question. Do not explain.

    Supporting Text:
    """
    return generate_response(prompt)

def ask_question(question: str, document: str) -> str:
    prompt = f"""
    You are a helpful assistant. Read the document below and answer the question based on its content.

    Document:
    {document[:6000]}

    Question: {question}
    Answer:
    """
    answer = generate_response(prompt)
    support = get_supporting_snippet(question, document)

    return f"**Answer:** {answer}\n\n📌 **Supported by:**\n> {support}"
