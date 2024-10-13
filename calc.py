#Todo quadruple. Handtere at brukere gir bokstaver i stedet for tall som input. Det gir feil nå. 

# avslutt = "Slutt"
# while avslutt !="Slutt":
def add(x,y):
    return x+y

sum = add(10,5)
print(sum)

def sub(x,y):
    return x-y

sum = sub(10,5)
print(sum)

def multi(a, b):
    return a*b

summulti = multi(6, 5)
print(summulti)

def dele(c, d):
    return c/d

sumdele = dele(6, 2)
print(sumdele)

def double(x):
    return x*2

sumdouble = double(6)
print(sumdouble)

def triple(x):
    return x*3

sumtriple = triple(6)
print(sumtriple)


def nterot(x, n):
    return x**n
nterot_resultat = nterot(int(input("Sett inn tallet du vil exponere: ")), 
int(input("Sett inn eksponenten: ")))
print(nterot_resultat)

def findBiggest(x,y):
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
    menuchoice = int(input("Valg:"))
    match menuchoice:
        case 0:
            avslutt = True
            print("Avslutter")
        case _:
            print("Feil valg")

"""
Denne delen er skjæringssetningen
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

# Prøver de 3 intervallene
# [-5,-1]
print(f"Intervall: [-5,-1]  [{f(-5)}, {f(-1)}]")
print("Skærer linjen y = 0")
# [-1,1]
print(f"Intervall: [-1,1]  [{f(-1)}, {f(1)}]")
print("Skærer linjen y = 0")
# [1,2]
print(f"Intervall: [1,2]  [{f(1)}, {f(2)}]")
print("Skærer linjen y = 0\nAlle ytterpunktene av intervallene er på hver side av linjen y = 0 og skjærer derfor linjen.")
print("Til nærmingen for [-5,-1]", round(tilnarming(-4),6))
print("Til nærmingen for [-1,1]", round(tilnarming(0),6))
print("Til nærmingen for [1,2]", round(tilnarming(1.5),6))

"""
Slutt skjæringsetningen
"""