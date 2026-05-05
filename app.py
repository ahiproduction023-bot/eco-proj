import streamlit as st
import pandas as pd
import os

# Настройка страницы
st.set_page_config(page_title="EcoJourney Challenge", layout="centered")

# --- ИНИЦИАЛИЗАЦИЯ СОСТОЯНИЯ (SESSION STATE) ---
# Это нужно, чтобы баллы и переходы между страницами работали корректно
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'tasks_done' not in st.session_state:
    st.session_state.tasks_done = 0
if 'menu_choice' not in st.session_state:
    st.session_state.menu_choice = "Логин"

# Список всех страниц
menu = ["Логин", "Карта проблем", "Задания", "Рейтинг", "Диагностика", "Соцсети"]

# --- БОКОВОЕ МЕНЮ ---
# Мы привязываем выбор в меню к переменной в session_state
choice = st.sidebar.selectbox(
    "Меню", 
    menu, 
    index=menu.index(st.session_state.menu_choice), 
    key="main_menu_select"
)

# Функция для ручного переключения страницы
def go_to_page(page_name):
    st.session_state.menu_choice = page_name
    st.rerun()

# --- 1. СТАРТОВЫЙ ЭКРАН (ЛОГИН) ---
if choice == "Логин":
    st.title("🌱 EcoJourney Challenge")
    auth_mode = st.radio("Выберите действие", ["Войти", "Создать аккаунт"])
    
    if auth_mode == "Создать аккаунт":
        st.subheader("Регистрация нового эко-героя")
        name = st.text_input("Ваше имя")
        nickname = st.text_input("Придумайте никнейм")
        region = st.selectbox("Ваш город / область", ["Актобе", "Алматы", "Астана", "Шымкент", "Другой"])
        
        if st.button("Зарегистрироваться"):
            if nickname:
                st.success(f"Регистрация прошла успешно! Добро пожаловать, {nickname}!")
                # Автоматический переход на карту проблем
                st.session_state.menu_choice = "Карта проблем"
                st.rerun()
            else:
                st.error("Пожалуйста, введите никнейм для регистрации.")

    else:
        st.subheader("Вход в личный кабинет")
        login_nick = st.text_input("Никнейм")
        st.text_input("Пароль", type="password")
        
        if st.button("Войти"):
            if login_nick:
                st.success("Вход выполнен!")
                # Автоматический переход на карту проблем
                st.session_state.menu_choice = "Карта проблем"
                st.rerun()
            else:
                st.error("Введите никнейм!")

# --- 2. КАРТА / СПИСОК ПРОБЛЕМ ---
elif choice == "Карта проблем":
    st.header("📍 Эко-точки твоего города")
    st.write("Изучи проблемы и выбери, где нужна твоя помощь.")
    
    problem = st.selectbox("Выберите объект", ["Центральный парк", "Река Илек"])
    
    if problem == "Центральный парк":
        st.subheader("Проблема: Свалка мусора у входа")
        if os.path.exists("park.jpg"):
            st.image("park.jpg", caption="Реальное фото: Свалка в парке")
        else:
            st.warning("Фото 'park.jpg' не найдено на GitHub. Загрузи его, чтобы пользователи видели проблему.")
        st.info("📊 Статистика: В вашем городе каждый день собирается около 150 кг мусора.")

    elif problem == "Река Илек":
        st.subheader("Проблема: Загрязнение береговой линии")
        if os.path.exists("river.jpg"):
            st.image("river.jpg", caption="Реальное фото: Берег реки")
        else:
            st.warning("Фото 'river.jpg' не найдено. Пожалуйста, добавь его в проект.")
        st.write("⚠️ Берег нуждается в срочной очистке от пластика и стекла.")

# --- 3. ЗАДАНИЯ (ЧЕЛЛЕНДЖИ) ---
elif choice == "Задания":
    st.header("🏆 Твои Эко-задания")
    st.metric("Твои баллы", st.session_state.score)
    st.write(f"Выполнено челленджей: **{st.session_state.tasks_done}**")
    
    task = st.selectbox("Выбери задание для выполнения", [
        "Сфоткай мусор и отправь в приложение (+10 баллов)",
        "Найди ближайший пункт переработки (+30 баллов)",
        "Собери команду для тазалау-акции (+50 баллов)"
    ])
    
    uploaded_file = st.file_uploader("Загрузи фото выполненного задания", type=['jpg', 'png', 'jpeg'])
    
    if st.button("Отправить на проверку"):
        if uploaded_file:
            # Начисляем баллы в зависимости от задания
            points = 10 if "Сфоткай" in task else 30 if "Найди" in task else 50
            st.session_state.score += points
            st.session_state.tasks_done += 1
            st.success(f"Отлично сработано! Тебе начислено {points} баллов.")
            st.balloons()
        else:
            st.warning("Прикрепи фото как доказательство выполнения!")

# --- 4. РЕЙТИНГ ---
elif choice == "Рейтинг":
    st.header("📊 Топ Эко-героев")
    
    # Создаем таблицу рейтинга
    data = {
        "Никнейм": ["GreenMaster", "EcoWarrior", "TazaAktobe", "EcoQueen", "Твой результат (You)"],
        "Баллы": [520, 480, 350, 290, st.session_state.score],
        "Заданий": [12, 10, 8, 7, st.session_state.tasks_done]
    }
    df = pd.DataFrame(data).sort_values(by="Баллы", ascending=False)
    
    st.table(df)
    st.info("🎁 **Главный приз:** У кого больше всего баллов и активности в соцсетях, тот получает экотрип по красивым местам Казахстана!")

# --- 5. ДИАГНОСТИКА (ТЕСТ) ---
elif choice == "Диагностика":
    st.header("🧠 Эко-диагностика")
    st.write("Пройди быстрый тест и узнай свой статус.")
    
    q1 = st.radio("Что ты делаешь с использованными батарейками?", 
                  ["Выбрасываю в мусор", "Сдаю в специальный пункт", "Коплю дома"])
    q2 = st.radio("Используешь ли ты шоперы вместо пластиковых пакетов?", 
                  ["Всегда", "Редко", "Никогда"])
    
    if st.button("Узнать мой уровень"):
        if q1 == "Сдаю в специальный пункт" and q2 == "Всегда":
            st.success("Твой статус: 🛡️ Охранник природы")
        elif q1 == "Выбрасываю в мусор" and q2 == "Никогда":
            st.error("Твой статус: 👶 Новичок. Тебе есть чему поучиться!")
        else:
            st.warning("Твой статус: 🌱 Эко-Стартер. Ты на правильном пути!")

# --- 6. СОЦИАЛЬНЫЕ СЕТИ ---
elif choice == "Соцсети":
    st.header("📢 Расскажи миру о проекте")
    st.write("Сделал доброе дело? Поделись этим в соцсетях, чтобы вдохновить других!")
    
    st.info("Используй хэштег: **#EcoJourneyChallenge**")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Instagram")
    with col2:
        st.button("TikTok")
    with col3:
        st.button("Telegram")
    
    st.write("---")
    st.write("Твой прогресс также учитывается при отборе на эко-тур!")
