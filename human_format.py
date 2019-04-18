'''
последняя задачка с codewars
https://www.codewars.com/kata/52742f58faf5485cae000b9a/solutions/python
'''

def format_duration(allSeconds):
    if not allSeconds:
        return 'now'
    else:
        global cnt, emp
        cnt, emp, com = [0, 0, 0, 0, 0], '', ', '
        year = allSeconds // 31536000   
        ots = allSeconds % 31536000         
        days = ots // 86400                      
        ots = ots % 86400
        hours = ots // 3600                      
        ots = ots % 3600 
        minutes = ots // 60
        seconds = ots % 60
        y = form_elem(year, ' year')
        d = form_elem(days, ' day')
        h = form_elem(hours, ' hour')
        m = form_elem(minutes, ' minute')
        s = form_elem(seconds, ' second')
        yc, dc, hc, mc, sc  = [ com  if x else emp for  x in ( y, d, h, m, s) ]
        if sum( cnt ) > 1:
            pres, idx, cyc = ' and ', 4, True
            while cyc:
                if cnt[idx]:
                    if idx == 4:
                        sc = pres
                        cyc = False
                    if idx == 3:
                        mc =pres  
                        cyc = False
                    if idx == 2:
                        hc =pres 
                        cyc = False
                    if idx == 1:
                        dc = pres  
                        cyc = False
                    if idx == 0:
                        yc = pres 
                        cyc = False
                idx -= 1    
        return (yc + y + dc + d  + hc + h + mc + m + sc + s )[2:]

def form_elem(elem, n):
    if elem:
        cnt[0] = 1 if n == ' year' else cnt[0]
        cnt[1] = 1 if n == ' day' else cnt[1]
        cnt[2] = 1 if n == ' hour' else cnt[2]
        cnt[3] = 1 if n == ' minute' else cnt[3]
        cnt[4] = 1 if n ==  ' second' else cnt[4]
        e = str(elem)
        end = 's' if elem > 1 else emp
        return e + n + end
    else:
        return emp


print (

format_duration(1)       ,   #  "1 second")
format_duration(62)     ,   # "1 minute and 2 seconds")
format_duration(608400)   ,   #, "2 minutes")
format_duration(3600) ,   #  "1 hour")
format_duration(3662) ,   #1 hour, 1 minute and 2 seconds")
sep = '\n'
        )
