"""После создания текста запроса в консоли,
требуется в коде переопределить все одинарные верхние кавычки двойными,
а также добавить знак переноса, как форматирование многострочной строки.
Используется при установке Запрос.Текст = "наш модифицированный mod_mtext ";
"""

## аналог ввода исходной многострочной строки, для удобства
mtext = """// тут НАЧАЛЬНЫЕ каменты
Выбрать СК.Ссылка как Клиент,
        СК.Код как Код
 Из Справочник.Контрагенты как СК 
     // тут ЛОКАЛЬНЫЕ каменты
  Поместить ТврСК
// а тут ГЛОБАЛЬНЫЕ каменты
Где СК.Код = "ЦБ100500"
Упорядочить По Код // крайний камент
"""

## непосредственный ввод  исходной многострочной строки из терминала
## в боевом режиме
##mtext = "\n".join(iter(input, ""))

ltext = mtext.split("\n")           
mod_ltext = []
print("-"*30)
for line in ltext:
    if line.lstrip().startswith("//"):
       mod_line = line
    else:
       mod_line = "| " + line
    new_mod_line = ""
    for let in mod_line:
        if let =="\"":
            mod_let = let*2
        else:
            mod_let = let
        new_mod_line += mod_let
    mod_ltext.append(new_mod_line)

# построчный вывод
for lin in mod_ltext: 
    print(lin)

mod_mtext = "\n".join(iter(mod_ltext))
##sms = """"""
##s = """{mdl}"""
##for mod_line in mod_ltext:
##    sms = sms + "\n" +  s.format(mdl=mod_line) - доработать
