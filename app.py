import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

API_KEY = "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"

if not API_KEY:
    st.error("GROQ_API_KEY is missing from your .env file.")
    st.stop()

client = Groq(api_key=API_KEY)

MODEL = "openai/gpt-oss-120b"


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="StudyMate AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* Remove Streamlit default spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128,128,128,0.2);
}

/* Logo */
.logo {
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 0;
}

.logo-subtitle {
    font-size: 13px;
    opacity: 0.6;
    margin-top: -5px;
}

/* Hero */
.hero {
    padding: 30px 10px 20px 10px;
}

.hero h1 {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.hero p {
    font-size: 18px;
    opacity: 0.65;
}

/* Cards */
.card {
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(128,128,128,0.2);
    min-height: 130px;
    transition: 0.2s;
}

.card:hover {
    border-color: rgba(128,128,128,0.5);
}

.card-title {
    font-size: 20px;
    font-weight: 700;
}

.card-text {
    font-size: 14px;
    opacity: 0.65;
}

/* Chat */
[data-testid="stChatMessage"] {
    border-radius: 15px;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}

/* Divider */
.divider {
    height: 1px;
    background: rgba(128,128,128,0.2);
    margin: 25px 0;
}

/* Footer */
.footer {
    text-align: center;
    font-size: 12px;
    opacity: 0.5;
    padding-top: 30px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "learning_mode" not in st.session_state:
    st.session_state.learning_mode = "General Tutor"


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="logo">🎓 StudyMate</div>
        <div class="logo-subtitle">
        Your intelligent academic companion
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='divider'></div>",
                unsafe_allow_html=True)

    # New chat
    if st.button(
        "＋  New Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### 📚 Learning Mode")

    mode = st.selectbox(
        "How should StudyMate help?",
        [
            "General Tutor",
            "Explain a Topic",
            "Assignment Helper",
            "Quiz Generator",
            "Summarizer",
            "Programming Tutor",
            "Statistics Tutor"
        ],
        label_visibility="collapsed"
    )

    st.session_state.learning_mode = mode

    st.markdown("<div class='divider'></div>",
                unsafe_allow_html=True)

    st.markdown("### 💡 StudyMate")

    st.caption(
        "Ask questions, understand difficult concepts, "
        "practice with quizzes, and improve your learning."
    )

    st.markdown("<div class='divider'></div>",
                unsafe_allow_html=True)

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        """
        <div style="
            position: fixed;
            bottom: 20px;
            font-size: 12px;
            opacity: 0.5;
        ">
        StudyMate AI • Powered by Groq
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = f"""
You are StudyMate AI, an intelligent academic assistant
designed to help university and college students learn.

Current learning mode:
{st.session_state.learning_mode}

Your goals:

1. Help students genuinely understand concepts.
2. Explain difficult ideas using simple language.
3. Use examples and analogies where useful.
4. Break complicated problems into clear steps.
5. For mathematics and statistics, show calculations step-by-step.
6. For programming questions, explain the code and why it works.
7. For assignments, guide the student rather than encouraging
   blind copying.
8. For quizzes, provide useful questions and explanations.
9. For summaries, identify the most important points.
10. Maintain conversation context.
11. If you don't know something, say so rather than inventing facts.
12. Be friendly, encouraging and academically responsible.

Your responses should be well structured using headings,
bullet points, tables or examples when appropriate.
"""


# =========================================================
# WELCOME SCREEN
# =========================================================

if len(st.session_state.messages) == 0:

    st.markdown(
        """
        <div class="hero">

        <h1>👋 Hello, Student!</h1>

        <p>
        What would you like to learn today?
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🚀 Quick Start")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="card">

            <div class="card-title">
            📚 Explain a Topic
            </div>

            <div class="card-text">
            Turn difficult academic concepts
            into simple explanations.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Try it",
            key="explain",
            use_container_width=True
        ):
            st.session_state.messages.append({
                "role": "user",
                "content":
                "Explain hypothesis testing to me like I'm a beginner."
            })
            st.rerun()

    with col2:
        st.markdown(
            """
            <div class="card">

            <div class="card-title">
            🧠 Practice Quiz
            </div>

            <div class="card-text">
            Generate practice questions
            and test your understanding.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Try it",
            key="quiz",
            use_container_width=True
        ):
            st.session_state.messages.append({
                "role": "user",
                "content":
                "Create a 5-question quiz on introductory statistics."
            })
            st.rerun()

    with col3:
        st.markdown(
            """
            <div class="card">

            <div class="card-title">
            💻 Coding Help
            </div>

            <div class="card-text">
            Understand programming concepts,
            errors and algorithms.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Try it",
            key="coding",
            use_container_width=True
        ):
            st.session_state.messages.append({
                "role": "user",
                "content":
                "Explain Python functions to me with examples."
            })
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.info(
        "💡 Tip: The more specific your question is, "
        "the more useful your answer will be."
    )


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "Ask StudyMate anything about your studies..."
)


# =========================================================
# PROCESS USER MESSAGE
# =========================================================

if user_input:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare conversation
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(
        st.session_state.messages
    )

    # Generate response
    with st.chat_message("assistant"):

        try:

            stream = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.4,
                max_completion_tokens=2048,
                stream=True
            )

            response_placeholder = st.empty()

            full_response = ""

            for chunk in stream:

                text = chunk.choices[0].delta.content

                if text:
                    full_response += text

                    response_placeholder.markdown(
                        full_response + "▌"
                    )

            response_placeholder.markdown(
                full_response
            )

        except Exception as e:

            full_response = (
                "Sorry, I couldn't process your request."
            )

            st.error(f"Error: {e}")

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
    StudyMate AI • An AI-powered learning assistant
    </div>
    """,
    unsafe_allow_html=True
)
