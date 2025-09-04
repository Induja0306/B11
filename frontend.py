import os
import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# --------------------------------------------------
# LOAD ENV VARIABLES
# --------------------------------------------------
load_dotenv()  # loads from .env file (not pushed to GitHub)

HF_TOKEN = os.getenv("HF_TOKEN")  # secret is stored in environment
MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="FinGuide Chatbot",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CLIENT
# --------------------------------------------------
@st.cache_resource
def get_client():
    return InferenceClient(
        model=MODEL_NAME,
        token=HF_TOKEN
    )

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>
    .main-header { font-size: 3rem; color: #2e86de; text-align: center; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.2rem; color: #576574; text-align: center; margin-bottom: 2rem; }
    .sidebar-header { font-size: 1.8rem; color: #2e86de; text-align: center; margin-bottom: 1.5rem; padding-bottom: 10px; border-bottom: 2px solid #2e86de; }
    .chat-container { background-color: #f8f9fa; border-radius: 10px; padding: 20px; margin-bottom: 20px; border-left: 5px solid #2e86de; }
    .user-message { background-color: #e3f2fd; padding: 12px; border-radius: 10px; margin: 10px 0; border-left: 3px solid #2e86de; }
    .bot-message { background-color: #ffffff; padding: 12px; border-radius: 10px; margin: 10px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-left: 3px solid #10ac84; }
    .stButton>button { background-color: #2e86de; color: white; border: none; border-radius: 5px; padding: 10px 24px; font-weight: 600; width: 100%; }
    .stButton>button:hover { background-color: #1c6cb0; color: white; }
    .budget-card { background-color: #ffffff; padding: 15px; border-radius: 10px; margin: 10px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .feature-card { background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #2e86de; }
    .example-prompt { background-color: #e3f2fd; padding: 10px; border-radius: 8px; margin: 8px 0; cursor: pointer; border-left: 3px solid #2e86de; }
    .example-prompt:hover { background-color: #bbdefb; }
    .model-info { background-color: #f1f8ff; padding: 10px; border-radius: 8px; margin: 10px 0; }
    .css-1d391kg { display: none; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-header">FinGuide</div>', unsafe_allow_html=True)

    st.markdown("### ⚙️ Model Information")
    st.markdown('<div class="model-info">', unsafe_allow_html=True)
    st.markdown(f"**Current Model:** {MODEL_NAME}")
    st.markdown("A powerful financial AI assistant specialized in personal finance topics.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Budget Planner")

    income = st.number_input("Monthly Income ($)", min_value=0, value=50000, step=1000)
    expenses = st.number_input("Monthly Expenses ($)", min_value=0, value=30000, step=1000)

    if income > 0:
        savings = income - expenses
        savings_percent = (savings / income) * 100 if income > 0 else 0
        st.markdown(f"""
        <div class="budget-card">
            <h4>Your Financial Summary</h4>
            <p><strong>Income:</strong> ${income:,}</p>
            <p><strong>Expenses:</strong> ${expenses:,}</p>
            <p><strong>Savings:</strong> ${savings:,} ({savings_percent:.1f}%)</p>
        </div>
        """, unsafe_allow_html=True)

        if savings < 0:
            st.error("You're spending more than you earn! Consider reducing expenses.")
        elif savings_percent < 20:
            st.warning("Try to save at least 20% of your income for better financial health.")
        else:
            st.success("Great job! You're saving a healthy portion of your income.")

    st.markdown("---")
    st.markdown("### 💡 Financial Tips")
    st.markdown("""<div class="feature-card"><strong>Emergency Fund</strong><p>Save 3-6 months of expenses for emergencies</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="feature-card"><strong>50/30/20 Rule</strong><p>50% needs, 30% wants, 20% savings/investments</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="feature-card"><strong>Debt Management</strong><p>Pay off high-interest debt first</p></div>""", unsafe_allow_html=True)

# --------------------------------------------------
# MAIN CONTENT
# --------------------------------------------------
st.markdown('<h1 class="main-header">Personal Finance Chatbot</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your AI-powered personal finance assistant</p>', unsafe_allow_html=True)

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">👤 <strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">🤖 <strong>FinSmart:</strong> {message["content"]}</div>', unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("💡 Ask about savings, budgeting, investments...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="user-message">👤 <strong>You:</strong> {user_input}</div>', unsafe_allow_html=True)

    with st.spinner("FinSmart is analyzing your query..."):
        try:
            client = get_client()

            messages = [
                {"role": "system", "content": "You are FinSmart, a professional personal-finance advisor. Keep answers concise, no more than 120 words."},
                {"role": "user", "content": user_input},
            ]

            resp = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                max_tokens=140,
                temperature=0.15,
                top_p=0.9
            )

            cleaned_response = resp.choices[0].message["content"].strip()

            st.session_state.messages.append({"role": "assistant", "content": cleaned_response})
            st.markdown(f'<div class="bot-message">🤖 <strong>FinSmart:</strong> {cleaned_response}</div>', unsafe_allow_html=True)

        except Exception as e:
            error_msg = "I’m having technical difficulties. Please try again later."
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.error(f"Error: {str(e)}")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; font-size: 0.9rem;">
    <p>FinGuide Chatbot • Powered by HuggingFaceH4/zephyr-7b-beta • Your financial wellness partner</p>
    <p>Disclaimer: This is an AI assistant. For personalized financial advice, consult a certified financial planner.</p>
</div>
""", unsafe_allow_html=True)
