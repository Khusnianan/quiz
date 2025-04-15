import streamlit as st
import random

# Ukuran grid
GRID_SIZE = 10

# Inisialisasi game
if "snake" not in st.session_state:
    st.session_state.snake = [(5, 5)]
    st.session_state.direction = "RIGHT"
    st.session_state.food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    st.session_state.score = 0
    st.session_state.game_over = False

def move_snake():
    head_x, head_y = st.session_state.snake[-1]

    if st.session_state.direction == "UP":
        head_y -= 1
    elif st.session_state.direction == "DOWN":
        head_y += 1
    elif st.session_state.direction == "LEFT":
        head_x -= 1
    elif st.session_state.direction == "RIGHT":
        head_x += 1

    new_head = (head_x, head_y)

    # Cek tabrakan
    if (
        new_head in st.session_state.snake
        or head_x < 0 or head_x >= GRID_SIZE
        or head_y < 0 or head_y >= GRID_SIZE
    ):
        st.session_state.game_over = True
        return

    st.session_state.snake.append(new_head)

    if new_head == st.session_state.food:
        st.session_state.score += 1
        while True:
            new_food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if new_food not in st.session_state.snake:
                st.session_state.food = new_food
                break
    else:
        st.session_state.snake.pop(0)

# Tombol arah
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("⬆️"):
        if st.session_state.direction != "DOWN":
            st.session_state.direction = "UP"

with col1:
    if st.button("⬅️"):
        if st.session_state.direction != "RIGHT":
            st.session_state.direction = "LEFT"

with col3:
    if st.button("➡️"):
        if st.session_state.direction != "LEFT":
            st.session_state.direction = "RIGHT"

with col2:
    if st.button("⬇️"):
        if st.session_state.direction != "UP":
            st.session_state.direction = "DOWN"

# Gerak ular setiap tombol diklik
move_snake()

# Render grid
for y in range(GRID_SIZE):
    row = ""
    for x in range(GRID_SIZE):
        if (x, y) == st.session_state.food:
            row += "🍎"
        elif (x, y) in st.session_state.snake:
            row += "🟩"
        else:
            row += "⬛"
    st.write(row)

# Status
st.write(f"Skor: {st.session_state.score}")
if st.session_state.game_over:
    st.error("💀 Game Over!")
    if st.button("Main Lagi"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()
