import streamlit as st
import requests
import random
import html

# Ambil soal quiz dari Open Trivia DB API
def get_questions(amount=5, category=None, difficulty="medium"):
    base_url = "https://opentdb.com/api.php"
    params = {
        "amount": amount,
        "type": "multiple",
        "difficulty": difficulty
    }
    if category:
        params["category"] = category

    response = requests.get(base_url, params=params)
    data = response.json()

    questions = []
    for item in data["results"]:
        q_text = html.unescape(item["question"])
        correct = html.unescape(item["correct_answer"])
        options = item["incorrect_answers"]
        options = [html.unescape(opt) for opt in options]
        options.append(correct)
        random.shuffle(options)
        questions.append({
            "question": q_text,
            "options": options,
            "answer": correct
        })
    return questions

# Inisialisasi game
if "questions" not in st.session_state:
    st.session_state.questions = get_questions(amount=5)
    st.session_state.index = 0
    st.session_state.score = 0

q = st.session_state.questions[st.session_state.index]

st.title("🎯 Quiz Time!")
st.subheader(f"Soal #{st.session_state.index + 1}")
st.write(q["question"])
selected = st.radio("Pilih jawaban:", q["options"])

# Check jawaban
if st.button("Submit Jawaban"):
    if selected == q["answer"]:
        st.success("✅ Benar!")
        st.session_state.score += 1
    else:
        st.error(f"❌ Salah! Jawaban yang benar: {q['answer']}")
    st.session_state.index += 1

    if st.session_state.index >= len(st.session_state.questions):
        st.balloons()
        st.success(f"🎉 Skor akhir: {st.session_state.score} dari {len(st.session_state.questions)}")
        if st.button("Main Lagi"):
            st.session_state.clear()
