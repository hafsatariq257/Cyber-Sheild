# 🛡️ CYBER SHIELD — Your Digital Bodyguard
**Detect • Protect • Prevent**

Cyber Shield is an interactive, AI-inspired cybersecurity defense simulator and educational dashboard built with Python and Streamlit. Engineered for real-time threat awareness, it enables users to scan suspicious messages, inspect deceptive URLs, evaluate password resilience against brute-force attacks, and check inbox emails for spoofing or spam indicators—all with a strict zero-data-storage privacy policy.

---

## ✨ Key Features & Security Checkpoints

* **Introductory Command Landing Page:** Features a dark cyber-crimson interface with an animated SVG Cyber-Sentinel backdrop, floating background nodes, and module overview before launching into the interactive dashboard.
* **Checkpoint 01 — Phishing & Scam Message Analyzer:** Scans SMS, WhatsApp, and text payloads for unrealistic prize bait, high-pressure urgency triggers, and suspicious link/credential requests, generating a live `0–100` Threat Risk Score.
* **Checkpoint 02 — Deceptive URL & Link Inspector:** Evaluates website links prior to visiting to flag unencrypted `HTTP` connections, masked URL shorteners (`bit.ly`, `tinyurl.com`, etc.), raw IP addresses, `@` redirection tricks, and deceptive domain keywords.
* **Checkpoint 03 — Password Strength & Brute-Force Evaluator:** Analyzes character length, casing, digits, and special symbols against cryptographic complexity standards and calculates an estimated brute-force crack time (from *Instantly* to *412 Years*).
* **Checkpoint 04 — Inbox Email Spam & Spoofing Guard:** Inspects sender email addresses and message bodies to catch domain spoofing (e.g., official bank or support names sent from free public domains like `@gmail.com`) and phishing triggers.
* **Built-in Live Demo Presets:** One-click sample buttons across all four checkpoints allow instant testing of both malicious and safe scenarios during live presentations.

---

## 🛠️ Tech Stack

* **Language:** Python 3.8+
* **Web Framework:** Streamlit
* **Frontend Styling:** Custom CSS3 (Keyframes, Glassmorphism, Radial Gradients) & Inline Animated SVG
* **Core Libraries:** Python Standard Library (`re`, `urllib.parse`)

---

## 🚀 Installation & Local Setup

1. **Clone or download the repository**
   ```bash
   git clone [https://github.com/your-username/cyber-shield.git](https://github.com/your-username/cyber-shield.git)
   cd cyber-shield

2. **Create and activate a virtual environment (recommended)**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

```


3. **Install Streamlit**
```bash
pip install streamlit

```


4. **Run the application**
```bash
streamlit run app.py

```



---

## 📂 Project Structure

```text
cyber-shield/
├── app.py              # Main Streamlit application, UI styling, & threat detection engine
└── README.md           # Project documentation

```

---

## 🔒 Privacy & Security Disclaimer

Cyber Shield operates entirely in-memory during your active browser session. **Zero personal messages, URLs, emails, or test passwords are saved, logged, or transmitted to external servers.** This tool is designed for cybersecurity education, awareness training, and real-time threat simulation.

```

```
