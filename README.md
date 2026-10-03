# 📚 BCA Study Buddy

A free AI study helper for BCA students who find **Coding, Digital Logic and Maths** hard. It explains topics in simple English or Hindi, quizzes you to practice, and points you to videos when you want to *see* the idea.

Built for a real group of friends for the **Hacktoberfest 2026 "Build for a Friend"** challenge, and improved after a friend tested it.

**🔗 Live demo:** https://bca-study-buddy.streamlit.app/

> The first open can take up to a minute. The app sleeps when nobody uses it (free hosting).

## ✨ Features

- **3 subjects:** Coding, Digital Logic, Maths
- **2 modes:** *Explain* (step by step, with a real-life example) and *Quiz me* (one question at a time, with kind feedback)
- **English or Hindi:** ask in either language
- **Fast answers:** the reply appears word by word while it is being written
- **Video help:** one tap opens YouTube with videos on your exact question, in English or Hindi
- **Tap-to-ask examples** for each subject
- **My chats:** a sidebar with new chat and past chats
- **Save notes:** download any chat as **PDF** or **text**
- **Clean, mobile-friendly design**

## 🗣️ Built with my friends' feedback

I made this for friends who struggle with Coding, Digital Logic and Maths. I gave them the link and listened.

- A friend told me the answers were great, but he wanted **videos or visuals** too. So I added the **Watch video** buttons.
- A friend hit a **page loading error**. A refresh fixed it, and now I know to tell people.
- Some answers showed raw math code (like `\rightarrow`). I changed the prompt so the AI writes plain text.
- Google changed the Gemma model name, and the app stopped working. Because the model is one line in `app.py`, the fix took one minute.

## 🧠 Why open-weight Gemma?

I used **Gemma**, Google's open-weight model, instead of a closed model:

- **Free to start:** a student can build and share this with no payment.
- **Swappable:** changing the model is one line in `app.py` (`MODEL = ...`). I had to do this once, and it was easy.
- **Open approach:** the model weights are open, so the same idea can later run on a local machine or another provider, and I can change how it teaches.

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
| `app.py` | The whole app: design, chat, history, video links, PDF export |
| `requirements.txt` | Python packages |
| `.streamlit/config.toml` | Theme and colors |

## ⚠️ Limits

- AI can make mistakes, especially in maths. Check important answers with your book or teacher.
- Chat history stays only while the page is open. Use **Save as PDF** to keep notes.
- The PDF shows English well. Hindi letters do not show in the PDF, so use **Save as text** for Hindi.
- The video buttons open YouTube search results. They do not play videos inside the app.
- The free API key has daily limits, so the app may say "try again later" when many people use it.

## 🗺️ Ideas for later

- Saved history with login
- Hindi support in PDF
- Videos and pictures inside the app
- More subjects (DBMS, Networks, OS)
- Run the model fully on the device

## 📄 License

MIT. See [LICENSE](LICENSE).

## 👤 Author

**Sunil Kumawat**, BCA student from Rajasthan, India.
