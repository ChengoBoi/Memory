import random #Importerar biblioteket för att använda slumpmässiga funktioner


class MemoryGame: 
    def __init__(self, fil: str, storlek: int = 6):
        self.fil = fil 
        self.storlek = storlek
        self.matris = []
        self.synlig = []
        self.hittade_par = 0
        self.totala_par = (storlek * storlek) // 2

    def läs_ord(self):
        #Läser in ord från filen och hanterar filrelaterade fel
        try:
            #Läser alla rader i txt filen och ta bort eventuella mellanslag
            with open(self.fil, 'r', encoding='utf-8') as f:
                ordlista = [rad.strip() for rad in f.readlines()]

            #Kontrollera att filen innehåller minst antal ord som krävs
            if len(ordlista) < self.totala_par:
                raise ValueError(f"Filen {self.fil} måste innehålla minst {self.totala_par} ord.")
            return ordlista
        
        # Felmeddelande om filen inte hittade
        except FileNotFoundError: 
            print(f"Fel: Filen '{self.fil}' hittades inte. Kontrollera att filen finns.")
            exit(1)
        #Felmeddelande om filen inte har tillräckligt många ord
        except ValueError as e:
            print(f"Fel: {e}")
            exit(1)
     

    def skapa_matris(self, ordlista):
        #Skapar en slumpmässigt blandad matris med dolda ord
        valda_ord = random.sample(ordlista, self.totala_par)
        alla_ord = valda_ord * 2 #Duplicera orden för att skapa par
        random.shuffle(alla_ord) # Blanda orden slumpmässigt

        # Dela upp de blandade orden i en 2D-matris
        self.matris = [alla_ord[i:i + self.storlek] for i in range(0, len(alla_ord), self.storlek)]
        # Skapa en synlighetsmatris som börjar med att alla rutor är dolda
        self.synlig = [[False] * self.storlek for _ in range(self.storlek)]

    def skriv_ut_matris(self):
       #Skriver ut spelmatrisen, där endast --- visas innan spelaren har vänt på dem
        
        #Skriver ut antal kolumnrubriker
        header = "   " + "   ".join(map(str, range(1, self.storlek + 1)))
        print(header)

        #Skriver ut raderna i matrisen
        for rad_idx, rad in enumerate(self.matris):
            #Visa endast ord om rutan är synlig, annars "---"
            synliga_raden = [
                cell if self.synlig[rad_idx][col_idx] else "---"
                for col_idx, cell in enumerate(rad)
            ]
            print(chr(65 + rad_idx), " ".join(f"{c:>3}" for c in synliga_raden))
        print("=" * 30) #En visuell separator under matrisen

    def validera_input(self, val):
        #Validerar användarens input.
        #Kontrollera att inmatningen har exakt två tecken
        if len(val) != 2 or not val[0].isalpha() or not val[1].isdigit():
            return False
        
        rad, kol = val[0].upper(), val[1]
        #Kontrollera att inmatningen är inom matrisens gränser
        if not ('A' <= rad < chr(65 + self.storlek)) or not (1 <= int(kol) <= self.storlek):
            return False
        return True

    def kör(self):
        #spelar spelet
        print("\nVälkommen till spelet Memory!!, försök och matcha alla ord gömda bakom rutorna 🎉 \n ") 
        
        #Läser in orden från txt filen och skapa matrisen
        ordlista = self.läs_ord()
        self.skapa_matris(ordlista)

        #Huvudloop
        while self.hittade_par < self.totala_par:
            self.skriv_ut_matris()
            print()  #Lägger till en tom rad innan valprompterna

            #Första valet av spelaren 
            val1 = input("Välj första rutan (t.ex. A1): ").strip()
            while not self.validera_input(val1):
                val1 = input("Felaktig inmatning. Välj igen (t.ex. A1): ").strip()
            rad1, kol1 = ord(val1[0].upper()) - 65, int(val1[1]) - 1

            print()  #Lägg till en tom rad innan matrisen skrivs ut
            self.synlig[rad1][kol1] = True
            self.skriv_ut_matris()
            print()  #Lägg till en tom rad innan nästa valpromp

            #Andra valet från spelaren
            val2 = input("Välj andra rutan (t.ex. F6): ").strip()
            while not self.validera_input(val2) or val2 == val1:
                val2 = input("Felaktig inmatning. Välj igen (t.ex. F6): ").strip()
            rad2, kol2 = ord(val2[0].upper()) - 65, int(val2[1]) - 1

            print()  # Lägg till en tom rad innan matrisen skrivs ut
            self.synlig[rad2][kol2] = True
            self.skriv_ut_matris()

            # Kontrollera om orden matchar varandra
            if self.matris[rad1][kol1] == self.matris[rad2][kol2]:
                print("Grattis! Du hittade ett par.")
                self.hittade_par += 1
            else:
                print()  # Lägg till en tom rad innan feedback
                print("Tyvärr, ingen match.")
                self.synlig[rad1][kol1] = False
                self.synlig[rad2][kol2] = False

            # Lämna mellanrum och vänta på användaren
            print("\n" + "-" * 30)
            input("Tryck på Enter för att fortsätta...")
            print("\n" * 3)  # Lägg till mellanrum för tydligare separation

        print("Grattis! Du har matchat alla par av ord i spelbrädan!! 🎉")


if __name__ == "__main__":
    spel = MemoryGame("memo.txt")
    spel.kör()
