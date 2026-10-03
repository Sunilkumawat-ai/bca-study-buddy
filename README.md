# 📚 BCA Study Buddy

A free AI study helper for BCA students who find **Coding, Digital Logic and Maths** hard. It explains topics in simple English or Hindi, and it can quiz you to practice.

Built for a real group of friends, for the **Hacktoberfest 2026 "Build for a Friend"** challenge.

**🔗 Live demo:** https://bca-study-buddy.streamlit.app/

## ✨ Features

- **3 subjects:** Coding, Digital Logic, Maths
- **2 modes:** *Explain* (step by step, with a real-life example) and *Quiz me* (one question at a time, with kind feedback)
- **English or Hindi:** ask in either language
- **Tap-to-ask examples** for each subject
- **My chats:** a sidebar with new chat and past chats
- **Save notes:** download any chat as **PDF** or **text**
- **Clean, mobile-friendly design**

## 🧠 Why open-weight Gemma?

I used **Gemma**, Google's open-weight model, instead of a closed model:

- **Free to start:** no payment is needed to build and share a student project.
- **Swappable:** changing the model is one line in `app.py` (`MODEL = ...`). I already had to do this once when the model name changed.
- **Open approach:** the model weights are open, so the same project can later run on a local machine or another provider.

## 🛠️ Tech stack

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/) for the app and hosting (Streamlit Community Cloud)
- [Gemma](https://ai.google.dev/gemma) through the Gemini API (Google AI Studio free key)
- [fpdf2](https://py-pdf.github.io/fpdf2/) for PDF export

## 🚀 Run it yourself

```bash
git clone https://github.com/Sunilkumawat-ai/bca-study-buddy.git
cd bca-study-buddy
pip install -r requirements.txt
```

Get a free key from [Google AI Studio](https://aistudio.google.com), then create a file `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your-key-here"
```

Start the app:

```bash
streamlit run app.py
```

Never upload your key to GitHub. This repo ignores `secrets.toml`.

## 📁 Project files

| File | What it does |
|------|--------------|
| `app.py` | The whole app: design, chat, history, PDF export |
| `requirements.txt` | Python packages |
| `.streamlit/config.toml` | Theme and colors |

## ⚠️ Limits

- AI can make mistakes, especially in maths. Check important answers with your book or teacher.
- Chat history stays only while the page is open. Use **Save as PDF** to keep notes.
- The PDF shows English well. Hindi letters do not show in the PDF, so use **Save as text** for Hindi.
- The free API key has daily limits.

## 🗺️ Ideas for later

- Saved history with login
- Hindi support in PDF
- More subjects (DBMS, Networks, OS)
- Run the model fully on the device

## 📄 License

MIT. See [LICENSE](LICENSE).

## 👤 Author

**Sunil Kumawat**, BCA student from Rajasthan, India.
