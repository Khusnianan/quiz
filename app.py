import streamlit as st
import requests
import random
import html
import time

# Fungsi untuk mengambil soal berdasarkan pengaturan
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

# Pengaturan permainan
st.sidebar.title("Pengaturan Permainan")
categories = {
    "General Knowledge": 9,
    "Science": 17,
    "Mathematics": 19,
    "History": 23,
    "Geography": 22
}

# Pengaturan Pengguna
category = st.sidebar.selectbox("Pilih Kategori Soal", list(categories.keys()))
difficulty = st.sidebar.radio("Pilih Kesulitan", ("easy", "medium", "hard"))
num_questions = st.sidebar.slider("Pilih Jumlah Soal", 5, 20, 5)
timer_duration = st.sidebar.slider("Timer (detik)", 10, 60, 30)

# Inisialisasi Game
if "questions" not in st.session_state:
    st.session_state.questions = get_questions(
        amount=num_questions,
        category=categories[category],
        difficulty=difficulty
    )
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.start_time = time.time()  # Time when game starts

q = st.session_state.questions[st.session_state.index]

# Timer dan Update Timer Mundur
elapsed_time = time.time() - st.session_state.start_time
time_left = timer_duration - elapsed_time

# Memperbarui Timer di UI
timer_placeholder = st.empty()
timer_placeholder.markdown(f"⏰ **Waktu tersisa**: {int(time_left)} detik")

if time_left <= 0:
    st.session_state.index += 1
    st.session_state.start_time = time.time()  # Restart timer for the next question
    time_left = timer_duration  # Reset the time left

# Styling custom CSS
st.markdown("""
    <style>
        .main {
            background-color: #f0f4f8;
            padding: 50px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .title {
            color: #2C3E50;
            font-family: 'Arial', sans-serif;
            font-size: 40px;
            font-weight: bold;
        }
        .question {
            font-size: 22px;
            color: #34495E;
            font-family: 'Arial', sans-serif;
        }
        .submit-btn {
            background-color: #1ABC9C;
            color: white;
            font-size: 18px;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            transition: 0.3s;
        }
        .submit-btn:hover {
            background-color: #16A085;
        }
        .score {
            font-size: 30px;
            color: #27AE60;
            font-family: 'Arial', sans-serif;
            font-weight: bold;
        }
        .reset-btn {
            background-color: #E74C3C;
            color: white;
            font-size: 18px;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            transition: 0.3s;
        }
        .reset-btn:hover {
            background-color: #C0392B;
        }
    </style>
""", unsafe_allow_html=True)

# Tampilan Quiz Time
st.markdown('<div class="main">', unsafe_allow_html=True)
st.title("🎯 Quiz Time!", anchor="quiz-time")
st.markdown('<p class="title">Waktu untuk menjawab!</p>', unsafe_allow_html=True)

# Soal & Pilihan
st.markdown('<p class="question">{}</p>'.format(q["question"]), unsafe_allow_html=True)
selected = st.radio("Pilih jawaban:", q["options"], key="answer")

# Cek jawaban
if st.button("Submit Jawaban", key="submit"):
    if selected == q["answer"]:
        st.success("✅ Benar!")
        st.session_state.score += 1
    else:
        st.error(f"❌ Salah! Jawaban yang benar: {q['answer']}")
    st.session_state.index += 1

    if st.session_state.index >= len(st.session_state.questions):
        st.balloons()
        st.markdown(f'<p class="score">🎉 Skor akhir: {st.session_state.score} dari {len(st.session_state.questions)}</p>', unsafe_allow_html=True)

        # Tombol untuk main lagi
        if st.button("Main Lagi", key="reset", on_click=lambda: st.session_state.clear()):
            st.experimental_rerun()  # Reload halaman

st.markdown('</div>', unsafe_allow_html=True)
