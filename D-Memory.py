import random


class MemoryGame:
    def __init__(self, fil: str, storlek: int = 6):
        self.fil = fil
        self.storlek = storlek
        self.matris = []
        self.synlig = []
        self.hittade_par = 0
        self.totala_par = (storlek * storlek) // 2

    def läs_ord(self):
        """Läser in ord från filen och hanterar filrelaterade fel."""
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

    def skapa_matris(self, ordlista):
        """Skapar en slumpmässigt blandad matris med dolda ord."""
        valda_ord = random.sample(ordlista, self.totala_par)
        alla_ord = valda_ord * 2
        random.shuffle(alla_ord)
        self.matris = [alla_ord[i:i + self.storlek] for i in range(0, len(alla_ord), self.storlek)]
        self.synlig = [[False] * self.storlek for _ in range(self.storlek)]

    def skriv_ut_matris(self):
        """Skriver ut spelmatrisen."""
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

    def kör(self):
        """Kör spelet."""
        ordlista = self.läs_ord()
        self.skapa_matris(ordlista)

        while self.hittade_par < self.totala_par:
            self.skriv_ut_matris()
            print()  # Lägg till en tom rad innan valprompterna

            # Första valet
            val1 = input("Välj första rutan (t.ex. A1): ").strip()
            while not self.validera_input(val1):
                val1 = input("Felaktig inmatning. Välj igen (t.ex. A1): ").strip()
            rad1, kol1 = ord(val1[0].upper()) - 65, int(val1[1]) - 1

            print()  # Lägg till en tom rad innan matrisen skrivs ut
            self.synlig[rad1][kol1] = True
            self.skriv_ut_matris()
            print()  # Lägg till en tom rad innan nästa valpromp

            # Andra valet
            val2 = input("Välj andra rutan (t.ex. F6): ").strip()
            while not self.validera_input(val2) or val2 == val1:
                val2 = input("Felaktig inmatning. Välj igen (t.ex. F6): ").strip()
            rad2, kol2 = ord(val2[0].upper()) - 65, int(val2[1]) - 1

            print()  # Lägg till en tom rad innan matrisen skrivs ut
            self.synlig[rad2][kol2] = True
            self.skriv_ut_matris()

            # Kontrollera om orden matchar
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

        print("Grattis! Du har matchat alla par!")


if __name__ == "__main__":
    spel = MemoryGame("memo.txt")
    spel.kör()
