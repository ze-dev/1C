#-------------------------------------------------------------------------------
# Language:    Python 3.6
# Author:      Eduard Zhukov
# GitHub:      https://github.com/ze-dev/1C
# Created:     04.11.2019
# Version      3.0
#-------------------------------------------------------------------------------
# Задача: Найти пересечение временных периодов, если оно существует
# Это стандартная задача в практике 1С-программистов.

#--------------------------------Решение----------------------------------------
import sys
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QSizePolicy,
    QCompleter, QHBoxLayout, QVBoxLayout, QApplication, QDateTimeEdit, QMessageBox) #, uic   # пока без внешней формы
import datetime as dt

##-------------------------------объявим функции:------------------------------
inscription = lambda txt: '<h3><b>' + txt + '</b><h3>'

def check_foo(el):
    if el == lab_buts[0]:
        return handle_click0
    if el == lab_buts[1]:
        return handle_click1
    if el == lab_buts[2]:
        return handle_click2

def sel_styles(dflt_clr = 'grey'):
    # for QDateTimeEdit изменим цвет текста
    sets =  '''
    font-weight: 200;
    color: ''' + dflt_clr + ''';
    font-size:12pt;
    border-width: 1px;
    border-radius: 5px;
    border-color: grey;
    border-style: outset;
    padding:10px;
    '''
    return sets

def set_font_clr(dflt_clr2 = 'black'):
##  изменим цвета текста в QDateTimeEdit в зависимости от значений
    any_period_was_wrong = False
    for i in range(1, len(linesEdit), 2):
        beg = linesEdit[i-1]
        end = linesEdit[i]

        if not beg.dateTime() <= end.dateTime():
            new_sets = sel_styles('red')
            any_period_was_wrong = True
        elif beg.dateTime() != dt_default or end.dateTime() != dt_default:
            new_sets = sel_styles(dflt_clr2)
        else:
            new_sets = sel_styles()
        [widg.setStyleSheet(new_sets) for widg in (beg, end)]

    if any_period_was_wrong:
        reply = QMessageBox()
        reply.warning(win, 'О Т К А З','Заполните правильно данные периодов!')
        return False
    else:
        return True

def handle_click0():
    ## 'Заполнить тестовыми значениями'
    clear_answer_lab()
    ##    -----------Вариант исходных 1 (из timePeriods_mainModule) :
    data = (
    #     НачПериода            КонПериода
    [2000, 2,  1,  0,  0,  0], [2003, 12, 31, 23, 59, 59],   # период 1
    [1998, 4, 20, 23, 59, 59], [2004,  8, 10,  9, 45, 59],   # период 2
    [2002, 9, 11,  8, 55, 49], [2017, 10, 27,  0,  0,  0]    # период 3
    )
    list(map(lambda fld,val: fld.setDateTime(QDateTime(*val)), linesEdit, data))
    set_font_clr()

def main_logic():
    global res, res_sec, mi, ma, res_str, fail
    res, res_str = [' ' for x in range(2)]
    res_sec = 0
    fail = False
    ## создаем список пар для сравнения, берем только заполненные и != дефолтным
    ip=[]
    index = []
    for i in range(0, len(linesEdit),2):
        pair = [x.dateTime().toPyDateTime() for x in (linesEdit[i], linesEdit[i+1])]
        if not (pair[0] == pair[1] and pair[0] == dt.datetime(*dt_default_list)):
            ip.append(pair)
            index.append(i)

    if len(ip) < 2:                # сравниваем минимум 2 периода
        reply = QMessageBox()
        reply.warning(win, 'О Т К А З','Заполните минимум 2 периода!')
        fail = True
        return False

    cr = (ip[0][0], ip[0][1])

    for i in range(1, len(ip)):
        mi = max(ip[i][0],cr[0])    # begins
        ma = min(ip[i][1],cr[1])    # ends
        if mi<=ma:
            cr = (mi,ma)
        else:
            fail = True
            res = 'NO union crossing.'
            break

    if not fail:
        res = 'GOT crossing!'
        delta = ma - mi
        # в периоде считается и первая его секунда и последняя
        res_sec = delta.total_seconds() + 1   # Краткое сообщение о результате
        res_str = 'Duration: {} sec.'.format(res_sec)
        # окрасим текст полей в зеленый в рассчитанном периоде пересечения
        for elem in index:
            if linesEdit[elem].dateTime().toPyDateTime() in (mi,ma):
                linesEdit[elem].setStyleSheet(sel_styles('green'))
            if linesEdit[elem + 1].dateTime().toPyDateTime() in (mi,ma):
                linesEdit[elem + 1].setStyleSheet(sel_styles('green'))

def set_answer_lab(new_txt):
    labels[6].setText('<font color=green>' + new_txt  + '</font>')

def clear_answer_lab(txt = ' <br> '):
    set_answer_lab(txt)

def handle_click1():
##  делаем простой расчет, просто количсетво секунд
    clear_answer_lab()
    if not set_font_clr():
        return False
    main_logic()
    ## изменяем ответ                           string  string
    set_answer_lab(inscription('{} <br>{}'.format(res, res_str)))

def handle_click2():
    clear_answer_lab()
    if not set_font_clr():
        return False
    main_logic()

    if not fail:
        extend_txt = info_period_time(res_sec, mi, ma)
    else:
        extend_txt = ' '
    set_answer_lab(inscription('{} <br>{}'.format(res, extend_txt)))

def info_period_time(allSeconds, nach, kon):
    '''nach, kon - начало, конец периода вида  datetime.datetime
    Разложим общее количество секунд на недели, дни и т.д.'''
    weeks = allSeconds // 604800    # кол-во секунд в неделе 7*24*60*60
    ots = allSeconds % 604800         # остальные секунды other_seconds
    days = ots // 86400                      # количество секунд в дне 24*60*60
    ots = ots % 86400
    hours = ots // 3600                      # секунд в часе 3600
    ots = ots % 3600
    minutes = ots // 60
    seconds = ots % 60
    msg = 'Интервал: {0} - {1}, длительность {2} секунд, \
        <br>или {3} недель, {4} дней, {5} часов, {6} минут, {7} секунд.'\
        .format(nach.strftime(format_dt_datetime), kon.strftime(format_dt_datetime), allSeconds, weeks, days, hours, minutes, seconds)
    return msg

##---------------------------создадим дефолтные переменные---------------------
format_dt = "dd.MM.yyyy hh:mm:ss"           # QDateTime
format_dt_datetime = "%d.%m.%Y %H:%M:%S"    # datetime.datetime
dt_default_list = [2000,1,1,0,0,0]
dt_default = QDateTime(*dt_default_list)

##  ===================================  BODY  =================================================
app = QApplication(sys.argv)
# 1)расположение вашего файла .ui:
##win = uic.loadUi("2810ui.ui") # пока без него, сделаем в след. приложении
# 2)вариант
win = QWidget()
win.setWindowTitle('Пересечение временных периодов (на PyQt5)') # main label up

# установка иконки
win.setWindowIcon(QIcon('watch2.png'))
# изменим размеры и привязки главного окна
win.resize(600, 370)
#win.move(600, 600)

# make ALL widgets at once--------------------------------------------------- 1
# inscriptions:
labels = [] #    0         1        2      3     4     5     6
for elem in ('Период', 'Начало', 'Конец', '1.', '2.', '3.', ' '):
    lab = QLabel(inscription(elem))
    lab.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
    labels.append(lab)

## изменяем цвет поля ответа [6] на нужный green
set_answer_lab (elem)

##  ----------------------- QDateTimeEdit boxes:
linesEdit = []
for elem in range(6):
    x = QDateTimeEdit()
    x.setStyleSheet(sel_styles())
    x.setAlignment(Qt.AlignLeft)  # положение курсора в поле
    x.setDisplayFormat(format_dt)
    x.setCalendarPopup(True)
    x.setMinimumHeight(35)
    linesEdit.append(x)

# make push buttons:
buts = []
lab_buts = ('&Заполнить тестовыми значениями', '&Простой расчет', '&Развернутый расчет')
for elem in lab_buts :
    x = QPushButton(elem)
    x.setStyleSheet('font: bold 10pt;')
    x.setMinimumHeight(50)              # вертикальный размер кнопки
    x.clicked.connect(check_foo(elem))  # делаем одну функцию с условиями по 3м кнопкам
    x.setAutoDefault(True)              # click on <Enter>
    x.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
    x.setStyleSheet('''
    color: #2c2e7f;
    background-color: #e7ddc4;
    font-weight: bold;
    font-size: 20px;
    font: bold 10pt;
    padding: 10px;
    pressed: {background-color: #A3C1DA; border: None; padding: None}   ;
''')
    buts.append(x)

## настроим ОДИНАКОВЫЕ РАСТЯЖЕНИЯ размеров для всех виджетов
[x.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed) for x in (*labels, *linesEdit, *buts)]

# draw horizontal and vertical blocks---------------------------------------- 2
# make Horizontal blocks:
hboxes = [QHBoxLayout() for i in range(6)]
[hboxes[0].addWidget(elem) for elem in labels[0:3] ]
[hboxes[1].addWidget(elem) for elem in (labels[3], *linesEdit[0:2]) ]
[hboxes[2].addWidget(elem) for elem in (labels[4], *linesEdit[2:4]) ]
[hboxes[3].addWidget(elem) for elem in (labels[5], *linesEdit[4:])  ]
hboxes[4].addWidget(labels[6])
[hboxes[5].addWidget(elem) for elem in buts ]

# make and fill in vbox
vbox = QVBoxLayout()    # vertical box
[vbox.addLayout(Hbox) for Hbox in hboxes]
win.setLayout(vbox)

win.show()
sys.exit(app.exec_())
## конец описания механизма================================================ end

