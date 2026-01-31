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

# Initialize session state
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = None
if 'pdf_processed' not in st.session_state:
    st.session_state.pdf_processed = False

# Header
st.title("🏠 LeaseLooker - AI Lease Analyzer")
st.subheader("Ask questions about your lease agreement")

# Sidebar for PDF upload
with st.sidebar:
    st.header("📁 Setup")
    
    # API Key input
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key"
    )
    
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload Lease PDF",
        type=['pdf']
    )
    
    # Process PDF button
    if uploaded_file and api_key:
        if st.button("🚀 Process Lease", use_container_width=True):
            with st.spinner("Processing your lease..."):
                try:
                    # Save uploaded file to temporary location
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    # Initialize RAG system
                    st.session_state.rag_system = LeaseRAG(tmp_path)
                    st.session_state.pdf_processed = True
                    
                    # Clean up temp file
                    os.unlink(tmp_path)
                    
                    st.success("✅ Lease processed!")
                    st.info(f"📊 {st.session_state.rag_system.num_chunks} chunks created")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.session_state.pdf_processed = False
    
    elif uploaded_file and not api_key:
        st.warning("⚠️ Please enter your OpenAI API key")
    
    # Sample questions
    if st.session_state.pdf_processed:
        st.markdown("---")
        st.markdown("### 💡 Quick Questions")
        if st.button("How much is the rent?"):
            st.session_state.quick_question = "How much is the rent?"
        if st.button("What is the security deposit?"):
            st.session_state.quick_question = "What is the security deposit?"
        if st.button("Can I have pets?"):
            st.session_state.quick_question = "Can I have pets?"

# Main content area
if not st.session_state.pdf_processed:
    # Welcome screen
    st.info("""
    ### 👋 Welcome!
    
    1. Enter your OpenAI API key in the sidebar
    2. Upload your lease PDF
    3. Click "Process Lease"
    4. Ask questions!
    """)

else:
    # Question input
    st.markdown("### 💬 Ask a Question")
    
    # Check for quick question
    default_q = ""
    if 'quick_question' in st.session_state:
        default_q = st.session_state.quick_question
        del st.session_state.quick_question
    
    user_question = st.text_input(
        "Type your question:",
        value=default_q,
        placeholder="e.g., How much is the rent?"
    )
    
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        ask_button = st.button("🔍 Ask", use_container_width=True)
    
    if (ask_button or default_q) and user_question:
        with st.spinner("Searching your lease..."):
            try:
                # Get response
                response = st.session_state.rag_system.query(user_question)
                
                st.markdown("---")
                
                # BOX 1: ANSWER
                st.markdown("### 📝 Answer")
                answer_text = response['answer']
                st.info(answer_text)
                
                # BOX 2: SOURCES WITH PAGE NUMBERS
                st.markdown("### 📚 Sources")
                sources = response['sources']
                
                for i, source in enumerate(sources, 1):
                    with st.expander(f"Source {i} - Page {source['page']}", expanded=(i==1)):
                        st.text(source['content'])
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                
                with st.expander("Debug Info"):
                    st.code(str(e))

# Footer
st.markdown("---")
st.caption("Built with Streamlit • LangChain • FAISS • BM25")