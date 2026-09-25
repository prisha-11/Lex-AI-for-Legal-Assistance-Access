import PyPDF2
import io

def extract_text_from_file(uploaded_file) -> str:
    """
    Extracts text from an uploaded Streamlit PDF or TXT file.
    """
    if uploaded_file is None:
        return ""

    file_extension = uploaded_file.name.split(".")[-1].lower()

    try:
        if file_extension == "pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text
        elif file_extension == "txt":
            return uploaded_file.getvalue().decode("utf-8")
        else:
            raise ValueError("Unsupported file format. Please upload a PDF or TXT file.")
    except Exception as e:
        raise Exception(f"Error processing file: {str(e)}")

