import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="ResearchGPT",
    page_icon="🔍",
    layout="wide"
)


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📄 ResearchGPT")
st.sidebar.write("Upload research papers and ask grounded questions.")

st.sidebar.markdown(
    """
    ### Workflow
    1. Upload PDF  
    2. Build FAISS index  
    3. Ask question  
    4. Get grounded answer  
    """
)


# -----------------------------
# Main Header
# -----------------------------
st.title("🔍 ResearchGPT — Research Paper Q&A System")
st.write(
    "Upload research papers, build a retrieval index, and ask questions answered using retrieved paper context."
)

st.markdown("---")


# -----------------------------
# Backend Health Check
# -----------------------------
st.subheader("✅ Backend Status")

try:
    health_response = requests.get(f"{API_URL}/", timeout=5)

    if health_response.status_code == 200:
        st.success("FastAPI backend is running.")
        with st.expander("Backend response"):
            st.json(health_response.json())
    else:
        st.warning("Backend is reachable, but returned an unexpected response.")

except requests.exceptions.ConnectionError:
    st.error("FastAPI backend is not running. Start it using: uvicorn app.main:app --reload")

except requests.exceptions.Timeout:
    st.error("FastAPI backend timed out. Please restart the backend.")


st.markdown("---")


# -----------------------------
# Upload PDF Section
# -----------------------------
st.subheader("📤 Upload Research Paper PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if uploaded_file is not None:
    st.info(f"Selected file: {uploaded_file.name}")

    if st.button("Upload PDF"):
        with st.spinner("Uploading PDF to backend..."):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf"
                )
            }

            response = requests.post(
                f"{API_URL}/upload-pdf",
                files=files,
                timeout=60
            )

            if response.status_code == 200:
                st.success("PDF uploaded successfully.")
                st.json(response.json())
            else:
                st.error("PDF upload failed.")
                try:
                    st.json(response.json())
                except Exception:
                    st.write(response.text)


st.markdown("---")


# -----------------------------
# Build Index Section
# -----------------------------
st.subheader("🧠 Build Research Paper Index")

st.write(
    "After uploading PDFs, build the FAISS index so ResearchGPT can retrieve relevant chunks."
)

if st.button("Build Index"):
    with st.spinner("Extracting text, chunking papers, creating embeddings, and building FAISS index..."):
        response = requests.post(
            f"{API_URL}/build-index",
            timeout=300
        )

        if response.status_code == 200:
            result = response.json()

            st.success("Index built successfully.")
            st.json(result)

            st.info(
                f"Processed {result.get('documents_processed')} document(s) "
                f"and generated {result.get('chunks_generated')} chunks."
            )
        else:
            st.error("Index build failed.")
            try:
                st.json(response.json())
            except Exception:
                st.write(response.text)


st.markdown("---")


# -----------------------------
# Query Section
# -----------------------------
st.subheader("💬 Ask Questions")

query = st.text_input(
    "Enter your question",
    placeholder="Example: What is self-attention?"
)

ask_btn = st.button("Ask ResearchGPT")

if ask_btn:
    if not query.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Retrieving relevant chunks and generating grounded answer..."):
            response = requests.post(
                f"{API_URL}/ask",
                json={"question": query},
                timeout=180
            )

            if response.status_code == 200:
                result = response.json()

                st.subheader("📌 Answer")

                answer_data = result.get("answer", {})

                if isinstance(answer_data, dict) and "answer" in answer_data:
                    st.write(answer_data["answer"])

                    if answer_data.get("model"):
                        st.caption(f"Model: {answer_data.get('model')}")
                else:
                    st.json(answer_data)

                st.subheader("📚 Retrieved Sources")
                retrieved_sources = result.get("retrieved_sources", [])

                if retrieved_sources:
                    st.dataframe(retrieved_sources, use_container_width=True)
                else:
                    st.info("No retrieved sources returned.")

                with st.expander("🔎 Full API Response"):
                    st.json(result)

            else:
                st.error("Question answering failed.")
                try:
                    st.json(response.json())
                except Exception:
                    st.write(response.text)


st.markdown("---")


# -----------------------------
# Explanation
# -----------------------------
with st.expander("ℹ️ How ResearchGPT Works"):
    st.write(
        """
        ResearchGPT follows a Retrieval-Augmented Generation pipeline:

        1. User uploads a research paper PDF.
        2. The backend stores the PDF in the `papers/` folder.
        3. Text is extracted from the PDF.
        4. Text is split into overlapping chunks.
        5. Chunks are converted into embeddings.
        6. Embeddings are indexed using FAISS.
        7. A user question is embedded and matched against the FAISS index.
        8. Relevant chunks are sent to the LLM.
        9. The LLM generates a grounded answer using retrieved context.
        """
    )


# -----------------------------
# Footer
# -----------------------------
st.markdown("Built using **RAG + FAISS + FastAPI + Streamlit + LLM Generation**")