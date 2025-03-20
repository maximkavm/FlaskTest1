import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    name = "John"  # Здесь вы можете установить имя, которое хотите передать
    results = []

    # Создаем соединение с базой данных
    conn = sqlite3.connect('results.db')

    # Создаем курсор
    c = conn.cursor()

    # Проверяем, существует ли таблица
    c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='results' ''')

    # Если таблицы нет, создаем ее
    if c.fetchone()[0] == 0:
        c.execute('''CREATE TABLE results
                     (id INTEGER PRIMARY KEY, result VARCHAR(255)''')

    # Получаем результаты из базы данных
    c.execute('SELECT * FROM results')
    rows = c.fetchall()

    if request.method == 'POST':
        num1 = int(request.form['num1'])
        num2 = int(request.form['num2'])
        result = num1 + num2  # Здесь вы можете выполнить любое вычисление
        ress = f'{num1} + {num2} = {result}'
        # Сохраняем результат в базу данных
        c.execute('INSERT INTO results (result) VALUES (?)', (ress,))
        conn.commit()

    # Закрываем соединение
    conn.close()
    # Создаем соединение с базой данных
    conn = sqlite3.connect('results.db')

    # Создаем курсор
    c = conn.cursor()
    c.execute('SELECT * FROM results')
    rows = c.fetchall()
    for row in rows:
        results.append(row[1])
    conn.close()

    return render_template('home.html', name=name, results=results)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
