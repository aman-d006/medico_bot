import streamlit as st
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from components.upload import render_uploader
from components.history_download import render_history_download
from components.chatUI import render_chat


# Configure page with wide layout
st.set_page_config(
    page_title="Medical Assistant | Professional AI Chat",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Chatbot Theme
st.markdown("""
<style>
    /* Color Palette */
    :root {
        --primary: #3B82F6;
        --primary-dark: #1E40AF;
        --primary-light: #60A5FA;
        --secondary: #1F2937;
        --dark-bg: #0F172A;
        --lighter-bg: #1E293B;
        --border: #334155;
        --text-primary: #F8FAFC;
        --text-secondary: #CBD5E1;
        --success: #10B981;
        --error: #EF4444;
        --warning: #F59E0B;
    }
    
    /* Reset and Base Styles */
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    .stDeployButton { display: none; }
    
    /* Remove top padding/empty space */
    .main > div {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, var(--dark-bg) 0%, #0F172A 100%);
        padding: 0 !important;
        color: var(--text-primary);
    }
    
    [data-testid="stToolbar"] {
        display: none;
    }
    
    [data-testid="stDecoration"] {
        display: none;
    }
    
    .main {
        padding: 0 !important;
        max-width: 100%;
        height: 100vh;
        overflow: hidden;
    }
    
    /* Remove all default padding and margins */
    [data-testid="stAppViewContainer"] > section {
        padding: 0 !important;
        margin: 0 !important;
        height: 100vh;
    }
    
    .stAppViewContainer {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }
    
    p, label {
        color: var(--text-secondary) !important;
        font-size: 14px;
    }
    
    /* Columns */
    [data-testid="column"] {
        padding: 0 !important;
        margin: 0 !important;
        gap: 0 !important;
        height: 100vh;
    }
    
    /* Left Sidebar Upload Section */
    .upload-sidebar {
        background: linear-gradient(180deg, var(--lighter-bg) 0%, #1e293b 100%);
        border-right: 2px solid var(--border);
        padding: 20px 16px;
        height: 100vh;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    
    .sidebar-title {
        color: var(--primary-light);
        font-size: 18px;
        font-weight: 700;
        margin: 0 0 8px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .upload-card {
        background: rgba(59, 130, 246, 0.05);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    .upload-card h4 {
        color: var(--primary-light);
        margin: 0 0 16px 0;
        font-size: 15px;
        font-weight: 600;
    }
    
    /* File Uploader Styling - FIXED VISIBILITY */
    .stFileUploader {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    .stFileUploader > div {
        background: transparent !important;
    }
    
    .stFileUploader label {
        display: none !important; /* Hide the default label */
    }
    
    /* Dropzone styling */
    [data-testid="stFileUploadDropzone"] {
        background: rgba(59, 130, 246, 0.03) !important;
        border: 2px dashed var(--border) !important;
        border-radius: 8px !important;
        padding: 32px 20px !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: var(--primary) !important;
        background: rgba(59, 130, 246, 0.05) !important;
    }
    
    [data-testid="stFileUploadDropzone"] p {
        color: var(--text-secondary) !important;
        font-size: 13px !important;
        margin-bottom: 12px !important;
    }
    
    /* Browse files button - VISIBLE NOW */
    [data-testid="stFileUploadDropzone"] button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 8px 24px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        cursor: pointer !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        transition: all 0.3s ease !important;
        margin: 8px 0 !important;
        display: inline-block !important;
    }
    
    [data-testid="stFileUploadDropzone"] button:hover {
        background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* File info styling */
    [data-testid="stFileUploaderFile"] {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
        padding: 8px 12px !important;
        margin-top: 12px !important;
        color: var(--text-primary) !important;
        font-size: 13px !important;
    }
    
    [data-testid="stFileUploaderFile"] button {
        background: rgba(239, 68, 68, 0.1) !important;
        color: var(--error) !important;
        border: 1px solid var(--error) !important;
        border-radius: 4px !important;
        padding: 4px 8px !important;
        font-size: 11px !important;
        margin-left: 8px !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        cursor: pointer !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.35) !important;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid var(--success) !important;
        color: var(--success) !important;
        border-radius: 6px !important;
        padding: 12px !important;
        font-size: 13px !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid var(--error) !important;
        color: var(--error) !important;
        border-radius: 6px !important;
        padding: 12px !important;
        font-size: 13px !important;
    }
    
    /* Right Chat Section */
    .chat-main {
        background: var(--dark-bg);
        height: 100vh;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }
    
    .chat-header {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(30, 64, 175, 0.05) 100%);
        border-bottom: 1px solid var(--border);
        padding: 16px 24px;
        text-align: left;
        flex-shrink: 0;
    }
    
    .chat-header h1 {
        font-size: 22px;
        margin: 0 0 4px 0;
        color: var(--text-primary);
    }
    
    .chat-header .tagline {
        font-size: 13px;
        color: var(--primary-light);
        opacity: 0.8;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-light);
    }
</style>
""", unsafe_allow_html=True)

# Create two-column layout: 20% upload, 80% chat
col_upload, col_chat = st.columns([1, 4], gap="small")

# LEFT COLUMN - Upload Section
with col_upload:
    st.markdown('<div class="upload-sidebar">', unsafe_allow_html=True)
    
    st.markdown('<h2 class="sidebar-title">📤 Upload Documents</h2>', unsafe_allow_html=True)
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.markdown('<h4>Medical PDFs</h4>', unsafe_allow_html=True)
    
    render_uploader()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# RIGHT COLUMN - Chat Section
with col_chat:
    st.markdown('<div class="chat-main">', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="chat-header">
        <h1>🩺 Medical Assistant</h1>
        <div class="tagline">AI-Powered Medical Document Analysis</div>
    </div>
    ''', unsafe_allow_html=True)
    
    render_chat()
    
    st.markdown('</div>', unsafe_allow_html=True)