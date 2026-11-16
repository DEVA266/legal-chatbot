"""
LexCraft AI - Legal Document Drafting Assistant
Dedicated Google Gemini Powered Chatbot for Advocates.
Features:
- Fixed to Google Gemini Engine (high accuracy, fast generation)
- Dual-pane layout (Chat & Statutory Intake on Left, Live Court-Ready Document on Right)
- Real-time Input / Output Token Telemetry and Cost Dashboard
- Specialized legal workflows for Section 138 NI Act, NDA, and Recovery Notices
- Dynamic editing and iterative refinement
- One-click Word (.docx) export with court-ready styling
- Mobile-friendly responsive design
"""

import os
import streamlit as st
from dotenv import load_dotenv
from config import APP_TITLE, APP_SUBTITLE, MODEL_PRICING, SUPPORTED_DOCUMENTS, USD_TO_INR
from core.llm_engine import call_llm, TokenUsage
from core.prompts import extract_document_from_response
from core.docx_exporter import create_legal_docx

# Load .env file automatically if present
load_dotenv()

# Fixed Model Configuration
GEMINI_MODEL = "gemini-3.8-flash"

# 1. Page Configuration
st.set_page_config(
    page_title="LexCraft AI - Legal Drafting Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for polished legal tech look
st.markdown("""
<style>
    /* Global styling */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Token badge styling */
    .token-badge {
        display: inline-flex;
        align-items: center;
        background-color: #f1f5f9;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 0.78rem;
        color: #334155;
        margin-top: 6px;
        margin-bottom: 4px;
        font-family: monospace;
    }
    
    /* Document preview container */
    .doc-preview-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        font-family: 'Times New Roman', serif;
        font-size: 1.05rem;
        line-height: 1.6;
        color: #1a202c;
        max-height: 75vh;
        overflow-y: auto;
    }
    
    /* Quick prompt button styling */
    .stButton button {
        border-radius: 6px;
    }
    
    /* Header title */
    .app-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.2rem;
    }
    .app-subtitle {
        font-size: 0.95rem;
        color: #64748b;
        margin-bottom: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)


# 2. State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_document" not in st.session_state:
    st.session_state.current_document = ""

if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

if "total_prompt_tokens" not in st.session_state:
    st.session_state.total_prompt_tokens = 0

if "total_completion_tokens" not in st.session_state:
    st.session_state.total_completion_tokens = 0

if "total_cost_usd" not in st.session_state:
    st.session_state.total_cost_usd = 0.0

if "last_latency" not in st.session_state:
    st.session_state.last_latency = 0.0


# 3. Sidebar Configuration & Telemetry
with st.sidebar:
    st.markdown("## ⚖️ **LexCraft AI**")
    st.caption("Legal Drafting & Statutory Intake Chatbot")
    st.markdown("---")

    # A. AI Engine & API Key Setup
    st.markdown("### 🤖 **AI Engine**")
    engine_type = st.radio(
        "Select Provider:",
        options=[
            "⚡ Groq (Llama 3.1 - Ultra Fast)",
            "🤖 Google Gemini (3.8 Flash)",
            "🛡️ Offline Smart Assistant"
        ],
        index=0,
        help="Groq delivers instant sub-second legal drafts without high-demand traffic spikes."
    )

    if "Groq" in engine_type:
        active_model = "llama-3.1-8b-instant"
        active_base_url = "https://api.groq.com/openai/v1"
        active_api_key = st.text_input(
            "Groq API Key:",
            type="password",
            value=os.getenv("GROQ_API_KEY", ""),
            placeholder="gsk_...",
            help="Paste your free Groq API key here."
        )
        if active_api_key:
            st.success("🟢 **Groq Active (< 1s responses)**")
        else:
            st.warning("⚠️ Enter your Groq API Key above.")
    elif "Gemini" in engine_type:
        active_model = "gemini-3.8-flash"
        active_base_url = None
        active_api_key = st.text_input(
            "Gemini API Key:",
            type="password",
            value=os.getenv("GEMINI_API_KEY", ""),
            placeholder="AIzaSy...",
            help="Paste your free Google Gemini API Key here."
        )
        if active_api_key:
            st.success("🟢 **Gemini Active**")
        else:
            st.warning("⚠️ Enter your Gemini API Key above.")
    else:
        active_model = "mock-offline-engine"
        active_base_url = None
        active_api_key = "mock"
        st.info("🟢 **Offline Statutory Assistant Active** (Zero API keys needed)")

    st.markdown("---")

    # B. Real-time Token & Cost Telemetry Dashboard
    st.markdown("### 📊 **Token & Cost Telemetry**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Total Tokens",
            value=f"{st.session_state.total_tokens:,}"
        )
    with col2:
        cost_inr = st.session_state.total_cost_usd * USD_TO_INR
        st.metric(
            label="Session Cost",
            value=f"${st.session_state.total_cost_usd:.4f}",
            delta=f"₹{cost_inr:.2f} INR"
        )

    col3, col4 = st.columns(2)
    with col3:
        st.caption(f"📥 **Input:** {st.session_state.total_prompt_tokens:,}")
    with col4:
        st.caption(f"📤 **Output:** {st.session_state.total_completion_tokens:,}")

    if st.session_state.last_latency > 0:
        st.caption(f"⚡ **Last Call Latency:** {st.session_state.last_latency:.2f}s")

    if st.button("🔄 Reset Chat & Tokens", use_container_width=True):
        st.session_state.messages = []
        st.session_state.current_document = ""
        st.session_state.total_tokens = 0
        st.session_state.total_prompt_tokens = 0
        st.session_state.total_completion_tokens = 0
        st.session_state.total_cost_usd = 0.0
        st.session_state.last_latency = 0.0
        st.rerun()

    st.markdown("---")

    # C. Mobile Testing Instructions
    with st.expander("📱 Test on Mobile Phone"):
        st.markdown(f"""
        To test directly on your mobile phone:
        1. Connect your phone to the same Wi-Fi as your PC.
        2. Open your mobile browser and enter:
        `http://192.168.1.6:8501`
        """)


# 4. Main View Layout: Split Screen
col_chat, col_doc = st.columns([1.1, 1.0], gap="large")

# ==========================================
# LEFT PANE: Lawyer Chat & Intake Interface
# ==========================================
with col_chat:
    st.markdown('<div class="app-title">⚖️ Legal Drafting Chatbot</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Intake interview, statutory verification, and iterative document refinement.</div>', unsafe_allow_html=True)

    # Quick Prompts / Pills for immediate testing
    st.markdown("**⚡ Quick Actions:**")
    quick_col1, quick_col2, quick_col3 = st.columns(3)
    quick_input = None
    with quick_col1:
        if st.button("📜 Section 138 Notice", use_container_width=True):
            quick_input = "Draft me a document on section 138"
    with quick_col2:
        if st.button("🛡️ Mutual NDA", use_container_width=True):
            quick_input = "Draft me a Mutual Non-Disclosure Agreement (NDA)"
    with quick_col3:
        if st.button("⚖️ Recovery Notice", use_container_width=True):
            quick_input = "Draft me a Legal Notice for Recovery of Dues against unpaid invoices"

    st.markdown("---")

    # Display Chat History
    chat_container = st.container()
    with chat_container:
        if not st.session_state.messages:
            with st.chat_message("assistant", avatar="⚖️"):
                st.markdown(
                    "Greetings Counsel. I am **LexCraft AI**, your specialized legal drafting assistant for Indian Legal Practice.\n\n"
                    "Tell me what document you wish to draft today, e.g.:\n"
                    "- *'Draft me a document on section 138'*\n"
                    "- *'I need an NDA for a new vendor engagement'*\n"
                    "- *'Draft a legal demand notice for unpaid invoices of Rs 10 Lakhs'*\n\n"
                    "I will ask the necessary statutory intake questions to collect the required details and generate a court-ready draft."
                )

        for msg in st.session_state.messages:
            avatar = "👤" if msg["role"] == "user" else "⚖️"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])
                
                # Show token telemetry badge if attached to assistant message
                if "usage" in msg and msg["usage"]:
                    u = msg["usage"]
                    st.markdown(
                        f"""<div class="token-badge">
                        📥 In: {u['prompt_tokens']} | 📤 Out: {u['completion_tokens']} | Total: {u['total_tokens']} tokens | ⚡ {u['latency_sec']}s
                        </div>""",
                        unsafe_allow_html=True
                    )

    # Chat Input Box
    user_prompt = st.chat_input("Enter your instructions, legal facts, or edits here...")
    
    # Handle quick prompt or typed prompt
    active_prompt = quick_input or user_prompt

    if active_prompt:
        # 1. Append User Message
        st.session_state.messages.append({"role": "user", "content": active_prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(active_prompt)

        # 2. Call LLM Engine with spinner
        with st.chat_message("assistant", avatar="⚖️"):
            engine_name = "Groq" if "Groq" in engine_type else ("Gemini" if "Gemini" in engine_type else "Offline Engine")
            with st.spinner(f"Analyzing statutory requirements & drafting with {engine_name}..."):
                response = call_llm(
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    model=active_model,
                    api_key=active_api_key,
                    base_url=active_base_url,
                    temperature=0.2
                )

                # Parse document if enclosed in tags
                chat_text, extracted_doc = extract_document_from_response(response.content)

                # If a document was generated or revised, update current document state
                if extracted_doc:
                    st.session_state.current_document = extracted_doc

                # Display assistant response
                st.markdown(chat_text)

                # Display token usage badge
                u = response.usage
                usage_dict = {
                    "prompt_tokens": u.prompt_tokens,
                    "completion_tokens": u.completion_tokens,
                    "total_tokens": u.total_tokens,
                    "latency_sec": u.latency_sec
                }
                st.markdown(
                    f"""<div class="token-badge">
                    📥 In: {u.prompt_tokens} | 📤 Out: {u.completion_tokens} | Total: {u.total_tokens} tokens | ⚡ {u.latency_sec}s
                    </div>""",
                    unsafe_allow_html=True
                )

                # Update cumulative telemetry
                st.session_state.total_tokens += u.total_tokens
                st.session_state.total_prompt_tokens += u.prompt_tokens
                st.session_state.total_completion_tokens += u.completion_tokens
                st.session_state.total_cost_usd += u.cost_usd
                st.session_state.last_latency = u.latency_sec

                # Append assistant message with usage metadata
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": chat_text,
                    "usage": usage_dict
                })

        st.rerun()


# ==========================================
# RIGHT PANE: Live Document Preview & Export
# ==========================================
with col_doc:
    st.markdown("### 📄 **Live Legal Document Preview**")
    
    if st.session_state.current_document:
        st.caption("✅ **Court-Ready Draft Generated** — Ready for review, editing, or export.")

        # Document Action Bar
        doc_col1, doc_col2 = st.columns([1, 1])
        with doc_col1:
            # Word (.docx) export button
            docx_file = create_legal_docx(st.session_state.current_document)
            st.download_button(
                label="📥 Download Word (.docx)",
                data=docx_file,
                file_name="legal_document_draft.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        with doc_col2:
            # Markdown export button
            st.download_button(
                label="📋 Download Markdown (.md)",
                data=st.session_state.current_document,
                file_name="legal_document_draft.md",
                mime="text/markdown",
                use_container_width=True
            )

        st.markdown("---")

        # Document Display Box
        st.markdown(f'<div class="doc-preview-box">', unsafe_allow_html=True)
        st.markdown(st.session_state.current_document)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**💡 Common Edits to test:**")
        edit_col1, edit_col2 = st.columns(2)
        with edit_col1:
            if st.button("➕ Add Section 141 Director Liability", use_container_width=True):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "Please update the draft to hold the Managing Director personally and vicariously liable under Section 141 of the Negotiable Instruments Act."
                })
                st.rerun()
        with edit_col2:
            if st.button("📈 Change Interest to 24% p.a.", use_container_width=True):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "Please modify the interest rate claim to 24% per annum from the date of default until realization."
                })
                st.rerun()

    else:
        # Placeholder when no document has been drafted yet
        st.info("ℹ️ **No document drafted yet.**\n\nStart by requesting a document in the chat (e.g. *'Draft me a document on section 138'* or click a preset on the left). As soon as the necessary legal details are gathered, the full court-ready draft will render here automatically.")

        # Show template previews
        with st.expander("📖 Preview Supported Document Blueprints"):
            for doc in SUPPORTED_DOCUMENTS:
                st.markdown(f"**{doc['title']}** `{doc['badge']}`")
                st.caption(f"Governing Law: {doc['law']}")
                st.markdown(f"*{doc['description']}*")
                st.markdown("---")
