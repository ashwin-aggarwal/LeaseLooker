# LeaseLooker 🏠

AI-Powered Lease Agreement Analyzer using Hybrid RAG (Retrieval-Augmented Generation)

## 🎯 What It Does

Upload your lease PDF, ask questions in plain English, get instant answers with page citations. No more scrolling through pages to find what you need!

**Example Questions:**
- "How much is the rent?"
- "Can I have pets?"
- "What are the late fees?"
- "How do I terminate the lease?"

## 🏗️ Architecture

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
```

### How Hybrid RAG Works

**FAISS (70%)** - Semantic search that understands meaning
- "monthly payment" → finds rent information
- Uses AI embeddings to understand context

**BM25 (30%)** - Keyword search for exact matches  
- "deposit" → finds all deposit mentions
- Traditional but precise

**Combined** - Best of both worlds!
- Get accurate answers even with different wording
- Never miss important exact terms

## 🚀 Quick Start

### Option 1: Run Locally

```bash
# Clone the repo
git clone https://github.com/ashwin-aggarwal/LeaseLooker.git
cd LeaseLooker

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app_simple.py
```

Open http://localhost:8501 and start analyzing!

### Option 2: Deploy to Cloud (FREE!)

[![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" → Select your repo
4. Set main file to `app_simple.py`
5. Deploy!

See [DEPLOY_STREAMLIT_CLOUD.md](DEPLOY_STREAMLIT_CLOUD.md) for detailed instructions.

### Option 3: Docker

```bash
# Build and run
docker-compose up

# Or manually
docker build -t leaselooker .
docker run -p 8501:8501 -e OPENAI_API_KEY='your-key' leaselooker
```

## 📦 Features

- ✅ **Hybrid RAG** - Combines FAISS semantic search (70%) + BM25 keyword search (30%)
- ✅ **Smart Chunking** - Intelligent text splitting with context preservation
- ✅ **Page Citations** - Every answer includes source page numbers
- ✅ **Simple UI** - Clean, intuitive Streamlit interface
- ✅ **No Storage** - Files processed in memory, not saved
- ✅ **Fast** - 2-5 seconds to process typical lease, 1-3 seconds per query

## 💡 Usage

1. **Enter your OpenAI API key** (in sidebar)
2. **Upload a lease PDF** (drag & drop)
3. **Click "Process Lease"**
4. **Ask questions!**

The system will:
- Find relevant sections in your lease
- Generate clear answers
- Show you exactly where it found the information

## 🧪 Example

```bash
# Test the RAG system directly
python debug_query.py ./data/Lease2.pdf "How much is the rent?"
```

Output:
```
Answer: The rent is TWENTY-TWO THOUSAND PESOS (PhP22,000.00) per month. (Page 4)

Sources (5 found):
[Source 1] Page 1: The next monthly payment for the house rental...
```

## 📁 Project Structure

```
LeaseLooker/
├── app_simple.py          # Main Streamlit app (recommended)
├── app.py                 # Advanced UI version
├── lease_rag.py          # Core hybrid RAG system
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker container
├── docker-compose.yml    # Docker setup
│
├── tests/
│   ├── test_rag.py       # Automated tests
│   ├── debug_query.py    # Debug utility
│   └── test_components.py # Component tests
│
└── docs/
    ├── QUICKSTART.md
    ├── TROUBLESHOOTING.md
    ├── DEPLOYMENT.md
    └── DEPLOY_STREAMLIT_CLOUD.md
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Adjust chunk size
CHUNK_SIZE = 250  # Characters per chunk

# Change retrieval weights
BM25_WEIGHT = 0.3  # Keyword search (30%)
FAISS_WEIGHT = 0.7 # Semantic search (70%)

# Use different model
MODEL_NAME = "gpt-4"  # More powerful but slower/expensive
```

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **RAG Framework:** LangChain (with langchain_classic)
- **Vector Store:** FAISS
- **Keyword Search:** BM25 (rank-bm25)
- **LLM:** OpenAI GPT-3.5-Turbo
- **PDF Processing:** PyPDF

## 💰 Cost Estimate

Based on OpenAI pricing:
- Processing a 20-page lease: ~$0.05
- Each question: ~$0.01
- **Typical session: $0.10-0.25**

Very affordable! Users can enter their own API keys.

## 🐛 Troubleshooting

### "ModuleNotFoundError: langchain_classic"
```bash
pip install langchain_classic
```

### "Error processing lease"
Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions.

### Run diagnostics
```bash
python test_components.py
```

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues & solutions
- **[DEPLOY_STREAMLIT_CLOUD.md](DEPLOY_STREAMLIT_CLOUD.md)** - Free cloud deployment
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - AWS, Docker, and other options

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

Built with:
- [LangChain](https://langchain.com/) - RAG framework
- [FAISS](https://github.com/facebookresearch/faiss) - Vector similarity search
- [Streamlit](https://streamlit.io/) - Web interface
- [OpenAI](https://openai.com/) - Language models

## 🔗 Links

- **Live Demo:** (Deploy to get your link!)
- **Report Issues:** [GitHub Issues](https://github.com/ashwin-aggarwal/LeaseLooker/issues)
- **Discussions:** [GitHub Discussions](https://github.com/ashwin-aggarwal/LeaseLooker/discussions)

---

**Made with ❤️ for renters everywhere**

Star ⭐ this repo if you find it helpful!