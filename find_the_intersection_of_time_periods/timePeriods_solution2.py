#-------------------------------------------------------------------------------
# Language:    Python 3.6
# Author:      Eduard Zhukov
# GitHub:      https://github.com/ze-dev/1C
# Created:     20.10.2019
# Version      2.0
#-------------------------------------------------------------------------------
# Задача: Найти пересечение временных периодов, если оно существует
# Это стандартная задача в практике 1С-программистов.

#--------------------------------Решение----------------------------------------

# Все используемые функции и исходные данные находятся в timePeriods_mainModule
# Тут только логика решения

from datetime import datetime
from timePeriods_mainModule import make_elem
from timePeriods_mainModule import info_period_time
from timePeriods_mainModule import inputPeriods as ip  # импорт исходных
fail = False
cr = (ip[0][0], ip[0][1])

for i in range(1, len(ip)):
    mi = max(ip[i][0],cr[0])    # begins
    ma = min(ip[i][1],cr[1])    # ends
    if mi<=ma:
        cr = (mi,ma)
    else:
        fail = True
        print('NO any crossing.')
        break

#---------можно использовать для проверки работоспособности ф-ий---------
#---------предыдущие вычисления сбросятся
##mi = '20010101101010'
##ma = '20010101101011'     # в этом периоде 2 секунды

if not fail:
    print('GOT crossing!')
    mi_s = datetime(*make_elem(mi))
    ma_s = datetime(*make_elem(ma))
    delta = ma_s - mi_s
    # в периоде считается и первая его секунда и последняя
    print(delta.total_seconds()+1)  # Краткое сообщение о результате
    print(info_period_time(mi, ma)) # Более развернутое сообщение о результате

input('для выхода нажмите enter..')


