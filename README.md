# 📚 Smart Research Assistant

A document-aware AI assistant that can **summarize**, **answer free-form questions**, and **generate + evaluate logical comprehension questions** from user-uploaded documents (PDF or TXT). Built with Gemini Pro API and Streamlit.

---

##  Features

- ✅ **PDF/TXT Upload or Text Paste**
- ✅ **Auto Summary** under 150 words
- ✅ **💬 Ask Anything Mode**: Chat interface for open-ended questions
- ✅ **🎯 Challenge Me Mode**: Generates 3 logic-based questions and evaluates user responses
- ✅ **Contextual Justifications** for each answer
- ✅ Built with **Gemini Pro API**
- ✅ Intuitive **ChatGPT-like UI using Streamlit**

---

##  Use Case

Helps users quickly understand and interact with long research papers, legal documents, manuals, or reports by enabling:

- Comprehension-based Q&A
- Reasoning-based testing
- Summary extraction
- Educational interaction for self-testing

---

## 🛠️ Tech Stack

| Layer        | Tech                         |
|--------------|------------------------------|
| Frontend     | [Streamlit](https://streamlit.io) |
| LLM Backend  | [Gemini 2.0 Flash](https://ai.google.dev) |
| File Parsing | PyMuPDF (PDF), TextIO (TXT) |
| Deployment   | Localhost / Streamlit Cloud ready |

---

## 🚀 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/smart-research-assistant.git
cd smart-research-assistant
```
### 2. Create a Virtual Environment

```bash
python -m venv myvenv
source venv\Scripts\activate #on windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Your Gemini API Key

Create a .env file

```bash
GEMINI_API_KEY = "your_gemini_api_key_here"
```

### Run The App
```bash
streamlit run app.py
```

## How It Works
### 1. Ask Anything Mode
i.You ask a question related to the uploaded document.

ii.The assistant answers using Gemini with grounded context from the text.

### 2.Challenge Me Mode
i. The assistant generates 3 logical/inference-based questions.

ii. You type your answers.

iii. It evaluates your responses with verdict and justification.


## 📸 Screenshots

### 🔼 Upload and Summary
![Upload UI](AppImages/homeUI.png)

### 💬 Ask Anything Mode
![Ask Anything](AppImages/ask_anything_working.png)

### 🎯 Challenge Me Mode
![Challenge Mode](AppImages/challenge_mode_working.png)
