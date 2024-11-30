#Todo quadruple. Handtere at brukere gir bokstaver i stedet for tall som input. Det gir feil nå. 

class Kalkulator:

    def __init__(self) -> None:
        pass

    def fibonacci(self, n):
        resultat = []
        if n < 1:
            print("DUST\n"*100)
        elif n == 1:
            resultat.append(0)
        elif n > 10000:
            print("Maks nummer er 9999")
        else:
            resultat.append(0)
            resultat.append(1)
            for i in range(1 ,n):
                tall = resultat[i] + resultat[i-1]
                resultat.append(tall)
            return resultat

    def add(self, x,y):
        return x+y

    def sub(self, x,y):
        return x-y

    def multi(self, a, b):
        return a*b

    def dele(self, c, d):
        return c/d

    def nterot(self, x, n):
        return x**n
    
    def findBiggest(self, x,y):
        if x > y:
            return x
        else: 
            return y                            



nummer_1 = int(input("Set inn forste tall: "))
nummer_2 = int(input("Set inn andre tall: "))
biggest = findBiggest(nummer_1, nummer_2)
print(f"{biggest} er størst")


# This is the menu. 
avslutt = False
while(not avslutt):
    print("---=== Meny ===---")
    print("0: Avslutt")
    print("1: Addere")
    menuchoice = int(input("Valg:"))
    match menuchoice:
        case 0:
            avslutt = True
            print("Avslutter")
        case 1:
            forste_tall = int(input("Sett in det første tallet du vi addere: "))
            andre_tall = int(input("Sett inn tall to: "))
            add(forste_tall, andre_tall)
        case _:
            print("Feil valg")

"""
Denne delen er skjæringssetningen og Newton-Raphson tilnærmingsmetode 
den finner ut om det krysser en linje y = 0 i dette tilfellet og må
omskrives til en generell version
"""

from math import exp

def f(x):
    return (((x-1)**2)*exp(x)-0.5)

def df(x):
    return (exp(x)*(((2*x)-2)+(x-1)**2))

def deltax(x):
    return f(x)/df(x)

def tilnarming(x):
    noyaktighet=0.000001
    c=x # startverdi

    while abs(deltax(c))>noyaktighet:
        c = c-deltax(c)
    return c

# Prøver de 3 intervallene skjæringssetningen
# [-5,-1]
print(f"Intervall: [-5,-1]  [{f(-5)}, {f(-1)}]")
print("Skærer linjen y = 0")
# [-1,1]
print(f"Intervall: [-1,1]  [{f(-1)}, {f(1)}]")
print("Skærer linjen y = 0")
# [1,2]
print(f"Intervall: [1,2]  [{f(1)}, {f(2)}]")
print("Skærer linjen y = 0\nAlle ytterpunktene av intervallene er på hver side av linjen y = 0 og skjærer derfor linjen.")
# Utregnes med newton-raphson
print("Til nærmingen for [-5,-1]", round(tilnarming(-4),6))
print("Til nærmingen for [-1,1]", round(tilnarming(0),6))
print("Til nærmingen for [1,2]", round(tilnarming(1.5),6))

"""
Slutt skjæringsetningen
"""