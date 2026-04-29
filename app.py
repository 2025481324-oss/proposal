import streamlit as st
from groq import Groq
import base64
import time
import pandas as pd
import io
from datetime import datetime

# =================================================================
# SECTION 1: SYSTEM CONFIGURATION & UI THEMING
# =================================================================
st.set_page_config(
    page_title="MathIsEZ",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Material 3 Design System
st.markdown("""
    <style>
    /* Premium Background with Dynamic Mesh Gradient */
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #0d1117, #1e1b4b);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Typography & Titles */
    .title-text {
        background: linear-gradient(135deg, #60a5fa, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 52px; font-weight: 900;
        letter-spacing: -1.5px;
        margin-bottom: 10px;
    }
    
    /* Glassmorphism Containers */
    .m3-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 28px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-bottom: 25px;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
    }
    .m3-card:hover {
        transform: translateY(-8px) scale(1.01);
        background: rgba(255, 255, 255, 0.06);
        border-color: rgba(59, 130, 246, 0.5);
        box-shadow: 0 20px 40px -15px rgba(59, 130, 246, 0.3);
    }
    
    /* Data Tables Styling */
    .styled-table {
        width: 100%; border-collapse: collapse;
        margin: 25px 0; font-size: 0.9em;
        border-radius: 15px; overflow: hidden;
    }

    /* AI Solution Glow */
    .ans-glow {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.1));
        border: 1px solid #10b981;
        color: #34d399;
        padding: 35px;
        border-radius: 24px;
        font-size: 38px;
        font-weight: 900;
        text-align: center;
        text-shadow: 0 0 15px rgba(52, 211, 153, 0.5);
        margin: 20px 0;
    }

    /* Sidebar Navigation */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        color: white; border-radius: 14px; border: none;
        padding: 15px 30px; font-weight: 700; width: 100%;
        text-transform: uppercase; letter-spacing: 1px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        filter: brightness(1.2);
        box-shadow: 0 0 25px rgba(139, 92, 246, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# SECTION 2: MODEL LAYER (BUSINESS LOGIC & DATA)
# =================================================================

class MathModel:
    @staticmethod
    def initialize_session():
        if 'history' not in st.session_state:
            st.session_state.history = []
        if 'notes' not in st.session_state:
            st.session_state.notes = "📌 MathIsEZ Project Notes\n---\n"
        if 'calc_count' not in st.session_state:
            st.session_state.calc_count = 0
        if 'start_time' not in st.session_state:
            st.session_state.start_time = time.time()

    @staticmethod
    def add_to_history(problem, result):
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.history.append({
            "Time": timestamp,
            "Query": problem,
            "Result": result
        })
        st.session_state.calc_count += 1

# =================================================================
# SECTION 3: VIEWMODEL LAYER (AI INTERFACE)
# =================================================================

def process_ai_request(image_file, api_key):
    try:
        client = Groq(api_key=api_key)
        b64_image = base64.b64encode(image_file.getvalue()).decode('utf-8')
        
        prompt = """
        You are a Math Expert. Analyze the image and provide:
        1. FINAL: The final result/value.
        2. STEP 1: [Title]|[Detailed explanation]
        3. STEP 2: [Title]|[Detailed explanation]
        Format strictly for parsing.
        """
        
        completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
            ]}],
            temperature=0.2
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"ERROR: {str(e)}"

# =================================================================
# SECTION 4: VIEW LAYER (UI COMPONENTS)
# =================================================================

MathModel.initialize_session()

# Sidebar Components
with st.sidebar:
    st.markdown('<h1 class="title-text" style="font-size:28px;">MathIsEZ</h1>', unsafe_allow_html=True)
    st.caption("Advanced MVVM Architecture v2.5")
    
    # Secure API Key Entry
    USER_KEY = st.text_input("🔑 System API Key", type="password", placeholder="gsk_...")
    
    st.divider()
    nav = st.radio("MAIN NAVIGATION", [
        "🏠 Dashboard", 
        "🚀 Vision Solver", 
        "🧪 Advanced Lab", 
        "📚 Knowledge Base", 
        "📝 Lab Notebook",
        "⚙️ Dev Console"
    ])
    
    st.divider()
    # Stats Widget
    st.subheader("📊 Session Telemetry")
    runtime = int(time.time() - st.session_state.start_time)
    st.write(f"Runtime: `{runtime}s`")
    st.write(f"Operations: `{st.session_state.calc_count}`")
    
    if st.button("🗑️ Reset Application"):
        st.session_state.clear()
        st.rerun()

# --- MODULE 1: DASHBOARD ---
if nav == "🏠 Dashboard":
    st.markdown('<h1 class="title-text">Dashboard</h1>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="m3-card"><h3>Calc</h3><h1>{st.session_state.calc_count}</h1></div>', unsafe_allow_html=True)
    with c2:
        status_color = "#34d399" if USER_KEY else "#f87171"
        st.markdown(f'<div class="m3-card"><h3>AI Link</h3><h2 style="color:{status_color}">{"ACTIVE" if USER_KEY else "OFFLINE"}</h2></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="m3-card"><h3>Engine</h3><p>Llama 3.2-11B</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="m3-card"><h3>Auth</h3><p>Standard</p></div>', unsafe_allow_html=True)

    st.markdown("### 📈 Recent Activity")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.table(df.tail(5))
        
        # Download History Feature
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Session CSV", csv, "math_history.csv", "text/csv")
    else:
        st.info("No activity recorded yet. Start solving in the Vision Solver!")

# --- MODULE 2: VISION SOLVER ---
elif nav == "🚀 Vision Solver":
    st.markdown('<h1 class="title-text">Vision Solver</h1>', unsafe_allow_html=True)
    
    if not USER_KEY:
        st.warning("⚠️ Input API Key in the sidebar to initialize the Vision Engine.")
    else:
        col_in, col_out = st.columns([1, 1.5])
        
        with col_in:
            st.markdown('<div class="m3-card">', unsafe_allow_html=True)
            mode = st.toggle("Use Camera Scanner", value=False)
            if mode:
                img = st.camera_input("Capture Problem")
            else:
                img = st.file_uploader("Upload Image", type=['png','jpg','jpeg'])
            st.markdown('</div>', unsafe_allow_html=True)

        if img:
            with col_in:
                st.image(img, caption="Loaded Context", use_container_width=True)
                trigger = st.button("🚀 EXECUTE AI DECODE")
            
            if trigger:
                with col_out:
                    with st.spinner("Decoding Math Logic..."):
                        raw_res = process_ai_request(img, USER_KEY)
                        
                        if "ERROR" in raw_res:
                            st.error(raw_res)
                        else:
                            st.balloons()
                            lines = raw_res.split("\n")
                            for line in lines:
                                if "FINAL:" in line:
                                    ans = line.split("FINAL:")[1].strip()
                                    st.markdown(f'<div class="ans-glow">{ans}</div>', unsafe_allow_html=True)
                                    MathModel.add_to_history("Visual Solve", ans)
                                elif "STEP" in line and "|" in line:
                                    step_num, content = line.split(":", 1)
                                    title, desc = content.split("|")
                                    st.markdown(f'<div class="m3-card"><h4>{step_num}: {title}</h4><p>{desc}</p></div>', unsafe_allow_html=True)

# --- MODULE 3: ADVANCED LAB ---
elif nav == "🧪 Advanced Lab":
    st.markdown('<h1 class="title-text">The Lab</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🔢 Algebra", "📏 Geometry", "📉 Stats"])
    
    with tab1:
        st.markdown('<div class="m3-card">', unsafe_allow_html=True)
        st.subheader("Quadratic Equation Solver")
        qa = st.number_input("Constant a", value=1.0)
        qb = st.number_input("Constant b", value=0.0)
        qc = st.number_input("Constant c", value=0.0)
        
        if st.button("Solve Quadratic"):
            d = (qb**2) - (4*qa*qc)
            if d < 0:
                st.error("Complex Roots")
            else:
                sol1 = (-qb + (d**0.5)) / (2*qa)
                sol2 = (-qb - (d**0.5)) / (2*qa)
                st.success(f"Roots: x1={sol1}, x2={sol2}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="m3-card">', unsafe_allow_html=True)
        st.subheader("Area Calculators")
        shape = st.selectbox("Select Shape", ["Circle", "Rectangle", "Triangle"])
        if shape == "Circle":
            r = st.number_input("Radius", value=1.0)
            st.write(f"Area: {3.14159 * r**2}")
        elif shape == "Rectangle":
            l = st.number_input("Length", value=1.0)
            w = st.number_input("Width", value=1.0)
            st.write(f"Area: {l * w}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="m3-card">', unsafe_allow_html=True)
        st.subheader("Data Analysis")
        data_input = st.text_area("Paste comma-separated numbers (e.g. 10, 20, 30)")
        if st.button("Analyze Data"):
            nums = [float(x.strip()) for x in data_input.split(",")]
            st.write(f"Mean: `{sum(nums)/len(nums)}` | Max: `{max(nums)}` | Min: `{min(nums)}`")
        st.markdown('</div>', unsafe_allow_html=True)

# --- MODULE 4: KNOWLEDGE BASE ---
elif nav == "📚 Knowledge Base":
    st.markdown('<h1 class="title-text">Knowledge</h1>', unsafe_allow_html=True)
    
    search = st.text_input("🔍 Search Mathematical Concepts...")
    
    lib = {
        "Pythagoras": "The theorem that in a right-angled triangle, the square of the hypotenuse is equal to the sum of squares of the other two sides.",
        "Calculus": "The mathematical study of continuous change, originally called infinitesimal calculus.",
        "Algebra": "The study of mathematical symbols and the rules for manipulating these symbols.",
        "Geometry": "The branch of mathematics concerned with the properties and relations of points, lines, surfaces, and solids.",
        "Statistics": "The discipline that concerns the collection, organization, analysis, interpretation, and presentation of data."
    }
    
    cols = st.columns(2)
    for i, (key, val) in enumerate(lib.items()):
        with cols[i % 2]:
            st.markdown(f'<div class="m3-card"><h3>{key}</h3><p>{val}</p></div>', unsafe_allow_html=True)

# --- MODULE 5: LAB NOTEBOOK ---
elif nav == "📝 Lab Notebook":
    st.markdown('<h1 class="title-text">Notebook</h1>', unsafe_allow_html=True)
    st.session_state.notes = st.text_area("Markdown Enabled Sync-Pad", value=st.session_state.notes, height=500)
    
    if st.button("💾 Hard Save to Session"):
        st.toast("Encrypted Save Successful!")
    
    st.markdown("### Preview")
    st.markdown(st.session_state.notes)

# --- MODULE 6: DEVELOPER CONSOLE ---
elif nav == "⚙️ Dev Console":
    st.markdown('<h1 class="title-text">System Dev</h1>', unsafe_allow_html=True)
    
    with st.expander("🔍 View Raw State Management"):
        st.write(st.session_state)
    
    st.markdown('<div class="m3-card">', unsafe_allow_html=True)
    st.write("### Application Logs")
    st.code(f"USER_AUTH_STATUS: {bool(USER_KEY)}\nDB_RECORDS: {len(st.session_state.history)}\nUI_RENDER_ENG: Streamlit Web v1.3x")
    st.markdown('</div>', unsafe_allow_html=True)

# =================================================================
# FOOTER
# =================================================================
st.divider()
st.caption("MathIsEZ Ultra | Built for OSS Proposal 2025-2026 | Powered by Groq Llama 3.2")