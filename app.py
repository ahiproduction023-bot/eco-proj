import streamlit as st
import pandas as pd
import os

# Настройка страницы
st.set_page_config(page_title="EcoJourney Challenge", layout="centered")

# --- ИНИЦИАЛИЗАЦИЯ (SESSION STATE) ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'tasks_done' not in st.session_state:
    st.session_state.tasks_done = 0

# Это КЛЮЧЕВАЯ переменная для перехода
if 'choice' not in st.session_state:
    st.session_state.choice = "Логин"

# Список страниц
menu = ["Логин", "Карта проблем", "Задания", "Рейтинг", "Диагностика", "Соцсети"]

# --- БОКОВОЕ МЕНЮ ---
# Мы используем индекс, который привязан к st.session_state.choice
current_index = menu.index(st.session_state.choice)

choice = st.sidebar.selectbox(
    "Меню навигации", 
    menu, 
    index=current_index,
    key="navigation_box"
)

# Если пользователь вручную кликнул в боковом меню, обновляем состояние
if choice != st.session_state.choice:
    st.session_state.choice = choice
    st.rerun()

# --- 1. СТАРТОВЫЙ ЭКРАН (ЛОГИН) ---
if st.session_state.choice == "Логин":
    st.title("🌱 EcoJourney Challenge")
    auth_mode = st.radio("Выберите действие", ["Войти", "Создать аккаунт"])
    
    if auth_mode == "Создать аккаунт":
        st.subheader("Регистрация нового эко-героя")
        name = st.text_input("Ваше имя")
        nickname = st.text_input("Придумайте никнейм")
        region = st.selectbox("Ваш город", ["Актобе", "Алматы", "Астана", "Шымкент", "Другой"])
        
        if st.button("Зарегистрироваться", key="reg_btn"):
            if nickname:
                st.success(f"Регистрация прошла успешно, {nickname}!")
                # ПРИНУДИТЕЛЬНЫЙ ПЕРЕХОД
                st.session_state.choice = "Карта проблем"
                st.rerun()
            else:
                st.error("Введите никнейм!")

    else:
        st.subheader("Вход в личный кабинет")
        login_nick = st.text_input("Никнейм")
        st.text_input("Пароль", type="password")
        
        if st.button("Войти", key="login_btn"):
            if login_nick:
                st.success("Вход выполнен!")
                # ПРИНУДИТЕЛЬНЫЙ ПЕРЕХОД
                st.session_state.choice = "Карта проблем"
                st.rerun()
            else:
                st.error("Введите никнейм!")

# --- 2. КАРТА / СПИСОК ПРОБЛЕМ ---
elif st.session_state.choice == "Карта проблем":
    st.header("📍 Эко-точки города")
    problem = st.selectbox("Объекты", ["Центральный парк", "Река Илек"])
    
    if problem == "Центральный парк":
        st.subheader("Свалка мусора у входа")
        if os.path.exists("park.jpg"):
            st.image("park.jpg")
        else:
            st.info("Здесь будет фото парка (загрузи park.jpg на GitHub)")
    
    elif problem == "Река Илек":
        st.subheader("Загрязнение берега")
        if os.path.exists("river.jpg"):
            st.image("river.jpg")
        else:
            st.info("Здесь будет фото реки (загрузи river.jpg на GitHub)")

# --- 3. ЗАДАНИЯ ---
elif st.session_state.choice == "Задания":
    st.header("🏆 Твои Эко-задания")
    st.write(f"Баллы: {st.session_state.score}")
    
    task = st.selectbox("Выбери задание", ["Сфоткай мусор", "Найди пункт переработки"])
    if st.button("Отправить"):
        st.session_state.score += 20
        st.session_state.tasks_done += 1
        st.balloons()
        st.rerun()

# --- 4. РЕЙТИНГ ---
elif st.session_state.choice == "Рейтинг":
    st.header("📊 Рейтинг")
    data = {"Никнейм": ["User1", "User2", "You"], "Баллы": [100, 80, st.session_state.score]}
    st.table(pd.DataFrame(data))

# --- 5. ДИАГНОСТИКА ---
elif st.session_state.choice == "Диагностика":
    st.header("🧠 Тест")
    if st.button("Я профи"):
        st.success("Отлично!")

# --- 6. СОЦСЕТИ ---
elif st.session_state.choice == "Соцсети":
    st.header("📢 Соцсети")
    st.write("Хэштег: #EcoJourneyChallenge")
