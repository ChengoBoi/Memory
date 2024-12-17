import random
import os

class MemoryGame:
    highscore_fil = "highscore.txt"

    def __init__(self):
        self.fil = "memo.txt"
        self.storlek = 6  # Standardstorlek
        self.matris = []
        self.synlig = []
        self.hittade_par = 0
        self.försök = 0
        self.totala_par = 0
        
    #Läser in ord från filen och hanterar filrelaterade fel.
    def läs_ord(self):
        try:
            with open(self.fil, 'r', encoding='utf-8') as f:
                ordlista = [rad.strip() for rad in f.readlines()]
            if len(ordlista) < self.totala_par:
                raise ValueError(f"Filen {self.fil} måste innehålla minst {self.totala_par} ord.")
            return ordlista
        except FileNotFoundError:
            print(f"Fel: Filen '{self.fil}' hittades inte. Kontrollera att filen finns.")
            exit(1)
        except ValueError as e:
            print(f"Fel: {e}")
            exit(1)
        except Exception as e:
            print(f"Ett oväntat fel uppstod vid inläsning av filen: {e}")
            exit(1)

    #Skapar en slumpmässigt blandad matris med dolda ord.
    def skapa_matris(self, ordlista):
        valda_ord = random.sample(ordlista, self.totala_par)
        alla_ord = valda_ord * 2
        random.shuffle(alla_ord)
        self.matris = [alla_ord[i:i + self.storlek] for i in range(0, len(alla_ord), self.storlek)]
        self.synlig = [[False] * self.storlek for _ in range(self.storlek)]


    #Skriver ut spelmatrisen.
    def skriv_ut_matris(self):
        header = "   " + "   ".join(map(str, range(1, self.storlek + 1)))
        print(header)
        for rad_idx, rad in enumerate(self.matris):
            synliga_raden = [
                cell if self.synlig[rad_idx][col_idx] else "---"
                for col_idx, cell in enumerate(rad)
            ]
            print(chr(65 + rad_idx), " ".join(f"{c:>3}" for c in synliga_raden))
        print("=" * 30)

    def validera_input(self, val):
        """Validerar användarens input."""
        if len(val) != 2 or not val[0].isalpha() or not val[1].isdigit():
            return False
        rad, kol = val[0].upper(), val[1]
        if not ('A' <= rad < chr(65 + self.storlek)) or not (1 <= int(kol) <= self.storlek):
            return False
        return True

    def välj_svårighetsgrad(self):
        """Låter spelaren välja storleken på matrisen."""
        while True:
            try:
                print("Välj svårighetsgrad:")
                print("2x2 (lätt) upp till 10x10 (svårt)")
                val = int(input("Ange matrisens storlek (t.ex. 2 för 2x2): ").strip())
                if 2 <= val <= 10:
                    self.storlek = val
                    self.totala_par = (val * val) // 2
                    break
                else:
                    print("Felaktig inmatning. Ange en storlek mellan 2 och 10.")
            except ValueError:
                print("Felaktig inmatning. Ange en siffra mellan 2 och 10.")

    def spara_highscore(self, namn):
        """Sparar spelarens resultat i highscore-filen."""
        data = self.läs_highscore()
        if self.storlek not in data:
            data[self.storlek] = []

        # Lägg till spelarens resultat
        data[self.storlek].append(f"{namn},{self.försök}")

        # Sortera highscore för denna storlek baserat på antal försök
        data[self.storlek] = sorted(data[self.storlek], key=lambda x: int(x.split(',')[1]))[:10]

        with open(self.highscore_fil, "w", encoding="utf-8") as f:
            for storlek, poster in data.items():
                for post in poster:
                    f.write(f"{storlek},{post}\n")

    def läs_highscore(self):
        """Läser in highscore-data från filen."""
        if not os.path.exists(self.highscore_fil):
            return {}
        data = {}
        with open(self.highscore_fil, "r", encoding="utf-8") as f:
            for rad in f:
                storlek, post = rad.strip().split(',', 1)
                storlek = int(storlek)
                if storlek not in data:
                    data[storlek] = []
                data[storlek].append(post)
        return data

    def visa_highscore(self):
        """Visar highscore-listan."""
        data = self.läs_highscore()
        print("\nTopplistor:")
        for storlek, lista in data.items():
            print(f"\nHighscore för {storlek}x{storlek}:")
            for idx, entry in enumerate(lista, start=1):
                namn, försök = entry.split(',')
                print(f"{idx}. {namn} - {försök} försök")

    def spela(self):
        """Huvudfunktion för att spela spelet."""
        self.välj_svårighetsgrad()
        namn = input("Ange ditt namn: ").strip()
        ordlista = self.läs_ord()
        self.skapa_matris(ordlista)

        while self.hittade_par < self.totala_par:
            self.skriv_ut_matris()
            print()

            # Första valet
            val1 = input("Välj första rutan (t.ex. A1): ").strip()
            while not self.validera_input(val1):
                val1 = input("Felaktig inmatning. Välj igen (t.ex. A1): ").strip()
            rad1, kol1 = ord(val1[0].upper()) - 65, int(val1[1]) - 1
            self.synlig[rad1][kol1] = True
            self.skriv_ut_matris()
            print()

            # Andra valet
            val2 = input("Välj andra rutan (t.ex. F6): ").strip()
            while not self.validera_input(val2) or val2 == val1:
                val2 = input("Felaktig inmatning. Välj igen (t.ex. F6): ").strip()
            rad2, kol2 = ord(val2[0].upper()) - 65, int(val2[1]) - 1
            self.synlig[rad2][kol2] = True
            self.skriv_ut_matris()

            # Kontrollera om orden matchar
            if self.matris[rad1][kol1] == self.matris[rad2][kol2]:
                print("Grattis! Du hittade ett par.\n")
                self.hittade_par += 1
            else:
                print("Tyvärr, ingen match.\n")
                self.synlig[rad1][kol1] = False
                self.synlig[rad2][kol2] = False

            self.försök += 1

        print(f"Grattis! Du har matchat alla par på {self.försök} försök!")
        self.spara_highscore(namn)
        self.visa_highscore()

    def huvudmeny(self):
        """Visar huvudmenyn och hanterar användarens val."""
        while True:
            print("\nVälkommen till Memory Game!")
            print("1. Spela Memory Game")
            print("2. Visa topplistor")
            print("3. Avsluta")
            val = input("Välj ett alternativ (1-3): ").strip()

            if val == "1":
                self.spela()
            elif val == "2":
                self.visa_highscore()
            elif val == "3":
                print("Hej då!")
                break
            else:
                print("Felaktigt val. Försök igen.")

if __name__ == "__main__":
    spel = MemoryGame()
    spel.huvudmeny()
