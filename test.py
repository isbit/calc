forste_tall = int(input("Tall 1: "))
            andre_tall = int(input("Tall 2: "))
            sannheten = True
            try:
                while sannheten:
                    valg = input("add, sub, multi, dele: ")
                    operasjoner =  {"add": kalkulator_objektet.add(forste_tall, andre_tall),
                    "sub": kalkulator_objektet.sub(forste_tall, andre_tall),
                    "multi" : kalkulator_objektet.multi(forste_tall, andre_tall),
                    "dele" : kalkulator_objektet.dele(forste_tall, andre_tall)}
            except: 