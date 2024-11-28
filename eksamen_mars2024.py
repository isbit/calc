# lengde = float(input("Lengde: "))
# hoyde = float(input("Høyde: "))
# bredde = float(input("Bredde: "))

# volum = (1/3) * bredde * lengde * hoyde
# print(volum)

# antall_rom = int(input("Hvor mange rom?: "))
# sum_areal = float(0)

# for rom in range(antall_rom):
#     if rom != antall_rom:
#         print(f"Rom: {rom + 1}")
#         while True:
#             try:
#                 bredde = float(input("Bredde: "))
#                 lengde = float(input("Lengde: "))
#             except ValueError:
#                 print("Prøv på nytt")

#             except NameError:
#                 print("prøv på nytt")
				
			
#         areal = bredde * lengde
#         sum_areal += areal
#     else:
#         break

# print(sum_areal)

# liste = 

'''
Oppgave 5
'''
# import matplotlib.pyplot as plt

# y_liste = list()
# y_liste.append(1)
# y_liste.append(1)

# for i in range(2, 10):
#     y_liste.append(y_liste[i-1] + y_liste[i-2])
# x_liste = [i+1 for i in range(len(y_liste))]

# print(len(y_liste))
# print(x_liste)

# plt.plot(x_liste, y_liste, "o-", label="Fibonaccirekkens 10 først tall")
# plt.xlabel("n'te fibonacchitall")
# plt.ylabel("Fibonacchi tallet")
# plt.title("Da er det i gang")
# plt.show()

'''
Oppgave 7

'''

# def lovlig_spenn(tall):
#     if -100 <= tall <= 100:
#         return True
#     else:
#         return False

# for i in range(-105, 106):
#     print(f"{i} - {lovlig_spenn(i)}")

# temperatur = int(input("Sett inn en temperatur i heltall: "))
# sjekk_av_temperatur = lovlig_spenn(temperatur)
# if sjekk_av_temperatur == True:
#     print(temperatur)
# else:
#     print("Det er for kaldt/varmt")

# liste = [1, 3, 2, 3, 5, 3, 1, 1, 5, 4, 6, 4, 3, 2]

# def topper(en_liste):
#     topper_i_liste = list()
#     for index in range(2, len(en_liste)-2):
#         if en_liste[index-2] < en_liste[index] and en_liste[index+2] < en_liste[index] and en_liste[index-1] < en_liste[index] and en_liste[index+1] < en_liste[index]:
#             topper_i_liste.append(en_liste[index])
#     return topper_i_liste

# toppene = topper(liste)
# for i in toppene:
#     print(i)

'''
7d
'''

# lista = [23, 25, 22, 29, 34, 32, 175, 26, 15, 12, 10, 12, 15, 13, -123, 14, 17, 16, 11]

# if __name__ == "__main__":
#     lovlige_tall_i_lista = []
#     for tall in lista:
#         if lovlig_spenn(tall) == True:
#             lovlige_tall_i_lista.append(tall)

#     print(lovlige_tall_i_lista)

'''
Oppgave 8
'''


# verdiene_aa_skrive_til_fila = [354, 664, 664.6, 656, 78.64, 894, 41, 789]
# verdiene_i_fila = []
# vekslet_verdi = []

# while True:
#     navn_fil1 = str(input("Hva er navn fil 1? "))
#     try:
#         with open(navn_fil1, "r", encoding="UTF8"):
#             break
#     except FileNotFoundError:
#         print("Filen ikke funnet")

# navn_fil2 = str(input("Hva er navn fil 2? "))
# valuta_type1 = str(input("Sett in første valuta "))
# valuta_type2 = str(input("Sett in andre valuta "))
# kursen = float(input("Hva er kursen: "))


# with open(navn_fil1, "w", encoding="UTF8") as fila:##########
#     fila.write(valuta_type1 + "\n") ######
#     for verdi in verdiene_aa_skrive_til_fila:
#         write_verdi = str(verdi)
#         fila.write(write_verdi + "\n")

# while True:
#     try:
#         with open(navn_fil1, "r", encoding= "UTF8") as fil1:
#             for verdi in fil1:
#                 verdiene_i_fila.append(verdi.strip())
#         break
#     except ValueError:
#         print("Value error")
#     except FileNotFoundError:
#         print("File not found")


# for verdi in verdiene_i_fila[1 : len(verdiene_i_fila)]:
#     omgjort = float(verdi) * kursen ##############
#     vekslet_verdi.append(omgjort)


# with open(navn_fil2, "w", encoding="UTF8") as fil2: #######
#     fil2.write(valuta_type2 + "\n") ########
#     for verdi in vekslet_verdi:
#         avrundet_verdi = (round(verdi, 2))
#         fil2.write(str(avrundet_verdi) + "\n")

# with open(navn_fil2, "r") as fil2:
#     for verdiene in fil2:
#         print(verdiene.strip())


'''
Oppgave 9
'''
from math import sqrt

class Punkt:
	
	def __init__(self, x_koordinat, y_koordinat):
		self.x_koordinat = x_koordinat
		self.y_koordinat = y_koordinat

	def avstand(self, annet_punkt) -> float:
		avstand = ((self.x_koordinat - annet_punkt.x_koordinat)**2 +
		(self.y_koordinat - annet_punkt.y_koordinat)**2)**0.5
		return avstand

	def __str__(self) -> str:
		return f"({self.x_koordinat}, {self.y_koordinat})"


class Linje:

	def __init__(self, startpunkt, sluttpunkt):
		self.punktliste = list()
		self.punktliste.append(startpunkt)
		self.punktliste.append(sluttpunkt)

	def legg_til_punkt(self, punkt):
		self.punktliste.append(punkt)

	def __str__(self):
		punkter = "Linje med koordinatene: "
		for punkt in self.punktliste:
			punkter += str(punkt) + ", "
		punkter = punkter[0: len(punkter)-2]
		return punkter
	
	def Lengde(self) -> float:
		resultat = 0.0
		if len(self.punktliste) < 2:
			return 0.0
		forrige_punkt = self.punktliste[0]
		for i in range(1, len(self.punktliste)):
			nytt_punkt = self.punktliste[i]
			resultat += forrige_punkt.avstand(nytt_punkt)
			forrige_punkt = nytt_punkt
		return resultat

class Tre_d_vector:
	
	def __init__(self, x_koordinat, y_koordinat, z_koordinat) -> float:
		self.x_koordinat = x_koordinat
		self.y_koordinat = y_koordinat
		self.z_koordinat = z_koordinat

	def __str__(self) -> str:
		return f'({self.x_koordinat}, {self.y_koordinat}, {self.z_koordinat})'
	
	def tre_d_lengde(self) -> float:
		lengde = sqrt((self.x_koordinat)**2 + (self.y_koordinat)**2 + (self.z_koordinat)**2)
		return lengde

def legge_sammen_to_vektorer(vektor1: Tre_d_vector, vektor2: Tre_d_vector):
	x_sum = vektor1.x_koordinat + vektor2.x_koordinat
	y_sum = vektor1.y_koordinat + vektor2.y_koordinat
	z_sum = vektor1.z_koordinat + vektor2.z_koordinat
	return x_sum, y_sum, z_sum

if __name__ == "__main__":
	punkt1 = Punkt(1, 2)
	punkt2 = Punkt(1, 6)
	print(punkt1.avstand(punkt2))
	linje = Linje(punkt1, punkt2)
	punkt3 = Punkt(8, 6)
	punkt4 = Punkt(1, 2)
	linje.legg_til_punkt(punkt3)
	linje.legg_til_punkt(punkt4)
	print(linje)
	lengde_flere_punkter = linje.Lengde()
	print(lengde_flere_punkter)


	vektor1 = Tre_d_vector(3,2,1)
	vektor2 = Tre_d_vector(3,7,4)
	to_vektorer = legge_sammen_to_vektorer(vektor1, vektor2)
	print(to_vektorer)