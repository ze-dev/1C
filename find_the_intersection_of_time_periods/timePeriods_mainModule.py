#---------------------------------------------------------------------------
# Language:    Python 3.6
# Author:      Eduard Zhukov
# GitHub:      https://github.com/ze-dev/1C
# Created:     27.11.2018
#---------------------------------------------------------------------------

# Задача: Найти пересечение временных периодов, если оно существует
# Это стандартная задача в практике 1С-программистов.
# В этом модуле только исходные данные и объявление функций
# Решения в модулях timePeriods_solution..

# ----------------------Исходные данные---------------------
# Вписываются здесь вручную, ввод в консоли не предусматривался.
# Количество анализируемых периодов может быть больше трех.
# Значения дат идентичны в обоих вариантах.
# Проверка на пустую дату "01.01.0001" не предусмотрена

#-----------Вариант исходных 1 с одинаковым форматом даты :
inputPeriods = (
#     НачПериода            КонПериода
 ("20000201000000", "20031231235959"),   # период 1
 ("19980420235959", "20040810094559"),   # период 2
 ("20020911085549", "20171027000000")    # период 3
 )

###-----------Вариант исходных 2 с разными форматами даты :
##inputPeriods = (
###     НачПериода            КонПериода
## ("20000201",            "20031231235959"),    # период 1
## ("20.04.1998 23:59:59", "20040810094559"),    # период 2
## ("11-09-2002 08:55:49", "27.10.2017")         # период 3
## )

#-------------------------Объявление функций--------------------------------

def convert_date(dt):
    '''Приведем входной формат даты dt из возможного списка:
    "20000701000000"
    "20040810"
    "20.04.1998 23:59:59"
    "27.10.2017"
    "20-04-1998 23:59:59"
    "27-10-2017"
    к универсальному виду: вернет "20000701000000".
    Если формат даты будет отличаться из списочного,
    будет выведено сообщение о не определенном формате,
    но программа начнет расчет и вернет необработанное исключение.'''
    resultDt = 0
    length = len(dt)
    if dt.isdigit():
        if length == 14:                                      #  if "20000701000000"
            resultDt = dt
        if length == 8:                                       #  if "20040810"
            resultDt = dt.ljust(14, "0")
    else:
        for char in (".", "-"):
            if dt.count(char) == 2:
                if length == 19 and dt.count(":") == 2:  #  if "20.(or -)04.1998 23:59:59"
                    left, right = dt.split(' ')
                    day, month, year = left.split(char)
                    h, m, s = right.split(':')
                    resultDt = "".join([year, month, day, h, m, s])
                if length == 10:                                        #  if "27.(or -)10.2017"
                    day, month, year = dt.split(char)
                    resultDt = ("".join([year, month, day]).ljust(14, "0"))
        if not resultDt:
            print('\n!!! Формат даты не определен. Проверьте даты!!!')
    return resultDt

def convert_period(periodsList):
    '''periodList = [ (нп1,кп1), (нп2,кп2), (.., ..) ]
    Вернет список периодов с форматами дат
    в универсальном формате "20000701000000" '''
    nPeriods = []
    for period in periodsList:
        nDate = []
        for date in period:
            nD = convert_date(date)
            nDate.append(nD)
        nPeriods.append(nDate)
    return nPeriods

def leap(y_):
    ''' y_- значение года (цел), вид: leap(1988)
    Вернет  1 - если высокосный, 0 - если стандартный год.'''
    if y_%4 == 0:
        if y_%100 == 0:
            if y_%400 == 0:
                ans = 1
            else:
                ans = 0
        else:
            ans = 1
    else:
        ans = 0
    return ans

def feb_days(y_):
    '''y_-целое значение года  (1900)
    Вернем количество дней ФЕВРАЛЯ Любого года в зависимости,
    високосный год (leap(y_) =1) или нет (0)'''
    return 28 + leap(y_)

def get_year(y_):
    '''get_year(2000), где y_ - целое значение года
    Возвращает весь год в виде словаря {01:31, ..},
    в зависимости, високосный он (1) или нет (0).
    Ключи - целые знач.'''
    monthes = (  1,         2,        3,   4,   5,    6,   7,   8,   9, 10, 11, 12)
    days        = (31, feb_days(y_), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    return dict(zip(monthes , days))

def year_days(num_year, first_mon = 1, last_mon = 12):
    '''num_year - значение года,
    first_m - номер первого нужного месяца(1), last - последнего(12).
    Если нужен год целиком, то номера месяцев не ставить-
    будут по умолчанию 1, 12 (Включительно)
    Вернет количество дней нужного периода внутри Любого Одного года.
    Подсчет ведется с первого по последний нужных месяцев Включительно'''
    year_ = get_year(num_year)
    return sum(year_[key] for key in range(first_mon, last_mon + 1))

def some_yrs_days(firstY, lastY):
    '''Вернет количество дней за период от first до last (года) включительно'''
    return sum(year_days(numYear) for numYear in range(firstY, lastY + 1))

def make_elem(dat_):
    '''dat_-строковое значение даты: '19880301205730'
    (д.б. передана сюда до целых сек (14цифр))
    Определяем значения элементов даты: значения года, месяца и т.д.):
    Вернет значения Y, M, D, h, m, s списком [1988, 03, 01, 20, 57, 30] '''
    Ye, Me, De = ((0, 4), (4, 6), (6, 8))           # позиции в дате: год, месяц, день
    he, me, se = ((8, 10), (10, 12), (12, 14)) # позиции час, минута, секунды
    elem_list = (Ye, Me, De, he, me, se)    # список позиций элементов даты
    res_list = [] # результирующий список элементов даты: год, мес, .., сек.
    for element in elem_list:
        start, end = element  # определим нач и кон позиции года, месяца, ..
        element_dim = dat_[start: end] # получим '1988'(г) или '02'(мес) и т.д.
        res_list.append(int(element_dim))
    return res_list

def from_yr_begin_to_date(dateElemList):
    '''Вернет величину отрезка с начала года до нужной даты в секундах,
    учитывая високосность года определения, включая нулевую сек. начала
    elemList должно быть в уже разобранном виде [1988, 3, 1, 20, 57, 30],
    разбирается на составные ф-ией make_elem.'''
    Ye, Me, De, he, me, se = dateElemList
    daysInWholeMons = year_days(Ye, 1, Me - 1) # кол-во дней в полных мес.
    daysInsideMon = (De - 1)                                  # кол-во дней в полных днях
    secInWholeHrs = he * 60 * 60                     # кол-во секунд за полные часы
    secInWholeMin = me * 60                           # кол-во секунд за полные минуты
    sec = se + 1     # кол-во секунд, включая нулевую секунду периода
    wholeSec = (daysInWholeMons + daysInsideMon)*86400 + \
                           secInWholeHrs + secInWholeMin + sec
    return wholeSec

def from_date_to_yr_end(dateElemList_):
    '''Вернет величину отрезка с нужной даты до конца года в секундах,
    учитывая високосность года определения, включая секунду начала.
    elemList должно быть в уже разобранном виде [1988, 3, 1, 20, 57, 30]'''
    numY = dateElemList_[0]
    sec = year_days(numY) * 86400 - from_yr_begin_to_date(dateElemList_) + 1
    return sec

def period_time(begin_, end_):   # begin < end
    '''Начало периода и конец должны подавться в виде "19880301205730"
    Вернет продолжительность периода  в секундах.'''
    begin, end = [make_elem(_) for _ in (begin_, end_)] # разбираем на элементы
    diff = end[0] - begin[0]  # определяем разницу значений годов
    if not diff:                          # весь период внутри одного года
        time = from_yr_begin_to_date(end) - from_yr_begin_to_date(begin) + 1
    elif diff == 1:                    # период не более,чем в двух смежных годах
        time = from_yr_begin_to_date(end) + from_date_to_yr_end(begin)
    elif diff > 1:                      # в границах более, чем в двух смежных
        time = from_yr_begin_to_date(end) + from_date_to_yr_end(begin) + \
                    some_yrs_days(begin[0] +1, end[0] - 1) * 86400
    return time                       # вернули в секундах

def info_period_time(nach, kon):
    '''nach, kon - начало, конец периода вида '20101009080706'
    Разложим общее количество секунд на недели, дни и т.д.'''
    allSeconds = period_time(nach, kon)
    weeks = allSeconds // 604800    # кол-во секунд в неделе 7*24*60*60
    ots = allSeconds % 604800         # остальные секунды other_seconds
    days = ots // 86400                      # количество секунд в дне 24*60*60
    ots = ots % 86400
    hours = ots // 3600                      # секунд в часе 3600
    ots = ots % 3600
    minutes = ots // 60
    seconds = ots % 60
    msg = 'Временной интервал с {0} по {1},\
                 \nпродолжительностью {2} секунд, \
                 \nили {3} недель, {4} дней, {5} часов, {6} минут, {7} секунд.'\
               .format(nach, kon, allSeconds, weeks, days, hours, minutes, seconds)
    return msg

def cross(periodList_):
    '''periodList_ = [period1, period2] , м.б. не отсортированным.
    Вернет (начало, конец) пересечениt 2х любых периодов, или 0, если нет'''
    periodList = sorted(periodList_)
    n0, k0, n1, k1 = [periodList[__][_] for __ in range (2) for _ in range(2)]
    if k0 >= n1:
        cros = sorted([n0, k0, n1, k1])[1:3]
    else:
        cros = 0
    return cros

# ----- Конец объявления ф-ий. Решения в модулях timePeriods_solution..------

if __name__ == '__main__':
    input("В этом модуле только исходные данные и объявление функций.\
    \nРешения в модулях timePeriods_solution..\
    \nДля выхода нажмите enter..")


