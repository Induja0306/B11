import streamlit as st
import os
from huggingface_hub import InferenceClient

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="FinGuide Chatbot",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 🔑 Hugging Face token (loaded from secrets or env)
HF_TOKEN = st.secrets.get("HF_TOKEN") or os.getenv("HF_TOKEN")

# 🎯 Model (Zephyr supports conversational mode)
MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"

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
    st.markdown(f"**Current Model:** {MODEL_NAME}")
    st.markdown("A powerful financial AI assistant specialized in personal finance topics.")

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
            <p><strong>Savings:</strong> ${savings:,} ({savings_perc_
