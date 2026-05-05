import streamlit as st
import pandas as pd

# Настройка страницы
st.set_page_config(page_title="EcoJourney Challenge", layout="centered")

# Инициализация "базы данных" в памяти (чтобы баллы сохранялись во время сессии)
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'tasks_done' not in st.session_state:
    st.session_state.tasks_done = 0

# Боковое меню для навигации
menu = ["Логин", "Карта проблем", "Задания", "Рейтинг", "Диагностика", "Соцсети"]
choice = st.sidebar.selectbox("Меню", menu)

# --- 1. СТАРТОВЫЙ ЭКРАН ---
if choice == "Логин":
    st.title("🌱 EcoJourney Challenge")
    auth_mode = st.radio("Выберите действие", ["Войти", "Создать аккаунт"])

    if auth_mode == "Создать аккаунт":
        name = st.text_input("Ваше имя")
        nickname = st.text_input("Никнейм")
        region = st.selectbox("Регион", ["Актобе", "Алматы", "Астана", "Шымкент", "Другой"])
        if st.button("Зарегистрироваться"):
            st.success(f"Привет, {nickname}! Добро пожаловать в команду {region}!")
    else:
        st.text_input("Никнейм")
        st.text_input("Пароль", type="password")
        st.button("Войти")

# --- 2. КАРТА / СПИСОК ПРОБЛЕМ ---
elif choice == "Карта проблем":
    st.header("📍 Эко-точки города")
    problem = st.selectbox("Выберите объект на карте", ["Центральный парк", "Река Илек", "Жилой массив"])

    if problem == "Центральный парк":
        st.subheader("Проблема: Свалка мусора у входа")
        st.image("https://via.placeholder.com/400x200?text=Photo+of+Trash+in+Park")
        st.info("Статистика: В вашем городе каждый день собирается около 150 кг мусора.")
    elif problem == "Река Илек":
        st.subheader("Проблема: Загрязнение береговой линии")
        st.write("Нужна очистка берега от пластика.")

# --- 3. ЗАДАНИЯ (ЧЕЛЛЕНДЖИ) ---
elif choice == "Задания":
    st.header("🏆 Твои Эко-задания")
    st.write(f"Твои баллы: **{st.session_state.score}** | Выполнено: **{st.session_state.tasks_done}**")

    task = st.selectbox("Выбери задание", [
        "Сфоткай мусор и отправь в приложение (+10 баллов)",
        "Найди пункт переработки (+30 баллов)",
        "Собери команду для тазалау-акции (+50 баллов)"
    ])

    uploaded_file = st.file_uploader("Загрузи фото-подтверждение", type=['jpg', 'png'])
    if st.button("Отправить на проверку"):
        if uploaded_file:
            points = 10 if "Сфоткай" in task else 30 if "Найди" in task else 50
            st.session_state.score += points
            st.session_state.tasks_done += 1
            st.success(f"Принято! Начислено {points} баллов.")
        else:
            st.warning("Сначала прикрепи фото!")

# --- 4. РЕЙТИНГ ---
elif choice == "Рейтинг":
    st.header("📊 Топ Эко-героев")
    data = {
        "Никнейм": ["GreenGuy", "EcoQueen", "Taza_Alem", "User123", "You"],
        "Баллы": [500, 450, 320, 210, st.session_state.score],
        "Заданий": [15, 12, 10, 5, st.session_state.tasks_done]
    }
    df = pd.DataFrame(data).sort_values(by="Баллы", ascending=False)
    st.table(df)
    st.warning(
        "🔥 У кого больше всего баллов и активности в соцсетях, тот получает экотрип по красивым местам Казахстана!")

# --- 5. ДИАГНОСТИКА ---
elif choice == "Диагностика":
    st.header("🧠 Эко-тест")
    q1 = st.radio("Как долго разлагается пластиковая бутылка?", ["10 лет", "100 лет", "450 лет"])
    q2 = st.radio("Сортируете ли вы мусор дома?", ["Да", "Нет", "Иногда"])

    if st.button("Узнать результат"):
        if q2 == "Да":
            st.balloons()
            st.success("Твой статус: Охранник природы! 🌲")
        else:
            st.info("Твой статус: Новичок. Давай исправлять! 🌱")

# --- 6. СОЦИАЛЬНЫЕ СЕТИ ---
elif choice == "Соцсети":
    st.header("📢 Расскажи друзьям")
    st.write("Поделись своими успехами, используя хэштег:")
    st.code("#EcoJourneyChallenge", language="text")
    st.write("Выбери платформу:")
    st.button("Поделиться в Instagram")
    st.button("Поделиться в TikTok")
    st.button("Поделиться в Telegram")