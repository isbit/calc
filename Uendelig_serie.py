'''
Lag en while løkke som er uendelig men som stopper ved en sum hvor tallet før = tallet nå (tilnærmet lik),
 når hver addering er så liten at hver addering i realiteten ikke legger til mere
'''

sum_liste = []
sum_liste.append(0)
sum_liste.append(10*((1/10)**1))

i = 1
while sum_liste[i] != sum_liste[i-1]:
    sum_liste.append(10*((1/10)**(i+1)))
    i = i + 1

print(sum_liste,'\nRunde = ', i, '\n', sum(sum_liste))
print(len(sum_liste))