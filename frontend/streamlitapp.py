import streamlit as st
import requests

st.set_page_config(
    page_title="ResearchGPT",
    layout="wide"
)

# Sidebar
st.sidebar.title("📄 ResearchGPT")
st.sidebar.write("Upload research papers and ask questions.")

# Main Title
st.title("🔍 Research Paper Q&A System")

# File Upload Section
st.subheader("📤 Upload PDF")
uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Processing PDF..."):
        files = {"file": uploaded_file}
        res = requests.post("http://localhost:8000/upload", files=files)
        st.success(res.json()["message"])

# Query Section
st.subheader("💬 Ask Questions")

query = st.text_input("Enter your question")

col1, col2 = st.columns([1, 5])

with col1:
    ask_btn = st.button("Ask")

if ask_btn and query:
    with st.spinner("Generating answer..."):
        res = requests.post(
            "http://localhost:8000/query",
            params={"q": query}
        )
        answer = res.json()["answer"]

    st.subheader("📌 Answer")
    st.write(answer)

    # Expandable context (optional future)
    with st.expander("ℹ️ How this works"):
        st.write("""
        - Your query is converted into embeddings  
        - Relevant chunks are retrieved from FAISS  
        - LLM generates an answer based on context  
        """)

# Footer
st.markdown("---")
st.markdown("Built using RAG + FAISS + Open Models")