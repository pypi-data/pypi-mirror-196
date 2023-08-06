import math
def seno(x):
    sinx = 0
    for i in range(10):
        coef = (-1) ** i
        num = x ** (2 * i + 1)
        den = math.factorial(2 * i + 1)
        sinx += coef * (num / den)
    return sinx

def coseno(x):
    cosx = 0
    for i in range(10):
        coef = (-1) ** i
        num = x ** (2 * i)
        den = math.factorial(2 * i)
        cosx += coef * (num / den)
    return cosx

def tangente(x):
    tanx = 0
    t1 = x
    t2 = (x**3)/3
    t3 = 2*(x**5)/15
    t4 = 17*(x**7)/315
    tanx = t1 + t2 + t3 + t4
    return tanx
