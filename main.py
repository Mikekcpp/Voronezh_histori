import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import sqlite3
import folium
from kivy.uix.popup import Popup

# Создаем базу данных с информацией о писателях
conn = sqlite3.connect('writers.db')
cursor = conn.cursor()

# Проверяем, существует ли таблица writers
cursor.execute('''
    SELECT name
    FROM sqlite_master
    WHERE type='table' AND name='writers'
''')

if cursor.fetchone() is None:
    # Если таблица не существует, создаем ее
    cursor.execute('''
        CREATE TABLE writers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            biography TEXT NOT NULL,
            birthplace TEXT NOT NULL,
            deathplace TEXT NOT NULL,
            photo BLOB NOT NULL
        )
    ''')

# Добавляем писателей в базу данных
writers = [
    ('Иван Бунин', 'Русский писатель', 'Воронеж', 'Париж', 'bunin.jpg'),
    ('Александр Куприн', 'Русский писатель', 'Наровчат', 'Ленинград', 'kuprin.jpg'),
    ('Иван Тургенев', 'Русский писатель', 'Орёл', 'Буживаль', 'turgenev.jpg')
]

cursor.executemany('INSERT OR IGNORE INTO writers VALUES (NULL, ?, ?, ?, ?, ?)', writers)

conn.commit()
conn.close()

# Создаем базу данных с рейтингом
conn = sqlite3.connect('rating.db')
cursor = conn.cursor()

# Проверяем, существует ли таблица rating
cursor.execute('''
    SELECT name
    FROM sqlite_master
    WHERE type='table' AND name='rating'
''')

if cursor.fetchone() is None:
    # Если таблица не существует, создаем ее
    cursor.execute('''
        CREATE TABLE rating (
            id INTEGER PRIMARY KEY,
            user TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')

# Добавляем пользователя в базу данных
cursor.execute('INSERT OR IGNORE INTO rating VALUES (NULL, ?, 0)', ('Пользователь 1',))

conn.commit()
conn.close()


class WriterGame(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        label = Label(text='Кто является автором произведения "Окаянные дни"?')
        self.layout.add_widget(label)

        button1 = Button(text='Иван Бунин')
        button1.bind(on_press=self.check_answer)
        self.layout.add_widget(button1)

        button2 = Button(text='Александр Куприн')
        button2.bind(on_press=self.check_answer)
        self.layout.add_widget(button2)

        button3 = Button(text='Иван Тургенев')
        button3.bind(on_press=self.check_answer)
        self.layout.add_widget(button3)

        return self.layout

    def check_answer(self, instance):
        if instance.text == 'Иван Бунин':
            popup = Popup(title='Результат', content=Label(text='Правильно!'), size_hint=(None, None), size=(200, 100))
            popup.open()
        else:
            popup = Popup(title='Результат', content=Label(text='Неправильно!'), size_hint=(None, None), size=(200, 100))
            popup.open()

    def show_map(self, instance):
        m = folium.Map(location=[51.6536, 39.2108], zoom_start=12)
        folium.Marker([51.6536, 39.2108], popup='Воронеж').add_to(m)
        m.save('voronezh_map.html')
        webbrowser.open('voronezh_map.html')


class WriterApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        label = Label(text='Нескучный Литературный Воронеж')
        self.layout.add_widget(label)

        button1 = Button(text='Играть')
        button1.bind(on_press=self.play_game)
        self.layout.add_widget(button1)

        button2 = Button(text='Рейтинг')
        button2.bind(on_press=self.show_rating)
        self.layout.add_widget(button2)

        button3 = Button(text='Карта')
        button3.bind(on_press=self.show_map)
        self.layout.add_widget(button3)

        return self.layout

    def play_game(self, instance):
        WriterGame().run()

    def show_rating(self, instance):
        conn = sqlite3.connect('rating.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM rating')
        rating = cursor.fetchall()

        popup = Popup(title='Рейтинг', size_hint=(None, None), size=(200, 200))
        layout = BoxLayout(orientation='vertical')
        for user in rating:
            label = Label(text=f'{user[1]} - {user[2]}')
            layout.add_widget(label)
        popup.add_widget(layout)
        popup.open()

    def show_map(self, instance):
        m = folium.Map(location=[51.6536, 39.2108], zoom_start=12)

        conn = sqlite3.connect('writers.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM writers')
        writers = cursor.fetchall()

        for writer in writers:
            if writer[3] == 'Воронеж':
                folium.Marker([51.6536, 39.2108], popup=writer[1]).add_to(m)
            elif writer[3] == 'Наровчат':
                folium.Marker([53.8833, 46.7333], popup=writer[1]).add_to(m)
            elif writer[3] == 'Орёл':
                folium.Marker([52.9667, 36.0667], popup=writer[1]).add_to(m)

        m.save('voronezh_map.html')
        popup = Popup(title='Карта', content=Label(text='Карта сохранена в файле voronezh_map.html'),
                      size_hint=(None, None), size=(200, 100))
        popup.open()



if __name__ == '__main__':
    WriterApp().run()

