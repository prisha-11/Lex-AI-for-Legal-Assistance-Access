import streamlit as st
from document_processor import extract_text_from_file
import ai_service
import os

st.set_page_config(page_title="Lex - GenAI Legal Assistant", page_icon="⚖️", layout="wide")

st.title("⚖️ Lex: Your GenAI Legal Assistant")
st.markdown("""
**Welcome to Lex!** I can help you understand common legal documents like Residential Lease Agreements, 
Quitclaim Deeds, Advance Directives, Power of Attorney documents, NDAs, and more. 

> **Disclaimer:** Lex is an AI, not a lawyer. The information provided is for educational and 
informational purposes only and does not constitute legal advice. Always consult a qualified 
attorney for professional legal advice regarding your specific situation.
""")

# Check for API key
if not ai_service.API_KEY:
    st.warning("⚠️ GEMINI_API_KEY is not set. Please add it to your Streamlit App Secrets.")

# File Uploader
st.sidebar.header("1. Upload Document")
uploaded_file = st.sidebar.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file is not None:
    with st.spinner("Extracting text from document..."):
        try:
            document_text = extract_text_from_file(uploaded_file)
            st.sidebar.success("Document loaded successfully!")
        except Exception as e:
            st.error(f"Error loading document: {e}")
            document_text = None

    if document_text:
        st.sidebar.header("2. Choose Action")
        action = st.sidebar.radio(
            "What would you like to do?",
            ["Summarize & Simplify", "Highlight Risks & Obligations", "Prepare for Lawyer Consultation", "Ask a Question"]
        )

        st.divider()

        if action == "Summarize & Simplify":
            st.header("Document Summary")
            if st.button("Generate Summary"):
                with st.spinner("Lex is analyzing and simplifying your document..."):
                    try:
                        summary = ai_service.summarize_and_simplify(document_text)
                        st.markdown(summary)
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

        elif action == "Highlight Risks & Obligations":
            st.header("Risks & Obligations Analysis")
            if st.button("Analyze Risks"):
                with st.spinner("Lex is identifying potential risks and obligations..."):
                    try:
                        risks = ai_service.highlight_risks(document_text)
                        st.markdown(risks)
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

        elif action == "Prepare for Lawyer Consultation":
            st.header("Lawyer Consultation Prep")
            if st.button("Generate Questions"):
                with st.spinner("Lex is generating a checklist for your lawyer..."):
                    try:
                        prep = ai_service.prepare_for_lawyer(document_text)
                        st.markdown(prep)
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

        elif action == "Ask a Question":
            st.header("Q&A")
            question = st.text_input("Ask a specific question about your document:")
            if st.button("Get Answer") and question:
                with st.spinner("Lex is searching for the answer..."):
                    try:
                        answer = ai_service.answer_question(document_text, question)
                        st.markdown(answer)
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

