import streamlit as st
from huggingface_hub import InferenceClient
import time
import random

# Set page configuration with expanded sidebar
st.set_page_config(
    page_title="FinGuide Chatbot",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Get Hugging Face token from secrets or use placeholder
HF_TOKEN = st.secrets.get("HF_TOKEN", "your_hugging_face_token_here")

# Available Granite models
GRANITE_MODELS = {
    "Granite-3.0-2B-Instruct": "ibm-granite/granite-3.0-2b-instruct",
    "Granite-3.0-8B-Instruct": "ibm-granite/granite-3.0-8b-instruct",
    "Granite-3.1-8B-Instruct": "ibm-granite/granite-3.1-8b-instruct"
}

# Initialize Hugging Face Inference API client
@st.cache_resource
def get_client(model_name):
    return InferenceClient(
        model=model_name,
        token=HF_TOKEN
    )

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2e86de;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #576574;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sidebar-header {
        font-size: 1.8rem;
        color: #2e86de;
        text-align: center;
        margin-bottom: 1.5rem;
        padding-bottom: 10px;
        border-bottom: 2px solid #2e86de;
    }
    .chat-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid #2e86de;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 12px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 3px solid #2e86de;
    }
    .bot-message {
        background-color: #ffffff;
        padding: 12px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 3px solid #10ac84;
    }
    .stButton>button {
        background-color: #2e86de;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 24px;
        font-weight: 600;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1c6cb0;
        color: white;
    }
    .budget-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .feature-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #2e86de;
    }
    .example-prompt {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 8px;
        margin: 8px 0;
        cursor: pointer;
        border-left: 3px solid #2e86de;
    }
    .example-prompt:hover {
        background-color: #bbdefb;
    }
    .model-selector {
        background-color: #f1f8ff;
        padding: 10px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .css-1d391kg { 
        display: none; 
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "ibm-granite/granite-3.0-2b-instruct"

# Sidebar content
with st.sidebar:
    # Add FinGuide header
    st.markdown('<div class="sidebar-header">FinGuide</div>', unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Model Settings")
    st.markdown('<div class="model-selector">', unsafe_allow_html=True)
    selected_model_name = st.selectbox(
        "Choose AI Model:",
        options=list(GRANITE_MODELS.keys()),
        index=0
    )
    st.session_state.selected_model = GRANITE_MODELS[selected_model_name]
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 Budget Planner")
    st.markdown("Track your income and expenses")
    
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
    st.markdown("""
    <div class="feature-card">
        <strong>Emergency Fund</strong>
        <p>Save 3-6 months of expenses for emergencies</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <strong>50/30/20 Rule</strong>
        <p>50% needs, 30% wants, 20% savings/investments</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <strong>Debt Management</strong>
        <p>Pay off high-interest debt first</p>
    </div>
    """, unsafe_allow_html=True)

# Main content area
st.markdown('<h1 class="main-header">Personal Finance Chatbot</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your AI-powered personal finance assistant</p>', unsafe_allow_html=True)

# Display chat messages from history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">👤 <strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">🤖 <strong>FinSmart:</strong> {message["content"]}</div>', unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("💡 Ask about savings, budgeting, investments...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    st.markdown(f'<div class="user-message">👤 <strong>You:</strong> {user_input}</div>', unsafe_allow_html=True)
    
    # Generate response
    with st.spinner("FinSmart is analyzing your query..."):
        try:
            # Create prompt for the model
            prompt = f"""<|system|>
You are FinSmart, a helpful financial advisor. Provide clear, practical advice about personal finance, budgeting, savings, and investments. Keep responses concise but informative (around 200-300 words). If the question is not related to finance, politely decline to answer.

<|user|>
{user_input}

<|assistant|>
"""
            
            # Get response from the model
            client = get_client(st.session_state.selected_model)
            response = client.text_generation(
                prompt=prompt,
                max_new_tokens=500,
                temperature=0.7,
                do_sample=True,
                return_full_text=False
            )
            
            # Clean up the response
            cleaned_response = response.strip()
            if "<|endoftext|>" in cleaned_response:
                cleaned_response = cleaned_response.split("<|endoftext|>")[0].strip()
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": cleaned_response})
            
            # Display assistant response
            st.markdown(f'<div class="bot-message">🤖 <strong>FinSmart:</strong> {cleaned_response}</div>', unsafe_allow_html=True)
            
        except Exception as e:
            error_msg = "I apologize, but I'm experiencing technical difficulties. Please try a different question or try again later."
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.markdown(f'<div class="bot-message">🤖 <strong>FinSmart:</strong> {error_msg}</div>', unsafe_allow_html=True)
            st.error(f"Error: {str(e)}")

# Main content area
st.markdown("---")
st.markdown("### 📈 Popular Financial Questions")

col1, col2 = st.columns(2)

with col1:
    if st.button("How to start investing?"):
        st.session_state.messages.append({"role": "user", "content": "How to start investing?"})
        st.session_state.messages.append({"role": "assistant", "content": "Start investing by: 1) Setting clear financial goals, 2) Building an emergency fund first, 3) Understanding your risk tolerance, 4) Starting with low-cost index funds or ETFs, 5) Considering SIPs for mutual funds, and 6) Diversifying your portfolio. Begin with small amounts and gradually increase as you learn more."})
        st.rerun()
    
    if st.button("Best ways to save money?"):
        st.session_state.messages.append({"role": "user", "content": "Best ways to save money?"})
        st.session_state.messages.append({"role": "assistant", "content": "Effective saving strategies include: 1) Pay yourself first (automate savings), 2) Follow a budget, 3) Reduce unnecessary expenses, 4) Cook at home more often, 5) Use cashback and discount apps, 6) Set specific savings goals, and 7) Review subscriptions regularly. Even small daily savings can add up significantly over time."})
        st.rerun()

with col2:
    if st.button("How to create a budget?"):
        st.session_state.messages.append({"role": "user", "content": "How to create a budget?"})
        st.session_state.messages.append({"role": "assistant", "content": "To create an effective budget: 1) Track your income and expenses for a month, 2) Categorize expenses (needs vs wants), 3) Set spending limits for each category, 4) Use the 50/30/20 rule as a guideline, 5) Use budgeting apps or spreadsheets, 6) Review and adjust monthly, and 7) Include savings as a non-negotiable expense. Remember, a budget is a plan for your money, not a restriction."})
        st.rerun()
    
    if st.button("Managing debt effectively?"):
        st.session_state.messages.append({"role": "user", "content": "Managing debt effectively?"})
        st.session_state.messages.append({"role": "assistant", "content": "To manage debt effectively: 1) List all debts with interest rates, 2) Prioritize high-interest debt first (avalanche method), 3) Consider debt consolidation if beneficial, 4) Negotiate lower interest rates with lenders, 5) Avoid taking on new debt, 6) Create a repayment plan with timelines, and 7) Build an emergency fund to prevent new debt. Always pay more than the minimum payment when possible."})
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; font-size: 0.9rem;">
    <p>FinGuide Chatbot • Powered by IBM Granite Model • Your financial wellness partner</p>
    <p>Disclaimer: This is an AI assistant. For personalized financial advice, consult a certified financial planner.</p>
</div>
""", unsafe_allow_html=True)
