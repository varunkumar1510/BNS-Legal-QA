import os
import re
import faiss
import numpy as np
import streamlit as st
import pyttsx3
import ollama
from gtts import gTTS  # ✅ NEW

# Constants
TEXT_FILE = "Updated1.0.txt"
INDEX_FILE = "faiss_index.bin"
EMBEDDINGS_FILE = "embeddings.npy"

# Session state init
if "index" not in st.session_state:
    st.session_state.index = None
if "sections" not in st.session_state:
    st.session_state.sections = None
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "last_docs" not in st.session_state:
    st.session_state.last_docs = []
if "history" not in st.session_state:
    st.session_state.history = []
if "auto_submit" not in st.session_state:
    st.session_state.auto_submit = False

# Section extractor
def extract_numbered_sections_from_text(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    sections = []
    pattern = re.compile(r'(?<=\n)(\d+\.)')
    matches = list(pattern.finditer(text))
    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i+1].start() if i + 1 < len(matches) else len(text)
        sections.append(text[start:end].strip())
    return sections

# Embedding function
def text_to_embedding_ollama(text):
    model_name = "mxbai-embed-large"
    response = ollama.embed(model=model_name, input=text)
    return response['embeddings'][0]

# FAISS + section loader
def get_faiss_index_and_sections():
    if os.path.exists(INDEX_FILE) and os.path.exists(EMBEDDINGS_FILE):
        index = faiss.read_index(INDEX_FILE)
        embeddings_array = np.load(EMBEDDINGS_FILE)
        sections_array = extract_numbered_sections_from_text(TEXT_FILE)[1:len(embeddings_array)+1]
    else:
        sections_array = extract_numbered_sections_from_text(TEXT_FILE)[1:]
        embeddings = [text_to_embedding_ollama(text) for text in sections_array]
        embeddings_array = np.array(embeddings, dtype=np.float32)
        np.save(EMBEDDINGS_FILE, embeddings_array)
        index = faiss.IndexFlatL2(embeddings_array.shape[1])
        index.add(embeddings_array)
        faiss.write_index(index, INDEX_FILE)
    return index, sections_array

# LLM prompt
def generate_answer(question, section_texts):
    section_str = "\n".join([f"{i+1}. {section}" for i, section in enumerate(section_texts)])
    prompt = f"""
You are an expert legal assistant trained on the Bharatiya Nyaya Sanhita (BNS). A user has asked a legal question based on their real-life experience.

Your job is to:
1. Understand the context and details of the user's question.
2. Review the following sections from the BNS and identify the ones that relate directly to the situation.
3. Provide a clear and concise legal explanation, written in a way a common person can understand.
4. Cite relevant sections using this format: "According to BNS Section XX".
5. Do not mention irrelevant sections. Focus only on what applies to the user’s situation.

---
User's Question:
"{question}"

---
Relevant Sections from the BNS:
{section_str}

---
Now, based on the above, provide a single-paragraph answer that directly addresses the user's concern.
"""
    output = ollama.generate(model="deepseek-r1:1.5b", prompt=prompt)
    return output['response'].split("</think>")[-1].strip()

# gTTS function ✅ NEW
def save_answer_as_mp3(answer_text, filename):
    tts = gTTS(text=answer_text, lang='en')
    tts.save(filename)
    return filename

# UI
st.set_page_config(page_title="Legal QA - BNS Assistant", layout="centered")
st.title("🇮🇳 Indian Law Assistant – Real-time Legal QA")

# Load embeddings/index
if st.session_state.index is None or st.session_state.sections is None:
    with st.spinner("Initializing FAISS & embeddings..."):
        st.session_state.index, st.session_state.sections = get_faiss_index_and_sections()

# Browser speech-to-text on load
st.markdown("""
<script>
window.addEventListener("load", () => {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-IN";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        const inputBox = window.parent.document.querySelector('input[type="text"]');
        inputBox.value = transcript;
        const inputEvent = new Event("input", { bubbles: true });
        inputBox.dispatchEvent(inputEvent);
        window.parent.postMessage({ type: "streamlit:setComponentValue", value: transcript }, "*");
    };

    recognition.onerror = function(event) {
        console.error("Speech recognition error:", event.error);
    };

    recognition.start();
});
</script>
""", unsafe_allow_html=True)

st.caption("Speak or type your legal question and get an answer based on Bharatiya Nyaya Sanhita (BNS)")
query_input = st.text_input("🎤 Speak or type your legal query:")

# Submit & regenerate buttons
col1, col2 = st.columns([1, 1])
with col1:
    submit = st.button("🔎 Submit")
with col2:
    regenerate = st.button("🔁 Regenerate Answer")

# Auto-submit if spoken query just arrived
if query_input and query_input != st.session_state.last_query and not submit:
    st.session_state.auto_submit = True

# Generate answer logic
if (submit or st.session_state.auto_submit) and query_input:
    with st.spinner("Generating your legal response..."):
        query_vec = np.array([text_to_embedding_ollama(query_input)], dtype=np.float32)
        D, I = st.session_state.index.search(query_vec, 3)
        docs = [st.session_state.sections[i] for i in I[0]]
        response = generate_answer(query_input, docs)
        st.session_state.last_query = query_input
        st.session_state.last_docs = docs
        st.session_state.history.append((query_input, response))
        st.session_state.auto_submit = False

    st.markdown("### 📜 Answer")
    st.write(response)

    # ✅ Save and play MP3
    mp3_filename = f"answer_{len(st.session_state.history)}.mp3"
    save_answer_as_mp3(response, mp3_filename)
    st.markdown("### 🔊 Listen to the Answer")
    st.audio(mp3_filename, format="audio/mp3")

# Regenerate logic
elif regenerate and st.session_state.last_query:
    query_input = st.session_state.last_query
    docs = st.session_state.last_docs
    response = generate_answer(query_input, docs)
    st.session_state.history.append((query_input, response))

    st.markdown("### 🔁 Regenerated Answer")
    st.write(response)

    mp3_filename = f"answer_{len(st.session_state.history)}_regen.mp3"
    save_answer_as_mp3(response, mp3_filename)
    st.markdown("### 🔊 Listen to Regenerated Answer")
    st.audio(mp3_filename, format="audio/mp3")

# Q&A History
if st.session_state.history:
    with st.expander("📚 Q&A History"):
        for i, (q, a) in enumerate(reversed(st.session_state.history), 1):
            st.markdown(f"*{i}. Question:* {q}")
            st.markdown(f"*Answer:* {a}")
            st.markdown("---")
