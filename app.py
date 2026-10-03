import streamlit as st
from google import genai
from fpdf import FPDF
from datetime import datetime
from urllib.parse import quote_plus

st.set_page_config(page_title="BCA Study Buddy", page_icon="📚", layout="centered")

MODEL = "gemma-4-26b-a4b-it"

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.stApp, .stMarkdown, p, h1, h2, h3, label, textarea, input, button { font-family: 'Inter', sans-serif; }
footer { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 760px; }
.hero { background: linear-gradient(135deg, #4F46E5, #7C3AED); padding: 28px 24px; border-radius: 20px; margin-bottom: 20px; }
.hero h1 { color: #FFFFFF !important; font-size: 2rem; font-weight: 800; margin: 0 0 6px 0; padding: 0; }
.hero p { color: #E0E7FF !important; margin: 0; font-size: 1rem; }
.badge { display: inline-block; background: rgba(255,255,255,0.18); color: #FFFFFF; padding: 4px 12px; border-radius: 999px; font-size: 0.75rem; font-weight: 600; margin-bottom: 12px; }
.note { font-size: 0.8rem; color: #64748B; text-align: center; margin-top: 18px; }
</style>
<div class="hero">
<div class="badge">Free • Open-weight Gemma</div>
<h1>📚 BCA Study Buddy</h1>
<p>Stuck in Coding, Digital Logic or Maths? Ask here. You get simple steps and easy examples, in English or Hindi.</p>
</div>
""",
    unsafe_allow_html=True,
)

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

BASE = (
    "You are BCA Study Buddy, a patient and kind teacher for a BCA student "
    "who finds this subject hard. Use very simple English and short sentences. "
    "If the student writes Hindi, reply in Hindi. Never make the student feel bad. Keep answers under 150 words unless asked for more. "
    "Do not use LaTeX or special math commands. Write arrows as -> and write maths in plain text like x^2 or a/b. "
)

SUBJECTS = {
    "💻 Coding": "Subject: programming (C, Python, Java). Give small code examples and explain each line. ",
    "🔌 Digital Logic": "Subject: digital logic (gates, truth tables, K-map, flip-flops). Use truth tables and simple examples. ",
    "➗ Maths": "Subject: BCA maths. Solve step by step and explain why each step is done. ",
}

EXAMPLES = {
    "💻 Coding": ["What is a pointer in C?", "Explain recursion simply", "while vs do-while loop"],
    "🔌 Digital Logic": ["What is a K-map?", "Why is NAND a universal gate?", "Latch vs flip-flop"],
    "➗ Maths": ["What is a matrix inverse?", "Permutation vs combination", "What is a subset?"],
}

MODES = {
    "📖 Explain": "Explain the topic step by step with one real-life example. ",
    "📝 Quiz me": "Ask ONE easy question about the topic. Wait for the answer. Then check it kindly and explain any mistake. ",
}


def clean_for_pdf(text):
    text = text.replace("**", "").replace("`", "")
    swaps = {"•": "-", "→": "->", "–": "-", "—": "-", "“": '"', "”": '"', "‘": "'", "’": "'"}
    for a, b in swaps.items():
        text = text.replace(a, b)
    return text.encode("latin-1", "replace").decode("latin-1")


def make_pdf(msgs):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "BCA Study Buddy - My Notes", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 6, "Saved on " + datetime.now().strftime("%d %b %Y"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    for m in msgs:
        who = "You" if m["role"] == "user" else "Study Buddy"
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 7, who + ":", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, clean_for_pdf(m["content"]), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)
    return bytes(pdf.output())


# ---------- chat history (kept while the page is open) ----------
if "chats" not in st.session_state:
    st.session_state["chats"] = [{"title": "New chat", "messages": []}]
    st.session_state["current"] = 0

with st.sidebar:
    st.header("🕘 My chats")
    if st.button("➕ New chat", use_container_width=True):
        st.session_state["chats"].append({"title": "New chat", "messages": []})
        st.session_state["current"] = len(st.session_state["chats"]) - 1
        st.rerun()
    for i, c in enumerate(st.session_state["chats"]):
        label = ("▶ " if i == st.session_state["current"] else "") + c["title"]
        if st.button(label, key="chat" + str(i), use_container_width=True):
            st.session_state["current"] = i
            st.rerun()
    st.caption("History stays while this page is open. Use Save as PDF to keep notes.")

chat = st.session_state["chats"][st.session_state["current"]]
messages = chat["messages"]

# ---------- choices ----------
subject = st.radio("Choose subject", list(SUBJECTS), horizontal=True)
mode = st.radio("What do you want?", list(MODES), horizontal=True)

st.caption("Tap a question to try it:")
cols = st.columns(3)
for i, ex in enumerate(EXAMPLES[subject]):
    if cols[i].button(ex, key=subject + str(i), use_container_width=True):
        st.session_state["pending"] = ex

for m in messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

typed = st.chat_input("Type your question here...")
question = typed or st.session_state.pop("pending", None)

if question:
    with st.chat_message("user"):
        st.markdown(question)

    history_text = ""
    for m in messages[-6:]:
        history_text += m["role"] + ": " + m["content"] + "\n"

    prompt = (
        BASE + SUBJECTS[subject] + MODES[mode]
        + "\n\nChat so far:\n" + history_text
        + "\nStudent: " + question
    )

    with st.chat_message("assistant"):
        try:
            def stream():
                for chunk in client.models.generate_content_stream(model=MODEL, contents=prompt):
                    if chunk.text:
                        yield chunk.text
            answer = st.write_stream(stream())
        except Exception as e:
            answer = "Sorry, something went wrong. Please try again. (" + str(e)[:100] + ")"
            st.markdown(answer)

    if chat["title"] == "New chat":
        chat["title"] = question[:26]
    messages.append({"role": "user", "content": question})
    messages.append({"role": "assistant", "content": answer})

# ---------- save and clear ----------
if messages:
    last_q = [m["content"] for m in messages if m["role"] == "user"][-1]
    v1, v2 = st.columns(2)
    v1.link_button(
        "▶️ Watch video (English)",
        "https://www.youtube.com/results?search_query=" + quote_plus(last_q + " explained"),
        use_container_width=True,
    )
    v2.link_button(
        "▶️ Watch video (Hindi)",
        "https://www.youtube.com/results?search_query=" + quote_plus(last_q + " in Hindi"),
        use_container_width=True,
    )
    c1, c2 = st.columns(2)
    try:
        c1.download_button(
            "📄 Save as PDF", make_pdf(messages), "study-buddy-notes.pdf",
            "application/pdf", use_container_width=True,
        )
    except Exception:
        c1.caption("PDF not possible for this chat. Use Save as text.")
    txt = "\n\n".join(
        ("You: " if m["role"] == "user" else "Study Buddy: ") + m["content"] for m in messages
    )
    c2.download_button(
        "📝 Save as text", txt.encode("utf-8"), "study-buddy-notes.txt",
        "text/plain", use_container_width=True,
    )
    if st.button("🗑️ Clear this chat", use_container_width=True):
        chat["messages"] = []
        chat["title"] = "New chat"
        st.rerun()

st.markdown(
    '<div class="note">AI can make mistakes. Check important answers with your book or teacher.<br>Built by Sunil for his friends • Hacktoberfest 2026</div>',
    unsafe_allow_html=True,
    )
