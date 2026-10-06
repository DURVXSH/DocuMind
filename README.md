# 📄 DocuMind — AI Document Intelligence Assistant

DocuMind is an AI-powered document question-answering application that allows users to upload PDF and DOCX documents and ask questions about their content using natural language.

It uses a **Retrieval-Augmented Generation (RAG)** pipeline to retrieve relevant information from uploaded documents before generating answers with Gemini.

The system is designed to provide **grounded answers with document and page citations** while reducing hallucinations.

---

## 🚀 Features

- 📄 Upload PDF and DOCX documents
- ✂️ Automatic text extraction and chunking
- 🧠 Semantic embeddings using Sentence Transformers
- 🔍 Similarity-based document retrieval
- 🗃️ Persistent vector storage using ChromaDB
- 🤖 Gemini-powered answer generation
- 📚 Source and page citations
- 💬 Conversation memory for follow-up questions
- 🛡️ Hallucination protection
- 📂 Multiple document support
- 🗑️ Delete individual documents
- 🧹 Clear all stored documents
- 📝 Application logging
- 🧪 Retrieval and robustness evaluation
- 🌐 Streamlit web interface

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │    PDF / DOCX       │
                    │      Document       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Text Extraction   │
                    │    PyPDF / DOCX     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Text Chunking    │
                    │  Size: 700 chars    │
                    │ Overlap: 150 chars  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Embeddings      │
                    │ MiniLM-L6-v2        │
                    │   384 dimensions    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      ChromaDB       │
                    │    Vector Store     │
                    └──────────┬──────────┘
                               │
                         User Question
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Retriever       │
                    │ Semantic + Keyword  │
                    │      Matching       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Gemini        │
                    │   Answer Generation │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Grounded Answer +   │
                    │ Source/Page Citation│
                    └─────────────────────┘
```

---

## 🔄 How It Works

### 1. Document Upload

The user uploads a PDF or DOCX file through the Streamlit interface.

### 2. Text Extraction

Text is extracted from each document.

For PDFs, page information is preserved so that answers can reference the correct page.

### 3. Text Chunking

Large documents are divided into smaller chunks.

DocuMind currently uses:

- Chunk size: **700 characters**
- Overlap: **150 characters**

The overlap helps preserve context between neighboring chunks.

### 4. Embedding Generation

Each chunk is converted into a numerical vector using:

**`all-MiniLM-L6-v2`**

The resulting embeddings contain **384 dimensions**.

### 5. Vector Storage

The embeddings and their metadata are stored in **ChromaDB**.

Each chunk contains metadata such as:

```text
Source filename
Page number
```

### 6. Question Retrieval

When the user asks a question, DocuMind:

1. Converts the question into an embedding.
2. Searches ChromaDB for similar chunks.
3. Applies relevance filtering.
4. Retrieves the most relevant document information.

### 7. Answer Generation

The retrieved information is passed to Gemini along with the user's question and conversation history.

Gemini is instructed to answer only from the provided document context.

### 8. Source Citation

Answers can include citations such as:

```text
[Source: Durvesh_Res.pdf, Page: 1]
```

This allows users to trace the answer back to the original document.

---

## 🛡️ Hallucination Protection

DocuMind is designed to reduce unsupported AI-generated answers.

The model is instructed to:

- Use only retrieved document context.
- Avoid inventing information.
- Avoid creating fake page numbers.
- Avoid creating fake filenames.
- State when information cannot be found.

For example, if a user asks something that does not exist in the document, DocuMind can respond:

> I could not find this information in the document.

---

## 💬 Conversation Memory

DocuMind supports follow-up questions.

For example:

```text
User:
What is the candidate's CGPA?

Assistant:
The candidate's CGPA is 8.70/10.

User:
What is their highest education?

Assistant:
The candidate's highest education is Bachelor of Technology.
```

The previous conversation is passed to the RAG pipeline to help understand follow-up questions.

---

## 🧪 Evaluation

DocuMind includes an evaluation suite for testing retrieval and answer reliability.

Current evaluation tests include:

- Highest education
- Technical skills
- CGPA
- Unanswerable question

Current evaluation results:

| Metric | Result |
|---|---:|
| Retrieval Accuracy | 100% |
| Page Accuracy | 100% |
| Hallucination Protection | 100% |

The evaluation dataset currently contains **4 questions**, including one deliberately unanswerable question.

---

## 🧪 Robustness Testing

The project has also been tested against several edge cases:

- Empty documents
- Empty pages
- Basic PDF extraction
- Large documents
- Conversation memory
- Single-document deletion
- Clear-all functionality
- Multiple document retrieval
- Chunk size validation

Large-document testing successfully processed approximately **360,000 characters into 655 chunks**, while maintaining the configured chunk-size limit.

---

## 🛠️ Tech Stack

### Programming Language

- Python

### AI / Machine Learning

- Google Gemini
- Sentence Transformers
- `all-MiniLM-L6-v2`

### Retrieval / Vector Database

- ChromaDB

### Document Processing

- PyPDF
- python-docx

### Application

- Streamlit

### Data / Utilities

- NumPy
- python-dotenv

### Development Tools

- Git
- GitHub
- VS Code

---

## 📁 Project Structure

```text
DocuMind/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── .streamlit/
│   └── config.toml
│
├── src/
│   ├── embeddings.py
│   ├── llm.py
│   ├── logger.py
│   ├── memory.py
│   ├── pdf_loader.py
│   ├── rag_pipeline.py
│   ├── retriever.py
│   ├── text_splitter.py
│   └── vector_store.py
│
├── tests/
│   └── evaluation_questions.py
│
├── data/
│   ├── uploads/
│   └── chroma_db/
│
└── logs/
    └── documind.log
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd DocuMind
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure Gemini API

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key_here
```

Do not commit the `.env` file to GitHub.

### 6. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

---

## 🔐 Environment Variables

DocuMind requires:

```text
GEMINI_API_KEY
```

The API key should be stored in `.env`.

Example:

```text
GEMINI_API_KEY=your_api_key_here
```

---

## 📌 Important Notes

### DOCX Page Numbers

DOCX files are currently treated as a single logical page because `python-docx` does not provide reliable rendered page-number information.

### Gemini API

Answer generation requires a valid Gemini API key and available API quota.

### Local Vector Database

ChromaDB is stored locally in:

```text
data/chroma_db/
```

The vector database is intentionally excluded from GitHub.

---

## 🎯 Future Improvements

Possible future improvements include:

- 🔐 User authentication
- 📑 Better DOCX page-level citations
- 📊 Retrieval evaluation dashboard
- ⚡ Streaming AI responses
- 🔎 Improved hybrid retrieval
- 🧠 Reranking models
- 📈 Usage analytics
- 🐳 Docker deployment
- ☁️ Cloud deployment
- 🗂️ Better document metadata management
- 📚 Support for additional file formats
- 🧪 Larger automated evaluation datasets

---

## 👨‍💻 Author

**Durvesh Shelar**

B.Tech — Artificial Intelligence and Data Science

Thakur College of Engineering and Technology, Mumbai

---

## ⭐ Project Goal

DocuMind was built as a practical implementation of **Retrieval-Augmented Generation (RAG)**, combining document processing, embeddings, vector search, LLMs, and a web application into a complete AI system.

The project focuses on building an AI assistant that answers questions from documents while maintaining traceability through source and page citations.
```

