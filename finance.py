from flask import Flask, request, render_template, url_for, request, redirect
import psycopg2

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    # Если метод формы POST
    if request.method == 'POST':
        # Забираем данные из формы
        date = request.form['date']
        products = request.form['text1']
        productsH = request.form['text2']
        clothes = request.form['text3']
        health = request.form['text4']
        debts = request.form['text5']
        communication = request.form['text6']
        transport = request.form['text7']
        fun = request.form['text8']

        costs = (date, products, productsH, clothes, health, debts, communication, transport, fun)

        # Вносим данные в таблицу
        pgInsertUpdate(costs)
        return redirect('/')

    # Если метод GET
    else:
        return render_template("index.html")


@app.route('/report', methods=['POST', 'GET'])
def report():
    if request.method == 'POST':
        # Получение диапозона дат из формы
        date_start = request.form['date_start']
        date_end = request.form['date_end']
        # Запрос в базу данных по диапозону дат
        row = pgSelectForReport(date_start, date_end)
        # Вернуть результат на веб страницу
        return render_template('report.html', row=row, date_start=date_start, date_end=date_end)
    else:
        return render_template('report.html')


def pgSelectForReport(date_start, date_end):
    db = psycopg2.connect(
        database="finance_db",
        user="postgres",
        password="b14b43b82b84",
        host="127.0.0.1",
        port="5432")
    cursor = db.cursor()
    # Запрос по диапозону дат
    cursor.execute("""SELECT * FROM costs WHERE (Date BETWEEN '{0}' AND '{1}')""".format(str(date_start), str(date_end)))
    row = cursor.fetchall()
    return row


def pgInsertUpdate(values):
    date = values[0]
    db = psycopg2.connect(
        database="finance_db",
        user="postgres",
        password="b14b43b82b84",
        host="127.0.0.1",
        port="5432")
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM costs WHERE date='%s'""" % str(date))
    rows = cursor.fetchall()
    print(rows)
    # Если такой строки нет то, добавляем новую строку
    if not rows:
        cursor.execute('''INSERT INTO costs VALUES %s''' % str(values))
        db.commit()
        db.close()
    # Если есть то выполняем сложение с существующей строкой
    else:
        rows_list = list(rows[0])  # Преобразовывем полученный кортеж в список для вычислений
        new_data = []  # Новый список значений
        for value1, value2 in zip(values[1:], rows_list[1:]):
            if value1 == '':
                new_data.append(value2)
            elif value2 == '':
                new_data.append(value1)
            else:
                new_data.append(str(float(value1) + float(value2)))
        new_data = tuple(new_data)  # Преобразовывем новые данные обратно в кортеж
        print(new_data)
        # Обновляем данные в бд
        cursor.execute("""UPDATE costs SET
                products = '{0}',
                productsh = '{1}',
                clothes = '{2}',
                health = '{3}',
                debts = '{4}',
                communication = '{5}',
                transport = '{6}',
                fun = '{7}'  WHERE date= '{8}'""".format(str(new_data[0]), str(new_data[1]), str(new_data[2]),
                                                         str(new_data[3]), str(new_data[4]), str(new_data[5]),
                                                         str(new_data[6]), str(new_data[7]), date))
        db.commit()
        db.close()


if __name__ == '__main__':
    app.run(debug=True, host="192.168.1.35")
