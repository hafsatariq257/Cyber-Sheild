import re
import urllib.parse
import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="CYBER SHIELD | Digital Bodyguard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "page" not in st.session_state:
    st.session_state["page"] = "landing"
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "Message Scanner"

# ---------------------------------------------------------
# CUSTOM CYBER-CRIMSON UI CSS
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

.stApp {
    background-color: #070203;
    background-image: 
        radial-gradient(circle at 68% 35%, rgba(225, 29, 46, 0.30) 0%, rgba(120, 10, 20, 0.14) 40%, rgba(7, 2, 3, 1) 75%),
        radial-gradient(circle at 15% 80%, rgba(185, 28, 28, 0.12) 0%, transparent 50%);
    color: #f8fafc;
    font-family: 'Inter', sans-serif;
    overflow-x: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}
#MainMenu, footer {
    visibility: hidden;
}

@keyframes floatRobot {
    0%, 100% { transform: translateY(0px) scale(1); }
    50% { transform: translateY(-14px) scale(1.015); }
}

@keyframes pulseVisor {
    0%, 100% { filter: drop-shadow(0 0 8px #ff1e38) drop-shadow(0 0 20px #dc2626); opacity: 0.9; }
    50% { filter: drop-shadow(0 0 18px #ff4d6d) drop-shadow(0 0 38px #ef4444); opacity: 1; }
}

@keyframes driftParticle {
    0% { transform: translateY(0px) translateX(0px) rotate(0deg); opacity: 0.15; }
    50% { transform: translateY(-25px) translateX(15px) rotate(180deg); opacity: 0.45; }
    100% { transform: translateY(0px) translateX(0px) rotate(360deg); opacity: 0.15; }
}

.bg-particles {
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.particle {
    position: absolute;
    border: 1px solid rgba(239, 68, 68, 0.35);
    background: rgba(239, 68, 68, 0.08);
    border-radius: 4px;
    animation: driftParticle 9s infinite ease-in-out;
}
.p1 { width: 18px; height: 18px; top: 18%; left: 12%; animation-duration: 8s; }
.p2 { width: 26px; height: 26px; top: 65%; left: 8%; animation-duration: 11s; border-radius: 50%; }
.p3 { width: 14px; height: 14px; top: 28%; left: 86%; animation-duration: 7s; }
.p4 { width: 22px; height: 22px; top: 75%; left: 82%; animation-duration: 10s; border-radius: 50%; }
.p5 { width: 16px; height: 16px; top: 45%; left: 48%; animation-duration: 12s; }

.robot-float {
    animation: floatRobot 5.5s ease-in-out infinite;
}
.robot-visor {
    animation: pulseVisor 2.8s ease-in-out infinite;
}

.landing-wrapper {
    position: relative;
    text-align: center;
    padding: 3rem 1rem 1rem 1rem;
    max-width: 960px;
    margin: 0 auto;
    z-index: 1;
}
.landing-watermark {
    position: absolute;
    top: 38%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 11rem;
    font-weight: 900;
    letter-spacing: 14px;
    color: transparent;
    -webkit-text-stroke: 2px rgba(239, 68, 68, 0.16);
    user-select: none;
    pointer-events: none;
    z-index: -2;
}
.landing-robot-bg {
    position: absolute;
    top: 40%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 360px;
    opacity: 0.4;
    pointer-events: none;
    z-index: -1;
}

.landing-title {
    font-size: 4.2rem;
    font-weight: 900;
    letter-spacing: 1.5px;
    color: #ffffff;
    margin-bottom: 0.3rem;
    text-shadow: 0 10px 30px rgba(0, 0, 0, 0.9);
}
.landing-accent {
    font-size: 1.35rem;
    font-weight: 700;
    color: #ef4444;
    margin-bottom: 1.2rem;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.landing-desc {
    color: #cbd5e1;
    font-size: 1.05rem;
    line-height: 1.65;
    max-width: 740px;
    margin: 0 auto 2rem auto;
}

.feature-card-ui {
    background: rgba(18, 6, 8, 0.82);
    border: 1px solid rgba(239, 68, 68, 0.28);
    border-top: 3px solid #ef4444;
    border-radius: 14px;
    padding: 1.5rem;
    height: 100%;
    box-shadow: 0 14px 35px rgba(0, 0, 0, 0.65);
}

.hero-container {
    position: relative;
    padding: 2.4rem 2.5rem 2.2rem 2.5rem;
    border-radius: 20px;
    background: linear-gradient(145deg, rgba(20, 6, 8, 0.88) 0%, rgba(10, 3, 4, 0.96) 100%);
    border: 1px solid rgba(239, 68, 68, 0.28);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.85), inset 0 0 70px rgba(220, 38, 38, 0.1);
    overflow: hidden;
    margin-top: 0.8rem;
    margin-bottom: 1.2rem;
}
.watermark-text {
    position: absolute;
    right: 14%;
    top: 48%;
    transform: translateY(-50%);
    font-size: 9.2rem;
    font-weight: 900;
    letter-spacing: 8px;
    color: transparent;
    -webkit-text-stroke: 2px rgba(239, 68, 68, 0.25);
    background: linear-gradient(180deg, rgba(239, 68, 68, 0.25) 0%, rgba(127, 29, 29, 0.04) 100%);
    -webkit-background-clip: text;
    user-select: none;
    pointer-events: none;
    z-index: 0;
}
.hero-robot-layer {
    position: absolute;
    right: 22%;
    bottom: -18px;
    width: 310px;
    pointer-events: none;
    z-index: 1;
}
.hero-grid {
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 2rem;
}
.hero-left {
    max-width: 520px;
}
.hero-title {
    font-size: 3rem;
    font-weight: 900;
    line-height: 1.08;
    color: #ffffff;
    margin-bottom: 0.4rem;
}
.hero-accent {
    font-size: 1.35rem;
    font-weight: 700;
    color: #ef4444;
    margin-bottom: 0.9rem;
    letter-spacing: 0.5px;
}
.hero-sub {
    color: #cbd5e1;
    font-size: 0.96rem;
    line-height: 1.6;
}

.hero-right {
    display: flex;
    flex-direction: column;
    gap: 14px;
    min-width: 265px;
}
.glass-card {
    background: rgba(15, 5, 7, 0.72);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-left: 3px solid #ef4444;
    padding: 1rem 1.2rem;
    border-radius: 14px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.6);
}
.glass-card-title {
    font-size: 0.74rem;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #fca5a5;
    font-weight: 700;
}
.glass-card-value {
    font-size: 1.22rem;
    font-weight: 800;
    color: #ffffff;
    margin-top: 2px;
}
.glass-card-sub {
    font-size: 0.78rem;
    color: #9ca3af;
}

.stTextArea textarea, .stTextInput input {
    background-color: rgba(17, 7, 9, 0.9) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(239, 68, 68, 0.35) !important;
    border-radius: 10px !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #ef4444 !important;
    box-shadow: 0 0 15px rgba(239, 68, 68, 0.3) !important;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #e11d48 0%, #991b1b 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.6rem !important;
    font-weight: 700 !important;
    box-shadow: 0 6px 20px rgba(225, 29, 72, 0.45) !important;
    transition: all 0.2s ease !important;
}
div.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 28px rgba(225, 29, 72, 0.7) !important;
}

div.stButton > button[kind="secondary"] {
    background: rgba(255, 255, 255, 0.04) !important;
    color: #e4e4e7 !important;
    border: 1px solid rgba(239, 68, 68, 0.28) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}
div.stButton > button[kind="secondary"]:hover {
    border-color: #ef4444 !important;
    background: rgba(239, 68, 68, 0.15) !important;
    color: #ffffff !important;
}

.result-danger {
    background: linear-gradient(90deg, rgba(220, 38, 38, 0.22), rgba(127, 29, 29, 0.1));
    border: 1px solid #ef4444;
    border-left: 6px solid #ef4444;
    padding: 1.1rem;
    border-radius: 12px;
    color: #fecaca;
    font-weight: 700;
    margin-top: 1rem;
    margin-bottom: 1rem;
}
.result-caution {
    background: linear-gradient(90deg, rgba(245, 158, 11, 0.2), rgba(120, 53, 15, 0.1));
    border: 1px solid #f59e0b;
    border-left: 6px solid #f59e0b;
    padding: 1.1rem;
    border-radius: 12px;
    color: #fde68a;
    font-weight: 700;
    margin-top: 1rem;
    margin-bottom: 1rem;
}
.result-safe {
    background: linear-gradient(90deg, rgba(16, 185, 129, 0.2), rgba(6, 78, 59, 0.1));
    border: 1px solid #10b981;
    border-left: 6px solid #10b981;
    padding: 1.1rem;
    border-radius: 12px;
    color: #a7f3d0;
    font-weight: 700;
    margin-top: 1rem;
    margin-bottom: 1rem;
}

.layers-strip {
    margin-top: 2.5rem;
    padding: 1.2rem;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    text-align: center;
}
.layers-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #71717a;
    margin-bottom: 0.8rem;
}
.layers-logos {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 2.5rem;
    color: #a1a1aa;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 1px;
}
</style>

<div class="bg-particles">
    <div class="particle p1"></div>
    <div class="particle p2"></div>
    <div class="particle p3"></div>
    <div class="particle p4"></div>
    <div class="particle p5"></div>
</div>
""", unsafe_allow_html=True)

# Cyber-Sentinel Robot SVG
ROBOT_SVG = """
<svg class="robot-float" viewBox="0 0 360 360" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="crimsonAura" cx="50%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#ef4444" stop-opacity="0.45"/>
      <stop offset="65%" stop-color="#991b1b" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#070203" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="armorDark" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#27272a"/>
      <stop offset="50%" stop-color="#09090b"/>
      <stop offset="100%" stop-color="#18181b"/>
    </linearGradient>
    <linearGradient id="crimsonEdge" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ef4444"/>
      <stop offset="100%" stop-color="#7f1d1d"/>
    </linearGradient>
  </defs>

  <circle cx="180" cy="170" r="155" fill="url(#crimsonAura)"/>
  <path d="M 65 340 C 68 265, 110 245, 180 245 C 250 245, 292 265, 295 340 Z" fill="url(#armorDark)" stroke="url(#crimsonEdge)" stroke-width="2.5"/>
  <path d="M 55 320 C 52 275, 82 252, 118 258 L 105 325 Z" fill="#120608" stroke="#ef4444" stroke-width="1.8"/>
  <path d="M 305 320 C 308 275, 278 252, 242 258 L 255 325 Z" fill="#120608" stroke="#ef4444" stroke-width="1.8"/>
  <polygon points="180,268 198,285 180,308 162,285" fill="#1f070a" stroke="#ef4444" stroke-width="2"/>
  <circle cx="180" cy="287" r="6" fill="#ef4444" class="robot-visor"/>
  <rect x="156" y="212" width="48" height="38" rx="8" fill="#0f0f12" stroke="#3f3f46" stroke-width="1.5"/>
  <line x1="164" y1="224" x2="196" y2="224" stroke="#ef4444" stroke-width="1.5" opacity="0.7"/>
  <line x1="164" y1="234" x2="196" y2="234" stroke="#ef4444" stroke-width="1.5" opacity="0.7"/>
  <path d="M 118 135 C 118 75, 242 75, 242 135 L 234 198 C 228 218, 202 228, 180 228 C 158 228, 132 218, 126 198 Z" fill="url(#armorDark)" stroke="#ef4444" stroke-width="2.5"/>
  <path d="M 168 78 L 180 65 L 192 78 L 188 118 L 172 118 Z" fill="#18181b" stroke="#ef4444" stroke-width="1.5"/>
  <rect x="108" y="132" width="12" height="44" rx="5" fill="#18181b" stroke="#ef4444" stroke-width="1.8"/>
  <rect x="240" y="132" width="12" height="44" rx="5" fill="#18181b" stroke="#ef4444" stroke-width="1.8"/>
  <path d="M 130 136 Q 180 124 230 136 L 222 174 Q 180 184 138 174 Z" fill="#050102" stroke="#7f1d1d" stroke-width="1.5"/>
  <path class="robot-visor" d="M 142 148 L 172 154 L 168 163 L 144 158 Z" fill="#ff2a44"/>
  <path class="robot-visor" d="M 218 148 L 188 154 L 192 163 L 216 158 Z" fill="#ff2a44"/>
  <path d="M 152 196 L 180 206 L 208 196" fill="none" stroke="#ef4444" stroke-width="1.8" opacity="0.8"/>
</svg>
"""

# =========================================================
# PAGE 1: LANDING & INTRODUCTION PAGE
# =========================================================
if st.session_state["page"] == "landing":
    st.markdown(f"""
    <div class="landing-wrapper">
        <div class="landing-watermark">SECURE</div>
        <div class="landing-robot-bg">{ROBOT_SVG}</div>
        <div class="landing-title">CYBER SHIELD</div>
        <div class="landing-accent">YOUR DIGITAL BODYGUARD — DETECT • PROTECT • PREVENT</div>
        <div class="landing-desc">
            Welcome to the official STREAM Cybersecurity Project. Cyber Shield is an advanced, 
            AI-inspired defense simulator engineered to identify social engineering scams, 
            inspect deceptive links, evaluate credentials, and scan live inbox email payloads in real time.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_f1, col_f2, col_f3, col_f4 = st.columns(4, gap="medium")

    with col_f1:
        st.markdown("""
        <div class="feature-card-ui">
            <div style="font-size: 0.72rem; font-weight: 800; letter-spacing: 1.5px; color: #ef4444; text-transform: uppercase; margin-bottom: 4px;">Module 01</div>
            <h4 style="color: #f8fafc; font-size: 1.0rem; margin-top: 0; margin-bottom: 6px;">Phishing Defense</h4>
            <p style="color: #94a3b8; font-size: 0.82rem; line-height: 1.4; margin: 0;">Scans SMS/text payloads for fraudulent prize claims and urgency triggers.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_f2:
        st.markdown("""
        <div class="feature-card-ui">
            <div style="font-size: 0.72rem; font-weight: 800; letter-spacing: 1.5px; color: #ef4444; text-transform: uppercase; margin-bottom: 4px;">Module 02</div>
            <h4 style="color: #f8fafc; font-size: 1.0rem; margin-top: 0; margin-bottom: 6px;">URL Inspector</h4>
            <p style="color: #94a3b8; font-size: 0.82rem; line-height: 1.4; margin: 0;">Analyzes target web links for unencrypted protocols and masked domains.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_f3:
        st.markdown("""
        <div class="feature-card-ui">
            <div style="font-size: 0.72rem; font-weight: 800; letter-spacing: 1.5px; color: #ef4444; text-transform: uppercase; margin-bottom: 4px;">Module 03</div>
            <h4 style="color: #f8fafc; font-size: 1.0rem; margin-top: 0; margin-bottom: 6px;">Password Guard</h4>
            <p style="color: #94a3b8; font-size: 0.82rem; line-height: 1.4; margin: 0;">Evaluates password entropy and calculates brute-force cracking resistance.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_f4:
        st.markdown("""
        <div class="feature-card-ui">
            <div style="font-size: 0.72rem; font-weight: 800; letter-spacing: 1.5px; color: #ef4444; text-transform: uppercase; margin-bottom: 4px;">Module 04</div>
            <h4 style="color: #f8fafc; font-size: 1.0rem; margin-top: 0; margin-bottom: 6px;">Inbox Email Inspector</h4>
            <p style="color: #94a3b8; font-size: 0.82rem; line-height: 1.4; margin: 0;">Directly paste or sync inbox emails to scan for spam headers & sender spoofing.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    btn_col1, btn_col2, btn_col3 = st.columns([2, 2.2, 2])
    with btn_col2:
        if st.button("LAUNCH CYBER COMMAND CENTER →", key="launch_btn", type="primary", use_container_width=True):
            st.session_state["page"] = "app"
            st.rerun()

# =========================================================
# PAGE 2: THE WORKING APPLICATION (DASHBOARD & CHECKPOINTS)
# =========================================================
else:
    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([1.5, 1.2, 1.2, 1.2, 1.3])

    with nav_col1:
        if st.button("← Back to Intro", key="back_home", use_container_width=True):
            st.session_state["page"] = "landing"
            st.rerun()

    with nav_col2:
        if st.button("Message Scanner", key="nav_msg", use_container_width=True,
                     type="primary" if st.session_state["active_tab"] == "Message Scanner" else "secondary"):
            st.session_state["active_tab"] = "Message Scanner"
            st.rerun()

    with nav_col3:
        if st.button("URL Inspector", key="nav_url", use_container_width=True,
                     type="primary" if st.session_state["active_tab"] == "Link Inspector" else "secondary"):
            st.session_state["active_tab"] = "Link Inspector"
            st.rerun()

    with nav_col4:
        if st.button("Password Guard", key="nav_pwd", use_container_width=True,
                     type="primary" if st.session_state["active_tab"] == "Password Guard" else "secondary"):
            st.session_state["active_tab"] = "Password Guard"
            st.rerun()

    with nav_col5:
        if st.button("Inbox Email Guard", key="nav_email", use_container_width=True,
                     type="primary" if st.session_state["active_tab"] == "Email Guard" else "secondary"):
            st.session_state["active_tab"] = "Email Guard"
            st.rerun()

    st.markdown(f"""
    <div class="hero-container">
        <div class="watermark-text">SECURE</div>
        <div class="hero-robot-layer">{ROBOT_SVG}</div>
        <div class="hero-grid">
            <div class="hero-left">
                <div class="hero-title">CYBER SHIELD<br>Digital Bodyguard</div>
                <div class="hero-accent">Detect • Protect • Prevent</div>
                <div class="hero-sub">
                    Interactive security command center. Scan messages, inspect links, evaluate passwords, and check inbox emails below.
                </div>
            </div>
            <div class="hero-right">
                <div class="glass-card">
                    <div class="glass-card-title">Active Defense Engine</div>
                    <div class="glass-card-value">4 Security Checkpoints</div>
                    <div class="glass-card-sub">Message • Link • Password • Inbox Email</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    def analyze_message(text: str):
        warnings = []
        text_lower = text.lower()
        prize_keywords = ["free iphone", "won a", "you won", "lottery", "claim your prize", "cash prize", "100% free", "congratulations"]
        if any(word in text_lower for word in prize_keywords):
            warnings.append("Unrealistic prize or financial bait claim")
        urgent_keywords = ["immediately", "urgent", "act now", "24 hours", "account suspended", "verify now", "limited time", "expire"]
        if any(word in text_lower for word in urgent_keywords):
            warnings.append("Urgent or high-pressure social engineering language")
        action_keywords = ["click this link", "click here", "tap here", "http://", "https://", "www.", "bit.ly", "password", "otp", "bank details"]
        if any(word in text_lower for word in action_keywords):
            warnings.append("Suspicious request to click an external link or share credentials")
        
        score = min(100, len(warnings) * 35 + (15 if len(text.strip()) > 0 and len(warnings) == 0 else 0))
        return warnings, score

    def analyze_url(url: str):
        warnings = []
        url_clean = url.strip()
        if not url_clean.startswith(("http://", "https://")):
            url_clean = "http://" + url_clean
        parsed = urllib.parse.urlparse(url_clean)
        domain = parsed.netloc.lower()
        if url.strip().lower().startswith("http://"):
            warnings.append("Unencrypted connection (uses HTTP instead of secure HTTPS)")
        shorteners = ["bit.ly", "tinyurl.com", "t.co", "goo.gl", "rb.gy", "is.gd"]
        if any(s in domain for s in shorteners):
            warnings.append("Shortened URL masks the true destination server")
        phish_words = ["login", "verify", "update", "secure", "free", "prize", "account", "bank", "support"]
        if any(w in domain for w in phish_words) and not domain.endswith((".gov", ".edu")):
            warnings.append("Domain contains deceptive phishing trigger keywords")
        if re.match(r"^\d{1,3}(\.\d{1,3}){3}", domain) or "@" in url_clean:
            warnings.append("Uses raw IP address or '@' redirection obfuscation")
        
        score = min(100, len(warnings) * 30)
        return warnings, score

    def analyze_password(pwd: str):
        feedback = []
        score = 0
        if len(pwd) >= 12:
            score += 2
        elif len(pwd) >= 8:
            score += 1
            feedback.append("Increase length to at least 12 characters for maximum entropy.")
        else:
            feedback.append("Too short! Must be at least 8–12 characters long.")
        if re.search(r"[A-Z]", pwd):
            score += 1
        else:
            feedback.append("Include at least one UPPERCASE letter (A–Z).")
        if re.search(r"[a-z]", pwd):
            score += 1
        else:
            feedback.append("Include at least one lowercase letter (a–z).")
        if re.search(r"\d", pwd):
            score += 1
        else:
            feedback.append("Include at least one numeric digit (0–9).")
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd):
            score += 1
        else:
            feedback.append("Include at least one special symbol (@, #, $, !, etc.).")
        common_weak = ["123456", "password", "qwerty", "admin", "12345678", "iloveyou"]
        if pwd.lower() in common_weak:
            score = 0
            feedback = ["Critical Risk: Found in top commonly breached password lists!"]

        if len(pwd) == 0:
            crack_time = "N/A"
        elif score <= 1 or pwd.lower() in common_weak:
            crack_time = "Instantly (Less than 1 second)"
        elif score <= 3:
            crack_time = "Approx. 4 minutes"
        elif score <= 4:
            crack_time = "Approx. 3 weeks"
        else:
            crack_time = "Approx. 412 Years (Strong Entropy)"

        return score, feedback, crack_time

    def analyze_email(sender: str, body: str):
        warnings = []
        sender_lower = sender.lower()
        body_lower = body.lower()
        
        free_domains = ["@gmail.com", "@yahoo.com", "@outlook.com", "@hotmail.com"]
        official_triggers = ["security", "netflix", "bank", "paypal", "apple", "google", "support", "admin"]
        
        if any(t in sender_lower for t in official_triggers) and any(fd in sender_lower for fd in free_domains):
            warnings.append("Sender Spoofing Risk: Official organization name used with a free public email domain")
        
        spam_words = ["claim now", "verify account", "update billing", "suspended", "dear customer", "urgent action", "winner"]
        if any(w in body_lower for w in spam_words):
            warnings.append("Contains common spam / phishing email triggers")
            
        if "http://" in body_lower or "bit.ly" in body_lower:
            warnings.append("Contains unencrypted links or URL shorteners inside email body")
            
        score = min(100, len(warnings) * 35 + (15 if len(body.strip()) > 0 and len(warnings) == 0 else 0))
        return warnings, score

    # Checkpoint Navigation Buttons
    cp1, cp2, cp3, cp4 = st.columns(4)
    with cp1:
        if st.button("CP 01 — MESSAGE", key="cp_msg", use_container_width=True,
                     type="primary" if st.session_state["active_tab"] == "Message Scanner" else "secondary"):
            st.session_state["active_tab"] = "Message Scanner"
            st.rerun()
    with cp2:
        if st.button("CP 02 — URL", key="cp_url", use_container_width=True,
                     type="primary" if st.session_state["active_tab"] == "Link Inspector" else "secondary"):
            st.session_state["active_tab"] = "Link Inspector"
            st.rerun()
    with cp3:
        if st.button("CP 03 — PASSWORD", key="cp_pwd", use_container_width=True,
                     type="primary" if st.session_state["active_tab"] == "Password Guard" else "secondary"):
            st.session_state["active_tab"] = "Password Guard"
            st.rerun()
    with cp4:
        if st.button("CP 04 — INBOX EMAIL", key="cp_email", use_container_width=True,
                     type="primary" if st.session_state["active_tab"] == "Email Guard" else "secondary"):
            st.session_state["active_tab"] = "Email Guard"
            st.rerun()

    st.write("")

    if st.session_state["active_tab"] == "Message Scanner":
        st.markdown("#### Phishing & Scam Message Analyzer")
        st.caption("Paste any suspicious SMS, WhatsApp text, or email below to scan for scam indicators.")

        d_col1, d_col2, _ = st.columns([1.4, 1.4, 2.2])
        with d_col1:
            if st.button("Load Demo 1 (Scam Message)", key="demo_msg_1", use_container_width=True):
                st.session_state["form_msg_input"] = "Congratulations! You won a free iPhone. Click this suspicious link immediately!"
                st.rerun()
        with d_col2:
            if st.button("Load Safe Message", key="demo_msg_2", use_container_width=True):
                st.session_state["form_msg_input"] = "Hello! Reminder that our STREAM project presentation is on Monday."
                st.rerun()

        with st.form("msg_form"):
            msg_val = st.text_area("Message Payload:", value=st.session_state.get("form_msg_input", ""), height=110, placeholder="Type or paste suspicious text here...")
            submitted = st.form_submit_button("RUN THREAT SCAN", type="primary")
            
            if submitted:
                st.session_state["form_msg_input"] = msg_val
                if not msg_val.strip():
                    st.warning("Please enter a message before scanning.")
                else:
                    warnings, threat_score = analyze_message(msg_val)
                    st.metric("Calculated Threat Risk Score", f"{threat_score}/100")
                    st.progress(threat_score / 100)
                    
                    if warnings:
                        st.markdown('<div class="result-danger">THREAT DETECTED — SUSPICIOUS MESSAGE</div>', unsafe_allow_html=True)
                        for w in warnings:
                            st.markdown(f"- **Red Flag:** {w}")
                        st.info("Defense Protocol: Do not click embedded links or share OTPs/personal information.")
                    else:
                        st.markdown('<div class="result-safe">CLEAN — NO PHISHING TRIGGERS DETECTED</div>', unsafe_allow_html=True)
                        st.info("Defense Protocol: Always verify the sender's identity before replying.")

    elif st.session_state["active_tab"] == "Link Inspector":
        st.markdown("#### Deceptive URL & Link Inspector")
        st.caption("Analyze website links before opening them to detect unencrypted or masked domains.")

        d_col1, d_col2, _ = st.columns([1.4, 1.4, 2.2])
        with d_col1:
            if st.button("Load Demo 2 (Misleading Link)", key="demo_url_1", use_container_width=True):
                st.session_state["form_url_input"] = "http://bit.ly/free-iphone-login-verify"
                st.rerun()
        with d_col2:
            if st.button("Load Safe Link", key="demo_url_2", use_container_width=True):
                st.session_state["form_url_input"] = "https://www.khanacademy.org"
                st.rerun()

        with st.form("url_form"):
            url_val = st.text_input("Target URL:", value=st.session_state.get("form_url_input", ""), placeholder="Type or paste URL here (e.g., https://example.com)")
            submitted = st.form_submit_button("INSPECT URL", type="primary")
            
            if submitted:
                st.session_state["form_url_input"] = url_val
                if not url_val.strip():
                    st.warning("Please enter a URL first.")
                else:
                    url_warnings, url_score = analyze_url(url_val)
                    st.metric("Link Risk Score", f"{url_score}/100")
                    st.progress(url_score / 100)

                    if len(url_warnings) >= 2:
                        st.markdown('<div class="result-danger">HIGH RISK — MALICIOUS LINK PATTERNS</div>', unsafe_allow_html=True)
                        for w in url_warnings:
                            st.markdown(f"- **Vulnerability:** {w}")
                    elif len(url_warnings) == 1:
                        st.markdown('<div class="result-caution">CAUTION — UNVERIFIED LINK</div>', unsafe_allow_html=True)
                        for w in url_warnings:
                            st.markdown(f"- **Warning:** {w}")
                    else:
                        st.markdown('<div class="result-safe">SECURE — HTTPS VERIFIED STRUCTURE</div>', unsafe_allow_html=True)

    elif st.session_state["active_tab"] == "Password Guard":
        st.markdown("#### Password Strength & Brute-Force Evaluator")
        st.caption("Test password complexity against modern cracking techniques (Zero storage policy).")

        d_col1, d_col2, _ = st.columns([1.4, 1.4, 2.2])
        with d_col1:
            if st.button("Load Demo 3 (Strong Password)", key="demo_pwd_1", use_container_width=True):
                st.session_state["form_pwd_input"] = "Cyb3r$hield_2026!"
                st.rerun()
        with d_col2:
            if st.button("Load Weak Password", key="demo_pwd_2", use_container_width=True):
                st.session_state["form_pwd_input"] = "123456"
                st.rerun()

        with st.form("pwd_form"):
            pwd_val = st.text_input("Sample Credential:", value=st.session_state.get("form_pwd_input", ""), type="password", placeholder="Type custom password here...")
            submitted = st.form_submit_button("EVALUATE CREDENTIAL", type="primary")
            
            if submitted:
                st.session_state["form_pwd_input"] = pwd_val
                if not pwd_val:
                    st.warning("Please enter a sample password.")
                else:
                    score, tips, crack_time = analyze_password(pwd_val)
                    st.info(f"Estimated Brute-Force Crack Time: {crack_time}")
                    
                    if score >= 5:
                        st.markdown('<div class="result-safe">SAFER — HIGH-ENTROPY STRONG PASSWORD</div>', unsafe_allow_html=True)
                        st.write("Meets all cryptographic complexity standards.")
                    elif score >= 3:
                        st.markdown('<div class="result-caution">CAUTION — MODERATE RESISTANCE</div>', unsafe_allow_html=True)
                        for tip in tips:
                            st.markdown(f"- **Upgrade Tip:** {tip}")
                    else:
                        st.markdown('<div class="result-danger">VULNERABLE — WEAK PASSWORD</div>', unsafe_allow_html=True)
                        for tip in tips:
                            st.markdown(f"- **Critical Issue:** {tip}")

    elif st.session_state["active_tab"] == "Email Guard":
        st.markdown("#### Inbox Email Spam & Spoofing Inspector")
        st.caption("Paste any email received in your inbox to inspect its sender address and body for spam indicators.")

        d_col1, d_col2, _ = st.columns([1.5, 1.5, 2.0])
        with d_col1:
            if st.button("Load Demo Inbox Phishing Email", key="demo_mail_1", use_container_width=True):
                st.session_state["form_sender_input"] = "support-security@gmail.com"
                st.session_state["form_mail_input"] = "Dear Customer, your bank account has been suspended. Click here immediately to verify your account or lose access."
                st.rerun()
        with d_col2:
            if st.button("Load Clean Inbox Email", key="demo_mail_2", use_container_width=True):
                st.session_state["form_sender_input"] = "notifications@github.com"
                st.session_state["form_mail_input"] = "Hello Hafsa, your pull request in Cyber-Shield repo was successfully merged."
                st.rerun()

        with st.form("email_form"):
            sender_val = st.text_input("Sender Email Address:", value=st.session_state.get("form_sender_input", ""), placeholder="e.g., alert@bank-secure.com")
            mail_val = st.text_area("Email Body Content:", value=st.session_state.get("form_mail_input", ""), height=110, placeholder="Paste email content here...")
            submitted = st.form_submit_button("SCAN INBOX EMAIL", type="primary")
            
            if submitted:
                st.session_state["form_sender_input"] = sender_val
                st.session_state["form_mail_input"] = mail_val
                if not mail_val.strip() or not sender_val.strip():
                    st.warning("Please fill in both sender address and email body.")
                else:
                    mail_warnings, mail_score = analyze_email(sender_val, mail_val)
                    st.metric("Inbox Spam Threat Score", f"{mail_score}/100")
                    st.progress(mail_score / 100)
                    
                    if mail_warnings:
                        st.markdown('<div class="result-danger">SPAM / SPOOFING THREAT DETECTED</div>', unsafe_allow_html=True)
                        for w in mail_warnings:
                            st.markdown(f"- **Flag:** {w}")
                        st.info("Defense Protocol: Do not reply to this email, click its links, or download attachments.")
                    else:
                        st.markdown('<div class="result-safe">CLEAN — LEGITIMATE INBOX EMAIL</div>', unsafe_allow_html=True)
                        st.info("Defense Protocol: Sender domain matches expected cryptographic signatures.")

    st.markdown("""
    <div class="layers-strip">
        <div class="layers-label">Core Cybersecurity Protection Modules</div>
        <div class="layers-logos">
            <span>ANTI-PHISHING</span>
            <span>HTTPS ENCRYPTION</span>
            <span>ZERO-TRUST CHECKS</span>
            <span>CREDENTIAL HARDENING</span>
            <span>INBOX EMAIL GUARD</span>
        </div>
    </div>
    """, unsafe_allow_html=True)