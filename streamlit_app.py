import streamlit as st
import requests
import datetime

BASE_URL = "http://localhost:8000"  # Backend endpoint

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="🌍 AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------ CUSTOM CSS ------------------
st.markdown(
    """
<style>
    /* ─────────────────────────────────────────────── */
    /*         Dark Mode - Travel Planner 2025/26       */
    /* ─────────────────────────────────────────────── */

    .stApp {
        background-color: #0f172a;          /* slate-900 */
    }

    /* Main title */
    .title-text {
        font-size: 44px;
        font-weight: 800;
        color: #e2e8f0;                     /* slate-200 */
        letter-spacing: -0.6px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.4);
    }

    /* Subtitle */
    .subtitle-text {
        font-size: 19px;
        color: #94a3b8;                     /* slate-400 */
        margin-bottom: 32px;
        font-weight: 400;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1e293b;          /* slate-800 */
        border-right: 1px solid #334155;
    }

    section[data-testid="stSidebar"] .sidebar-content {
        padding-top: 1.5rem;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] small {
        color: #cbd5e1 !important;          /* slate-300 */
    }

    section[data-testid="stSidebar"] .stMarkdown {
        color: #cbd5e1;
    }

    /* Example queries look better now */
    section[data-testid="stSidebar"] ul,
    section[data-testid="stSidebar"] li {
        color: #94a3b8;
    }

    /* Input box */
    .stTextInput > div > div > input {
        background-color: #1e293b;
        color: #e2e8f0;
        border: 1px solid #475569;
        border-radius: 10px;
        padding: 14px 16px;
        font-size: 16px;
    }

    .stTextInput > div > div > input::placeholder {
        color: #64748b;
    }

    /* Form submit button */
    .stFormSubmitButton > button {
        background-color: #3b82f6 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px;
        padding: 0.7rem 1.6rem;
        font-weight: 600;
    }

    .stFormSubmitButton > button:hover {
        background-color: #2563eb !important;
    }

    /* Response box - dark version */
    .response-box {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 28px;
        border-radius: 16px;
        border: 1px solid #334155;
        margin: 32px 0 48px 0;
        box-shadow: 0 8px 24px rgba(0,0,0,0.45);
        color: #e2e8f0;
    }

    .response-box h2 {
        color: #60a5fa;                     /* blue-400 */
        margin-bottom: 1.3rem;
    }

    .response-box p,
    .response-box li,
    .response-box hr {
        color: #cbd5e1;
    }

    .response-box small {
        color: #94a3b8;
    }

    hr {
        border-color: #334155;
        margin: 2rem 0;
    }

    /* Footer */
    .footer {
        margin-top: 64px;
        padding: 24px;
        font-size: 14px;
        text-align: center;
        color: #94a3b8;
        border-top: 1px solid #334155;
        background-color: #0f172a;
    }

    /* Streamlit elements adjustments */
    .stSpinner > div > div {
        border-top-color: #60a5fa !important;
    }

    .stSuccess {
        background-color: rgba(34, 197, 94, 0.15) !important;
        color: #86efac !important;
        border: 1px solid #166534 !important;
    }

    .stError {
        background-color: rgba(239, 68, 68, 0.15) !important;
        color: #fca5a5 !important;
        border: 1px solid #7f1d1d !important;
    }
</style>
    """,
    unsafe_allow_html=True,
)

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/201/201623.png", width=120
    )
    st.markdown("## 🌍 AI Travel Planner")
    st.markdown("Plan your perfect trip using an intelligent travel agent.")
    st.markdown("---")
    st.markdown("### ✨ Example Queries")
    st.markdown(
        """
        - Plan a 5-day trip to Goa  
        - Create a budget trip to Paris  
        - Family trip to Kerala for 7 days  
        - Solo travel to Japan  
        """
    )
    st.markdown("---")
    st.markdown("### ⚙️ System Status")
    st.success("Backend: Connected")
    st.markdown("---")
    st.markdown("Made with ❤️ by Ashish")

# ------------------ MAIN UI ------------------
st.markdown('<div class="title-text">✈️ AI Travel Planner</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle-text">Tell me where you want to go and I’ll plan your trip!</div>',
    unsafe_allow_html=True,
)

# Chat input box
with st.form(key="query_form", clear_on_submit=True):
    st.markdown("### 💬 Ask your travel agent")
    user_input = st.text_input(
        "Your Travel Request",
        placeholder="e.g. Plan a trip to Goa for 5 days with budget hotels",
    )
    submit_button = st.form_submit_button("🚀 Generate Plan")

# ------------------ API CALL ------------------
if submit_button and user_input.strip():
    try:
        with st.spinner("🧠 Planning your trip..."):
            payload = {"query": user_input}
            response = requests.post(
                f"{BASE_URL}/query",
                json=payload,
                timeout=300,
            )

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

            st.markdown(
                f"""
                <div class="response-box">
                <h2>🌍 Your AI Travel Plan</h2>
                <p><b>🕒 Generated:</b> {timestamp}</p>
                <p><b>🤖 Agent:</b> Atriyo's Travel AI</p>
                <hr>
                {answer.replace("\n", "<br>")}
                <hr>
                <small>
                ⚠️ This plan is AI-generated. Please verify prices, bookings, and travel requirements.
                </small>
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:
            st.error(
                f"❌ Bot failed to respond "
                f"(status={response.status_code}): {response.text}"
            )

    except requests.RequestException as e:
        st.error(
            "❌ Cannot reach the backend. "
            "Is FastAPI running on http://localhost:8000?\n\n"
            f"Details: {e}"
        )
        st.stop()

    except Exception as e:
        st.error(f"❌ The response failed due to: {e}")
        st.stop()

# ------------------ FOOTER ------------------
st.markdown(
    """
    <div class="footer">
    ✈️ AI Travel Planner · Built with Streamlit + FastAPI  
    © 2026 Atriyo | Travel smarter, not harder.
    </div>
    """,
    unsafe_allow_html=True,
)
