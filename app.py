import streamlit as st
from groq import Groq
import base64
import time

# --- 1. CONFIG & PREMIUM MATERIAL 3 CSS ---
st.set_page_config(page_title="MathIsEZ Ultra", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* Animated Gradient Background */
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #111827, #0f172a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #f1f5f9;
    }
    
    .title-text {
        background: linear-gradient(to right, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 45px; font-weight: 900;
    }

    /* Glassmorphism Cards */
    .m3-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 24px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }
    .m3-card:hover {
        transform: translateY(-5px);
        border: 1px solid #3b82f6;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    .ans-glow {
        background: rgba(16, 185, 129, 0.1);
        border: 2px solid #10b981;
        color: #34d399;
        padding: 30px;
        border-radius: 20px;
        font-size: 35px;
        font-weight: 800;
        text-align: center;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
    }

    .stButton>button {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        color: white; border-radius: 100px; border: none;
        padding: 10px 25px; font-weight: bold; width: 100%;
        transition: 0.3s;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. STATE MANAGEMENT ---
if 'history' not in st.session_state: st.session_state.history = []
if 'notes' not in st.session_state: st.session_state.notes = "Formulas:\n- Quadratic: x = (-b ± √(b² - 4ac)) / 2a"

# --- 3. SIDEBAR (AUTHENTICATION & NAV) ---
with st.sidebar:
    st.markdown('<h2 class="title-text" style="font-size:25px;">MathIsEZ</h2>', unsafe_allow_html=True)
    
    # SAFE API KEY INPUT (Prevents GitHub block)
    USER_API_KEY = st.text_input("🔑 Groq API Key", type="password", placeholder="gsk_...")
    st.caption("Get your key at console.groq.com")
    
    st.divider()
    nav = st.radio("Navigation", ["🏠 Home Dashboard", "🚀 Scan & Solve", "🧪 Lab Tools", "📚 Library", "📝 My Notes"])
    
    st.divider()
    if st.button("🗑️ Clear Session History"):
        st.session_state.history = []
        st.rerun()

# --- 4. MODULES ---

if nav == "🏠 Home Dashboard":
    st.markdown('<h1 class="title-text">Dashboard</h1>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="m3-card"><h3>Calculations</h3><h1>{len(st.session_state.history)}</h1><p>Solved this session</p></div>', unsafe_allow_html=True)
    with col2:
        engine_status = "Optimal" if USER_API_KEY else "Awaiting Key"
        st.markdown(f'<div class="m3-card"><h3>AI Engine</h3><p>Llama-3.2 Vision</p><p>Status: <span style="color:#3b82f6">{engine_status}</span></p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="m3-card"><h3>Sync</h3><p>Proposal Repo</p><p>Status: <span style="color:#10b981">Online</span></p></div>', unsafe_allow_html=True)

elif nav == "🚀 Scan & Solve":
    st.markdown('<h1 class="title-text">Visual Solver</h1>', unsafe_allow_html=True)
    
    if not USER_API_KEY:
        st.info("💡 Please enter your Groq API Key in the sidebar to activate the AI Solver.")
    else:
        l, r = st.columns([1, 1.2])
        with l:
            st.markdown('<div class="m3-card">', unsafe_allow_html=True)
            img = st.file_uploader("Upload Image", type=['png','jpg','jpeg'])
            if not img: img = st.camera_input("Camera Scanner")
            st.markdown('</div>', unsafe_allow_html=True)

        if img:
            with l:
                st.image(img, use_container_width=True)
                btn = st.button("🚀 DECODE & SOLVE")
            
            if btn:
                with r:
                    try:
                        client = Groq(api_key=USER_API_KEY)
                        b64 = base64.b64encode(img.getvalue()).decode('utf-8')
                        with st.spinner("⚡ AI is calculating..."):
                            response = client.chat.completions.create(
                                model="llama-3.2-11b-vision-preview",
                                messages=[{"role": "user", "content": [
                                    {"type": "text", "text": "Solve this. Format: FINAL: [Ans], STEP 1: [Title]|[Desc]"},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                                ]}]
                            )
                        ans = response.choices[0].message.content
                        st.balloons()
                        for line in ans.split("\n"):
                            if "FINAL:" in line:
                                val = line.replace("FINAL:", "").strip()
                                st.markdown(f'<div class="ans-glow">{val}</div>', unsafe_allow_html=True)
                                st.session_state.history.append(val)
                            elif "STEP" in line and "|" in line:
                                t, d = line.split("|")
                                st.markdown(f'<div class="m3-card"><h4>{t}</h4><p>{d}</p></div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Authentication Error: Ensure your API key is correct.")

elif nav == "🧪 Lab Tools":
    st.markdown('<h1 class="title-text">Lab Tools</h1>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔢 Scientific", "⚖️ Converter"])
    with t1:
        st.markdown('<div class="m3-card">', unsafe_allow_html=True)
        eq = st.text_input("Formula Input (e.g., 25*4)")
        if st.button("Calculate"):
            try: st.success(f"Result: {eval(eq)}")
            except: st.error("Invalid Formula")
        st.markdown('</div>', unsafe_allow_html=True)
    with t2:
        st.markdown('<div class="m3-card">', unsafe_allow_html=True)
        num = st.number_input("Value", value=1.0)
        st.write(f"**{num}** Kilometers is **{num * 0.621:.2f}** Miles")
        st.markdown('</div>', unsafe_allow_html=True)

elif nav == "📚 Library":
    st.markdown('<h1 class="title-text">Math Library</h1>', unsafe_allow_html=True)
    st.markdown('<div class="m3-card"><h4>Isaac Newton</h4><p>The father of Calculus and the laws of motion.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="m3-card"><h4>Quadratic Formula</h4><code>x = [-b ± sqrt(b² - 4ac)] / 2a</code></div>', unsafe_allow_html=True)

elif nav == "📝 My Notes":
    st.markdown('<h1 class="title-text">Notebook</h1>', unsafe_allow_html=True)
    st.session_state.notes = st.text_area("Observations:", value=st.session_state.notes, height=350)
    if st.button("Save Notes"): st.toast("Notes saved to local session!")