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
        # try:
        pgInsertUpdate(costs)
        return redirect('/')
        # except:
        #     return "При добавлении в базу данных произошла ошибка!"

    # Если метод GET
    else:
        return render_template("index.html")


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

    # Если такой строки нет то, добавляем новую строку
    if not rows:
        cursor.execute('''INSERT INTO costs VALUES %s''' % str(values))
        db.commit()
        db.close()
    # Если нет то выполняем сложение с существующей строкой
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
