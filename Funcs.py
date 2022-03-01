from scipy.stats import ttest_1samp, ttest_ind
from statistics import multimode
import numpy as np


# вычисление корня(Для удобства)
def sqrt(n):
    return n ** 0.5


# Коэффициент вариаций        
def koeff_vars(lst):
    lst = [i for i in lst if i is not None] # Проверка.
    try:
        return sredn_otklon(lst) / sredn(lst)
    except ZeroDivisionError:
        pass

    
# Среднее квадратическое отклонение
def sredn_otklon(lst):
    lst = [i for i in lst if i is not None] # Проверка.
    return dispersion(lst) ** 0.5


# Среднее арифметическое
def sredn(lst):
    lst = [i for i in lst if i is not None] # Проверка.
    if lst:
        return sum(lst) / len(lst)


# Линеаризация списка рекурсией
def linear(lst): #Может понадобиться
    if not lst:
        return lst
    if type(lst[0]) is list:
        return linear(lst[0]) + linear(lst[1:])
    return lst[:1] + linear(lst[1:])


# Мода
def moda(lst):
    lst = [i for i in lst if i is not None] # Проверка.
    return max(lst, key=lambda x:lst.count(x))


# Медиана
def median(lst):
    lst = [i for i in lst if i is not None] # Проверка.
    n = len(lst)
    if n < 1:
            return None
    if n % 2 == 1:
            return sorted(lst)[n//2]
    else:
            return sum(sorted(lst)[n//2-1:n//2+1])/2.0

# Т-критерий для независимых выборок
def ttest1(a, b):
    a = [i for i in a if i is not None] # Проверка.
    b = [i for i in b if i is not None] # Проверка.
    x1, x2 = sredn(a), sredn(b)
    n1, n2 = len(a), len(b)
    o1, o2 = sredn_otklon(a), sredn_otklon(b)
    try:
        t = abs((x1 - x2) / sqrt((o1**2/n1) + (o2**2/n2)))
    except ZeroDivisionError:
        pass
    return t

# Т-критерий для зависимых выборок
def ttest2(a, b):
    a = [i for i in a if i is not None] # Проверка.
    b = [i for i in b if i is not None] # Проверка.
    M = 0
    l = []
    for i in zip(a, b):
        if len(i) > 1:
            l.append(i[0] - i[1])
        else:
            l.append(i)
    M = sredn(l)
    o = sredn_otklon(l)
    n = len(a)
    try:
        return abs(M / (o / sqrt(n)))
    except ZeroDivisionError:
        pass
    
    

# Выброс
def vibr(lst):
    lst = [i for i in lst if i is not None] # Проверка.
    lst.sort()
    s = sredn(lst)
    z = dict()
    for i in lst:
        if s - i not in z:
            z[abs(s - i)] = [i]
        else:
            z[abs(s - i)].append(i)
    x = max(linear(list(z.keys())))
    x = z[x]
    return x[0]

    
# Разброс значений
def scope(lst):
    lst = [i for i in lst if i is not None] # Проверка.
    return max(lst) - min(lst)


# Ошибка средней
def error_sredn(my_list):
    my_list = [i for i in my_list if i is not None] # Проверка. Очень полезная агада
    my_list = list(my_list)
    Sx = 0
    Sx2 = 0
    n = len(my_list)
    while (len(my_list) != 0):
        x = my_list.pop()
        Sx = Sx + x
        Sx2 = Sx2 + x * x
    return round((Sx2 / n - Sx * Sx / n / n), 5)


# Дисперсия
def dispersion(lst):
    lst = [i for i in lst if i is not None] # Проверка.
    m = sredn(lst)
    s = 0
    for i in list(set(lst)):
        s += sum([(i - m) ** 2 for k in range(lst.count(i))])
    try:
        return s / (len(lst) - 1)
    except:
        return 0.0
