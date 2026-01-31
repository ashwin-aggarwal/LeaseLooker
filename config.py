"""
Configuration file for LeaseLooker RAG System
Modify these settings to customize behavior
"""

# ====================================
# DOCUMENT PROCESSING SETTINGS
# ====================================

# Text chunking configuration
CHUNK_SIZE = 250  # Characters per chunk
CHUNK_OVERLAP = 50  # Overlap between chunks (maintains context)

# Text splitting separators (in order of preference)
SEPARATORS = ["\n\n", "\n", ". ", " ", ""]

# ====================================
# RETRIEVAL SETTINGS
# ====================================

# Number of chunks to retrieve
NUM_CHUNKS = 3

# Hybrid retriever weights (must sum to 1.0)
BM25_WEIGHT = 0.3  # Keyword search weight
FAISS_WEIGHT = 0.7  # Semantic search weight

# ====================================
# LLM SETTINGS
# ====================================

# Model configuration
MODEL_NAME = "gpt-3.5-turbo"  # Options: gpt-3.5-turbo, gpt-4, gpt-4-turbo
TEMPERATURE = 0  # 0 = deterministic, 1 = creative

# Response length
MAX_RESPONSE_SENTENCES = 5  # Maximum sentences in answer

# ====================================
# PROMPT TEMPLATE
# ====================================

PROMPT_TEMPLATE = """Answer the question based ONLY on the context below.
For every fact, you MUST cite the Page Number found in the metadata.
Try to answer in a concise manner. No more than {max_sentences} sentences.

Context:
{context}

Question: {input}
Answer:"""

# ====================================
# STREAMLIT UI SETTINGS
# ====================================

# Page configuration
PAGE_TITLE = "LeaseLooker - AI Lease Analyzer"
PAGE_ICON = "📄"
LAYOUT = "wide"

# File upload settings
MAX_FILE_SIZE_MB = 200
ALLOWED_EXTENSIONS = ['pdf']

# ====================================
# SAMPLE QUESTIONS
# ====================================

SAMPLE_QUESTIONS = [
    "How much is the rent?",
    "What is the security deposit?",
    "Can I have pets?",
    "What are the late fee charges?",
    "How much notice is required to terminate?",
    "Who is responsible for repairs?",
    "Is subletting allowed?",
    "What utilities are included?",
    "Is renters insurance required?",
    "What are the parking rules?",
]

# ====================================
# ADVANCED SETTINGS
# ====================================

# Embedding model
EMBEDDING_MODEL = "text-embedding-ada-002"

# Timeout settings
PROCESSING_TIMEOUT = 300  # seconds (5 minutes)

# Cache settings
ENABLE_CACHE = True

# Debug mode
DEBUG = False  # Set to True for verbose output