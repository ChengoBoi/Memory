import tkinter as tk
from tkinter import messagebox, ttk
import random
import os

#Klass som innehåller alla funktioner för Memory-spelet. Inklusive logik, gränssnitt och highscore-hantering.
class MemoryGame:

    #Klassens konstruktör. Initierar spelet genom att sätta upp nödvändiga variabler och visa startlayouten.
    def __init__(self, fönster, ord_fil="memo.txt", highscore_fil="highscore.txt"): #Parameter. Tkinter-Widget. Referencer till objekt
        self.fönster = fönster #Huvudfönstret för spelet
        self.ord_fil = ord_fil  #Fil för ordlistan
        self.highscore_fil = highscore_fil  #Fil för highscores
        self.namn = ""  #Spelarens namn
        self.matris = []  #Spelbrädsmatrisen. Innehåller en lista av rader
        self.synlig = []  #Spårar vilka rutor som är synliga
        self.knappar = []  #Knappar för spelmatrisen
        self.försök = 0  #Räknar antal försök spelaren kör
        self.hittade_par = 0  #Antal matchade par
        self.storlek = (0, 0)  #Storlek på spelmatrisen (rader, kolumner)
        self.totala_par = 0  #Totala antalet par i spelet
        self.första_val = None  #Koordinater för första valda rutan
        self.låst = False  #För att förhindra snabba klick
        self.startlayout()  #Visa startlayouten

    #Visar startlayouten där spelaren kan ange sitt namn och välja storlek på spelbrädet.
    def startlayout(self):

        tk.Label(self.fönster, text="🎮Välkommen till spelet Memory!🎮", font=("Arial", 16)).pack(pady=15)
        tk.Label(self.fönster, text="Ange ditt namn:").pack()
        namn_entry = tk.Entry(self.fönster)
        namn_entry.pack(pady=5)

        tk.Label(self.fönster, text="Välj storlek (t.ex. 4x3):").pack()
        storlek_entry = tk.Entry(self.fönster)
        storlek_entry.pack(pady=5)

        #Felhantering vid inläsning av användarens data
        def starta_spel():
            namn = namn_entry.get().strip() #Tar bort oödiga mellanslag
            if not namn:
                messagebox.showerror("Error", "Du måste först ange ett namn!")
                return

            storlek_text = storlek_entry.get().strip()
            try:
                if "x" not in storlek_text:
                    raise ValueError("Storleken måste anges i formatet 3x4 eller 4x3")

                rader, kolumner = storlek_text.split("x")
                if not rader.isdigit() or not kolumner.isdigit():
                    raise ValueError("Både rader och kolumner måte vara heltal")
                
                rader, kolumner = int(rader), int(kolumner)

                if rader*kolumner %2 !=0:
                    raise ValueError("Matrisstolek måste vara jämn")
                
                if rader*kolumner //2 > self.läs_max_ord():
                    raise ValueError(f"Matrisstorleken kräver fler ord än vad som finns ({self.läs_max_ord()} par)!")
            except ValueError as e:
                messagebox.showerror("Error", f"Ogiltig storlek: {e}")
                return

            #Sparar värden i instansvariabler. Anropar. 
            self.namn = namn 
            self.storlek = (rader, kolumner)
            self.totala_par = (rader * kolumner) // 2
            self.initiera_spel()

        start_knapp = tk.Button(self.fönster, text="Starta spelet", command=starta_spel)
        start_knapp.pack(pady=15)

        highscore_knapp = tk.Button(self.fönster, text="Visa Highscore", command=self.visa_highscore_popup)
        highscore_knapp.pack(pady=20)

    #Läser in det maximala antalet ord från ordlistfilen.
    def läs_max_ord(self):
        try:
            with open(self.ord_fil, 'r') as f:
                return len(f.readlines()) #läser alla rader i filen och returnerar en lista där varje element är en rad i filen.
        except FileNotFoundError:
            messagebox.showerror("Fel", f"Filen '{self.ord_fil}' hittades inte.")
            self.fönster.quit() #Förhindra att spelet fortsätter utan ord.

    #Initierar spelet genom att läsa ordlistan, skapa spelmatrisen och bygga gränssnittet.
    def initiera_spel(self):
        ordlista = self.läs_ord()
        self.skapa_matris(ordlista)
        self.bygg_gränssnitt()

    #Läser antal rader i ordlistfilen
    def läs_ord(self):
        try:
            with open(self.ord_fil, 'r', encoding='utf-8') as f:
                ordlista = [rad.strip() for rad in f.readlines()]
            return random.sample(ordlista, self.totala_par) * 2
        except FileNotFoundError:
            messagebox.showerror("Fel", f"Filen '{self.ord_fil}' hittades inte.")
            self.fönster.quit()

    #Skapar en matris för spelet genom att slumpa och arrangera orden i rader och kolumner.
    def skapa_matris(self, ordlista):
        random.shuffle(ordlista)
        rader, kolumner = self.storlek #Hämtar antalet rader och kolumner från self.storlek.
        self.matris = [ordlista[i * kolumner:(i + 1) * kolumner] for i in range(rader)] #Hämtar listan som motsvarar en hel rad i spelbrädan.
        self.synlig = [[False] * kolumner for _ in range(rader)] #Inga rutor är synliga vid spelstart

    #Bygger gränssnittet för spelet med knappar för varje cell.
    def bygg_gränssnitt(self):
        for widget in self.fönster.winfo_children(): #Returnerar en lista över alla widgetar som redan finns i fönstret.
            widget.destroy()

        self.knappar = []
        rader, kolumner = self.storlek
        for rad in range(rader):
            rad_knappar = []
            for kol in range(kolumner):
                knapp = tk.Button(
                    self.fönster, text="---", width=10, height=3,
                    command=lambda r=rad, k=kol: self.vald_ruta(r, k) #Lambda används för att passera rad och kolumn till vald_ruta.
                )
                knapp.grid(row=rad, column=kol)
                rad_knappar.append(knapp)
            self.knappar.append(rad_knappar)

    #Hanterar spelarens klick på en ruta, visar ordet och kontrollerar om det bildar ett par.
    def vald_ruta(self, rad, kol):
        if self.låst or self.synlig[rad][kol]:
            return

        self.synlig[rad][kol] = True
        self.knappar[rad][kol].config(text=self.matris[rad][kol]) #Uppdaterar knappens text med det ord som finns i motsvarande position i matrisen.

        if not self.första_val:
            self.första_val = (rad, kol)
        else:
            self.låst = True
            self.fönster.after(1000, lambda: self.utvärdera_par(rad, kol))

    #Utvärderar om de två valda rutorna bildar ett par och hanterar resultatet
    def utvärdera_par(self, rad2, kol2):
        if not self.första_val:
            return

        rad1, kol1 = self.första_val #Hämtar koordinaterna från första valet

        if self.matris[rad1][kol1] == self.matris[rad2][kol2]:
            self.hittade_par += 1
            if self.hittade_par == self.totala_par:
                self.avsluta_spel()
        else: #Om de inte matchar vänder sig korten
            self.synlig[rad1][kol1] = False
            self.synlig[rad2][kol2] = False
            self.knappar[rad1][kol1].config(text="---")
            self.knappar[rad2][kol2].config(text="---")

        self.första_val = None
        self.låst = False
        self.försök += 1

    #Skriver grattis och sparar highscore
    def avsluta_spel(self):
        messagebox.showinfo("Grattis, du har klarat av spelet!", f"Du lyckades matcha alla ord på {self.försök+1} försök!")
        self.spara_highscore()
        self.visa_highscore_popup()

    #Sparar spelarens resultat i highscore-filen.
    def spara_highscore(self):
        rader, kolumner = self.storlek
        ny_rad = f"{self.namn},{self.försök+1},{rader}x{kolumner}\n"

        if not os.path.exists(self.highscore_fil):
            with open(self.highscore_fil, 'w') as f:
                f.write(ny_rad)
        else:
            with open(self.highscore_fil, 'a') as f:
                f.write(ny_rad)

    #Visar highscore-listan i ett nytt popup-fönster efter spelets slut.
    def visa_highscore_popup(self):
        popup = tk.Toplevel(self.fönster)
        popup.title("Highscore listan")

        tree = ttk.Treeview(popup, columns=("Namn", "Antal försök", "Storlek"), show="headings")
        tree.heading("Namn", text="Namn")
        tree.heading("Antal försök", text="Antal försök")
        tree.heading("Storlek", text="Storlek")

        with open(self.highscore_fil, 'r') as f:
            highscore_data = f.readlines()

        highscores = []
        for rad in highscore_data:
            namn, försök, storlek = rad.strip().split(",")
            rader, kolumner = map(int, storlek.split("x"))
            svårighet = rader * kolumner
            highscores.append((int(försök), svårighet, namn, storlek))

        highscores.sort()

        for försök, svårighet, namn, storlek in highscores:
            tree.insert("", "end", values=(namn, försök, storlek))

        tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        #Avslutar spelet
        def stäng_och_avsluta():
            popup.destroy()
            self.fönster.quit()

        close_btn = tk.Button(popup, text="Avsluta spelet", command=stäng_och_avsluta)
        close_btn.pack(pady=5)

#Skapar olika instanser av Tkinter
if __name__ == "__main__":
    huvud_fönster = tk.Tk() #Skapar huvudfönster för GUI 
    huvud_fönster.title("Memory-spel") #Sätter titeln på huvudfönstret till "Memory-spel".
    spel = MemoryGame(huvud_fönster)
    huvud_fönster.mainloop()
