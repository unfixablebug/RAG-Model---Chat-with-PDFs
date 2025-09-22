import rag_model
import os
import tempfile
import streamlit as st
from io import BytesIO
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# --- Streamlit UI ---
def main():
    st.set_page_config(page_title="Chat with PDFs", layout="wide")
    st.title("📄 Chat with your PDF")

    if "db" not in st.session_state:
        st.session_state.db = None
    # Upload PDF
    uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_pdf:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_pdf.getvalue())
            tmp_path = tmp_file.name
        if st.session_state.db is None:  # only ingest once
            st.session_state.db = rag_model.run_complete_ingestion_pipeline(tmp_path)
        os.unlink(tmp_path)
        user_q = st.text_input("Ask a question about this PDF")
        if user_q:
            answer = rag_model.query_and_answer_generation(st.session_state.db, user_q)
            st.success(answer)

if __name__ == "__main__":
    main()