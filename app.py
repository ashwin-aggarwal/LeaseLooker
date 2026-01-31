import streamlit as st
import os
from LeaseRAG import LeaseRAG
import tempfile

# Page configuration
st.set_page_config(
    page_title="LeaseLooker - AI Lease Analyzer",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-size: 1.1rem;
        padding: 0.75rem;
        border-radius: 0.5rem;
    }
    .answer-box {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .source-box {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'pdf_processed' not in st.session_state:
    st.session_state.pdf_processed = False

# Header
st.markdown('<div class="main-header">🏠 LeaseLooker</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Lease Agreement Analyzer with Hybrid RAG</div>', unsafe_allow_html=True)

# Sidebar for PDF upload
with st.sidebar:
    st.header("📁 Upload Lease")
    
    # API Key input
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key. Get one at https://platform.openai.com/api-keys"
    )
    
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload a lease agreement PDF (max 200MB)"
    )
    
    # Process PDF button
    if uploaded_file and api_key:
        if st.button("🚀 Process Lease"):
            with st.spinner("Processing your lease agreement..."):
                try:
                    # Save uploaded file to temporary location
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    # Initialize RAG system
                    st.session_state.rag_system = LeaseRAG(tmp_path)
                    st.session_state.pdf_processed = True
                    st.session_state.chat_history = []
                    
                    # Clean up temp file
                    os.unlink(tmp_path)
                    
                    st.success("✅ Lease processed successfully!")
                    st.info(f"📊 Created {st.session_state.rag_system.num_chunks} chunks from your lease")
                    
                except Exception as e:
                    st.error(f"❌ Error processing lease: {str(e)}")
                    st.session_state.pdf_processed = False
    
    elif uploaded_file and not api_key:
        st.warning("⚠️ Please enter your OpenAI API key to process the lease.")
    
    # Info section
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This app uses **Hybrid RAG** combining:
    - 🔍 **Semantic Search** (FAISS)
    - 📝 **Keyword Search** (BM25)
    
    Ask questions about:
    - Rent & fees
    - Lease terms & dates
    - Policies & rules
    - Maintenance & repairs
    - Termination clauses
    """)
    
    # Sample questions
    st.markdown("---")
    st.markdown("### 💡 Sample Questions")
    sample_questions = [
        "How much is the rent?",
        "What is the security deposit?",
        "Can I have pets?",
        "What are the late fee charges?",
        "How much notice is required to terminate?",
        "Who is responsible for repairs?",
        "Is subletting allowed?",
        "What utilities are included?"
    ]
    
    for q in sample_questions:
        if st.button(q, key=f"sample_{q}"):
            if st.session_state.pdf_processed:
                st.session_state.current_question = q

# Main content area
if not st.session_state.pdf_processed:
    # Welcome screen
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("""
        ### 👋 Welcome to LeaseLooker!
        
        Get started by:
        1. 🔑 Entering your OpenAI API key in the sidebar
        2. 📄 Uploading a lease agreement PDF
        3. 🚀 Clicking "Process Lease"
        4. 💬 Asking questions about your lease
        
        **Powered by Hybrid RAG Technology**
        - Combines semantic understanding with keyword matching
        - Provides accurate answers with page citations
        - Maintains conversation context
        """)

else:
    # Chat interface
    st.markdown("### 💬 Ask Questions About Your Lease")
    
    # Display chat history
    for i, (question, answer, sources) in enumerate(st.session_state.chat_history):
        # Question
        with st.chat_message("user"):
            st.write(question)
        
        # Answer
        with st.chat_message("assistant"):
            st.write("**Answer:**")
            st.write(answer)
            
            st.write("")
            st.write("**Sources:**")
            
            for j, source in enumerate(sources, 1):
                st.write(f"**Source {j}** - Page {source['page']}")
                st.text(source['content'][:200] + "...")
                st.write("---")
    
    # Input for new question
    user_question = st.chat_input("Ask a question about your lease...")
    
    # Handle sample question click
    if 'current_question' in st.session_state:
        user_question = st.session_state.current_question
        del st.session_state.current_question
    
    if user_question:
        # Display user question
        with st.chat_message("user"):
            st.write(user_question)
        
        # Get answer from RAG system
        with st.chat_message("assistant"):
            with st.spinner("Searching through your lease..."):
                try:
                    response = st.session_state.rag_system.query(user_question)
                    answer = response['answer']
                    sources = response['sources']
                    
                    # Simple text display - no fancy formatting
                    st.write("**Answer:**")
                    st.write(answer)
                    
                    st.write("")
                    st.write("**Sources:**")
                    
                    for i, source in enumerate(sources, 1):
                        st.write(f"**Source {i}** - Page {source['page']}")
                        st.text(source['content'][:200] + "...")
                        st.write("---")
                    
                    # Add to chat history
                    st.session_state.chat_history.append((user_question, answer, sources))
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    # Show raw response for debugging
                    with st.expander("🔍 Debug Info (click to expand)"):
                        st.write("**Error Details:**")
                        st.code(str(e))
                        if hasattr(st.session_state.rag_system, 'retriever_chain'):
                            st.write("✅ Retriever chain exists")
                        else:
                            st.write("❌ Retriever chain missing")
                        st.write(f"**Number of chunks:** {st.session_state.rag_system.num_chunks}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    Built with ❤️ using Streamlit, LangChain, FAISS, and BM25<br>
    Hybrid RAG: Semantic + Keyword Search for Accurate Answers
</div>
""", unsafe_allow_html=True)