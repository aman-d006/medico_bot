import streamlit as st

def render_uploader():
    """Render file uploader component"""
    
    # Custom styling for uploader
    st.markdown("""
    <style>
        /* Additional uploader styling */
        .uploaded-files {
            margin-top: 16px;
        }
        
        .file-item {
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 10px 12px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .file-name {
            color: var(--text-primary);
            font-size: 13px;
            font-weight: 500;
        }
        
        .file-size {
            color: var(--text-secondary);
            font-size: 11px;
            margin-left: 8px;
        }
        
        .remove-btn {
            background: rgba(239, 68, 68, 0.1);
            color: var(--error);
            border: 1px solid var(--error);
            border-radius: 4px;
            padding: 4px 8px;
            font-size: 11px;
            cursor: pointer;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Upload Medical PDFs",
        type=['pdf'],
        accept_multiple_files=True,
        key="pdf_uploader",
        help="Upload medical documents in PDF format (max 200MB per file)"
    )
    
    # Display uploaded files
    if uploaded_files:
        st.markdown('<div class="uploaded-files">', unsafe_allow_html=True)
        st.markdown(f"**📎 {len(uploaded_files)} file(s) uploaded**")
        
        for file in uploaded_files:
            file_size = file.size / 1024 / 1024  # Convert to MB
            st.markdown(f'''
            <div class="file-item">
                <span class="file-name">📄 {file.name}</span>
                <span class="file-size">({file_size:.1f} MB)</span>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Process button
        if st.button("🔍 Process Documents", use_container_width=True):
            with st.spinner("Processing documents..."):
                # Add your processing logic here
                st.success("✅ Documents processed successfully!")
    
    return uploaded_files