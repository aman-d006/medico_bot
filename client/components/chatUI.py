import streamlit as st
import time
import sys
import re
import html
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.api import ask_question


def init_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "loading" not in st.session_state:
        st.session_state.loading = False


def apply_chat_theme():
    """Apply chat-specific theme"""
    st.markdown("""
    <style>
        /* Chat container */
        .chat-container {
            display: flex;
            flex-direction: column;
            height: calc(100vh - 70px);
            background: var(--dark-bg);
        }
        
        /* Messages area */
        .messages-area {
            flex: 1;
            overflow-y: auto;
            padding: 20px 24px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        
        /* Message row */
        .message-row {
            display: flex;
            gap: 12px;
            animation: fadeIn 0.3s ease;
        }
        
        .user-row {
            justify-content: flex-end;
        }
        
        .assistant-row {
            justify-content: flex-start;
        }
        
        /* Avatar */
        .avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            flex-shrink: 0;
        }
        
        .user-avatar {
            background: var(--primary);
            color: white;
        }
        
        .assistant-avatar {
            background: var(--secondary);
            color: var(--primary-light);
            border: 1px solid var(--border);
        }
        
        /* Message bubble */
        .bubble {
            max-width: 80%;
            padding: 14px 18px;
            border-radius: 12px;
            font-size: 14px;
            line-height: 1.6;
            word-wrap: break-word;
        }
        
        .user-bubble {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            border-radius: 12px 12px 4px 12px;
        }
        
        .assistant-bubble {
            background: var(--lighter-bg);
            color: var(--text-primary);
            border: 1px solid var(--border);
            border-radius: 12px 12px 12px 4px;
        }
        
        /* Medical content styling */
        .medical-content {
            color: var(--text-primary);
        }
        
        .medical-content h3 {
            color: var(--primary-light);
            font-size: 16px;
            font-weight: 700;
            margin: 20px 0 12px 0;
            padding-bottom: 6px;
            border-bottom: 1px solid var(--border);
        }
        
        .medical-content h4 {
            color: var(--text-primary);
            font-size: 15px;
            font-weight: 600;
            margin: 16px 0 8px 0;
        }
        
        .medical-content strong {
            color: var(--primary-light);
            font-weight: 700;
        }
        
        .medical-content ul {
            margin: 8px 0 16px 0;
            padding-left: 24px;
            list-style-type: none;
        }
        
        .medical-content li {
            color: var(--text-secondary);
            margin: 6px 0;
            position: relative;
            padding-left: 20px;
        }
        
        .medical-content li::before {
            content: "•";
            color: var(--primary-light);
            font-weight: bold;
            position: absolute;
            left: 0;
        }
        
        .medical-content p {
            color: var(--text-secondary);
            margin: 8px 0;
        }
        
        .no-info-message {
            background: rgba(59, 130, 246, 0.05);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 12px 16px;
            margin-bottom: 20px;
            color: var(--text-secondary);
            font-style: italic;
        }
        
        .medical-disclaimer {
            background: rgba(239, 68, 68, 0.05);
            border-left: 3px solid var(--error);
            padding: 16px 20px;
            margin: 20px 0 8px 0;
            border-radius: 0 6px 6px 0;
            font-size: 13px;
            color: var(--error);
            font-weight: 500;
        }
        
        .document-suggestions {
            background: rgba(16, 185, 129, 0.05);
            border-left: 3px solid var(--success);
            padding: 16px 20px;
            margin: 20px 0 8px 0;
            border-radius: 0 6px 6px 0;
        }
        
        .document-suggestions strong {
            color: var(--success);
        }
        
        /* Sources section */
        .sources-section {
            margin-top: 20px;
            padding-top: 16px;
            border-top: 1px solid var(--border);
        }
        
        .sources-title {
            color: var(--primary-light);
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .source-item {
            color: var(--text-secondary);
            font-size: 12px;
            padding: 4px 0 4px 24px;
            position: relative;
            word-break: break-word;
        }
        
        .source-item::before {
            content: "📄";
            position: absolute;
            left: 0;
            font-size: 12px;
            opacity: 0.8;
        }
        
        /* Input area */
        .input-area {
            padding: 16px 24px;
            background: linear-gradient(180deg, var(--lighter-bg) 0%, var(--secondary) 100%);
            border-top: 1px solid var(--border);
        }
        
        /* Clear button */
        .stButton > button {
            background: rgba(239, 68, 68, 0.1) !important;
            color: var(--error) !important;
            border: 1px solid var(--error) !important;
            border-radius: 6px !important;
            padding: 8px 12px !important;
            font-size: 14px !important;
            min-width: 40px !important;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
    """, unsafe_allow_html=True)


def clean_response(text):
    """Clean response by removing HTML tags and formatting"""
    if not text:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove div tags and extra whitespace
    text = text.replace('</div>', '').replace('<div>', '')
    text = re.sub(r'\s+', ' ', text)
    
    # Fix bullet points
    text = text.replace('•', '\n•')
    text = text.replace('-', '\n•')
    
    # Fix line breaks
    text = text.replace('. ', '.\n')
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    return text.strip()


def format_response(text):
    """Format response with proper HTML structure"""
    if not text:
        return ""
    
    # Clean first
    text = clean_response(text)
    
    # Split into sections
    lines = text.split('\n')
    html_parts = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        
        # Check for headers
        if line.startswith('**') and line.endswith('**'):
            header = line.strip('*').strip()
            html_parts.append(f'<h3>{header}</h3>')
        
        # Check for bullet points
        elif line.startswith('•'):
            content = line[1:].strip()
            # Check if it's a bold bullet
            if '**' in content:
                parts = re.split(r'\*\*(.*?)\*\*', content)
                formatted = ''
                for j, part in enumerate(parts):
                    if j % 2 == 1:
                        formatted += f'<strong>{part}</strong>'
                    else:
                        formatted += part
                html_parts.append(f'<li>{formatted}</li>')
            else:
                html_parts.append(f'<li>{content}</li>')
        
        # Check for disclaimer
        elif 'IMPORTANT:' in line or 'disclaimer' in line.lower():
            html_parts.append(f'<div class="medical-disclaimer">{line}</div>')
        
        # Check for document suggestions
        elif 'documents might contain' in line.lower():
            html_parts.append(f'<div class="document-suggestions"><strong>{line}</strong>')
            # Collect following bullet points
            i += 1
            suggestions = []
            while i < len(lines) and lines[i].strip().startswith('•'):
                suggestions.append(f'<li>{lines[i].strip()[1:].strip()}</li>')
                i += 1
            if suggestions:
                html_parts.append('<ul>' + ''.join(suggestions) + '</ul>')
            html_parts.append('</div>')
            continue
        
        # Regular text
        else:
            html_parts.append(f'<p>{line}</p>')
        
        i += 1
    
    # Wrap bullet points in ul
    final_html = []
    in_list = False
    for part in html_parts:
        if part.startswith('<li>'):
            if not in_list:
                final_html.append('<ul>')
                in_list = True
            final_html.append(part)
        else:
            if in_list:
                final_html.append('</ul>')
                in_list = False
            final_html.append(part)
    
    if in_list:
        final_html.append('</ul>')
    
    return '\n'.join(final_html)


def render_chat():
    """Main chat rendering function"""
    apply_chat_theme()
    init_session_state()
    
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Messages area
    st.markdown('<div class="messages-area">', unsafe_allow_html=True)
    
    if st.session_state.messages:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'''
                <div class="message-row user-row">
                    <div class="bubble user-bubble">{html.escape(msg["content"])}</div>
                    <div class="avatar user-avatar">👤</div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                # Format assistant message
                content = msg["content"]
                
                # Split into no-info message and rest
                if "do not contain specific information" in content.lower():
                    parts = content.split('**', 1)
                    if len(parts) > 1:
                        no_info = clean_response(parts[0])
                        rest = '**' + parts[1]
                        
                        assistant_html = f'''
                        <div class="message-row assistant-row">
                            <div class="avatar assistant-avatar">🤖</div>
                            <div class="bubble assistant-bubble">
                                <div class="no-info-message">{no_info}</div>
                                <div class="medical-content">{format_response(rest)}</div>
                        '''
                    else:
                        assistant_html = f'''
                        <div class="message-row assistant-row">
                            <div class="avatar assistant-avatar">🤖</div>
                            <div class="bubble assistant-bubble">
                                <div class="medical-content">{format_response(content)}</div>
                        '''
                else:
                    assistant_html = f'''
                    <div class="message-row assistant-row">
                        <div class="avatar assistant-avatar">🤖</div>
                        <div class="bubble assistant-bubble">
                            <div class="medical-content">{format_response(content)}</div>
                    '''
                
                # Add sources
                if "sources" in msg and msg["sources"]:
                    assistant_html += '''
                        <div class="sources-section">
                            <div class="sources-title">📚 Sources</div>
                    '''
                    for src in msg["sources"]:
                        if src:
                            assistant_html += f'<div class="source-item">{html.escape(str(src))}</div>'
                    assistant_html += '</div>'
                
                assistant_html += '''
                            </div>
                        </div>
                        '''
                st.markdown(assistant_html, unsafe_allow_html=True)
    else:
        st.markdown('''
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: var(--text-secondary); text-align: center; padding: 40px;">
            <div style="font-size: 64px; margin-bottom: 20px; opacity: 0.5;">🩺</div>
            <h3 style="color: var(--text-primary); margin-bottom: 12px;">Medical Assistant</h3>
            <p style="max-width: 500px; line-height: 1.6;">Upload medical documents in the sidebar and ask questions to get AI-powered insights and analysis.</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close messages-area
    
    # Input area
    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([20, 1])
    
    with col1:
        user_input = st.chat_input(
            "Ask a question about your medical documents...",
            key="chat_input",
            disabled=st.session_state.loading
        )
    
    with col2:
        if st.button("🗑️", key="clear_btn", help="Clear chat history"):
            st.session_state.messages = []
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close input-area
    st.markdown('</div>', unsafe_allow_html=True)  # Close chat-container
    
    # Process input
    if user_input and not st.session_state.loading:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
        })
        st.session_state.loading = True
        st.rerun()
    
    # Handle response
    if st.session_state.loading and len(st.session_state.messages) > 0:
        last_msg = st.session_state.messages[-1]
        if last_msg["role"] == "user":
            with st.spinner(""):
                time.sleep(0.3)
                try:
                    response = ask_question(last_msg["content"])
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Extract answer
                        answer = None
                        if isinstance(data, dict):
                            if "content" in data:
                                answer = data.get("content")
                            elif "response" in data:
                                answer = data.get("response")
                            elif "answer" in data:
                                answer = data.get("answer")
                        
                        answer = answer or "No response received"
                        sources = data.get("sources", []) if isinstance(data, dict) else []
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer,
                            "sources": sources
                        })
                    else:
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": "Failed to get response from server",
                            "sources": []
                        })
                except Exception as e:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Connection Error: {str(e)}",
                        "sources": []
                    })
                finally:
                    st.session_state.loading = False
                    st.rerun()