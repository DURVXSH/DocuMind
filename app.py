import os

import streamlit as st

from src.logger import logger

from src.pdf_loader import (
    extract_text_from_pdf,
    extract_text_from_docx
)

from src.text_splitter import split_text

from src.embeddings import create_embeddings

from src.vector_store import (
    add_chunks,
    get_all_sources,
    delete_document,
    clear_all_documents
)

from src.rag_pipeline import answer_question


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="DocuMind",
    page_icon="📄",
    layout="wide"
)


# -----------------------------
# Session State
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "processed_documents" not in st.session_state:
    st.session_state.processed_documents = []

if "active_document" not in st.session_state:
    st.session_state.active_document = None


# -----------------------------
# Header
# -----------------------------

st.title("📄 DocuMind")

st.markdown(
    "### AI Document Intelligence Assistant"
)

st.write(
    "Upload your documents, ask questions in natural language, "
    "and get answers grounded in your documents with source citations."
)


if st.session_state.active_document:

    st.success(
        f"📄 Active document: "
        f"**{st.session_state.active_document}**"
    )


if not st.session_state.messages:

    st.markdown(
        """
        ## 👋 Welcome to DocuMind

        Your AI-powered document assistant.

        **Get started in 3 simple steps:**

        1. 📤 **Upload** a PDF or DOCX from the sidebar
        2. 📚 **Select** the document you want to analyze
        3. 💬 **Ask** questions in natural language

        DocuMind retrieves relevant information from your document
        and provides grounded answers with **source and page citations**.
        """
    )


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.title("📄 DocuMind")

    st.caption(
        "AI Document Intelligence Assistant"
    )

    st.divider()

    st.subheader("📤 Upload Document")

    st.caption(
        "Upload a PDF or DOCX file to start."
    )

    # -----------------------------
    # Upload document
    # -----------------------------

    uploaded_file = st.file_uploader(
        "Upload a PDF or DOCX",
        type=["pdf", "docx"]
    )

    st.divider()

    # -----------------------------
    # New chat
    # -----------------------------

    if st.button(
        "➕ New Chat",
        key="new_chat"
    ):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    # -----------------------------
    # Documents from ChromaDB
    # -----------------------------

    available_documents = get_all_sources()

    st.subheader(
    f"📚 Your Documents ({len(available_documents)})"
    )

    # -----------------------------
    # Document selection
    # -----------------------------

    if available_documents:

        selected_document = st.radio(
            "Select a document:",
            available_documents,
            index=(
                available_documents.index(
                    st.session_state.active_document
                )
                if st.session_state.active_document
                in available_documents
                else 0
            ),
            key="document_selector"
        )

        st.session_state.active_document = selected_document

        st.divider()

        # -----------------------------
        # Delete Selected Document
        # -----------------------------

        if st.button(
            "🗑️ Delete Selected",
            key="delete_selected"
        ):

            deleted = delete_document(
                selected_document
            )

            if deleted:

                st.session_state.messages = []

                st.session_state.active_document = None

                if selected_document in st.session_state.processed_documents:

                    st.session_state.processed_documents.remove(
                        selected_document
                    )

                logger.info(
                    f"Document deleted: "
                    f"{selected_document}"
                )

                st.rerun()

            else:

                st.warning(
                    "Document could not be deleted."
                )

        # -----------------------------
        # Clear All Documents
        # -----------------------------

        confirm_clear = st.checkbox(
            "I want to clear all documents",
            key="confirm_clear"
        )

        if st.button(
            "🧹 Clear All Documents",
            key="clear_all"
        ):

            if confirm_clear:

                cleared = clear_all_documents()

                if cleared:

                    st.session_state.messages = []

                    st.session_state.active_document = None

                    st.session_state.processed_documents = []

                    logger.info(
                        "All documents cleared from ChromaDB."
                    )

                    st.rerun()

                else:

                    st.warning(
                        "No documents found."
                    )

            else:

                st.warning(
                    "Please confirm before clearing all documents."
                )

    else:

        st.caption(
            "No documents processed yet."
        )

    st.divider()

    # -----------------------------
    # How it works
    # -----------------------------

    st.subheader("⚙️ How DocuMind Works")

    st.caption(
        "1. Upload a PDF or DOCX\n\n"
        "2. Process the document\n\n"
        "3. Select a document\n\n"
        "4. Ask questions\n\n"
        "5. Get AI-powered answers with sources"
    )
    st.divider()

    st.subheader("🟢 System Status")

    st.caption(
    "Document processing: Ready"
)

    st.caption(
    "Vector database: Connected"
)

    st.caption(
    "RAG pipeline: Ready"
)

    st.caption(
    "AI assistant: Available"
)

    st.divider()

    st.caption(
        "Built with Python • Streamlit • RAG • Gemini"
    )


# -----------------------------
# Document Processing
# -----------------------------

if uploaded_file:

    st.info(
        f"📄 Selected: **{uploaded_file.name}**"
    )

    # Check ChromaDB instead of only session state

    available_documents = get_all_sources()

    if uploaded_file.name in available_documents:

        st.info(
            "ℹ️ This document has already been processed. "
            "You can select it from the Documents section."
        )

    else:

        if st.button(
            "Process Document",
            key="process_document"
        ):

            os.makedirs(
                "data/uploads",
                exist_ok=True
            )

            file_path = os.path.join(
                "data/uploads",
                uploaded_file.name
            )

            with open(
                file_path,
                "wb"
            ) as file:

                file.write(
                    uploaded_file.getbuffer()
                )

            with st.spinner(
                "📄 Processing document..."
            ):

                # -----------------------------
                # Extract text
                # -----------------------------

                if uploaded_file.name.lower().endswith(".pdf"):

                    pages = extract_text_from_pdf(
                        file_path
                    )

                elif uploaded_file.name.lower().endswith(".docx"):

                    pages = extract_text_from_docx(
                        file_path
                    )

                else:

                    pages = []

                # -----------------------------
                # Split text
                # -----------------------------

                chunks = split_text(
                    pages,
                    uploaded_file.name
                )

                # -----------------------------
                # Check extracted content
                # -----------------------------

                if not chunks:

                    st.error(
                        "❌ No readable text was found "
                        "in this document."
                    )

                    st.stop()

                # -----------------------------
                # Create embeddings
                # -----------------------------

                texts = [
                    chunk["text"]
                    for chunk in chunks
                ]

                embeddings = create_embeddings(
                    texts
                )

                # -----------------------------
                # Store in ChromaDB
                # -----------------------------

                add_chunks(
                    chunks,
                    embeddings
                )

            # -----------------------------
            # Update session state
            # -----------------------------

            if uploaded_file.name not in st.session_state.processed_documents:

                st.session_state.processed_documents.append(
                    uploaded_file.name
                )

            st.session_state.active_document = (
                uploaded_file.name
            )

            logger.info(
                f"Document processed: "
                f"{uploaded_file.name} | "
                f"Pages: {len(pages)} | "
                f"Chunks: {len(chunks)}"
            )

            st.success(
              f"✅ **{uploaded_file.name}** processed successfully!"
            )

            st.info(
              f"📄 **Pages:** {len(pages)}  &nbsp;&nbsp;|&nbsp;&nbsp; "
              f"🧩 **Chunks:** {len(chunks)}"
            )

            st.rerun()


# -----------------------------
# Display Previous Messages
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message("user", avatar="👤"):

     st.markdown(
        message["question"]
    )

    with st.chat_message("assistant", avatar="🤖"):

     st.markdown(
        message["answer"]
    )

    if message["sources"]:

         st.markdown("##### 📚 Sources")

         for source in message["sources"]:

          st.info(
            f"📄 **{source['source']}**  •  "
            f"Page {source['page']}"
        )


# -----------------------------
# Chat Input
# -----------------------------

question = st.chat_input(
    "💬 Ask a question about your document..."
)


if question:

    if not st.session_state.active_document:

        st.warning(
            "📄 Please upload and process a document "
            "before asking a question."
        )

        st.stop()

    logger.info(
        f"Question asked: {question} | "
        f"Document: {st.session_state.active_document}"
    )

    # -----------------------------
    # Build conversation history
    # -----------------------------

    conversation_history = ""

    for message in st.session_state.messages:

        conversation_history += (
            f"User: {message['question']}\n"
            f"Assistant: {message['answer']}\n"
        )

    # -----------------------------
    # Generate answer
    # -----------------------------

    with st.spinner(
        "🤖 Thinking..."
    ):

        answer, sources = answer_question(
            question,
            conversation_history,
            source=st.session_state.active_document
        )

    # -----------------------------
    # Store conversation
    # -----------------------------

    st.session_state.messages.append(
        {
            "question": question,
            "answer": answer,
            "sources": sources
        }
    )

    # -----------------------------
    # Log interaction
    # -----------------------------

    logger.info(
        f"Answer generated | "
        f"Question: {question} | "
        f"Sources: {sources}"
    )

    st.rerun()