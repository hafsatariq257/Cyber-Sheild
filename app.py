import re
import base64
import random
import urllib.parse
from pathlib import Path
import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="PhishTrace | Multichannel Phishing Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "page" not in st.session_state:
    st.session_state["page"] = "landing"
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "Message Scanner"

# ---------------------------------------------------------
# IMAGE FILES (Exact filenames matching your file tree)
# ---------------------------------------------------------
IMG_WARNINGS = "shield.jpg.jpg"
IMG_PLEXUS   = "1000378210.jpg"
IMG_SCENE    = "1000378209.jpg"


@st.cache_data
def img64(name: str) -> str:
    """Return image as base64 data-URI (empty string if file not found)."""
    for base in (Path(__file__).parent, Path.cwd()):
        p = base / name
        if p.exists():
            ext = p.suffix.lower().strip(".")
            mime = "jpeg" if ext in ("jpg", "jpeg") else ext
            return f"data:image/{mime};base64," + base64.b64encode(p.read_bytes()).decode()
    return ""


# ---------------------------------------------------------
# CUSTOM CYBER-CRIMSON UI CSS
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');

.stApp {
    background-color: #070203;
    background-image: 
        radial-gradient(circle at 68% 35%, rgba(225, 29, 46, 0.30) 0%, rgba(120, 10, 20, 0.14) 40%, rgba(7, 2, 3, 1) 75%),
        radial-gradient(circle at 15% 80%, rgba(185, 28, 28, 0.12) 0%, transparent 50%);
    color: #ffffff;
    font-family: 'Inter', sans-serif;
    overflow-x: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}
#MainMenu, footer {
    visibility: hidden;
}

.block-container, [data-testid="stMainBlockContainer"] {
    position: relative;
    z-index: 2;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
}

@keyframes floatRobot {
    0%, 100% { transform: translateY(0px) scale(1); }
    50% { transform: translateY(-14px) scale(1.015); }
}

@keyframes pulseVisor {
    0%, 100% { filter: drop-shadow(0 0 8px #ff1e38) drop-shadow(0 0 20px #dc2626); opacity: 0.95; }
    50% { filter: drop-shadow(0 0 18px #ff4d6d) drop-shadow(0 0 38px #ef4444); opacity: 1; }
}

@keyframes driftParticle {
    0% { transform: translateY(0px) translateX(0px) rotate(0deg); opacity: 0.25; }
    50% { transform: translateY(-25px) translateX(15px) rotate(180deg); opacity: 0.6; }
    100% { transform: translateY(0px) translateX(0px) rotate(360deg); opacity: 0.25; }
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
    border: 1px solid rgba(239, 68, 68, 0.45);
    background: rgba(239, 68, 68, 0.12);
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

.feature-card-ui {
    background: rgba(22, 7, 10, 0.94);
    border: 1px solid rgba(248, 113, 113, 0.55);
    border-top: 4px solid #ef4444;
    border-radius: 14px;
    padding: 1.6rem 1.4rem;
    height: 100%;
    box-shadow: 0 14px 35px rgba(0, 0, 0, 0.75);
    transition: transform .25s ease, box-shadow .25s ease;
}
.feature-card-ui:hover {
    transform: translateY(-8px);
    box-shadow: 0 0 30px rgba(239, 68, 68, .55), 0 14px 35px rgba(0, 0, 0, .75);
}
.mod-tag {
    font-size: 1.15rem;
    font-weight: 900;
    letter-spacing: 2px;
    color: #ff6b7d;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.mod-title {
    color: #ffffff;
    font-size: 1.55rem;
    font-weight: 900;
    margin: 0 0 10px 0;
}
.mod-desc {
    color: #f1f5f9;
    font-size: 1.1rem;
    line-height: 1.55;
    margin: 0;
}

.hero-container {
    position: relative;
    padding: 2.2rem 2.2rem 2rem 2.2rem;
    border-radius: 20px;
    background: linear-gradient(145deg, rgba(24, 7, 10, 0.94) 0%, rgba(12, 3, 5, 0.98) 100%);
    border: 1px solid rgba(248, 113, 113, 0.45);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.85), inset 0 0 70px rgba(220, 38, 38, 0.14);
    overflow: hidden;
    margin-top: 0.8rem;
    margin-bottom: 1.2rem;
}
.watermark-text {
    position: absolute;
    right: 12%;
    top: 48%;
    transform: translateY(-50%);
    font-size: 8.5rem;
    font-weight: 900;
    letter-spacing: 8px;
    color: rgba(239, 68, 68, 0.16);
    -webkit-text-stroke: 2px rgba(248, 113, 113, 0.42);
    user-select: none;
    pointer-events: none;
    z-index: 0;
}
.hero-robot-layer {
    position: absolute;
    right: 22%;
    bottom: -18px;
    width: 300px;
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
    gap: 1.5rem;
}
.hero-left {
    max-width: 560px;
}
.hero-title {
    font-size: 3.2rem;
    font-weight: 900;
    line-height: 1.1;
    color: #ffffff;
    margin-bottom: 0.4rem;
}
.hero-accent {
    font-size: 1.5rem;
    font-weight: 800;
    color: #ff5a6e;
    margin-bottom: 0.8rem;
    letter-spacing: 0.5px;
}
.hero-sub {
    color: #f1f5f9;
    font-size: 1.15rem;
    line-height: 1.6;
}

.hero-right {
    display: flex;
    flex-direction: column;
    gap: 14px;
    min-width: 265px;
}
.glass-card {
    background: rgba(20, 6, 9, 0.88);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.22);
    border-left: 4px solid #ef4444;
    padding: 1.1rem 1.3rem;
    border-radius: 14px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
}
.glass-card-title {
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1.3px;
    color: #fecaca;
    font-weight: 800;
}
.glass-card-value {
    font-size: 1.5rem;
    font-weight: 900;
    color: #ffffff;
    margin-top: 3px;
}
.glass-card-sub {
    font-size: 1rem;
    color: #e2e8f0;
    font-weight: 600;
    margin-top: 2px;
}

.stTextArea textarea, .stTextInput input {
    background-color: rgba(22, 8, 11, 0.95) !important;
    color: #ffffff !important;
    border: 1px solid rgba(248, 113, 113, 0.55) !important;
    border-radius: 10px !important;
    font-size: 1.1rem !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #ef4444 !important;
    box-shadow: 0 0 15px rgba(239, 68, 68, 0.4) !important;
}

/* ENLARGED BUTTON FONTS FOR LAUNCH & NAVIGATION BUTTONS */
div.stButton > button[kind="primary"],
div[data-testid="stFormSubmitButton"] > button[kind="primary"],
div[data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"] {
    background: linear-gradient(90deg, #e11d48 0%, #991b1b 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 1rem 1.8rem !important;
    font-size: 1.25rem !important;
    font-weight: 900 !important;
    letter-spacing: 1px !important;
    box-shadow: 0 6px 20px rgba(225, 29, 72, 0.5) !important;
    transition: all 0.2s ease !important;
}
div.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 28px rgba(225, 29, 72, 0.75) !important;
}

div.stButton > button[kind="secondary"] {
    background: rgba(255, 255, 255, 0.08) !important;
    color: #ffffff !important;
    border: 1px solid rgba(248, 113, 113, 0.45) !important;
    border-radius: 10px !important;
    padding: 1rem 1.4rem !important;
    font-size: 1.2rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.5px !important;
}
div.stButton > button[kind="secondary"]:hover {
    border-color: #ef4444 !important;
    background: rgba(239, 68, 68, 0.22) !important;
    color: #ffffff !important;
}

[data-testid="stCaptionContainer"] p, .stMarkdown p, label {
    color: #f1f5f9 !important;
    font-size: 1.08rem !important;
}

.result-danger {
    background: linear-gradient(90deg, rgba(220, 38, 38, 0.28), rgba(127, 29, 29, 0.16));
    border: 1px solid #ef4444;
    border-left: 6px solid #ef4444;
    padding: 1.2rem;
    border-radius: 12px;
    color: #ffffff;
    font-size: 1.15rem;
    font-weight: 800;
    margin-top: 1rem;
    margin-bottom: 1rem;
}
.result-caution {
    background: linear-gradient(90deg, rgba(245, 158, 11, 0.26), rgba(120, 53, 15, 0.14));
    border: 1px solid #f59e0b;
    border-left: 6px solid #f59e0b;
    padding: 1.2rem;
    border-radius: 12px;
    color: #fef3c7;
    font-size: 1.15rem;
    font-weight: 800;
    margin-top: 1rem;
    margin-bottom: 1rem;
}
.result-safe {
    background: linear-gradient(90deg, rgba(16, 185, 129, 0.26), rgba(6, 78, 59, 0.14));
    border: 1px solid #10b981;
    border-left: 6px solid #10b981;
    padding: 1.2rem;
    border-radius: 12px;
    color: #d1fae5;
    font-size: 1.15rem;
    font-weight: 800;
    margin-top: 1rem;
    margin-bottom: 1rem;
}

.layers-strip {
    margin-top: 2.5rem;
    padding: 1.4rem;
    border-top: 1px solid rgba(255, 255, 255, 0.18);
    text-align: center;
}
.layers-label {
    font-size: 0.95rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #e2e8f0;
    font-weight: 700;
    margin-bottom: 0.8rem;
}
.layers-logos {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 2rem;
    color: #ffffff;
    font-weight: 800;
    font-size: 1.1rem;
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

# ---------------------------------------------------------
# LANDING PAGE EXTRA CSS & BG STYLING
# ---------------------------------------------------------
st.markdown("""
<style>
.bg-plexus, .bg-plexus2 {
    position: fixed; inset: -12%;
    background-size: cover; background-position: center;
    pointer-events: none; z-index: 0;
}
.bg-plexus  { opacity: .68; animation: plexDrift 38s ease-in-out infinite alternate; }
.bg-plexus2 { opacity: .42; mix-blend-mode: screen; animation: plexDrift2 55s ease-in-out infinite alternate; }
@keyframes plexDrift  { from { transform: scale(1.05) translate(0,0) rotate(0deg); }
                        to   { transform: scale(1.28) translate(-4%,-5%) rotate(2deg); } }
@keyframes plexDrift2 { from { transform: scale(1.3) translate(3%,4%) rotate(0deg) scaleX(-1); }
                        to   { transform: scale(1.1) translate(-3%,-2%) rotate(-3deg) scaleX(-1); } }
.bg-vignette {
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background: radial-gradient(circle at 70% 40%, rgba(225,29,46,.22) 0%, rgba(7,2,3,.68) 72%);
}

.L-hero {
    position: relative; z-index: 2;
    display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
    gap: 2rem; max-width: 1200px; margin: 0 auto; padding: 2.5rem 0.5rem 1.5rem 0.5rem;
}
.L-left { flex: 1 1 520px; max-width: 680px; }

.cyber-badge-box {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 10px 22px;
    border-radius: 35px;
    border: 2px solid rgba(248, 113, 113, 0.8);
    background: rgba(30, 4, 8, 0.9);
    backdrop-filter: blur(14px);
    color: #ffffff;
    font-size: 1.05rem;
    font-weight: 900;
    letter-spacing: 2.5px;
    box-shadow: 0 0 25px rgba(239, 68, 68, 0.45);
    animation: badgePulse 2.4s ease-in-out infinite;
}
@keyframes badgePulse { 0%,100% { box-shadow: 0 0 0 0 rgba(239,68,68,.55);} 50% { box-shadow: 0 0 0 12px rgba(239,68,68,0);} }

.L-title {
    font-size: 5.5rem;
    font-weight: 900;
    line-height: 1.02;
    letter-spacing: 1.5px;
    background: linear-gradient(90deg, #ffffff 0%, #ff6b7d 45%, #ffffff 90%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 5s linear infinite;
    margin-top: 1rem;
    margin-bottom: 1rem;
}
@keyframes shimmer { to { background-position: 200% center; } }

.L-pick {
    font-size: 1.95rem;
    font-weight: 900;
    color: #ff5a6e;
    margin: 1rem 0 0.6rem 0;
    letter-spacing: 2px;
    text-transform: uppercase;
    text-shadow: 0 0 28px rgba(239, 68, 68, 0.9);
}

.L-desc {
    color: #f8fafc;
    font-size: 1.3rem;
    font-weight: 600;
    line-height: 1.75;
    text-shadow: 0 2px 12px rgba(0, 0, 0, 0.9);
}

.L-right { position: relative; flex: 1 1 440px; min-height: 480px; display: flex; justify-content: center; align-items: center; }
.L-scene {
    position: absolute; width: 540px; max-width: 100%; mix-blend-mode: screen; opacity: .92;
    animation: sceneFloat 9s ease-in-out infinite; border-radius: 24px;
}
@keyframes sceneFloat { 0%,100% { transform: translateY(0) rotate(-1.5deg) scale(1);} 50% { transform: translateY(-18px) rotate(1.5deg) scale(1.04);} }
.L-robot { position: relative; width: 350px; z-index: 3; filter: drop-shadow(0 0 40px rgba(239,68,68,.7)); }
.L-ring {
    position: absolute; width: 440px; height: 440px; border-radius: 50%;
    border: 1.5px dashed rgba(248,113,113,.65); animation: spin 22s linear infinite; z-index: 1;
}
.L-ring.r2 { width: 540px; height: 540px; border-style: dotted; animation-duration: 36s; animation-direction: reverse; }
@keyframes spin { to { transform: rotate(360deg); } }

.bgx { position: fixed; pointer-events: none; z-index: 0; }
.L-scene { height: 520px; background-size: cover; background-position: center; }

.bg-grid {
    left: -25%; width: 150%; bottom: -8vh; height: 55vh;
    background-image:
        linear-gradient(rgba(239,68,68,.65) 1px, transparent 1px),
        linear-gradient(90deg, rgba(239,68,68,.55) 1px, transparent 1px);
    background-size: 60px 60px;
    transform: perspective(420px) rotateX(62deg);
    transform-origin: center bottom;
    animation: gridMove 3.5s linear infinite;
    -webkit-mask-image: linear-gradient(to top, rgba(0,0,0,.95), transparent 85%);
            mask-image: linear-gradient(to top, rgba(0,0,0,.95), transparent 85%);
    opacity: .65;
}
@keyframes gridMove { from { background-position: 0 0, 0 0; } to { background-position: 0 60px, 0 0; } }

.rain {
    position: fixed; top: -60%; z-index: 0; pointer-events: none;
    font-family: 'Courier New', monospace; line-height: 1.5; letter-spacing: 2px;
    color: rgba(255,90,110,.72); text-shadow: 0 0 8px rgba(239,68,68,.9);
    -webkit-mask-image: linear-gradient(to bottom, transparent, #000 40%, transparent);
            mask-image: linear-gradient(to bottom, transparent, #000 40%, transparent);
    animation: rainFall linear infinite;
}
@keyframes rainFall { from { transform: translateY(0); } to { transform: translateY(190vh); } }

.bgi {
    position: fixed; z-index: 0; pointer-events: none; color: rgba(255,100,115,.72);
    filter: drop-shadow(0 0 10px rgba(239,68,68,.9));
    animation: iconFloat ease-in-out infinite;
}
@keyframes iconFloat {
    0%,100% { transform: translateY(0) rotate(-6deg); opacity: .55; }
    50%     { transform: translateY(-34px) rotate(8deg); opacity: .95; }
}

.chip {
    position: fixed; z-index: 0; pointer-events: none; padding: 7px 15px;
    border: 1px solid rgba(248,113,113,.8); background: rgba(55,6,12,.82);
    color: #fecaca; font-size: .85rem; font-weight: 800; letter-spacing: 1.8px;
    border-radius: 6px; box-shadow: 0 0 18px rgba(239,68,68,.45);
    animation: chipFloat ease-in-out infinite;
}
@keyframes chipFloat {
    0%,100% { transform: translate(0,0); opacity: .6; }
    50%     { transform: translate(14px,-22px); opacity: 1; }
}

.star { position: fixed; z-index: 0; pointer-events: none; width: 4px; height: 4px; border-radius: 50%;
        background: #ff8090; box-shadow: 0 0 10px #ff2a44; animation: twinkle 3s ease-in-out infinite; }
@keyframes twinkle { 0%,100% { opacity: .25; transform: scale(.7);} 50% { opacity: 1; transform: scale(1.6);} }

.orb { border-radius: 50%; filter: blur(70px); animation: orbDrift 16s ease-in-out infinite alternate; }
.orb.o1 { width: 380px; height: 380px; left: -6%; top: 10%; background: rgba(225,29,46,.38); }
.orb.o2 { width: 460px; height: 460px; right: -8%; top: 42%; background: rgba(160,10,30,.42); animation-duration: 22s; }
.orb.o3 { width: 300px; height: 300px; left: 38%; top: -8%; background: rgba(255,60,80,.25); animation-duration: 19s; }
@keyframes orbDrift { from { transform: translate(0,0) scale(1);} to { transform: translate(60px,-50px) scale(1.25);} }

.bg-radar {
    left: -150px; bottom: -150px; width: 440px; height: 440px; border-radius: 50%;
    border: 1.5px solid rgba(248,113,113,.75);
    background: repeating-radial-gradient(circle, transparent 0 38px, rgba(239,68,68,.45) 39px 40px);
    box-shadow: 0 0 40px rgba(239,68,68,.45), inset 0 0 40px rgba(239,68,68,.25);
    opacity: .85;
}
.bg-radar::after {
    content: ""; position: absolute; inset: 0; border-radius: 50%;
    background: conic-gradient(from 0deg, rgba(255,42,68,.85), transparent 28%);
    animation: spin 4.5s linear infinite;
}

.hud { width: 54px; height: 54px; border: 0 solid rgba(255,100,115,.95); animation: hudPulse 2.6s ease-in-out infinite; }
.hud.tl { top: 14px; left: 14px; border-top-width: 3px; border-left-width: 3px; }
.hud.tr { top: 14px; right: 14px; border-top-width: 3px; border-right-width: 3px; }
.hud.bl { bottom: 44px; left: 14px; border-bottom-width: 3px; border-left-width: 3px; }
.hud.br { bottom: 44px; right: 14px; border-bottom-width: 3px; border-right-width: 3px; }
@keyframes hudPulse { 0%,100% { opacity: .55; } 50% { opacity: 1; filter: drop-shadow(0 0 8px #ff2a44); } }

.bg-ticker {
    left: 0; bottom: 0; width: 100%; height: 36px; overflow: hidden; z-index: 3;
    background: rgba(25,4,8,.94); border-top: 1px solid rgba(248,113,113,.7);
}
.bg-ticker div {
    display: inline-block; white-space: nowrap; line-height: 36px; color: #fecaca;
    font-size: .9rem; font-weight: 800; letter-spacing: 2px; animation: tick 40s linear infinite;
}
@keyframes tick { from { transform: translateX(0); } to { transform: translateX(-50%); } }

.intro-terminal-box {
    background: rgba(14, 3, 6, 0.96);
    border: 1px solid rgba(248, 113, 113, 0.65);
    border-radius: 14px;
    padding: 1.5rem 1.8rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.05rem;
    color: #fecaca;
    line-height: 1.65;
    box-shadow: inset 0 0 30px rgba(220, 38, 38, 0.16), 0 10px 30px rgba(0, 0, 0, 0.7);
    margin: 1.8rem auto;
    max-width: 1100px;
    position: relative;
    z-index: 2;
}
.terminal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(248, 113, 113, 0.4);
    padding-bottom: 0.6rem;
    margin-bottom: 0.9rem;
    color: #ffffff;
    font-size: 0.95rem;
    font-weight: 700;
    letter-spacing: 1.5px;
}
.terminal-dots {
    display: flex;
    gap: 6px;
}
.tdot { width: 12px; height: 12px; border-radius: 50%; }
.tdot.red { background: #ef4444; }
.tdot.yellow { background: #f59e0b; }
.tdot.green { background: #10b981; }

.cyber-stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.2rem;
    max-width: 1100px;
    margin: 1.8rem auto;
    position: relative;
    z-index: 2;
}
.cyber-stat-card {
    background: rgba(20, 5, 8, 0.92);
    border: 1px solid rgba(248, 113, 113, 0.5);
    border-radius: 12px;
    padding: 1.4rem;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.65);
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.cyber-stat-card:hover {
    transform: translateY(-4px);
    border-color: #ef4444;
}
.stat-num {
    font-size: 2.4rem;
    font-weight: 900;
    color: #ffffff;
    text-shadow: 0 0 15px rgba(239, 68, 68, 0.85);
    margin-bottom: 0.25rem;
}
.stat-label {
    font-size: 0.95rem;
    text-transform: uppercase;
    letter-spacing: 1.4px;
    color: #f1f5f9;
    font-weight: 800;
}

.clean-banner {
    position: relative;
    z-index: 2;
    max-width: 1100px;
    margin: 2rem auto 1.5rem auto;
    height: 210px;
    border-radius: 20px;
    overflow: hidden;
    background: linear-gradient(135deg, rgba(24, 7, 10, 0.95) 0%, rgba(12, 3, 5, 0.98) 100%);
    border: 1.5px solid rgba(248, 113, 113, 0.55);
    box-shadow: 0 0 45px rgba(239, 68, 68, 0.35);
}
.clean-banner-content {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: space-around;
    flex-wrap: wrap;
    background: radial-gradient(circle at center, rgba(239, 68, 68, 0.15) 0%, transparent 70%);
    padding: 1rem;
    z-index: 2;
}
.stat { text-align: center; color: #ffffff; }
.stat b { display: block; font-size: 2.8rem; font-weight: 900; color: #ff5a6e; text-shadow: 0 0 18px rgba(239,68,68,.9); }
.stat small { letter-spacing: 2px; color: #ffffff; font-weight: 800; font-size: .95rem; }
.scan-line {
    position: absolute; left: 0; width: 100%; height: 3px; z-index: 4;
    background: linear-gradient(90deg, transparent, #ff2a44, transparent);
    box-shadow: 0 0 18px #ff2a44; animation: scan 3.2s linear infinite;
}
@keyframes scan { from { top: 0; } to { top: 100%; } }

@media (max-width: 768px) {
    .block-container, [data-testid="stMainBlockContainer"] {
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
    }
    .bg-radar, .chip, .hud { display: none; }
    .bg-grid { height: 35vh; }
    .L-hero {
        padding: 1.5rem 0.2rem 1rem 0.2rem;
        gap: 1.2rem;
    }
    .L-title { font-size: 3.5rem; }
    .L-pick { font-size: 1.4rem; letter-spacing: 1px; }
    .L-desc { font-size: 1.1rem; }
    .L-right { min-height: 340px; }
    .L-robot { width: 240px; }
    .L-scene { width: 340px; height: 340px; }
    .L-ring, .L-ring.r2 { display: none; }
    .clean-banner { height: auto; min-height: 190px; }
    .stat b { font-size: 2.1rem; }
    .stat small { font-size: 0.82rem; }
    .hero-container { padding: 1.6rem 1.4rem; }
    .hero-title { font-size: 2.4rem; }
    .hero-accent { font-size: 1.3rem; }
    .hero-right { min-width: 100%; }
}
</style>
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
ROBOT_SVG = " ".join(line.strip() for line in ROBOT_SVG.splitlines() if line.strip())

# =========================================================
# PAGE 1: LANDING & INTRODUCTION PAGE
# =========================================================
if st.session_state["page"] == "landing":
    plex = img64(IMG_PLEXUS)
    scene = img64(IMG_SCENE)

    st.markdown(
        "<style>"
        f'.bg-plexus, .bg-plexus2 {{ background-image: url("{plex}"); }}'
        f'.img-scene {{ background-image: url("{scene}"); }}'
        "</style>"
        '<div class="bg-plexus"></div>'
        '<div class="bg-plexus2"></div>'
        '<div class="bg-vignette"></div>',
        unsafe_allow_html=True,
    )

    rnd = random.Random(7)

    ICONS = {
        "lock":   '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
        "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
        "bug":    '<ellipse cx="12" cy="14" rx="4" ry="6"/><path d="M12 8V5M8 11L4 9M16 11l4-2M8 15H3M16 15h5M9 19l-3 3M15 19l3 3"/>',
        "key":    '<circle cx="8" cy="12" r="4"/><path d="M12 12h9M18 12v4M15 12v3"/>',
        "wifi":   '<path d="M2 9a15 15 0 0 1 20 0M5 13a10 10 0 0 1 14 0M8.5 16.5a5 5 0 0 1 7 0"/><circle cx="12" cy="20" r="1"/>',
        "search": '<circle cx="10" cy="10" r="6"/><path d="M15 15l6 6"/>',
        "warn":   '<path d="M12 3L2 21h20z"/><path d="M12 10v5M12 18v.5"/>',
        "mail":   '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 7 9-7"/>',
    }
    icon_layout = [
        ("lock", 6, 14, 54, 7, 0), ("shield", 20, 70, 62, 9, 1), ("bug", 44, 8, 46, 8, 2),
        ("key", 33, 38, 44, 10, 0.5), ("wifi", 60, 82, 52, 7, 3), ("search", 52, 52, 50, 9, 1.5),
        ("warn", 90, 14, 48, 8, 2.5), ("mail", 78, 60, 50, 10, 0), ("lock", 92, 78, 44, 9, 4),
        ("shield", 3, 48, 40, 8, 2), ("bug", 70, 30, 40, 11, 1), ("key", 12, 88, 42, 8, 3),
    ]
    icons_html = "".join(
        f'<svg class="bgi" style="left:{x}%;top:{y}%;width:{s}px;height:{s}px;animation-duration:{d}s;animation-delay:{dl}s" '
        f'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">{ICONS[n]}</svg>'
        for n, x, y, s, d, dl in icon_layout
    )

    chip_layout = [
        ("ACCESS DENIED", 4, 30, 6), ("BREACH DETECTED", 40, 90, 8), ("SCANNING...", 66, 6, 7),
        ("SECURITY ALERT", 84, 44, 9), ("THREAT BLOCKED", 22, 55, 7), ("ENCRYPTED", 58, 68, 6),
        ("FIREWALL ACTIVE", 8, 76, 8), ("PHISHING FOUND", 88, 88, 7),
    ]
    chips_html = "".join(
        f'<div class="chip" style="left:{x}%;top:{y}%;animation-duration:{d}s">{t}</div>'
        for t, x, y, d in chip_layout
    )

    rain_chars = "01ABCDEF9X#$%"
    rain_html = "".join(
        f'<div class="rain" style="left:{i * 4.4 + rnd.uniform(0, 2):.1f}%;font-size:{rnd.randint(11, 15)}px;'
        f'animation-duration:{rnd.randint(11, 24)}s;animation-delay:-{rnd.randint(0, 20)}s">'
        + "<br>".join(rnd.choice(rain_chars) for _ in range(26)) + "</div>"
        for i in range(23)
    )

    stars_html = "".join(
        f'<i class="star" style="left:{rnd.uniform(0, 100):.1f}%;top:{rnd.uniform(0, 95):.1f}%;'
        f'animation-delay:{rnd.uniform(0, 3):.1f}s;animation-duration:{rnd.uniform(2, 5):.1f}s"></i>'
        for _ in range(55)
    )

    ticker_text = ("⚠ PHISHING ATTEMPT BLOCKED &nbsp;•&nbsp; ✔ HTTPS VERIFIED &nbsp;•&nbsp; ⚠ SPOOFED SENDER DETECTED "
                   "&nbsp;•&nbsp; ✔ PASSWORD HARDENED &nbsp;•&nbsp; ⚠ MALICIOUS LINK FLAGGED &nbsp;•&nbsp; "
                   "✔ ZERO DATA STORED &nbsp;•&nbsp; ")

    bg_extra = (
        '<div class="bgx orb o1"></div><div class="bgx orb o2"></div><div class="bgx orb o3"></div>'
        + rain_html
        + '<div class="bgx bg-grid"></div>'
        + '<div class="bgx bg-radar"></div>'
        + stars_html + icons_html + chips_html
        + '<div class="bgx hud tl"></div><div class="bgx hud tr"></div>'
        + '<div class="bgx hud bl"></div><div class="bgx hud br"></div>'
        + f'<div class="bgx bg-ticker"><div>{ticker_text * 2}</div></div>'
    )
    st.markdown(bg_extra, unsafe_allow_html=True)

    hero_html = (
        '<div class="L-hero">'
        '<div class="L-left">'
        '<div class="cyber-badge-box" style="margin-bottom:1.2rem;">● AI CYBERSECURITY DEFENSE SYSTEM</div>'
        '<div class="L-title">PhishTrace</div>'
        '<div class="L-pick">Multichannel Phishing Detection</div>'
        '<div style="margin: 1rem 0 1.4rem 0;"><span class="cyber-badge-box" style="font-size:1.15rem; padding:12px 26px;">DETECT • PROTECT • PREVENT</span></div>'
        '<div class="L-desc">An AI-inspired cybersecurity defense platform engineered to neutralize phishing traps, '
        'expose deceptive links, evaluate password entropy, and inspect live inbox emails before threats strike.</div>'
        '<div style="margin-top:1.5rem;"><span class="cyber-badge-box" style="font-size:0.95rem; padding:8px 18px;">FIREWALL ACTIVE</span></div>'
        '</div>'
        '<div class="L-right">'
        '<div class="L-ring"></div><div class="L-ring r2"></div>'
        '<div class="L-scene img-scene"></div>'
        f'<div class="L-robot">{ROBOT_SVG}</div>'
        '</div>'
        '</div>'
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    terminal_html = """
    <div class="intro-terminal-box">
        <div class="terminal-header">
            <span>[SYS_LOG] PHISHTRACE LIVE DEFENSE KERNEL STREAM</span>
            <div class="terminal-dots">
                <div class="tdot red"></div>
                <div class="tdot yellow"></div>
                <div class="tdot green"></div>
            </div>
        </div>
        <div>&gt; initializing multichannel threat inspection pipeline... OK</div>
        <div>&gt; loading 4-layer security checkpoints (Message, URL, Password, Inbox)... READY</div>
        <div>&gt; status: ALL SYSTEMS ARMED. ZERO-TRUST PROTOCOL ACTIVE.</div>
    </div>
    """
    st.markdown(terminal_html, unsafe_allow_html=True)

    stats_grid_html = """
    <div class="cyber-stats-grid">
        <div class="cyber-stat-card">
            <div class="stat-num">100%</div>
            <div class="stat-label">Client-Side Privacy</div>
        </div>
        <div class="cyber-stat-card">
            <div class="stat-num">&lt;0.1s</div>
            <div class="stat-label">Scan Latency</div>
        </div>
        <div class="cyber-stat-card">
            <div class="stat-num">4 Core</div>
            <div class="stat-label">Defense Checkpoints</div>
        </div>
        <div class="cyber-stat-card">
            <div class="stat-num">24/7</div>
            <div class="stat-label">Active Monitoring</div>
        </div>
    </div>
    """
    st.markdown(stats_grid_html, unsafe_allow_html=True)

    clean_banner_html = """
    <div class="clean-banner">
        <div class="scan-line"></div>
        <div class="clean-banner-content">
            <div class="stat"><b>4</b><small>SECURITY CHECKPOINTS</small></div>
            <div class="stat"><b>24/7</b><small>ACTIVE DEFENSE</small></div>
            <div class="stat"><b>0</b><small>DATA STORED</small></div>
        </div>
    </div>
    """
    st.markdown(clean_banner_html, unsafe_allow_html=True)

    modules = [
        ("Module 01", "Phishing Defense", "Scans SMS/text payloads for fraudulent prize claims and urgency triggers."),
        ("Module 02", "URL Inspector", "Analyzes target web links for unencrypted protocols and masked domains."),
        ("Module 03", "Password Guard", "Evaluates password entropy and calculates brute-force cracking resistance."),
        ("Module 04", "Inbox Email Inspector", "Directly paste or sync inbox emails to scan for spam headers & sender spoofing."),
    ]
    cols = st.columns(4, gap="medium")
    for col, (tag, title, desc) in zip(cols, modules):
        with col:
            st.markdown(
                f'<div class="feature-card-ui" style="position:relative;z-index:2;">'
                f'<div class="mod-tag">{tag}</div>'
                f'<h4 class="mod-title">{title}</h4>'
                f'<p class="mod-desc">{desc}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.write("")
    st.write("")

    btn_col1, btn_col2, btn_col3 = st.columns([1.5, 2.5, 1.5])
    with btn_col2:
        if st.button("LAUNCH PHISHTRACE COMMAND CENTER →", key="launch_btn", type="primary", use_container_width=True):
            st.session_state["page"] = "app"
            st.rerun()

# =========================================================
# PAGE 2: THE WORKING APPLICATION (DASHBOARD & CHECKPOINTS)
# =========================================================
else:
    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([1.4, 1.3, 1.3, 1.3, 1.4])

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
                <div class="hero-title">PhishTrace<br>Multichannel Phishing Detection</div>
                <div class="hero-accent">Detect • Protect • Prevent</div>
                <div class="hero-sub">
                    An AI-inspired cybersecurity defense platform engineered to neutralize phishing traps, expose deceptive links, evaluate password entropy, and inspect live inbox emails before threats strike.
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
        st.markdown("### Phishing & Scam Message Analyzer")
        st.caption("Paste any suspicious SMS, WhatsApp text, or email below to scan for scam indicators.")

        d_col1, d_col2, _ = st.columns([1.4, 1.4, 2.2])
        with d_col1:
            if st.button("Load Demo 1 (Scam Message)", key="demo_msg_1", use_container_width=True):
                st.session_state["form_msg_input"] = "Congratulations! You won a free iPhone. Click this suspicious link immediately!"
                st.rerun()
        with d_col2:
            if st.button("Load Safe Message", key="demo_msg_2", use_container_width=True):
                st.session_state["form_msg_input"] = "Hello! Reminder that our PhishTrace project presentation is on Monday."
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
        st.markdown("### Deceptive URL & Link Inspector")
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
        st.markdown("### Password Strength & Brute-Force Evaluator")
        st.caption("Test password complexity against modern cracking techniques (Zero storage policy).")

        d_col1, d_col2, _ = st.columns([1.4, 1.4, 2.2])
        with d_col1:
            if st.button("Load Demo 3 (Strong Password)", key="demo_pwd_1", use_container_width=True):
                st.session_state["form_pwd_input"] = "Ph1shTr@ce_2026!"
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
        st.markdown("### Inbox Email Spam & Spoofing Inspector")
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
                st.session_state["form_mail_input"] = "Hello Hafsa, your pull request in PhishTrace repo was successfully merged."
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
        <div class="layers-label">PhishTrace Core Protection Modules</div>
        <div class="layers-logos">
            <span>ANTI-PHISHING</span>
            <span>HTTPS ENCRYPTION</span>
            <span>ZERO-TRUST CHECKS</span>
            <span>CREDENTIAL HARDENING</span>
            <span>INBOX EMAIL GUARD</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
