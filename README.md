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
