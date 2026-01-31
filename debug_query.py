"""
Debug script to test the RAG system and see exact responses
"""

import os
import sys

# Set debug mode
os.environ['DEBUG'] = 'True'

# Check if PDF path provided
if len(sys.argv) < 2:
    print("Usage: python debug_query.py <pdf_path> [question]")
    sys.exit(1)

pdf_path = sys.argv[1]
question = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "How much is the rent?"

print("=" * 70)
print("DEBUG SCRIPT - Testing RAG System")
print("=" * 70)

# Check API key
if not os.environ.get('OPENAI_API_KEY'):
    print("\n❌ ERROR: OPENAI_API_KEY not set!")
    print("\nSet it with:")
    print("  export OPENAI_API_KEY='sk-...'")
    sys.exit(1)

print(f"\n✅ API Key found: {os.environ['OPENAI_API_KEY'][:20]}...")
print(f"📄 PDF: {pdf_path}")
print(f"❓ Question: {question}")

# Import and initialize
print("\n" + "-" * 70)
print("Initializing RAG system...")
print("-" * 70)

try:
    from LeaseRAG import LeaseRAG
    rag = LeaseRAG(pdf_path)
    print(f"✅ RAG system initialized with {rag.num_chunks} chunks")
except Exception as e:
    print(f"❌ Error initializing: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Run query
print("\n" + "-" * 70)
print("Running query...")
print("-" * 70)

try:
    response = rag.query(question)
    
    print("\n✅ Query successful!")
    print("\n" + "=" * 70)
    print("RESPONSE STRUCTURE:")
    print("=" * 70)
    print(f"\nKeys in response: {list(response.keys())}")
    
    print("\n" + "-" * 70)
    print("ANSWER:")
    print("-" * 70)
    print(f"\n{response['answer']}\n")
    
    print("-" * 70)
    print(f"SOURCES ({len(response['sources'])} found):")
    print("-" * 70)
    for i, source in enumerate(response['sources'], 1):
        print(f"\n[Source {i}] Page {source['page']}")
        print(f"{source['content'][:200]}...\n")
    
    print("-" * 70)
    print("RAW RESPONSE:")
    print("-" * 70)
    print(response['raw_response'])
    
except Exception as e:
    print(f"\n❌ Error during query: {e}")
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()
    
    # Try to get more info
    print("\n" + "-" * 70)
    print("DEBUGGING INFO:")
    print("-" * 70)
    print(f"Retriever chain exists: {rag.retriever_chain is not None}")
    print(f"Number of chunks: {rag.num_chunks}")
    
    # Try a direct invoke to see raw response
    try:
        print("\nAttempting direct invoke...")
        raw = rag.retriever_chain.invoke({"input": question})
        print(f"Raw response keys: {list(raw.keys())}")
        print(f"Raw response: {raw}")
    except Exception as e2:
        print(f"Direct invoke also failed: {e2}")