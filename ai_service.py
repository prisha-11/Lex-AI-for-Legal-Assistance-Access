import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        try:
            key = st.secrets["GEMINI_API_KEY"]
        except:
            pass
    return key

# Use a model with good reasoning capabilities for legal text
MODEL_NAME = "gemini-3.5-flash-lite" 

# System instruction to guide the model's behavior
SYSTEM_INSTRUCTION = """
You are Lex, an AI assistant designed to help everyday people understand legal documents.
Your primary focus is on common legal documents such as: Residential Lease Agreements, 
Quitclaim Deeds, Advance Directives (Living Wills), Medical Power of Attorney, 
Financial Power of Attorney (POA), Last Will and Testament, Bills of Sale, 
Non-Disclosure Agreements (NDAs), and Promissory Notes.

CRITICAL DIRECTIVE: You MUST ALWAYS clarify that you are an AI, not a lawyer. 
You provide information and basic assistance to help users understand their documents 
and prepare for legal consultations. You MUST NEVER provide definitive legal advice, 
tell users what legal action to take, or guarantee the legal validity of any document.

Always be clear, use plain English, avoid unnecessary legalese, and structure your 
responses with headings and bullet points for readability.
"""

def get_model():
    key = get_api_key()
    if key:
        genai.configure(api_key=key)
    return genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=SYSTEM_INSTRUCTION
    )

def summarize_and_simplify(document_text: str) -> str:
    """Summarizes and simplifies the legal document."""
    model = get_model()
    prompt = f"""
    Please provide a plain-English summary of the following legal document. 
    1. Identify the type of document (e.g., Lease, NDA, Will).
    2. Outline the core purpose of the document in 1-2 sentences.
    3. Summarize the key terms and conditions in simple bullet points.
    4. Highlight any sections that seem particularly important for an everyday person to understand.

    Document Text:
    {document_text}
    """
    response = model.generate_content(prompt)
    return response.text

def highlight_risks(document_text: str) -> str:
    """Identifies potential risks, obligations, and unusual clauses."""
    model = get_model()
    prompt = f"""
    Analyze the following legal document and highlight potential risks, obligations, 
    and any clauses that an everyday person should pay close attention to.
    1. List the primary obligations of the user (assuming the user is the one signing or receiving the document).
    2. Identify any potential risks, liabilities, or penalties.
    3. Point out any unusual, heavily one-sided, or highly restrictive clauses.
    4. Keep the explanation in plain English.

    Document Text:
    {document_text}
    """
    response = model.generate_content(prompt)
    return response.text

def prepare_for_lawyer(document_text: str) -> str:
    """Generates a checklist of questions for a legal professional."""
    model = get_model()
    prompt = f"""
    Based on the following legal document, generate a list of smart, relevant questions 
    and concerns that the user should bring up when consulting a human lawyer.
    Help the user prepare for their consultation so they can get the most value out of it.
    Focus on areas that are ambiguous, potentially risky, or require professional legal interpretation.

    Document Text:
    {document_text}
    """
    response = model.generate_content(prompt)
    return response.text

def answer_question(document_text: str, question: str) -> str:
    """Answers a specific question based on the document."""
    model = get_model()
    prompt = f"""
    Based ONLY on the provided legal document, please answer the following question.
    If the answer is not in the document, explicitly state that you cannot find the answer in the text.
    
    Question: {question}

    Document Text:
    {document_text}
    """
    response = model.generate_content(prompt)
    return response.text

