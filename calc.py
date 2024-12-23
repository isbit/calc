'''
Too do:

-- Handtere at brukere gir bokstaver i stedet for tall som input. Det gir feil nå. 
-- 2. gradslikning ABC.
-- En funksjon som finer h**2 = k*2 + k**2 ved hjelp av sin(theta), cos(theta) og tan(theta).
'''


class Kalkulator:

    def __init__(self) -> None:
        pass

    def fibonacci(self, n):
        resultat = []
        resultat.append(0)
        resultat.append(1)
        for i in range(1 ,n-1):
            tall = resultat[i] + resultat[i-1]
            resultat.append(tall)
        return resultat, resultat[n-1]

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

kalkulator_objektet = Kalkulator()
sum = kalkulator_objektet.add(9,4)
print(sum)

# This is the menu. 
avslutt = False
while(not avslutt):
    print("---=== Meny ===---")
    print("0: Avslutt")
    print("1: Addere, Substrahere, Multiplisere, Dele")
    print("2: Eksponent  n^x ")
    print("3: Fibonacchi verdi og rekke")
    menuchoice = int(input("Valg:"))
    match menuchoice:
        case 0:
            avslutt = True
            print("Avslutter")
        case 1:
            forste_tall = int(input("Tall 1: "))
            andre_tall = int(input("Tall 2: "))
            valg = input("add, sub, multi, dele: ")
            operasjoner =  {"add": kalkulator_objektet.add(forste_tall, andre_tall),
            "sub": kalkulator_objektet.sub(forste_tall, andre_tall),
            "multi" : kalkulator_objektet.multi(forste_tall, andre_tall),
            "dele" : kalkulator_objektet.dele(forste_tall, andre_tall)}
            if valg in operasjoner:
                operasjon = operasjoner[valg]
                print(f"\nSvar:\n{operasjon}\n")
            else:
                print("Ikke riktig input")
        case 2:
            forste_tall = int(input("Tall 1: "))
            andre_tall = int(input("Tall 2: "))
            resultat = kalkulator_objektet.nterot(forste_tall, andre_tall)
            print(f"\nSvar:\n{resultat}\n")
        case 3:
            antall = int(input("Sett inn antall du ønsker: "))
            resultat_listen = kalkulator_objektet.fibonacci(antall)
                
            if antall < 1:
                print("DUST\n"*100)
            elif antall == 1:
                print("0")
            elif antall > 10000:
                print("Maks nummer er 10 000")
            else:
                print(f"\nHele rekken: \n{resultat_listen[0]}")
                print(f"\nDet {antall}. fibonaccitallet \n{resultat_listen[1]}")
        case _:
            print("Feil valg")

"""
Denne delen er skjæringssetningen og Newton-Raphson tilnærmingsmetode 
den finner ut om det krysser en linje y = 0 i dette tilfellet og må
omskrives til en generell version
"""
'''
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
'''

"""
Slutt skjæringsetningen
"""