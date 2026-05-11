"""
ASMA — AI Agent powered by Azure AI Foundry.
Run: streamlit run app/main.py
"""
from pathlib import Path
import streamlit as st
from foundry_client import FoundryChatClient
from config import settings

# ============ Page config ============
st.set_page_config(
    page_title="Asma — AI Agent",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============ Load custom CSS ============
css_path = Path(__file__).parent / "style.css"
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ============ Initialize state ============
if "client" not in st.session_state:
    st.session_state.client = FoundryChatClient(
        endpoint=settings.FOUNDRY_ENDPOINT,
        api_key=settings.FOUNDRY_API_KEY,
        deployment=settings.MODEL_DEPLOYMENT_NAME,
        api_version=settings.API_VERSION,
        system_prompt=settings.SYSTEM_PROMPT,
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# ============ Sidebar ============
with st.sidebar:
    st.markdown("""
        <div class="asma-profile">
            <div class="asma-avatar">A</div>
            <div class="asma-name">Asma</div>
            <div class="asma-role">Your AI Agent</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="asma-section">⚙️ Model Settings</div>', unsafe_allow_html=True)
    temperature = st.slider("Creativity", 0.0, 1.0, 0.7, 0.1,
                            help="Higher = more creative, lower = more focused")
    max_tokens = st.slider("Response length", 100, 4000, 800, 100)

    st.markdown('<div class="asma-section">🛠️ Actions</div>', unsafe_allow_html=True)
    if st.button("🗑️ New conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.client.reset()
        st.rerun()

    if st.session_state.messages:
        chat_export = "\n\n".join(
            f"**{m['role'].title()}:** {m['content']}"
            for m in st.session_state.messages
        )
        st.download_button(
            "💾 Export chat",
            chat_export,
            file_name="asma-conversation.md",
            mime="text/markdown",
            use_container_width=True,
        )

    st.markdown('<div class="asma-section">ℹ️ About</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div style="font-size: 0.85rem; color: #94a3b8;">
            <b>Model:</b> {settings.MODEL_DEPLOYMENT_NAME}<br>
            <b>Engine:</b> Azure AI Foundry<br>
            <b>Version:</b> 1.0.0
        </div>
    """, unsafe_allow_html=True)

# ============ Main area ============
st.markdown("""
    <div class="asma-hero">
        <h1 class="asma-logo">Asma<span class="dot">.</span></h1>
        <div class="asma-tagline">Your intelligent AI agent — ask anything, get expert answers</div>
        <div class="asma-status">
            <span class="dot-live"></span>
            Online · Ready to assist
        </div>
    </div>
""", unsafe_allow_html=True)

# ============ Quick action buttons (empty state only) ============
if not st.session_state.messages:
    st.markdown("""
        <div class="asma-welcome">
            <h3>👋 Hi! How can I help you today?</h3>
            <p>Try one of these, or type your own question below.</p>
        </div>
    """, unsafe_allow_html=True)

    quick_actions = [
        ("💡", "Explain a concept", "Explain quantum computing in simple terms"),
        ("✍️", "Help me write", "Help me write a professional email to schedule a meeting"),
        ("🐛", "Debug code", "I have a Python error: 'list index out of range'. How do I debug it?"),
        ("📊", "Summarize", "Summarize the key benefits of cloud computing for a business"),
    ]

    cols = st.columns(2)
    for i, (icon, label, prompt) in enumerate(quick_actions):
        with cols[i % 2]:
            if st.button(f"{icon}  **{label}**\n\n{prompt[:60]}...", key=f"qa_{i}"):
                st.session_state.pending_prompt = prompt
                st.rerun()

# ============ Render message history ============
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "✨"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ============ Handle input (typed or from quick action) ============
user_input = st.chat_input("Ask Asma anything...")
if st.session_state.pending_prompt:
    user_input = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    # Show assistant reply with typing indicator
    with st.chat_message("assistant", avatar="✨"):
        placeholder = st.empty()
        placeholder.markdown(
            '<div class="asma-typing"><span></span><span></span><span></span></div>',
            unsafe_allow_html=True,
        )
        try:
            reply = st.session_state.client.send_message(
                user_input,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            placeholder.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            placeholder.error(f"⚠️ Something went wrong: {e}")

    st.rerun()