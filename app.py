import streamlit as st
from google import genai

st.set_page_config(page_title="BCA Study Buddy", page_icon="📚", layout="centered")

# If the model name stops working later, change it here
MODEL = "gemma-3-27b-it"

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
    "If the student writes Hindi, reply in Hindi. Never make the student feel bad. "
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

subject = st.radio("Choose subject", list(SUBJECTS), horizontal=True)
mode = st.radio("What do you want?", list(MODES), horizontal=True)

st.caption("Tap a question to try it:")
cols = st.columns(3)
for i, ex in enumerate(EXAMPLES[subject]):
    if cols[i].button(ex, key=subject + str(i), use_container_width=True):
        st.session_state["pending"] = ex

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for m in st.session_state["messages"]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

typed = st.chat_input("Type your question here...")
question = typed or st.session_state.pop("pending", None)

if question:
    with st.chat_message("user"):
        st.markdown(question)

    chat = ""
    for m in st.session_state["messages"][-6:]:
        chat += m["role"] + ": " + m["content"] + "\n"

    prompt = (
        BASE + SUBJECTS[subject] + MODES[mode]
        + "\n\nChat so far:\n" + chat
        + "\nStudent: " + question
    )

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                out = client.models.generate_content(model=MODEL, contents=prompt)
                answer = out.text
            except Exception as e:
                answer = "Sorry, something went wrong. Please try again. (" + str(e)[:100] + ")"
        st.markdown(answer)

    st.session_state["messages"].append({"role": "user", "content": question})
    st.session_state["messages"].append({"role": "assistant", "content": answer})

if st.session_state["messages"]:
    if st.button("🗑️ Clear chat"):
        st.session_state["messages"] = []
        st.rerun()

st.markdown(
    '<div class="note">AI can make mistakes. Check important answers with your book or teacher.<br>Built by Sunil for his friends • Hacktoberfest 2026</div>',
    unsafe_allow_html=True,
)
