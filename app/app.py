import os
import re
import sys
import html
import time
import datetime

import streamlit as st

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

st.set_page_config(
    page_title="CyberSafe Assistant — Cybersecurity Awareness",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------
# Backend loading — safely imports get_chatbot_response + reset_chat
# ------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_backend():
    try:
        from src.chatbot import get_chatbot_response
        return get_chatbot_response, None
    except Exception as e:                      # e.g. ValueError: key missing
        return None, str(e)

BACKEND_FN, BACKEND_ERR = load_backend()

# ------------------------------------------------------------
# Timestamp helpers — weekday + date + time (WhatsApp style)
# ------------------------------------------------------------
def fmt_stamp(ts: float) -> str:
    """e.g. 'Fri 27 Nov, 7:24 AM'"""
    dt = datetime.datetime.fromtimestamp(ts)
    return dt.strftime("%a %d %b, ") + dt.strftime("%I:%M %p").lstrip("0")

def fmt_day(d: datetime.date) -> str:
    """Day-divider label with the full day name and date."""
    today = datetime.date.today()
    full = d.strftime("%A, %d %b %Y")
    if d == today:
        return f"Today · Hari ini — {full}"
    if d == today - datetime.timedelta(days=1):
        return f"Yesterday · Semalam — {full}"
    return full

# ------------------------------------------------------------
# Error intelligence — friendly cards, never raw JSON / secrets
# ------------------------------------------------------------
def sanitize(text: str) -> str:
    text = re.sub(r"(AIza[0-9A-Za-z_\-]{8,}|sk-[0-9A-Za-z_\-]{8,})", "[hidden]", str(text))
    text = re.sub(r"\s+", " ", text).strip()
    return text[:160] + ("…" if len(text) > 160 else "")

def classify_error(raw: str) -> dict:
    t = str(raw).lower()
    def err(kind, sev, icon, title, body, hint, retryable):
        return dict(kind=kind, severity=sev, icon=icon, title=title,
                    body=body, hint=hint, retryable=retryable)
    if ("missing" in t and "key" in t) or "check your .env" in t:
        return err("error_config", "danger", "🔧", "Setup needed · Persediaan diperlukan",
                   "The chatbot engine can't find its Gemini API key, so it can't answer yet. "
                   "Mesin chatbot tidak menjumpai kunci API Gemini.",
                   "Team: create a .env file at the project root with GEMINI_API_KEY=your-key "
                   "(see .env.example), then restart the app.", False)
    if "api_key_invalid" in t or "api key not valid" in t or "invalid api key" in t \
       or ("400" in t and "key" in t) or "permission_denied" in t or "403" in t:
        return err("error_config", "danger", "🔧", "API key rejected · Kunci API ditolak",
                   "Google rejected the configured API key. The team needs to check the .env file. "
                   "Google menolak kunci API — pasukan perlu menyemak fail .env.",
                   "Team: verify GEMINI_API_KEY is the full, active key from Google AI Studio, then restart.", False)
    if "503" in t or "unavailable" in t or "high demand" in t or "overloaded" in t:
        return err("error_busy", "warn", "🚦", "AI is busy right now · AI sedang sibuk",
                   "The Gemini service is temporarily overloaded — this is Google's side, not your question. "
                   "Perkhidmatan Gemini sedang sibuk buat sementara waktu.",
                   "Wait a few seconds and press “Try again” below. Your question is saved. "
                   "Tunggu beberapa saat dan tekan “Cuba lagi”.", True)
    if "429" in t or "resource_exhausted" in t or "quota" in t or "rate limit" in t:
        return err("error_rate", "warn", "⏳", "Rate limit reached · Had kadar dicapai",
                   "The free API quota was hit for this minute. Nothing is broken — it resets shortly. "
                   "Kuota API percuma telah dicapai buat masa ini.",
                   "Wait about a minute, then press “Try again”. Tunggu ~1 minit dan cuba lagi.", True)
    if "404" in t or "not_found" in t or ("model" in t and "not found" in t):
        return err("error_config", "danger", "🔧", "Model not found · Model tidak dijumpai",
                   "The backend is requesting a model name that doesn't exist. "
                   "Backend meminta nama model yang tidak wujud.",
                   "Team: check the model name in src/chatbot.py (e.g. gemini-3.5-flash-lite).", False)
    if any(k in t for k in ("timeout", "timed out", "deadline", "connection", "getaddrinfo",
                            "name resolution", "ssl", "network", "unreachable", "max retries")):
        return err("error_network", "info", "📡", "Connection problem · Masalah sambungan",
                   "I couldn't reach the AI service — check your internet connection. "
                   "Saya tidak dapat menghubungi perkhidmatan AI — semak sambungan internet anda.",
                   "Reconnect and press “Try again”. Sambung semula dan cuba lagi.", True)
    return err("error_generic", "danger", "⚠️", "Something went wrong · Berlaku ralat",
               "An unexpected error occurred while contacting the AI. "
               "Ralat tidak dijangka berlaku semasa menghubungi AI.",
               "Details: " + sanitize(raw), True)

def call_backend(question: str):
    """Call Syasya's function with bounded auto-retry for transient errors."""
    if BACKEND_FN is None:
        return None, classify_error(BACKEND_ERR or "Backend not available")
    last_err = None
    for attempt in range(3):
        try:
            answer = BACKEND_FN(question)
            if answer is None or not str(answer).strip():
                raise ValueError("The backend returned an empty response.")
            return str(answer).strip(), None
        except Exception as e:
            last_err = classify_error(str(e))
            if last_err["retryable"] and attempt < 2:
                if hasattr(st, "toast"):
                    st.toast(f"🚦 AI busy — retrying ({attempt + 2}/3)…", icon="⏳")
                time.sleep(1.2 * (attempt + 1))
                continue
            return None, last_err
    return None, last_err

# ------------------------------------------------------------
# Language intelligence — greetings, typos, Malay, sentiment
# (word-boundary matching so "phishing" never triggers "hi")
# ------------------------------------------------------------
GREETING_RE = re.compile(
    r"^\s*(?:hi+|hello+|helo+|hey+|hai+|hlw|hiya|yo|salam|assalamu'?alaikum|"
    r"selamat\s+(?:pagi|petang|tengah\s?hari|malam|sejahtera)|"
    r"good\s+(?:morning|afternoon|evening|night))"
    r"(?:\s+(?:bot|there|all|everyone|semua|team|kawan))*\s*[!.,?🙂👋]*\s*$", re.I)
POSITIVE_RE = re.compile(
    r"^\s*(?:thanks?(?:\s+(?:you|a\s?lot|so\s?much))?|thx|ty|tq|terima\s?kasih|"
    r"awesome|great|nice|good\s?bot|bagus|terbaik|mantap|syukur|alhamdulillah)"
    r"(?:\s+(?:bot|so\s?much|very\s?much))*\s*[!.,🙂🙏]*\s*$", re.I)
EMPATHY_RE = re.compile(
    r"\b(angry|hate|stupid|useless|frustrat\w*|annoy\w*|dumb|idiot|upset|furious|mad|"
    r"marah|benci|bodoh|teruk|menyusahkan|geram|hampeh|kecewa|stress|tertekan|"
    r"tak\s?guna|waste\s?of\s?time)\b", re.I)
OFFDOMAIN_RE = re.compile(
    r"\b(resep\w*|recipe|nasi\s?lemak|pantun|poem|sajak|syair|filem|movie|film|bola|"
    r"football|soccer|cuaca|weather|capital\s?of|ibu\s?negeri|lagu|song|lirik|lyrics|"
    r"math\w*|matematik|homework|kerja\s?sekolah|translate|terjemah\w*|joke|lawak|"
    r"dating|crush|bitcoin|harga\s?emas)\b", re.I)
CYBER_RE = re.compile(
    r"\b(phish\w*|password|kata\s?laluan|malware|mfa|2fa|hack\w*|godam|scam|penipuan|"
    r"wi-?fi|privacy|privasi|vpn|virus|link|pautan|email|akaun|account|otp|data|"
    r"safe|selamat|secure|security|keselamatan|siber|cyber|online|dalam\s?talian)\b", re.I)
OOD_MARKERS = ("i do not know", "i don't know", "outside my domain", "outside the scope",
               "not related to", "i cannot answer", "i can only", "saya tidak tahu",
               "di luar skop", "tiada kaitan", "tidak berkaitan", "saya hanya boleh")

GREETING_REPLY = ("Hello! 👋 Hai! I'm your Cybersecurity Awareness Assistant. "
                  "Ask me about phishing, passwords, MFA, malware, privacy or safe browsing — "
                  "in English or Bahasa Melayu, typos welcome! "
                  "Tanya saya tentang keselamatan siber dalam BM atau English. 😊")
POSITIVE_REPLY = ("You're welcome! 🌟 Sama-sama! Stay safe online, and ask me anything "
                  "else about cybersecurity whenever you like. Jaga keselamatan dalam talian! 🛡️")
EMPATHY_REPLY = ("I'm sorry you're feeling frustrated — that's completely understandable. 💛 "
                 "Saya faham anda mungkin berasa kecewa atau marah, dan itu okay. "
                 "I'm here to help, not to judge. Could you tell me what you're trying to do "
                 "(e.g. recover an account, spot a scam, secure your phone)? "
                 "Beritahu saya apa yang anda cuba selesaikan — saya akan bantu langkah demi langkah.")
OOD_BODY = ("I do not know. Please ask the Cybersecurity Awareness Assistant about online safety — "
            "phishing, passwords, MFA, malware, social engineering, privacy or safe internet use. "
            "Saya tidak tahu. Sila tanya soalan berkaitan keselamatan siber seperti phishing, "
            "kata laluan, MFA, malware, privasi atau pelayaran selamat.")

def answer_question(q: str) -> dict:
    ans, err = call_backend(q)
    if ans is not None:
        if any(m in ans.lower() for m in OOD_MARKERS):
            return dict(role="assistant", kind="ood", content=OOD_BODY)
        return dict(role="assistant", kind="normal", content=ans)
    return dict(role="assistant", kind=err["kind"], content=err["body"],
                title=err["title"], hint=err["hint"], icon=err["icon"],
                severity=err["severity"], retryable=err["retryable"], q=q)

def route_question(q: str) -> dict:
    t = q.strip()
    if GREETING_RE.match(t):
        return dict(role="assistant", kind="normal", content=GREETING_REPLY)
    if POSITIVE_RE.match(t):
        return dict(role="assistant", kind="normal", content=POSITIVE_REPLY)
    if EMPATHY_RE.search(t):
        return dict(role="assistant", kind="empathy", content=EMPATHY_REPLY)
    if OFFDOMAIN_RE.search(t) and not CYBER_RE.search(t):
        return dict(role="assistant", kind="ood", content=OOD_BODY)
    return answer_question(t)

# ------------------------------------------------------------
# Safe markdown-lite renderer for Gemini answers
# ------------------------------------------------------------
def _inline(s: str) -> str:
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return s

def md_to_html(text: str) -> str:
    lines = html.escape(text.strip()).split("\n")
    out, para, items, mode = [], [], [], None
    def flush():
        nonlocal para, items, mode
        if para:
            out.append("<p>" + "<br>".join(_inline(p) for p in para) + "</p>"); para = []
        if items:
            tag = "ol" if mode == "ol" else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{_inline(i)}</li>" for i in items) + f"</{tag}>")
            items = []
        mode = None
    for ln in lines:
        s = ln.strip()
        if not s:
            flush(); continue
        m = re.match(r"^(?:-|\*|•)\s+(.*)", s)
        n = re.match(r"^\d+[.)]\s+(.*)", s)
        h = re.match(r"^#{1,4}\s+(.*)", s)
        if m:
            if mode not in (None, "ul"): flush()
            mode = "ul"; items.append(m.group(1))
        elif n:
            if mode not in (None, "ol"): flush()
            mode = "ol"; items.append(n.group(1))
        elif h:
            flush(); out.append(f"<h4>{_inline(h.group(1))}</h4>")
        else:
            if mode: flush()
            para.append(s)
    flush()
    return "".join(out) or "<p></p>"

# ------------------------------------------------------------
# Visual system — midnight SOC palette + WhatsApp stamps
# ------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@500&display=swap');
:root{--bg0:#05070F;--bg1:#0A1220;--surface:rgba(13,22,38,.82);--ink:#EAF3FF;--muted:#9FB3D1;
--line:rgba(148,197,255,.16);--cyan:#22D3EE;--blue:#3B82F6;--green:#34D399;--acid:#A3E635;
--amber:#FBBF24;--red:#F87171;--rose:#FB7185;--violet:#8B5CF6;}
html,body,*{scrollbar-width:thin;scrollbar-color:var(--cyan) var(--bg1);}
*::-webkit-scrollbar{width:10px;height:10px}
*::-webkit-scrollbar-track{background:var(--bg1);border-radius:999px}
*::-webkit-scrollbar-thumb{background:linear-gradient(180deg,var(--cyan),var(--blue));
border-radius:999px;border:2px solid var(--bg1)}
*::-webkit-scrollbar-thumb:hover{background:linear-gradient(180deg,#67E8F9,#60A5FA)}
.stApp{background:linear-gradient(160deg,rgba(5,8,16,.90),rgba(8,14,28,.92) 45%,rgba(6,20,26,.94)),
url('https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1920&q=80')
center/cover fixed no-repeat;color:var(--ink);font-family:'Inter',system-ui,'Segoe UI',sans-serif;}
.stApp::before{content:"";position:fixed;inset:-20%;z-index:0;pointer-events:none;
background:radial-gradient(42% 34% at 18% 12%,rgba(34,211,238,.14),transparent 70%),
radial-gradient(38% 30% at 84% 78%,rgba(139,92,246,.13),transparent 70%),
radial-gradient(30% 26% at 70% 18%,rgba(163,230,53,.07),transparent 70%);
animation:aurora 26s ease-in-out infinite alternate;}
.stApp::after{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;opacity:.5;
background:repeating-linear-gradient(0deg,rgba(148,197,255,.035) 0 1px,transparent 1px 56px),
repeating-linear-gradient(90deg,rgba(148,197,255,.035) 0 1px,transparent 1px 56px);}
@keyframes aurora{from{transform:translate3d(-2%,-1%,0) rotate(-1deg)}
to{transform:translate3d(2%,2%,0) rotate(1.5deg)}}
[data-testid="stAppViewContainer"]{position:relative;z-index:1}
header[data-testid="stHeader"]{background:transparent}
#MainMenu,footer{visibility:hidden}
.block-container{max-width:880px;padding-top:1.1rem;padding-bottom:2.2rem}
h1,h2,h3{font-family:'Space Grotesk','Inter',sans-serif;color:var(--ink)}
.brand{display:flex;align-items:center;gap:14px}
.brand .logo{width:52px;height:52px;border-radius:16px;display:grid;place-items:center;font-size:26px;
background:linear-gradient(135deg,#0EA5E9,#2563EB 55%,#7C3AED);border:1px solid rgba(103,232,249,.5);
box-shadow:0 0 26px rgba(34,211,238,.35)}
.brand h1{margin:0;font-size:1.55rem;line-height:1.1;background:linear-gradient(90deg,#67E8F9,#A3E635);
-webkit-background-clip:text;background-clip:text;color:transparent}
.brand .sub{font-size:.78rem;color:var(--muted);letter-spacing:.12em;text-transform:uppercase}
.status{display:inline-flex;align-items:center;gap:8px;font-family:'JetBrains Mono',monospace;
font-size:.7rem;letter-spacing:.1em;padding:7px 12px;border-radius:999px;border:1px solid var(--line);
background:var(--surface);white-space:nowrap}
.status .dot{width:8px;height:8px;border-radius:50%;animation:pulse 2s infinite}
.status.ok{color:#86EFAC;border-color:rgba(52,211,153,.5)}.status.ok .dot{background:var(--green)}
.status.warn{color:#FDE68A;border-color:rgba(251,191,36,.5)}.status.warn .dot{background:var(--amber)}
.status.bad{color:#FECACA;border-color:rgba(248,113,113,.5)}.status.bad .dot{background:var(--red)}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(255,255,255,.25)}50%{box-shadow:0 0 0 5px rgba(255,255,255,0)}}
.intro{margin:16px 0 6px;padding:18px 20px;border-radius:18px;
background:linear-gradient(135deg,rgba(34,211,238,.10),rgba(139,92,246,.10));
border:1px solid rgba(34,211,238,.35);backdrop-filter:blur(6px)}
.intro h3{margin:0 0 6px;font-size:1.05rem}
.intro p{margin:4px 0;color:#CFE3FF;font-size:.92rem;line-height:1.55}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.chip{border:1px solid rgba(163,230,53,.4);color:#D9F99D;background:rgba(163,230,53,.08);
padding:3px 11px;border-radius:999px;font-size:.7rem;letter-spacing:.05em}
.sec{font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);
margin:18px 0 8px;font-family:'JetBrains Mono',monospace}
.ghost{border:1px dashed rgba(148,197,255,.35);border-radius:16px;padding:26px 20px;text-align:center;
color:var(--muted);background:rgba(10,18,32,.5)}
.ghost .big{font-size:34px;display:block;margin-bottom:8px}
.msg{display:flex;gap:12px;margin:14px 0 4px;align-items:flex-start}
.msg.user{flex-direction:row-reverse}
.avatar{width:38px;height:38px;border-radius:12px;display:grid;place-items:center;font-size:19px;
flex:0 0 38px;border:1px solid var(--line)}
.msg.user .avatar{background:linear-gradient(135deg,#0EA5E9,#2563EB)}
.msg.bot .avatar{background:linear-gradient(135deg,#059669,#0D9488)}
.stack{max-width:80%;display:flex;flex-direction:column}
.msg.user .stack{align-items:flex-end}
.meta{font-size:.66rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0 2px 4px}
.bubble{padding:12px 16px;border-radius:16px;line-height:1.6;font-size:.94rem;border:1px solid var(--line);
box-shadow:0 10px 26px rgba(0,0,0,.35)}
.msg.user .bubble{background:linear-gradient(135deg,rgba(14,165,233,.30),rgba(37,99,235,.32));
border-color:rgba(56,189,248,.45);border-top-right-radius:4px;color:#EAF6FF}
.msg.bot .bubble{background:rgba(16,185,129,.14);border-color:rgba(52,211,153,.35);
border-top-left-radius:4px;color:#E9FBF3}
.bubble p{margin:.35em 0}.bubble ul,.bubble ol{margin:.35em 0;padding-left:1.2em}
.bubble h4{margin:.5em 0 .25em;font-size:.98rem;color:#A7F3D0}
.bubble code{background:rgba(34,211,238,.15);border:1px solid rgba(34,211,238,.3);padding:1px 6px;
border-radius:6px;font-family:'JetBrains Mono',monospace;font-size:.85em}
/* WhatsApp-style stamp: weekday + date + time under each bubble */
.stamp{font-family:'JetBrains Mono',monospace;font-size:.62rem;letter-spacing:.05em;
color:#7C8DB0;margin:4px 2px 0;display:flex;align-items:center;gap:5px}
.msg.user .stamp{justify-content:flex-end}
.stamp .tick{color:var(--cyan);font-size:.66rem}
/* Day divider pill with full day name + date */
.day-divider{display:flex;align-items:center;gap:10px;margin:20px 0 8px;color:#7C8DB0;
font-family:'JetBrains Mono',monospace;font-size:.62rem;letter-spacing:.12em;text-transform:uppercase}
.day-divider::before,.day-divider::after{content:"";flex:1;height:1px;
background:linear-gradient(90deg,transparent,rgba(148,197,255,.25),transparent)}
.day-divider span{border:1px solid var(--line);background:var(--surface);padding:3px 12px;border-radius:999px}
.card{padding:14px 16px;border-radius:16px;border:1px solid var(--line);background:var(--surface);
box-shadow:0 10px 26px rgba(0,0,0,.35);max-width:100%}
.card-top{display:flex;align-items:center;gap:10px;margin-bottom:6px}
.card-ico{font-size:20px}
.card-title{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:.95rem}
.card-body{font-size:.9rem;line-height:1.6;color:#DCE9FF}
.card .hint{margin-top:10px;padding-top:9px;border-top:1px dashed rgba(148,197,255,.3);
font-size:.78rem;color:var(--muted);line-height:1.5}
.tag{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:.6rem;letter-spacing:.1em;
padding:3px 8px;border-radius:999px;border:1px solid currentColor;opacity:.9}
.card.warn{background:rgba(251,191,36,.10);border-color:rgba(251,191,36,.5)}
.card.warn .card-title,.card.warn .tag{color:#FCD34D}
.card.danger{background:rgba(248,113,113,.10);border-color:rgba(248,113,113,.5)}
.card.danger .card-title,.card.danger .tag{color:#FCA5A5}
.card.info{background:rgba(59,130,246,.12);border-color:rgba(96,165,250,.5)}
.card.info .card-title,.card.info .tag{color:#93C5FD}
.card.scope{background:rgba(251,113,133,.10);border-color:rgba(251,113,133,.5)}
.card.scope .card-title{color:#FDA4AF}
.card.empathy{background:rgba(251,191,36,.08);border-color:rgba(251,191,36,.45)}
.card.empathy .card-title{color:#FDE68A}
.stButton>button,.stFormSubmitButton>button{min-height:44px;border-radius:12px;font-weight:600;
font-family:'Inter',sans-serif;background:linear-gradient(135deg,#0EA5E9,#2563EB);color:#fff;
border:1px solid rgba(103,232,249,.4);transition:transform .15s ease,box-shadow .15s ease}
.stButton>button:hover,.stFormSubmitButton>button:hover{transform:translateY(-1px);
box-shadow:0 8px 22px rgba(34,211,238,.35);color:#fff}
.stButton>button:focus-visible,.stFormSubmitButton>button:focus-visible{outline:2px solid var(--acid);
outline-offset:2px}
[data-testid="stBaseButton-secondary"]{background:rgba(34,211,238,.07);color:#A5F3FC;
border:1px solid rgba(34,211,238,.45)}
[data-testid="stBaseButton-secondary"]:hover{background:rgba(34,211,238,.16);color:#CFFAFE}
[data-testid="stForm"]{background:rgba(10,18,32,.74);border:1px solid var(--line);border-radius:16px;
padding:14px 16px;backdrop-filter:blur(8px)}
[data-testid="stTextInput"] input{background:#0B1526;color:var(--ink);
border:1px solid rgba(148,197,255,.28);border-radius:12px;padding:12px 14px}
[data-testid="stTextInput"] input:focus{border-color:var(--cyan);box-shadow:0 0 0 3px rgba(34,211,238,.22)}
[data-testid="stTextInput"] label p{color:var(--muted);font-size:.85rem}
[data-testid="stAlert"]{background:rgba(251,191,36,.12);border:1px solid rgba(251,191,36,.45);
color:#FDE68A;border-radius:12px}
[data-testid="stSpinner"] p{color:#A5F3FC}
.foot{color:#7C8DB0;font-size:.74rem;text-align:center;margin:20px 0 4px;line-height:1.6}
@media (max-width:640px){[data-testid="column"]{width:100%!important;flex:1 1 100%!important}
.stack{max-width:88%}.brand h1{font-size:1.25rem}.block-container{padding-left:1rem;padding-right:1rem}}
@media (prefers-reduced-motion:reduce){.stApp::before,.status .dot{animation:none}
.stButton>button,.stFormSubmitButton>button{transition:none}}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Session state
# ------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------------------------------------
# Header + live status
# ------------------------------------------------------------
last = st.session_state.messages[-1] if st.session_state.messages else None
if BACKEND_FN is None:
    s_cls, s_txt = "bad", "SETUP NEEDED"
elif last and last.get("kind") in ("error_busy", "error_rate"):
    s_cls, s_txt = "warn", "AI BUSY"
elif last and last.get("kind") == "error_network":
    s_cls, s_txt = "warn", "OFFLINE?"
else:
    s_cls, s_txt = "ok", "AI ONLINE"

h1, h2 = st.columns([3, 1.4], vertical_alignment="center")
with h1:
    st.markdown("""
    <div class="brand"><div class="logo">🛡️</div>
    <div><h1>CyberSafe Assistant</h1>
    <div class="sub">Cybersecurity Awareness · EN / BM</div></div></div>""", unsafe_allow_html=True)
with h2:
    st.markdown(f'<div style="text-align:right"><span class="status {s_cls}">'
                f'<span class="dot"></span>{s_txt}</span></div>', unsafe_allow_html=True)

st.markdown("""
<div class="intro">
  <h3>👋 Welcome! · Selamat Datang!</h3>
  <p>I help you stay safe online — spotting phishing, building strong passwords, enabling MFA,
     spotting malware and protecting your privacy. <i>Saya membantu anda kekal selamat dalam
     talian — mengenali phishing, kata laluan kukuh, MFA, malware dan privasi.</i></p>
  <p style="color:#9FB3D1;font-size:.8rem">Type naturally — typos and Bahasa Melayu are understood.
     Taip secara biasa — salah eja dan BM difahami. ✨</p>
  <div class="chips"><span class="chip">Phishing</span><span class="chip">Passwords</span>
  <span class="chip">MFA / 2FA</span><span class="chip">Malware</span>
  <span class="chip">Social Engineering</span><span class="chip">Wi-Fi Safety</span>
  <span class="chip">Privacy</span><span class="chip">Online Scams</span></div>
</div>""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Suggested questions
# ------------------------------------------------------------
st.markdown('<div class="sec">💡 Suggested · Soalan Cadangan</div>', unsafe_allow_html=True)

def process_question(q: str):
    st.session_state.messages.append(dict(role="user", kind="normal", content=q, ts=time.time()))
    with st.spinner("🛡️ Thinking… · Sedang berfikir…"):
        reply = route_question(q)
    reply["ts"] = time.time()
    st.session_state.messages.append(reply)
    st.rerun()

SUGGESTED = [
    ("🎣 What is phishing?", "What is phishing?"),
    ("🔐 Why use MFA?", "Why should I use multi-factor authentication (MFA)?"),
    ("🔑 Strong password?", "How do I create a strong password?"),
    ("🦠 Apa itu malware?", "Apa itu malware?"),
    ("📶 Is public Wi-Fi safe?", "Is public Wi-Fi safe?"),
    ("🚨 I clicked a scam link!", "I clicked a suspicious link. What should I do?"),
]
c1, c2 = st.columns(2)
for i, (label, q) in enumerate(SUGGESTED):
    with (c1 if i % 2 == 0 else c2):
        if st.button(label, key=f"sug_{i}", use_container_width=True):
            process_question(q)

# ------------------------------------------------------------
# Conversation header + Clear (resets UI AND backend memory)
# ------------------------------------------------------------
s1, s2 = st.columns([4, 1.3], vertical_alignment="center")
with s1:
    st.markdown('<div class="sec">💬 Conversation · Perbualan</div>', unsafe_allow_html=True)
with s2:
    if st.button("🗑️ Clear", key="clear_chat", use_container_width=True,
                 help="Reset the conversation / Kosongkan perbualan"):
        st.session_state.messages = []
        if RESET_FN is not None:
            try:
                RESET_FN()
            except Exception:
                pass
        if hasattr(st, "toast"):
            st.toast("Chat cleared · Sembang dikosongkan", icon="🗑️")
        st.rerun()

# ------------------------------------------------------------
# Rendering: day dividers + bubbles with weekday/date/time stamps
# ------------------------------------------------------------
def render_message(m: dict):
    stamp = fmt_stamp(m.get("ts", time.time()))
    if m["role"] == "user":
        body = html.escape(m["content"]).replace("\n", "<br>")
        st.markdown(f"""
        <div class="msg user"><div class="avatar">🧑‍💻</div>
          <div class="stack"><div class="meta">You · Anda</div>
          <div class="bubble">{body}</div>
          <div class="stamp"><span class="tick">✓✓</span>{stamp}</div></div></div>""",
                    unsafe_allow_html=True)
        return
    kind = m.get("kind", "normal")
    if kind == "normal":
        st.markdown(f"""
        <div class="msg bot"><div class="avatar">🛡️</div>
          <div class="stack"><div class="meta">CyberSafe Assistant</div>
          <div class="bubble">{md_to_html(m["content"])}</div>
          <div class="stamp">{stamp}</div></div></div>""", unsafe_allow_html=True)
        return
    if kind == "empathy":
        sev, icon, title, tag = "empathy", "💛", "I hear you · Saya faham", ""
        body, hint = html.escape(m["content"]), ""
    elif kind == "ood":
        sev, icon, title, tag = "scope", "🧭", "Outside my domain · Di luar skop saya", ""
        body, hint = html.escape(m["content"]), ""
    else:
        sev = m.get("severity", "danger"); icon = m.get("icon", "⚠️")
        title = m.get("title", "Error"); body = html.escape(m["content"])
        hint = html.escape(m.get("hint", ""))
        tag = '<span class="tag">RETRY AVAILABLE</span>' if m.get("retryable") else ""
    hint_html = f'<div class="hint">{hint}</div>' if hint else ""
    st.markdown(f"""
    <div class="msg bot"><div class="avatar">🛡️</div>
      <div class="stack" style="max-width:100%;flex:1">
        <div class="meta">CyberSafe Assistant</div>
        <div class="card {sev}">
          <div class="card-top"><span class="card-ico">{icon}</span>
            <span class="card-title">{html.escape(title)}</span>{tag}</div>
          <div class="card-body">{body}</div>{hint_html}
        </div>
        <div class="stamp">{stamp}</div></div></div>""", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="ghost"><span class="big">🛰️</span>
      Ask me anything about staying safe online — or tap a suggested question above.<br>
      <i>Tanya saya apa-apa tentang keselamatan dalam talian — atau tekan soalan cadangan di atas.</i>
    </div>""", unsafe_allow_html=True)
else:
    prev_day = None
    for m in st.session_state.messages:
        if "ts" not in m:
            m["ts"] = time.time()
        d = datetime.datetime.fromtimestamp(m["ts"]).date()
        if d != prev_day:
            st.markdown(f'<div class="day-divider"><span>{fmt_day(d)}</span></div>',
                        unsafe_allow_html=True)
            prev_day = d
        render_message(m)

last = st.session_state.messages[-1] if st.session_state.messages else None
if last and last["role"] == "assistant" and last.get("retryable"):
    q = last.get("q", "")
    short = q if len(q) <= 42 else q[:42] + "…"
    if st.button(f"🔄 Try again · Cuba lagi — “{short}”", key="retry_btn", type="primary"):
        st.session_state.messages.pop()
        with st.spinner("🛡️ Retrying… · Mencuba semula…"):
            reply = answer_question(q)
        reply["ts"] = time.time()
        st.session_state.messages.append(reply)
        if reply.get("kind") == "normal" and hasattr(st, "toast"):
            st.toast("Answer received · Jawapan diterima", icon="✅")
        st.rerun()

# ------------------------------------------------------------
# Input
# ------------------------------------------------------------
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Ask your cybersecurity question… · Tanya soalan keselamatan siber…",
        key="input", max_chars=600,
        placeholder="e.g., Is public Wi-Fi safe? · cth: Adakah Wi-Fi awam selamat?")
    submitted = st.form_submit_button("Ask · Hantar", type="primary", use_container_width=True)
    if submitted:
        if not user_input.strip():
            st.error("⚠️ Please enter a question first. · Sila masukkan soalan dahulu.")
        else:
            process_question(user_input.strip())

st.markdown("""
<div class="foot">🛡️ Educational awareness guidance only — not professional advice.<br>
CSC649 Group Project · Aina (Frontend) × Syasya (Backend) · Gemini API</div>""",
            unsafe_allow_html=True)