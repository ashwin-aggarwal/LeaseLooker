# LeaseLooker - Hybrid RAG Lease Analyzer

A powerful Streamlit web application that uses Hybrid RAG (Retrieval-Augmented Generation) to analyze lease agreements. Combines semantic search (FAISS) and keyword search (BM25) for accurate, contextual answers about your lease.

## 🚀 Features

- **Hybrid RAG System**: Combines FAISS (semantic) + BM25 (keyword) retrieval
- **Interactive Chat Interface**: Ask questions in natural language
- **Source Citations**: Every answer includes page references
- **Conversation History**: Maintains context across questions
- **Drag & Drop Upload**: Easy PDF upload interface
- **Real-time Processing**: See progress as your lease is analyzed

## 🏗️ Architecture

```
User Question
     ↓
Hybrid Retriever (30% BM25 + 70% FAISS)
     ↓
Top 3 Relevant Chunks
     ↓
GPT-3.5-Turbo (with context)
     ↓
Answer + Page Citations
```

## 📋 Prerequisites

- Python 3.8+
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/ashwin-aggarwal/LeaseLooker.git
cd LeaseLooker
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 🎯 Usage

### Streamlit App (Recommended)

1. **Start the app**
```bash
streamlit run app.py
```

2. **Open in browser**
   - The app will automatically open at `http://localhost:8501`

3. **Use the app**
   - Enter your OpenAI API key in the sidebar
   - Upload a lease PDF
   - Click "Process Lease"
   - Ask questions about your lease!

### Command Line Interface

You can also use the RAG system directly from the command line:

```bash
# Basic query
python lease_rag.py path/to/lease.pdf "How much is the rent?"

# Without a specific question (defaults to "How much is the rent?")
python lease_rag.py path/to/lease.pdf
```

## 💡 Example Questions

- "How much is the rent?"
- "What is the security deposit?"
- "Can I have pets?"
- "What are the late fee charges?"
- "How much notice is required to terminate?"
- "Who is responsible for repairs?"
- "Is subletting allowed?"
- "What utilities are included?"

## 🧪 How It Works

### 1. Document Processing
```python
# Load PDF and split into chunks
loader = PyPDFLoader(pdf_path)
pages = loader.load()

# Chunk with overlap for context
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=250,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(pages)
```

### 2. Hybrid Retrieval Setup
```python
# Semantic search with FAISS
vectorstore = FAISS.from_documents(chunks, OpenAIEmbeddings())
faiss_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Keyword search with BM25
bm25_retriever = BM25Retriever.from_documents(chunks)
bm25_retriever.k = 3

# Combine: 30% BM25, 70% FAISS
hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, faiss_retriever],
    weights=[0.3, 0.7]
)
```

### 3. Question Answering
```python
# Create chain with context-aware prompt
prompt = ChatPromptTemplate.from_template(template)
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Retrieve and generate
retriever_chain = create_retrieval_chain(hybrid_retriever, document_chain)
response = retriever_chain.invoke({"input": question})
```

## 📊 Technical Details

- **Chunk Size**: 250 characters (optimized for lease clauses)
- **Chunk Overlap**: 50 characters (maintains context)
- **Retrieval**: Top 3 chunks from each method
- **Model**: GPT-3.5-Turbo (fast, cost-effective)
- **Embedding**: OpenAI text-embedding-ada-002

## 🎨 Customization

### Adjust Retrieval Weights
In `lease_rag.py`, modify the weights:
```python
hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, faiss_retriever],
    weights=[0.3, 0.7]  # Adjust these values
)
```

### Change Chunk Size
```python
rag = LeaseRAG(
    pdf_path, 
    chunk_size=500,      # Larger chunks
    chunk_overlap=100    # More overlap
)
```

### Use Different Model
```python
llm = ChatOpenAI(
    model_name="gpt-4",  # More powerful
    temperature=0
)
```
┌─────────────────┐
│   User Upload   │
│      (PDF)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PDF Chunking   │
│   (250 chars)   │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐  ┌───────┐
│ FAISS │  │ BM25  │
│ (70%) │  │ (30%) │
└───┬───┘  └───┬───┘
    │          │
    └────┬─────┘
         ▼
┌─────────────────┐
│ Ensemble (Top 3)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  GPT-3.5-Turbo  │
│   + Context     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Answer + Pages  │
└─────────────────┘

## 🔒 Privacy & Security

- **API Key**: Never committed to code, entered via UI
- **Local Processing**: PDF processing happens locally
- **No Data Storage**: Files are temporary and deleted after processing
- **OpenAI API**: Only text chunks sent, not full PDF

## 📁 Project Structure

```
LeaseLooker/
├── app.py                  # Streamlit web interface
├── lease_rag.py           # Core RAG system
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .gitignore           # Git ignore rules
```

## 🐛 Troubleshooting

### "OPENAI_API_KEY not set"
- Make sure you've entered your API key in the sidebar
- Check that the key is valid at platform.openai.com

### "Failed to load PDF"
- Ensure PDF is not password-protected
- Check file isn't corrupted
- Try a different PDF viewer to verify

### "Out of memory"
- Reduce chunk_size parameter
- Process smaller PDFs
- Close other applications

### BM25 Installation Issues
```bash
pip install rank_bm25 --upgrade
```

## 🚦 Performance

- **Processing**: ~2-5 seconds for typical lease (10-30 pages)
- **Query Time**: ~1-3 seconds per question
- **Memory**: ~200-500 MB depending on PDF size

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - feel free to use for personal or commercial projects

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Vector search powered by [FAISS](https://github.com/facebookresearch/faiss)
- Keyword search using [BM25](https://en.wikipedia.org/wiki/Okapi_BM25)
- UI built with [Streamlit](https://streamlit.io/)

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check existing issues for solutions
