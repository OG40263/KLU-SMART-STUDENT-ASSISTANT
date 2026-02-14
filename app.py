import streamlit as st
import google.generativeai as genai
import requests
from streamlit_lottie import st_lottie

# --- 1. SETUP & BRAIN ---
API_KEY = "AIzaSyDKFx3vTpyYvjBUldvnrFj6TIIMAGga4vc" 
genai.configure(api_key=API_KEY)
# Using 'gemini-1.5-flash' for the best stability on Free Tier
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. CONFIG & STYLING ---
st.set_page_config(page_title="KLU Assistant", layout="wide", page_icon="🤖")

def load_lottieurl(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# Aesthetic robot animation
lottie_ai = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_at6aymiz.json")

# Custom CSS for that professional "KLU Red" feel
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stChatMessage"] {
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        background-color: white;
    }
    /* Official KLU Red for the progress bar */
    .stProgress > div > div > div > div { background-color: #B91C2E; }
    footer {visibility: hidden;}
    .footer-text {
        text-align: center; color: #888; padding: 20px; font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: KLU CALCULATOR ---
with st.sidebar:
    if lottie_ai:
        st_lottie(lottie_ai, height=150, key="sidebar_bot")
    
    st.title("📊 KLU Calculator")
    st.info("Goal: 75%+")
    
    # Grid layout for inputs
    col1, col2 = st.columns(2)
    with col1:
        l = st.number_input("Lecture %", 0, 100, 80, key="L")
        t = st.number_input("Tutorial %", 0, 100, 80, key="T")
    with col2:
        p = st.number_input("Practical %", 0, 100, 80, key="P")
        s = st.number_input("Skilling %", 0, 100, 80, key="S")
    
    # Official KLU Weighted Formula
    weighted = ((l * 100) + (t * 25) + (p * 50) + (s * 25)) / 200
    
    if weighted < 75:
        st.error(f"Status: {weighted}% (Detained)")
    else:
        st.success(f"Status: {weighted}% (Safe)")

# --- 4. MAIN INTERFACE ---
st.title("🤖 KLU Smart Assistant")

# Tabs for a clean UX
tab1, tab2 = st.tabs(["💬 Assistant", "📈 Performance Tracker"])

with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about KLU life..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Feeding your attendance context to the AI
            full_context = f"Student Attendance: {weighted}%. Prompt: {prompt}"
            try:
                response = model.generate_content(full_context)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception:
                st.error("Wait 60 seconds... Quota limit reached.")

with tab2:
    st.subheader("Attendance Health Overview")
    st.progress(weighted / 100)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Overall", f"{weighted}%")
    m2.metric("Target", "75%")
    m3.metric("Margin", f"{round(weighted-75, 2)}%", delta_color="normal")
    
    st.write("---")
    st.markdown("### 💡 AI Recommendations")
    if weighted < 75:
        st.warning("Prioritize your **Lecture** and **Practical** hours this week to reach 75%.")
    else:
        st.success("You are in the green zone! Maintaining this will keep you safe for end-exams.")

st.markdown("<div class='footer-text'>Developed by 40263 | KLU Assistant v2.0</div>", unsafe_allow_html=True)