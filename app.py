import streamlit as st
import google.generativeai as genai
import requests
from streamlit_lottie import st_lottie

# --- 1. SECURE CONFIGURATION ---
# Accessing the key from Streamlit Secrets for 100% security
API_KEY = st.secrets["GEMINI_API_KEY"] 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. AESTHETIC UI SETUP ---
st.set_page_config(page_title="KLU Student Assistant", layout="wide", page_icon="🤖")

def load_lottieurl(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# Anonymous Robot Animation
lottie_ai = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_at6aymiz.json")

# Modern CSS: Glassmorphism & Anonymous Footer
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .stProgress > div > div > div > div { background-color: #B91C2E; }
    footer {visibility: hidden;}
    .custom-footer {
        text-align: center; padding: 20px; color: #888; font-size: 13px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: ANONYMOUS CALCULATOR ---
with st.sidebar:
    if lottie_ai:
        st_lottie(lottie_ai, height=150, key="bot_anim")
    
    st.title("📊 Attendance Calc")
    st.caption("Official KLU LTPS Weighted Formula")
    
    c1, c2 = st.columns(2)
    with c1:
        l = st.number_input("Lecture %", 0, 100, 80, key="L")
        t = st.number_input("Tutorial %", 0, 100, 80, key="T")
    with c2:
        p = st.number_input("Practical %", 0, 100, 80, key="P")
        s = st.number_input("Skilling %", 0, 100, 80, key="S")
    
    weighted = ((l * 100) + (t * 25) + (p * 50) + (s * 25)) / 200
    
    if weighted < 75:
        st.error(f"Status: {weighted}% (Detained)")
    else:
        st.success(f"Status: {weighted}% (Safe)")

# --- 4. MAIN INTERFACE ---
st.title("🤖 KLU Smart Assistant")

tab1, tab2 = st.tabs(["💬 AI Assistant", "📈 Attendance Tracker"])

with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me about KLU..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Anonymous context
            full_context = f"Context: I am a KLU student. My current weighted attendance is {weighted}%. Prompt: {prompt}"
            try:
                response = model.generate_content(full_context)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error("AI is resting. Try again in 60s.")

with tab2:
    st.subheader("Performance Dashboard")
    st.progress(weighted / 100)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Current", f"{weighted}%")
    m2.metric("Target", "75%")
    m3.metric("Margin", f"{round(weighted-75, 2)}%")
    
    st.write("---")
    st.markdown("### 💡 AI Recommendations")
    if weighted < 75:
        st.warning("Prioritize Lecture and Practical components to boost your score above 75%.")
    else:
        st.success("You are meeting the university requirements. Maintain this consistency.")

# Anonymous Footer
st.markdown("<div class='custom-footer'>Created by KLU Student Community | v2.0</div>", unsafe_allow_html=True)
    
   


