import random

# Funktion för att läsa in ord från filen
def läs_ord(fil):
    with open(fil, 'r', encoding='utf-8') as f:  # Lägg till encoding='utf-8'
        return [rad.strip() for rad in f.readlines()]

# Funktion för att skapa en slumpmässig matris
def skapa_matris(ordlista, storlek):
    valda_ord = random.sample(ordlista, storlek * storlek // 2)
    alla_ord = valda_ord * 2
    random.shuffle(alla_ord)
    return [alla_ord[i:i + storlek] for i in range(0, len(alla_ord), storlek)]

# Funktion för att skriva ut matrisen
def skriv_ut_matris(matris, synlig):
    header = "   " + "   ".join(map(str, range(1, len(matris) + 1)))
    print(header)
    for rad_idx, rad in enumerate(matris):
        synliga_raden = [
            cell if synlig[rad_idx][col_idx] else "---"
            for col_idx, cell in enumerate(rad)
        ]
        print(chr(65 + rad_idx), " ".join(f"{c:>3}" for c in synliga_raden))
    print("=" * 30)

# Funktion för att validera användarens input
def validera_input(val, storlek):
    if len(val) != 2 or not val[0].isalpha() or not val[1].isdigit():
        return False
    rad, kol = val[0].upper(), val[1]
    if not ('A' <= rad < chr(65 + storlek)) or not (1 <= int(kol) <= storlek):
        return False
    return True

# Huvudprogrammet
def spela_memory():
    fil = "memo.txt"
    storlek = 6  # För en 6x6-matris
    ordlista = läs_ord(fil)
    
    matris = skapa_matris(ordlista, storlek)
    synlig = [[False] * storlek for _ in range(storlek)]
    hittade_par = 0
    totala_par = storlek * storlek // 2

    while hittade_par < totala_par:
        skriv_ut_matris(matris, synlig)
        print()  # Lägg till en tom rad innan valprompterna

        # Första valet
        val1 = input("Välj första rutan (t.ex. A1): ").strip()
        while not validera_input(val1, storlek):
            val1 = input("Felaktig inmatning. Välj igen (t.ex. A1): ").strip()
        rad1, kol1 = ord(val1[0].upper()) - 65, int(val1[1]) - 1

        print()  # Lägg till en tom rad innan matrisen skrivs ut
        synlig[rad1][kol1] = True
        skriv_ut_matris(matris, synlig)
        print()  # Lägg till en tom rad innan nästa valpromp

        # Andra valet
        val2 = input("Välj andra rutan (t.ex. F6): ").strip()
        while not validera_input(val2, storlek) or val2 == val1:
            val2 = input("Felaktig inmatning. Välj igen (t.ex. F6): ").strip()
        rad2, kol2 = ord(val2[0].upper()) - 65, int(val2[1]) - 1

        print()  # Lägg till en tom rad innan matrisen skrivs ut
        synlig[rad2][kol2] = True
        skriv_ut_matris(matris, synlig)

        # Kontrollera om orden matchar
        if matris[rad1][kol1] == matris[rad2][kol2]:
            print("Grattis! Du hittade ett par.")
            hittade_par += 1
        else:
            print()  # Lägg till en tom rad innan feedback
            print("Tyvärr, ingen match.")
            synlig[rad1][kol1] = False
            synlig[rad2][kol2] = False
        
        # Lämna mellanrum och vänta på användaren
        print("\n" + "-" * 30)
        input("Tryck på Enter för att fortsätta...")
        print("\n" * 3)  # Lägg till mellanrum för tydligare separation

    print("Grattis! Du har matchat alla par!")

if __name__ == "__main__":
    spela_memory()
