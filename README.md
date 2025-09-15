# BNS-Legal-QA
🇮🇳 AI-powered legal assistant for Bharatiya Nyaya Sanhita (BNS). Supports speech-to-text queries, semantic search with FAISS, LLM-based legal answers, and text-to-speech output for user-friendly legal guidance.


# 🇮🇳 Indian Law Assistant – BNS Legal QA

A **real-time legal question-answering system** based on the **Bharatiya Nyaya Sanhita (BNS)**.  
Users can **speak or type legal queries**, and the system retrieves relevant sections of BNS and provides **plain-language legal answers**. Answers are also available as **audio (MP3)**.

---

## Features

- **Speech-to-text input** (via browser microphone)
- **Semantic search** using FAISS
- **Embedding generation** via `mxbai-embed-large` (Ollama)
- **Answer generation** using `deepseek-r1:1.5b` LLM
- **Audio answers** using gTTS
- **Q&A History** tracking

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/BNS-Legal-QA.git
cd BNS-Legal-QA






**Create a virtual environment
**
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows

**
Install dependencies**

pip install -r requirements.txt

**Usage**
streamlit run app.py


Speak or type your legal query in the input box.

Click Submit to generate a legal answer.

Listen to the answer via the generated MP3 audio.

Click Regenerate Answer if you want an alternative response.

Expand Q&A History to see past questions and answers.

**Requirements**

Python 3.10+

Streamlit

FAISS

Numpy

pyttsx3

gTTS

ollama

Install all dependencies using pip install -r requirements.txt.

Notes

The first run may take time to generate embeddings and build the FAISS index.

Ensure you have an Ollama account and API configured for embedding and LLM generation.

Text data is in Updated1.0.txt.




streamlit
faiss-cpu
numpy
pyttsx3
gTTS
ollama


---

**✅ **Additional Notes for GitHub:****

1. **Do not commit large FAISS index and embeddings** unless necessary; they can be regenerated. You can add them to `.gitignore`.
2. Include `.gitignore`:



pycache/
*.pyc
faiss_index.bin
embeddings.npy
*.mp3
.venv/
