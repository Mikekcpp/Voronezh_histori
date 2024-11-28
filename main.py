from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout

from kivy.garden.drawer import DrawerLayout
import sqlite3


# Создание базы данных для рейтинга
conn = sqlite3.connect("rating.db")
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS rating (
        id INTEGER PRIMARY KEY,
        user TEXT,
        score INTEGER
    )
"""
)

conn.commit()
conn.close()

# Создание базы данных для писателей
conn = sqlite3.connect("writers.db")
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS writers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        biography TEXT,
        birthplace TEXT,
        deathplace TEXT,
        photo TEXT
    )
"""
)

conn.commit()
conn.close()


class WriterGame(BoxLayout):
    def __init__(self, **kwargs):
        super(WriterGame, self).__init__(**kwargs)
        self.orientation = "vertical"

        label = Label(text='Кто является автором произведения "Окаянные дни"?')
        self.add_widget(label)

        button1 = Button(text="Иван Бунин")
        button1.bind(on_press=self.check_answer)
        self.add_widget(button1)

        button2 = Button(text="Александр Куприн")
        button2.bind(on_press=self.check_answer)
        self.add_widget(button2)

        button3 = Button(text="Иван Тургенев")
        button3.bind(on_press=self.check_answer)
        self.add_widget(button3)

    def check_answer(self, instance):
        if instance.text == "Иван Бунин":
            popup = Popup(
                title="Результат",
                content=Label(text="Правильно!"),
                size_hint=(None, None),
                size=(200, 100),
            )
            popup.open()
            self.update_score()
        else:
            popup = Popup(
                title="Результат",
                content=Label(text="Неправильно!"),
                size_hint=(None, None),
                size=(200, 100),
            )
            popup.open()

    def update_score(self):
        conn = sqlite3.connect("rating.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM rating")
        rating = cursor.fetchall()

        for user in rating:
            if user[1] == "Пользователь 1":
                new_score = user[2] + 1
                cursor.execute(
                    "UPDATE rating SET score = ? WHERE user = ?",
                    (new_score, "Пользователь 1"),
                )

        conn.commit()
        conn.close()


class MapWidget(FloatLayout):
    def __init__(self, **kwargs):
        super(MapWidget, self).__init__(**kwargs)
        self.map_image = Image(
            source="photo_5352626336243509126_y.jpg",
            allow_stretch=True,
            keep_ratio=False,
        )
        self.add_widget(self.map_image)

    def add_marker(self, x, y, text):
        marker = Label(text=text, font_size=20, color=(1, 0, 0, 1), pos=(x, y))
        self.add_widget(marker)


class WriterApp(App):
    def build(self):
        layout = DrawerLayout()

        self.map_image = Image(
            source="photo_5352626336243509126_y.jpg",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
        )
        layout.add_widget(self.map_image)

        drawer = BoxLayout(orientation="vertical")
        layout.add_widget(drawer)

        button1 = Button(text="Рейтинг")
        button1.bind(on_press=self.show_rating)
        drawer.add_widget(button1)

        button2 = Button(text="Писатели")
        button2.bind(on_press=self.show_writers)
        drawer.add_widget(button2)

        button3 = Button(text="Добавить писателя")
        button3.bind(on_press=self.add_writer)
        drawer.add_widget(button3)

        button4 = Button(text="Библиотека")
        button4.bind(on_press=self.show_library)
        drawer.add_widget(button4)

        button5 = Button(text="Форум")
        button5.bind(on_press=self.show_forum)
        drawer.add_widget(button5)

        button6 = Button(text="Профиль")
        button6.bind(on_press=self.show_profile)
        drawer.add_widget(button6)

        return layout

    def play_game(self, instance):
        game = WriterGame()
        popup = Popup(
            title="Игра", content=game, size_hint=(None, None), size=(400, 300)
        )
        popup.open()

    def show_rating(self, instance):
        conn = sqlite3.connect("rating.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM rating")
        rating = cursor.fetchall()

        popup = Popup(title="Рейтинг", size_hint=(None, None), size=(200, 200))
        layout = BoxLayout(orientation="vertical")
        for user in rating:
            label = Label(text=f"{user[1]} - {user[2]}")
            layout.add_widget(label)
        popup.add_widget(layout)
        popup.open()

    def show_map(self, instance):
        # Создаём popup с картой
        popup = Popup(title="Карта", size_hint=(0.9, 0.9))
        layout = FloatLayout()
        self.map_image = Image(
            source="photo_5352626336243509126_y.jpg",
            allow_stretch=True,
            keep_ratio=False,
        )
        layout.add_widget(self.map_image)
        popup.add_widget(layout)
        popup.open()

    def add_writer(self, instance):
        popup = Popup(
            title="Добавить писателя", size_hint=(None, None), size=(200, 200)
        )
        layout = BoxLayout(orientation="vertical")
        name_input = Label(text="Имя писателя")
        layout.add_widget(name_input)
        biography_input = Label(text="Биография писателя")
        layout.add_widget(biography_input)
        birthplace_input = Label(text="Место рождения писателя")
        layout.add_widget(birthplace_input)
        deathplace_input = Label(text="Место смерти писателя")
        layout.add_widget(deathplace_input)
        photo_input = Label(text="Фото писателя")
        layout.add_widget(photo_input)
        button = Button(text="Добавить")
        button.bind(on_press=self.add_writer_to_db)
        layout.add_widget(button)
        popup.add_widget(layout)
        popup.open()

    def add_writer_to_db(self, instance):
        conn = sqlite3.connect("writers.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO writers VALUES (NULL, ?, ?, ?, ?, ?)",
            ("Иван Бунин", "Русский писатель", "Воронеж", "Париж", "bunin.jpg"),
        )

        conn.commit()
        conn.close()

    def show_writers(self, instance):
        conn = sqlite3.connect("writers.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM writers")
        writers = cursor.fetchall()

        popup = Popup(title="Писатели", size_hint=(None, None), size=(200, 200))
        layout = BoxLayout(orientation="vertical")
        for writer in writers:
            label = Label(text=f"{writer[1]} - {writer[2]}")
            layout.add_widget(label)
        popup.add_widget(layout)
        popup.open()

    def play_quiz(self, instance):
        popup = Popup(title="Викторина", size_hint=(None, None), size=(200, 200))
        layout = BoxLayout(orientation="vertical")
        question_label = Label(text='Кто является автором произведения "Окаянные дни"?')
        layout.add_widget(question_label)
        button1 = Button(text="Иван Бунин")
        button1.bind(on_press=self.check_answer)
        layout.add_widget(button1)
        button2 = Button(text="Александр Куприн")
        button2.bind(on_press=self.check_answer)
        layout.add_widget(button2)
        button3 = Button(text="Иван Тургенев")
        button3.bind(on_press=self.check_answer)
        layout.add_widget(button3)
        popup.add_widget(layout)
        popup.open()

    def check_answer(self, instance):
        if instance.text == "Иван Бунин":
            popup = Popup(
                title="Результат",
                content=Label(text="Правильно!"),
                size_hint=(None, None),
                size=(200, 100),
            )
            popup.open()
            self.update_score()
        else:
            popup = Popup(
                title="Результат",
                content=Label(text="Неправильно!"),
                size_hint=(None, None),
                size=(200, 100),
            )
            popup.open()

    def update_score(self):
        conn = sqlite3.connect("rating.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM rating")
        rating = cursor.fetchall()

        for user in rating:
            if user[1] == "Пользователь 1":
                new_score = user[2] + 1
                cursor.execute(
                    "UPDATE rating SET score = ? WHERE user = ?",
                    (new_score, "Пользователь 1"),
                )

        conn.commit()
        conn.close()

    def play_quests(self, instance):
        popup = Popup(title="Квесты", size_hint=(None, None), size=(200, 200))
        layout = BoxLayout(orientation="vertical")
        quest_label = Label(text="Найдите дом-музей Ивана Бунина")
        layout.add_widget(quest_label)
        button = Button(text="Найти")
        button.bind(on_press=self.find_quest)
        layout.add_widget(button)
        popup.add_widget(layout)
        popup.open()

    def find_quest(self, instance):
        popup = Popup(
            title="Результат",
            content=Label(text="Вы нашли дом-музей Ивана Бунина!"),
            size_hint=(None, None),
            size=(200, 100),
        )
        popup.open()
        self.update_score()

    def play_game_mode(self, instance):
        popup = Popup(title="Игровой режим", size_hint=(None, None), size=(200, 200))
        layout = BoxLayout(orientation="vertical")
        game_label = Label(text="Выберите персонажа")
        layout.add_widget(game_label)
        button1 = Button(text="Иван Бунин")
        button1.bind(on_press=self.choose_character)
        layout.add_widget(button1)
        button2 = Button(text="Александр Куприн")
        button2.bind(on_press=self.choose_character)
        layout.add_widget(button2)
        popup.add_widget(layout)
        popup.open()

    def choose_character(self, instance):
        popup = Popup(
            title="Выбранный персонаж",
            content=Label(text=f"Вы выбрали {instance.text}"),
            size_hint=(None, None),
            size=(200, 100),
        )
        popup.open()
        self.start_game()

    def start_game(self):
        popup = Popup(title="Игровой режим", size_hint=(None, None), size=(200, 200))
        layout = BoxLayout(orientation="vertical")
        game_label = Label(text="Вы находитесь в Воронеже")
        layout.add_widget(game_label)
        button = Button(text="Идти в дом-музей Ивана Бунина")
        button.bind(on_press=self.go_to_museum)
        layout.add_widget(button)
        popup.add_widget(layout)
        popup.open()

    def go_to_museum(self, instance):
        popup = Popup(
            title="Дом-музей Ивана Бунина",
            content=Label(text="Вы пришли в дом-музей Ивана Бунина"),
            size_hint=(None, None),
            size=(200, 100),
        )
        popup.open()
        self.update_score()

    def show_library(self, instance):
        popup = Popup(title="Библиотека", size_hint=(None, None), size=(200, 200))
        layout = BoxLayout(orientation="vertical")
        library_label = Label(text="Выберите книгу")
        layout.add_widget(library_label)
        button1 = Button(text="Окаянные дни")
        button1.bind(on_press=self.read_book)
        layout.add_widget(button1)
        button2 = Button(text="Поединок")
        button2.bind(on_press=self.read_book)
        layout.add_widget(button2)
        popup.add_widget(layout)
        popup.open()

    def read_book(self, instance):
        popup = Popup(
            title="Книга",
            content=Label(text=f"Вы прочитали {instance.text}"),
            size_hint=(None, None),
            size=(200, 100),
        )
        popup.open()
        self.update_score()

    def show_forum(self, instance):
        popup = Popup(title="Форум", size_hint=(None, None), size=(200, 200))
        layout = BoxLayout(orientation="vertical")
        forum_label = Label(text="Обсуждение книг")
        layout.add_widget(forum_label)
        button = Button(text="Прочитать обсуждение")
        button.bind(on_press=self.read_discussion)
        layout.add_widget(button)
        popup.add_widget(layout)
        popup.open()

    def read_discussion(self, instance):
        popup = Popup(
            title="Обсуждение",
            content=Label(text="Вы прочитали обсуждение"),
            size_hint=(None, None),
            size=(200, 100),
        )
        popup.open()
        self.update_score()


if __name__ == "__main__":
    WriterApp().run()
