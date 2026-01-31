"""
Lease RAG System - Hybrid Retrieval with FAISS + BM25
Implements semantic search (FAISS) and keyword search (BM25) for lease analysis
"""

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

# Import configuration
try:
    from config import (
        CHUNK_SIZE, CHUNK_OVERLAP, SEPARATORS, NUM_CHUNKS,
        BM25_WEIGHT, FAISS_WEIGHT, MODEL_NAME, TEMPERATURE,
        PROMPT_TEMPLATE, MAX_RESPONSE_SENTENCES, DEBUG
    )
except ImportError:
    # Default values if config.py not found
    CHUNK_SIZE = 250
    CHUNK_OVERLAP = 50
    SEPARATORS = ["\n\n", "\n", ". ", " ", ""]
    NUM_CHUNKS = 3
    BM25_WEIGHT = 0.3
    FAISS_WEIGHT = 0.7
    MODEL_NAME = "gpt-3.5-turbo"
    TEMPERATURE = 0
    MAX_RESPONSE_SENTENCES = 5
    DEBUG = False
    PROMPT_TEMPLATE = """Answer the question based ONLY on the context below.
For every fact, you MUST cite the Page Number found in the metadata.
Try to answer in a concise manner. No more than {max_sentences} sentences.

Context:
{context}

Question: {input}
Answer:"""


class LeaseRAG:
    """
    Hybrid RAG system for lease document analysis.
    Combines FAISS (semantic search) and BM25 (keyword search) for optimal retrieval.
    """
    
    def __init__(self, pdf_path: str, chunk_size: int = None, chunk_overlap: int = None):
        """
        Initialize the LeaseRAG system.
        
        Args:
            pdf_path: Path to the PDF lease document
            chunk_size: Size of text chunks (default from config)
            chunk_overlap: Overlap between chunks (default from config)
        """
        self.pdf_path = pdf_path
        self.chunk_size = chunk_size or CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or CHUNK_OVERLAP
        self.chunks = None
        self.hybrid_retriever = None
        self.retriever_chain = None
        self.num_chunks = 0
        
        # Verify API key
        if not os.environ.get('OPENAI_API_KEY'):
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        # Initialize the system
        self._load_and_chunk_document()
        self._setup_retrievers()
        self._setup_chain()
    
    def _load_and_chunk_document(self):
        """Load PDF and split into chunks."""
        if DEBUG:
            print(f"Loading lease from: {self.pdf_path}")
        
        # Load PDF
        loader = PyPDFLoader(self.pdf_path)
        pages = loader.load()
        
        # Chunk the document
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=SEPARATORS,
            add_start_index=True
        )
        self.chunks = text_splitter.split_documents(pages)
        self.num_chunks = len(self.chunks)
        
        if DEBUG:
            print(f"Created {self.num_chunks} chunks from the lease")
    
    def _setup_retrievers(self):
        """Setup both FAISS and BM25 retrievers, then combine them."""
        if DEBUG:
            print("Setting up hybrid retrieval system...")
        
        # Semantic Search with FAISS
        if DEBUG:
            print("  - Creating FAISS vector store...")
        vectorstore = FAISS.from_documents(
            self.chunks, 
            OpenAIEmbeddings()
        )
        faiss_retriever = vectorstore.as_retriever(search_kwargs={"k": NUM_CHUNKS})
        
        # Keyword Search with BM25
        if DEBUG:
            print("  - Creating BM25 retriever...")
        bm25_retriever = BM25Retriever.from_documents(self.chunks)
        bm25_retriever.k = NUM_CHUNKS
        
        # Hybrid Ensemble Retriever
        if DEBUG:
            print(f"  - Combining retrievers ({BM25_WEIGHT*100}% BM25, {FAISS_WEIGHT*100}% FAISS)...")
        self.hybrid_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, faiss_retriever],
            weights=[BM25_WEIGHT, FAISS_WEIGHT]
        )
        
        if DEBUG:
            print("Hybrid retrieval system ready!")
    
    def _setup_chain(self):
        """Setup the LLM chain for question answering."""
        if DEBUG:
            print("Setting up LLM chain...")
        
        # Create prompt template (matching notebook exactly)
        template = """Answer the question based ONLY on the context below.
For every fact, you MUST cite the Page Number found in the metadata.
Try to answer is a concise manner. No more than 5 sentences.

Context:
{context}

Question: {input}
Answer:"""
        
        prompt = ChatPromptTemplate.from_template(template)
        
        # Create LLM
        llm = ChatOpenAI(model_name=MODEL_NAME, temperature=TEMPERATURE)
        
        # Creating Document Chain for the LLM to process the text
        document_chain = create_stuff_documents_chain(llm, prompt)
        
        # Creating Retrieval Chain
        self.retriever_chain = create_retrieval_chain(self.hybrid_retriever, document_chain)
        
        if DEBUG:
            print("LLM chain ready!")
    
    def query(self, question: str) -> dict:
        """
        Query the lease document.
        
        Args:
            question: The question to ask about the lease
            
        Returns:
            dict with 'answer' and 'sources' keys
        """
        if not self.retriever_chain:
            raise ValueError("RAG system not initialized")
        
        # Run the query (matching notebook exactly)
        response = self.retriever_chain.invoke({"input": question})
        
        # Extract sources with page numbers
        sources = []
        for doc in response.get('context', []):
            sources.append({
                'content': doc.page_content,
                'page': doc.metadata.get('page', 'Unknown'),
                'source': doc.metadata.get('source', 'Unknown')
            })
        
        return {
            'answer': response['answer'],
            'sources': sources,
            'raw_response': response
        }
    
    def get_stats(self) -> dict:
        """Get statistics about the loaded document."""
        return {
            'num_chunks': self.num_chunks,
            'chunk_size': self.chunk_size,
            'chunk_overlap': self.chunk_overlap,
            'pdf_path': self.pdf_path
        }


# Example usage and testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python lease_rag.py <pdf_path> [question]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    # Initialize RAG system
    print("=" * 60)
    print("Initializing Lease RAG System")
    print("=" * 60)
    
    rag = LeaseRAG(pdf_path)
    
    # Print stats
    stats = rag.get_stats()
    print(f"\n📊 Document Stats:")
    print(f"  - Chunks: {stats['num_chunks']}")
    print(f"  - Chunk size: {stats['chunk_size']}")
    print(f"  - Overlap: {stats['chunk_overlap']}")
    
    # Test query
    if len(sys.argv) > 2:
        question = " ".join(sys.argv[2:])
    else:
        question = "How much is the rent?"
    
    print(f"\n❓ Question: {question}")
    print("=" * 60)
    
    response = rag.query(question)
    
    print(f"\n💡 Answer:")
    print(f"{response['answer']}")
    
    print(f"\n📚 Sources ({len(response['sources'])}):")
    for i, source in enumerate(response['sources'], 1):
        print(f"\n  Source {i} (Page {source['page']}):")
        print(f"  {source['content'][:200]}...")