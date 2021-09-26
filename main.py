from flask import Flask, request, render_template, url_for, request, redirect
from queries import queries
app = Flask(__name__)


@app.route('/costs', methods=['POST', 'GET'])
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

        costsTuple = (date, products, productsH, clothes, health, debts, communication, transport, fun)

        # Вносим данные в таблицу
        queries.pgInsertUpdateCosts(costsTuple)
        return render_template("index.html", date=date)

    # Если метод GET
    else:
        return render_template("index.html")


@app.route('/income', methods=['POST', 'GET'])
def income():
    if request.method == 'POST':
        date = request.form['date']
        income1 = request.form['text1']
        income2 = request.form['text2']
        reserve = request.form['text3']

        incomeTuple = (date, income1, income2, reserve)

        queries.pgInsertUpdateIncome(incomeTuple)
        return render_template("income.html", date=date)
    else:
        return render_template('income.html')


@app.route('/report', methods=['POST', 'GET'])
def report():
    if request.method == 'POST':
        # Получение диапозона дат из формы
        date_start = request.form['date_start']
        date_end = request.form['date_end']
        # Запрос в базу данных по диапозону дат
        row = queries.pgSelectForReport(date_start, date_end)
        # Подсчет итоговых значений
        r1, r2, r3, r4, r5, r6, r7, r8 = 0, 0, 0, 0, 0, 0, 0, 0
        total = 0.0
        for el in row:
            r1 += el[1]
            r2 += el[2]
            r3 += el[3]
            r4 += el[4]
            r5 += el[5]
            r6 += el[6]
            r7 += el[7]
            r8 += el[8]
            for elem in el[1:]:
                total = total + elem
        list_total = [str(round(r1, 2)), str(round(r2, 2)), str(round(r3, 2)), str(round(r4, 2)), str(round(r5, 2)),
                      str(round(r6, 2)), str(round(r7, 2)), str(round(r8, 2)), str(round(total, 2))]

        # Вернуть результат на веб страницу
        return render_template('report.html', row=row, date_start=date_start, date_end=date_end, list_total=list_total)
    else:
        return render_template('report.html')


@app.route('/report2', methods=['POST', 'GET'])
def report2():
    if request.method == 'POST':
        # Получение диапозона дат из формы
        date_start = request.form['date_start']
        date_end = request.form['date_end']
        # Запрос в базу данных по диапозону дат
        row = queries.pgSelectForReport2(date_start, date_end)
        # Подсчет итоговых значений
        r1, r2, r3 = 0, 0, 0
        total = 0.0
        for el in row:
            r1 += el[1]
            r2 += el[2]
            r3 += el[3]
            for elem in el[1:3]:
                total = total + elem
        list_total = [str(round(r1, 2)), str(round(r2, 2)), str(round(r3, 2)), str(round(total, 2))]
        return render_template('report2.html', row=row, date_start=date_start, date_end=date_end, list_total=list_total)

    else:
        return render_template('report2.html')


@app.route('/yearreport', methods=['POST', 'GET'])
def yearReport():
    listOfYears = queries.pgSelectForYearReport()
    listOfMonths = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
                       'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    if request.method == 'POST':
        year = request.form['year']
        listOfSum = queries.pgSelectForYearReportCosts(year)
        dictReport = dict(zip(listOfMonths, listOfSum))
        listSumColumns = (0, 0, 0, 0, 0, 0, 0, 0)
        for el in listOfSum:
            for el2 in el:
                listSumColumns = [round(x, 2) + round(y, 2) for x, y in zip(listSumColumns, el2)]
        sumForYear = sum(listSumColumns)
        listMean = [round(x / 12, 2) for x in listSumColumns]
        return render_template('yearreport.html', dictReport=dictReport, listOfMonths=listOfMonths, years=listOfYears,
                               year=year, sumForYear=sumForYear, listMean=listMean)
    else:
        return render_template('yearreport.html', years=listOfYears)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
