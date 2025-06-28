import streamlit as st
from io import StringIO
from utilities import generate_summary, generate_logic_questions, evaluate_user_answer, ask_question

# --- File Parsers ---
def extract_text_from_pdf(uploaded_file):
    import fitz  # PyMuPDF
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

def extract_text_from_txt(uploaded_file):
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    return stringio.read()

# --- Page Config ---
st.set_page_config(page_title="📚 Smart Research Assistant", layout="wide")

# --- Session State ---
if "document_text" not in st.session_state: st.session_state.document_text = ""
if "summary" not in st.session_state: st.session_state.summary = ""
if "summary_generated" not in st.session_state: st.session_state.summary_generated = False
if "challenge_qs" not in st.session_state: st.session_state.challenge_qs = []
if "chat_history" not in st.session_state: st.session_state.chat_history = []

st.title("📚 Smart Assistant for Research Summarization")

# --- Upload Section ---
with st.sidebar:
    st.header("📤 Upload or Paste Document")
    upload_tab, paste_tab = st.tabs(["📄 Upload File", "✍️ Paste Text"])

    uploaded_file = None
    pasted_text = ""

    with upload_tab:
        uploaded_file = st.file_uploader("Choose a PDF or TXT file", type=["pdf", "txt"])
    
    with paste_tab:
        pasted_text = st.text_area("Or paste your text here:", height=300)

    # Document text extraction
    if uploaded_file or pasted_text.strip():
        if uploaded_file:
            if uploaded_file.name.endswith(".pdf"):
                text = extract_text_from_pdf(uploaded_file)
            else:
                text = extract_text_from_txt(uploaded_file)
        else:
            text = pasted_text

        if text != st.session_state.document_text:
            st.session_state.document_text = text
            st.session_state.summary_generated = False
            st.session_state.chat_history = []
            st.session_state.challenge_qs = []

    # Generate summary if not yet done
    if st.session_state.document_text and not st.session_state.summary_generated:
        with st.spinner("Generating summary..."):
            st.session_state.summary = generate_summary(st.session_state.document_text[:6000])
            st.session_state.summary_generated = True
        st.success("✅ Summary ready!")

# --- Summary Display ---
if st.session_state.summary:
    st.subheader("📝 Document Summary")
    st.markdown(
        f"""
        <div style='
            background-color: white;
            color: black;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            font-size: 1rem;
            line-height: 1.5;
        '>
            {st.session_state.summary}
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Mode Selection ---
mode = st.radio("Choose Mode:", ["💬 Ask Anything", "🎯 Challenge Me"], horizontal=True)

# --- Chat Input (must be outside to work properly) ---
user_input = None
if mode == "💬 Ask Anything":
    user_input = st.chat_input("Ask something based on the uploaded document...")

# --- Ask Anything Mode ---
if mode == "💬 Ask Anything":
    st.subheader("💬 Ask Questions Based on Document")

    if not st.session_state.document_text:
        st.warning("Please upload or paste a document first.")
    else:
        if user_input:
            with st.spinner("Thinking..."):
                assistant_reply = ask_question(user_input, st.session_state.document_text)
                st.session_state.chat_history.append((user_input, assistant_reply))

        # Show full chat history
        for user_msg, assistant_msg in st.session_state.chat_history:
            with st.chat_message("user"):
                st.markdown(user_msg)
            with st.chat_message("assistant"):
                st.markdown(assistant_msg)

        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []

# --- Challenge Me Mode ---
if mode == "🎯 Challenge Me":
    st.subheader("🎯 Test Your Comprehension")

    if not st.session_state.document_text:
        st.warning("Please upload or paste a document first.")
    else:
        if st.button("🔄 Generate Challenge Questions"):
            with st.spinner("🧠 Thinking..."):
                st.session_state.challenge_qs = generate_logic_questions(st.session_state.document_text)

        for idx, q in enumerate(st.session_state.challenge_qs):
            st.markdown(f"**Q{idx+1}:** {q}")
            user_ans = st.text_input("Your answer:", key=f"user_ans_{idx}")
            if st.button(f"✅ Evaluate Answer {idx+1}", key=f"eval_btn_{idx}"):
                with st.spinner("Evaluating..."):
                    result = evaluate_user_answer(q, user_ans, st.session_state.document_text)
                    st.markdown(result["justification"])
                    st.markdown(f"📌 **Supported by:**\n> {result['support']}")
