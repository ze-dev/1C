'''Вычисление количества десятичных часов и ЧЧ:мм по количеству секунд
Использовал для пересчетов времени в Учет времени ЗН'''
ans = ""
while ans == "" :
    a = int( input("\nВведем количество секунд: ") )
    h = a / 3600
    m = (a - (int(h) * 60 * 60 )) / 60
    ans = input("dec_hrs > {}  |  hh:mm > {}:{}    Еще? ДА - Ентер > "\
    .format(round(h,3),int(h),(round(m) if m>=9.5 else "0"+str(round(m)))))
