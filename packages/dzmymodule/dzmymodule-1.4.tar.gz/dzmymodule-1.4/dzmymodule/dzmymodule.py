from dzmymodule import *
def inv():
    while True:
        s = input()
        if s.islower() or s.isupper() or s.isdigit(): 
            break
        else:
            print(s.swapcase())
    return inv()

def da():
    string = input()
    new_string = ''
    summa = 0
    for el in string:
        if el.isdigit():
            el = int(el)
            if el == 9:
                el = 0
            else:
                el += 1
            summa += el
            new_string += str(el)
        else:
            new_string += el
        

    print(new_string, summa, sep ='\n')
    return da()
def square(x):
    #Возвращает квадрат числа x.
    return x ** 2