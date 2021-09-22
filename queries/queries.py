from settings import dbstg


def pgSelectForReport(date_start, date_end):
    db = dbstg.connectToDb()
    cursor = db.cursor()
    # Запрос по диапозону дат
    cursor.execute(
        """SELECT * FROM costs WHERE (Date BETWEEN '{0}' AND '{1}')""".format(str(date_start), str(date_end)))
    row = cursor.fetchall()
    return row


def pgInsertUpdateCosts(values):
    date = values[0]
    db = dbstg.connectToDb()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM costs WHERE date='%s'""" % str(date))
    rows = cursor.fetchall()
    # Если такой строки нет то, добавляем новую строку
    if not rows:
        cursor.execute('''INSERT INTO costs VALUES %s''' % str(values))
        db.commit()
        db.close()
    # Если есть то выполняем сложение с существующей строкой
    else:
        cursor.execute("""UPDATE costs SET
                products = products + {0},
                productsh = productsh + {1},
                clothes = clothes + {2},
                health = health + {3},
                debts = debts +{4},
                communications = communications + {5},
                transport = transport + {6},
                fun = fun + {7}  WHERE date= '{8}'""".format(values[1], values[2], values[3], values[4],
                                                             values[5], values[6], values[7], values[8], date))
        db.commit()
        db.close()


def pgInsertUpdateIncome(values):
    date = values[0]
    db = dbstg.connectToDb()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM income WHERE date='%s'""" % str(date))
    rows = cursor.fetchall()
    # Если такой строки нет то, добавляем новую строку
    if not rows:
        cursor.execute('''INSERT INTO income VALUES %s''' % str(values))
        db.commit()
        db.close()
    # Если есть то выполняем сложение с существующей строкой
    else:
        cursor.execute("""UPDATE income SET
                   incomeyana = incomeyana + {0},
                   incomevova = incomevova + {1},
                   reserve = reserve + {2}
                   WHERE date = '{3}'""".format(values[1], values[2], values[3], date))
        db.commit()
        db.close()


def pgSelectForReport2(date_start, date_end):
    db = dbstg.connectToDb()
    cursor = db.cursor()
    # Запрос по диапозону дат
    cursor.execute(
        """SELECT * FROM income WHERE (Date BETWEEN '{0}' AND '{1}')""".format(str(date_start), str(date_end)))
    row = cursor.fetchall()
    return row


def pgSelectForYearreport():
    db=dbstg.connectToDb()
    cursor = db.cursor()
    cursor.execute("select DISTINCT date_part('year', date) from costs")
    listOfYears = cursor.fetchall()
    return listOfYears
