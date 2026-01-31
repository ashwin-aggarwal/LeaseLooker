"""
Test script for LeaseRAG system
Run this to verify your installation and test the hybrid RAG
"""

import os
import sys
from lease_rag import LeaseRAG


def test_rag_system(pdf_path: str):
    """
    Test the RAG system with a series of questions.
    
    Args:
        pdf_path: Path to a test PDF lease
    """
    
    print("=" * 70)
    print("LEASELOOKER - HYBRID RAG TEST")
    print("=" * 70)
    
    # Check API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("\n❌ ERROR: OPENAI_API_KEY not set!")
        print("\nPlease set your API key:")
        print("  export OPENAI_API_KEY='sk-...'  # Linux/Mac")
        print("  set OPENAI_API_KEY=sk-...       # Windows")
        sys.exit(1)
    
    print("\n✅ API Key found")
    
    # Initialize RAG system
    print(f"\n📄 Loading lease: {pdf_path}")
    print("-" * 70)
    
    try:
        rag = LeaseRAG(pdf_path)
        print("✅ RAG system initialized successfully!")
    except Exception as e:
        print(f"\n❌ ERROR initializing RAG system:")
        print(f"   {str(e)}")
        sys.exit(1)
    
    # Display stats
    stats = rag.get_stats()
    print(f"\n📊 Document Statistics:")
    print(f"   - Total chunks: {stats['num_chunks']}")
    print(f"   - Chunk size: {stats['chunk_size']} characters")
    print(f"   - Chunk overlap: {stats['chunk_overlap']} characters")
    
    # Test questions
    test_questions = [
        "How much is the rent?",
        "What is the security deposit?",
        "Can I have pets?",
        "What are the late fees?",
        "How much notice is required to terminate the lease?"
    ]
    
    print("\n" + "=" * 70)
    print("RUNNING TEST QUERIES")
    print("=" * 70)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n[{i}/{len(test_questions)}] Question: {question}")
        print("-" * 70)
        
        try:
            response = rag.query(question)
            
            print(f"\n💡 Answer:")
            print(f"   {response['answer']}")
            
            print(f"\n📚 Sources: {len(response['sources'])} chunks retrieved")
            for j, source in enumerate(response['sources'], 1):
                page = source.get('page', 'Unknown')
                content_preview = source['content'][:100].replace('\n', ' ')
                print(f"   [{j}] Page {page}: {content_preview}...")
                
        except Exception as e:
            print(f"\n❌ ERROR processing question:")
            print(f"   {str(e)}")
            continue
        
        print()
    
    print("=" * 70)
    print("TEST COMPLETE!")
    print("=" * 70)
    print("\n✅ All systems operational!")
    print("\nNext steps:")
    print("  1. Run: streamlit run app.py")
    print("  2. Upload your lease PDF")
    print("  3. Start asking questions!")


def interactive_mode(pdf_path: str):
    """
    Interactive question-answering mode.
    
    Args:
        pdf_path: Path to a PDF lease
    """
    print("\n" + "=" * 70)
    print("INTERACTIVE MODE")
    print("=" * 70)
    print("\nInitializing RAG system...")
    
    rag = LeaseRAG(pdf_path)
    
    print("\n✅ Ready! Type 'quit' to exit.")
    print("\nSample questions:")
    print("  - How much is the rent?")
    print("  - What is the security deposit?")
    print("  - Can I have pets?")
    print("  - What are the late fees?")
    
    while True:
        print("\n" + "-" * 70)
        question = input("\n❓ Your question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not question:
            continue
        
        try:
            response = rag.query(question)
            
            print(f"\n💡 Answer:")
            print(f"{response['answer']}")
            
            print(f"\n📚 Sources ({len(response['sources'])} chunks):")
            for i, source in enumerate(response['sources'], 1):
                print(f"\n  Source {i} (Page {source.get('page', 'Unknown')}):")
                print(f"  {source['content'][:200]}...")
                
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python test_rag.py <pdf_path>              # Run automated tests")
        print("  python test_rag.py <pdf_path> --interactive # Interactive Q&A")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if not os.path.exists(pdf_path):
        print(f"❌ ERROR: File not found: {pdf_path}")
        sys.exit(1)
    
    # Check for interactive mode
    if len(sys.argv) > 2 and sys.argv[2] == '--interactive':
        interactive_mode(pdf_path)
    else:
        test_rag_system(pdf_path)