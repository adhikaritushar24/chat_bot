# ═══════════════════════════════════════════════════════════════════
# 🚀 TECH ALPHA PROJECT - AI CHATBOT WITH THEME SWITCHING
# ═══════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────
# 📦 IMPORTS & DEPENDENCIES
# ─────────────────────────────────────────────────────────────────────
import os
import time
import json
import csv
import streamlit as st
import streamlit.components.v1 as components
from io import BytesIO, StringIO
from fpdf import FPDF

# ═══════════════════════════════════════════════════════════════════
# 🎨 FRONTEND - COMPLETE UI/UX SECTION
# ═══════════════════════════════════════════════════════════════════

# ───────────────────────────────────────────────────────────────────
# 1️⃣ STREAMLIT CONFIGURATION
# ───────────────────────────────────────────────────────────────────
st.set_page_config(page_title="🤖 AI Chatbot", page_icon="🤖", layout="wide")

# ───────────────────────────────────────────────────────────────────
# 2️⃣ SESSION STATE MANAGEMENT (Frontend State)
# ───────────────────────────────────────────────────────────────────
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'scroll_to_top' not in st.session_state:
    st.session_state.scroll_to_top = False
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = "dark"

# ───────────────────────────────────────────────────────────────────
# 3️⃣ THEME & STYLING (CSS Styling)
# ───────────────────────────────────────────────────────────────────
def apply_premium_theme(theme_mode):
    """Apply premium CSS styling for Light and Dark themes."""
    if theme_mode == "dark":
        css = """
        <style>
            * {
                margin: 0;
                padding: 0;
            }
            
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #0a0e27 0%, #1a1a3e 50%, #0f1629 100%) !important;
                min-height: 100vh;
            }
            
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #111827 0%, #0f1419 100%) !important;
                border-right: 3px solid #4f46e5;
            }
            
            [data-testid="stSidebarContent"] {
                background: transparent !important;
            }
            
            .stTextInput > div > div > input,
            .stSelectbox > div > div > select,
            .stTextArea > div > div > textarea {
                background-color: #1a1f3a !important;
                color: #e0e7ff !important;
                border: 2px solid #4f46e5 !important;
                border-radius: 10px !important;
                padding: 12px !important;
                font-size: 15px !important;
                box-shadow: 0 8px 24px rgba(79, 70, 229, 0.2) !important;
            }
            
            .stTextInput > div > div > input::placeholder {
                color: #6366f1 !important;
            }
            
            .stButton > button {
                background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 10px !important;
                font-weight: 700 !important;
                font-size: 15px !important;
                padding: 12px 24px !important;
                box-shadow: 0 10px 28px rgba(79, 70, 229, 0.35) !important;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }
            
            .stButton > button:hover {
                transform: translateY(-4px) !important;
                box-shadow: 0 16px 36px rgba(79, 70, 229, 0.5) !important;
            }
            
            .stButton > button:active {
                transform: translateY(-1px) !important;
            }
            
            [data-testid="stFormSubmitButton"] > button {
                background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
                color: white !important;
                font-weight: 700 !important;
                font-size: 16px !important;
                border-radius: 10px !important;
                box-shadow: 0 10px 28px rgba(79, 70, 229, 0.35) !important;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
                border: none !important;
            }
            
            [data-testid="stFormSubmitButton"] > button:hover {
                transform: translateY(-4px) !important;
                box-shadow: 0 16px 36px rgba(79, 70, 229, 0.5) !important;
            }
            
            .stDownloadButton > button {
                background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 10px !important;
                font-weight: 700 !important;
                font-size: 14px !important;
                box-shadow: 0 10px 28px rgba(16, 185, 129, 0.35) !important;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }
            
            .stDownloadButton > button:hover {
                transform: translateY(-4px) !important;
                box-shadow: 0 16px 36px rgba(16, 185, 129, 0.5) !important;
            }
            
            h1, h2, h3, h4, h5, h6 {
                color: #e0e7ff !important;
                font-weight: 800 !important;
            }
            
            .stMarkdown, .stText, p, span {
                color: #cbd5e1 !important;
            }
            
            .stInfo {
                background: linear-gradient(135deg, rgba(79, 70, 229, 0.15), rgba(99, 102, 241, 0.1)) !important;
                border-left: 5px solid #4f46e5 !important;
                border-radius: 12px !important;
                backdrop-filter: blur(10px) !important;
            }
            
            .stSuccess {
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.1)) !important;
                border-left: 5px solid #10b981 !important;
                border-radius: 12px !important;
            }
            
            .stWarning {
                background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(217, 119, 6, 0.1)) !important;
                border-left: 5px solid #f59e0b !important;
                border-radius: 12px !important;
            }
            
            .stError {
                background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(220, 38, 38, 0.1)) !important;
                border-left: 5px solid #ef4444 !important;
                border-radius: 12px !important;
            }
            
            .stSlider > div > div > div {
                color: #4f46e5 !important;
            }
            
            .stCheckbox > label {
                color: #cbd5e1 !important;
                font-weight: 600 !important;
            }
            
            hr {
                border-color: rgba(79, 70, 229, 0.3) !important;
            }
        </style>
        """
    else:  # LIGHT MODE
        css = """
        <style>
            * {
                margin: 0;
                padding: 0;
            }
            
            [data-testid="stAppViewContainer"] {
                background: #f8f9fa !important;
                min-height: 100vh;
            }
            
            [data-testid="stSidebar"] {
                background: #e3f2fd !important;
                border-right: 2px solid #2563eb;
            }
            
            [data-testid="stSidebarContent"] {
                background: transparent !important;
            }
            
            .stTextInput > div > div > input,
            .stSelectbox > div > div > select,
            .stTextArea > div > div > textarea {
                background-color: #ffffff !important;
                color: #000000 !important;
                border: 2px solid #bfdbfe !important;
                border-radius: 10px !important;
                padding: 12px !important;
                font-size: 15px !important;
                box-shadow: 0 2px 8px rgba(37, 99, 235, 0.08) !important;
                font-weight: 500 !important;
            }
            
            .stTextInput > div > div > input::placeholder {
                color: #93c5fd !important;
                font-weight: 500 !important;
            }
            
            .stButton > button {
                background: #2563eb !important;
                color: white !important;
                border: none !important;
                border-radius: 10px !important;
                font-weight: 600 !important;
                font-size: 15px !important;
                padding: 12px 24px !important;
                box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
                transition: all 0.3s ease !important;
            }
            
            .stButton > button:hover {
                background: #1d4ed8 !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35) !important;
            }
            
            .stButton > button:active {
                transform: translateY(0px) !important;
            }
            
            [data-testid="stFormSubmitButton"] > button {
                background: #2563eb !important;
                color: white !important;
                font-weight: 600 !important;
                font-size: 16px !important;
                border-radius: 10px !important;
                box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
                transition: all 0.3s ease !important;
                border: none !important;
                padding: 12px !important;
            }
            
            [data-testid="stFormSubmitButton"] > button:hover {
                background: #1d4ed8 !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35) !important;
            }
            
            .stDownloadButton > button {
                background: #10b981 !important;
                color: white !important;
                border: none !important;
                border-radius: 10px !important;
                font-weight: 600 !important;
                font-size: 14px !important;
                box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25) !important;
                transition: all 0.3s ease !important;
                padding: 10px !important;
            }
            
            .stDownloadButton > button:hover {
                background: #059669 !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 16px rgba(16, 185, 129, 0.35) !important;
            }
            
            h1, h2, h3, h4, h5, h6 {
                color: #1e3a8a !important;
                font-weight: 800 !important;
            }
            
            .stMarkdown, .stText, p, span {
                color: #1e3a8a !important;
            }
            
            .stInfo {
                background: #dbeafe !important;
                border-left: 4px solid #2563eb !important;
                border-radius: 10px !important;
            }
            
            .stSuccess {
                background: #dcfce7 !important;
                border-left: 4px solid #10b981 !important;
                border-radius: 10px !important;
            }
            
            .stWarning {
                background: #fef3c7 !important;
                border-left: 4px solid #f59e0b !important;
                border-radius: 10px !important;
            }
            
            .stError {
                background: #fee2e2 !important;
                border-left: 4px solid #ef4444 !important;
                border-radius: 10px !important;
            }
            
            .stSlider > div > div > div {
                color: #2563eb !important;
            }
            
            .stCheckbox > label {
                color: #1e3a8a !important;
                font-weight: 600 !important;
            }
            
            hr {
                border-color: #e0e7ff !important;
            }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

# ───────────────────────────────────────────────────────────────────
# 4️⃣ SIDEBAR RENDERING
# ───────────────────────────────────────────────────────────────────
def render_sidebar():
    """Render sidebar with theme toggle, settings, and FAQ."""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎨 Theme")
    col1, col2 = st.sidebar.columns(2, gap="small")
    with col1:
        if st.button("☀️ Light", key="light_btn", use_container_width=True):
            st.session_state.theme_mode = "light"
            st.rerun()
    with col2:
        if st.button("🌙 Dark", key="dark_btn", use_container_width=True):
            st.session_state.theme_mode = "dark"
            st.rerun()
    st.sidebar.markdown("---")

    st.sidebar.markdown("### ⚙️ Settings")
    max_turns = st.sidebar.slider("📊 Keep last N turns", min_value=1, max_value=20, value=6)
    model_name = st.sidebar.text_input("🤖 Model name", value="command-nightly")
    auto_summarize = st.sidebar.checkbox("📝 Auto-summarize history", value=False)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### ❓ FAQ")
    faq_questions = {
        "What can this bot do?": "This chatbot can answer questions, provide suggestions, and summarize conversations.",
        "How does the bot remember context?": "It keeps track of recent messages and can summarize older chats to maintain context.",
        "Can I export the chat?": "Yes! You can download the chat history as JSON, CSV, or PDF.",
        "Does it support multiple personalities?": "Yes, the bot can switch modes like casual, study helper, or recommendations."
    }
    faq_choice = st.sidebar.selectbox("Select a question", [""] + list(faq_questions.keys()))
    if faq_choice:
        st.sidebar.info(faq_questions[faq_choice])
    
    return max_turns, model_name, auto_summarize

# ───────────────────────────────────────────────────────────────────
# 5️⃣ MAIN HEADER RENDERING
# ───────────────────────────────────────────────────────────────────
def render_header():
    """Render main header and title."""
    st.markdown("<h1 style='text-align: center; font-size: 55px; font-weight: 900; letter-spacing: -1px;'>VEXEL </h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; font-weight: 500; opacity: 0.85; margin-top: -15px;'>Intelligent AI Assistant • Powered by Advanced Technology 💭</p>", unsafe_allow_html=True)
    st.markdown("---")

# ───────────────────────────────────────────────────────────────────
# 6️⃣ CHAT INPUT RENDERING
# ───────────────────────────────────────────────────────────────────
def render_chat_input():
    """Render chat input form and suggestions."""
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("💬 Type your message here...")
        send_clicked = st.form_submit_button("🚀 Send", use_container_width=True)
    
    if user_input and len(user_input) > 2:
        suggestion = get_suggestions(user_input)
        if suggestion:
            st.info(f"💡 Suggestion: {suggestion}")
    
    return user_input, send_clicked

# ───────────────────────────────────────────────────────────────────
# 7️⃣ CHAT DISPLAY RENDERING
# ───────────────────────────────────────────────────────────────────
def render_chat_display():
    """Render chat history display."""
    if st.session_state.chat_history:
        st.markdown("### 💬 Conversation")
        for turn in reversed(st.session_state.chat_history):
            ts = turn.get("time")
            user_msg = turn.get('user','')
            ai_msg = turn.get('ai','')
            
            st.markdown(f"**🧑 You** `{ts}`" if ts else f"**🧑 You**")
            st.markdown(f"<p style='color: #1e40af; font-size: 16px; font-weight: 500;'>>> {user_msg}</p>", unsafe_allow_html=True)
            
            st.markdown(f"**🤖 AI**")
            st.markdown(f"<p style='color: #1e40af; font-size: 16px; font-weight: 500;'>>> {ai_msg}</p>", unsafe_allow_html=True)
            st.markdown("---")
    else:
        st.info("💭 Start a conversation by typing a message!")

# ───────────────────────────────────────────────────────────────────
# 8️⃣ EXPORT CONTROLS RENDERING
# ───────────────────────────────────────────────────────────────────
def render_export_controls():
    """Render export and control buttons."""
    st.markdown("### 📥 Export & Controls")
    col1, col2, col3, col4 = st.columns(4, gap="small")

    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history.clear()
            st.rerun()

    if st.session_state.chat_history:
        with col2:
            history_json = json.dumps(st.session_state.chat_history, indent=2)
            st.download_button("📄 JSON", data=history_json, file_name="chat_history.json", mime="application/json", use_container_width=True)
        
        with col3:
            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow(["timestamp","user","ai"])
            for t in st.session_state.chat_history:
                writer.writerow([t.get("time",""), t.get("user",""), t.get("ai","")])
            csv_bytes = csv_buffer.getvalue().encode("utf-8")
            st.download_button("📊 CSV", data=csv_bytes, file_name="chat_history.csv", mime="text/csv", use_container_width=True)
        
        with col4:
            try:
                pdf = FPDF()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()
                pdf.set_font("Arial", size=11)
                for t in st.session_state.chat_history:
                    # Clean unicode characters for PDF compatibility
                    user_text = f"[{t.get('time','')}] You: {t.get('user','')}"
                    ai_text = f"AI: {t.get('ai','')}"
                    # Replace special unicode characters
                    user_text = user_text.encode('ascii', 'replace').decode('ascii')
                    ai_text = ai_text.encode('ascii', 'replace').decode('ascii')
                    pdf.multi_cell(0, 6, user_text)
                    pdf.multi_cell(0, 6, ai_text)
                    pdf.ln(1)
                pdf_bytes = pdf.output(dest='S').encode('latin-1')
                st.download_button("📑 PDF", data=pdf_bytes, file_name="chat_history.pdf", mime="application/pdf", use_container_width=True)
            except Exception as e:
                st.warning(f"PDF download temporarily unavailable: {str(e)}")

# ═══════════════════════════════════════════════════════════════════
# 🤖 BACKEND - CORE LOGIC SECTION
# ═══════════════════════════════════════════════════════════════════

# ───────────────────────────────────────────────────────────────────
# 1️⃣ COHERE API SETUP
# ───────────────────────────────────────────────────────────────────
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    st.error("❌ Cohere API key not found. Set COHERE_API_KEY environment variable.")
    st.stop()

@st.cache_resource
def get_cohere_client(api_key):
    """Initialize and cache Cohere API client."""
    import cohere
    return cohere.Client(api_key)

co = get_cohere_client(COHERE_API_KEY)

# ───────────────────────────────────────────────────────────────────
# 2️⃣ UTILITY FUNCTIONS
# ───────────────────────────────────────────────────────────────────
def build_prompt(history, user_input, max_turns=6):
    """Build conversation prompt from chat history."""
    recent = history[-max_turns:] if history else []
    conversation_prompt = ""
    for turn in recent:
        conversation_prompt += f"Human: {turn.get('user','')}\nAI: {turn.get('ai','')}\n"
    conversation_prompt += f"Human: {user_input}\nAI (answer clearly and completely):"
    return conversation_prompt

def summarize_history(history, keep_last, co_client, model_name):
    """Summarize old chat history to maintain context."""
    if len(history) <= keep_last + 2:
        return history
    to_summarize = history[:-keep_last]
    summary_prompt = "Summarize the following conversation into a short context summary:\n\n"
    for turn in to_summarize:
        summary_prompt += f"Human: {turn.get('user','')}\nAI: {turn.get('ai','')}\n"
    summary_prompt += "\nSummary:"
    resp = co_client.chat(model=model_name, message=summary_prompt)
    summary_text = resp.text.strip()
    new_history = [{"user": "[summary]", "ai": summary_text, "time": time.strftime("%Y-%m-%d %H:%M:%S")}]
    new_history.extend(history[-keep_last:])
    return new_history

def get_suggestions(user_input):
    """Generate AI suggestions based on user input keywords."""
    user_lower = user_input.lower()
    suggestion_map = {
        "hello": "👋 Hi! How can I help you today?",
        "hi": "👋 Hello! What would you like to know?",
        "how": "❓ Ask me anything - I'm here to help!",
        "what": "🤔 I can answer questions about various topics",
        "tell": "📚 Sure! I can provide information on any topic",
        "code": "💻 Need help with coding? I'm here!",
        "explain": "📖 I can explain complex topics simply",
        "help": "🆘 What do you need help with?",
        "who": "👤 I'm Tech Alpha - your AI Assistant!",
        "when": "⏰ I can help with time-related questions",
        "where": "🗺️ I can provide location information",
        "why": "🔍 Let me explain the reasoning behind that",
    }
    for key, suggestion in suggestion_map.items():
        if key in user_lower:
            return suggestion
    return None

def scroll_to_top():
    """Smooth scroll to top of page."""
    components.html(
        """
        <script>
        try {
            parent.window.scrollTo({ top: 0, behavior: 'smooth' });
        } catch(e) {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        </script>
        """,
        height=0,
    )

# ───────────────────────────────────────────────────────────────────
# 3️⃣ MESSAGE PROCESSING LOGIC
# ───────────────────────────────────────────────────────────────────
def process_message(user_input, max_turns, model_name, auto_summarize):
    """Process user message and get AI response."""
    if not user_input or not user_input.strip():
        return False
    
    # Auto-summarize if needed
    if auto_summarize and len(st.session_state.chat_history) > (max_turns * 3):
        st.session_state.chat_history = summarize_history(
            st.session_state.chat_history, keep_last=max_turns, co_client=co, model_name=model_name
        )

    # Get AI response
    prompt = build_prompt(st.session_state.chat_history, user_input, max_turns=max_turns)
    with st.spinner("⚡ Generating reply..."):
        t0 = time.time()
        response = co.chat(model=model_name, message=prompt)
        latency = time.time() - t0

    # Store in history
    bot_reply = response.text.strip()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.chat_history.append({"user": user_input, "ai": bot_reply, "time": timestamp})

    st.session_state.scroll_to_top = True
    st.success(f"✅ Reply received in {latency:.2f}s")
    return True

# ═══════════════════════════════════════════════════════════════════
# 🎯 MAIN APPLICATION FLOW
# ═══════════════════════════════════════════════════════════════════

# Apply theme
apply_premium_theme(st.session_state.theme_mode)

# Render all frontend components
max_turns, model_name, auto_summarize = render_sidebar()
render_header()
user_input, send_clicked = render_chat_input()

# Process message if sent
if send_clicked:
    process_message(user_input, max_turns, model_name, auto_summarize)

# Display chat and export controls
render_chat_display()
if st.session_state.get('scroll_to_top', False):
    scroll_to_top()
    st.session_state.scroll_to_top = False

render_export_controls()


