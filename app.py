import streamlit as st
from groq import Groq
import base64
import time

# --- 1. CONFIG & PREMIUM CSS ---
st.set_page_config(page_title="MathIsEZ Ultra", page_icon="⚡", layout="wide")

# Replace with your key: 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
GROQ_API_KEY = "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" 

st.markdown("""
    <style>
    /* Main Background - Deep Midnight */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        color: #f1f5f9;
    }
    
    /* Custom Glassmorphism Card */
    .m3-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease, border 0.3s ease;
        margin-bottom: 20px;
    }
    .m3-card:hover {
        transform: translateY(-5px);
        border: 1px solid #3b82f6;
    }
    
    /* Glowing Result Box */
    .ans-glow {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
        border: 2px solid #10b981;
        color: #34d399;
        padding: 30px;
        border-radius: 20px;
        font-size: 40px;
        font-weight: 900;
        text-align: center;
        box-shadow: 0 0 30px rgba(16, 185, 129, 0.3);
        margin: 20px 0;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Interactive Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        color: white;
        border-radius: 100px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC INITIALIZATION ---
if 'history' not in st.session_state: st.session_state.history = []

def call_ai(image_b64):
    client = Groq(api_key=GROQ_API_KEY)
    try:
        response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[{"role": "user", "content": [
                {"type": "text", "text": "Solve this. Format: FINAL: [Ans], STEP 1: [Title]|[Desc]"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]}]
        )
        return response.choices[0].message.content
    except Exception as e: return f"ERROR: {str(e)}"

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🧮 MathIsEZ")
    st.caption("poetry of logical ideas")
    nav = st.radio("Navigation", ["🏠 Home", "🚀 Scan & Solve", "🧪 Lab Tools", "📚 Library", "📝 Notes"])
    
    st.divider()
    st.subheader("📋 Session Log")
    for h in reversed(st.session_state.history):
        st.markdown(f"✅ `{h}`")

# --- 4. MODULES ---

# --- HOME DASHBOARD ---
if nav == "🏠 Home":
    st.title("Welcome to MathIsEZ Ultra ⚡")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="m3-card"><h3>Calculations</h3><h1>12</h1><p>Solved this week</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="m3-card"><h3>Engine</h3><p>Groq Llama 3.2</p><p>Status: <span style="color:#10b981">Online</span></p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="m3-card"><h3>Sync</h3><p>Android Device</p><p>Status: <span style="color:#3b82f6">Linked</span></p></div>', unsafe_allow_html=True)

# --- SCAN TO SOLVE ---
elif nav == "🚀 Scan & Solve":
    st.title("AI Visual Solver ✨")
    left, right = st.columns([1, 1.2])
    
    with left:
        st.markdown('<div class="m3-card">', unsafe_allow_html=True)
        img = st.file_uploader("Upload Image", type=['png','jpg','jpeg'])
        if not img: img = st.camera_input("Scanner")
        st.markdown('</div>', unsafe_allow_html=True)

    if img:
        with left:
            st.image(img, use_container_width=True)
            run_btn = st.button("INITIATE HYPERDRIVE")
        
        if run_btn:
            with right:
                p = st.progress(0)
                for i in range(101): time.sleep(0.005); p.progress(i)
                
                b64 = base64.b64encode(img.getvalue()).decode('utf-8')
                res = call_ai(b64)
                
                if "ERROR" not in res:
                    st.balloons()
                    for line in res.split("\n"):
                        if "FINAL:" in line:
                            val = line.replace("FINAL:", "").strip()
                            st.markdown(f'<div class="ans-glow">{val}</div>', unsafe_allow_html=True)
                            st.session_state.history.append(val)
                        elif "STEP" in line and "|" in line:
                            t, d = line.split("|")
                            st.markdown(f'<div class="m3-card"><h4>{t}</h4><p>{d}</p></div>', unsafe_allow_html=True)
                else:
                    st.error("Connection Failed. Check API Key.")

# --- OTHER BOXES (Filled) ---
elif nav == "🧪 Lab Tools":
    st.title("Smart Lab 🧪")
    st.markdown('<div class="m3-card"><h4>Unit Converter</h4><p>Convert area, volume, and mass using MVVM logic.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="m3-card"><h4>Scientific Calc</h4><p>High-precision trigonometry and calculus tools.</p></div>', unsafe_allow_html=True)

elif nav == "📚 Library":
    st.title("Knowledge Vault 📚")
    st.markdown('<div class="m3-card"><h4>The Mathematicians</h4><p>Learn about Gauss, Euler, and Ramanujan.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="m3-card"><h4>PDF Resources</h4><p>Access Algebra and Geometry textbooks.</p></div>', unsafe_allow_html=True)

elif nav == "📝 Notes":
    st.title("Study Notes 📝")
    st.text_area("Your Notes", placeholder="Write down formulas here...", height=400)
    st.button("Save to Device")