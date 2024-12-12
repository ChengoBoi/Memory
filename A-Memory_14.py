import tkinter as tk
from tkinter import messagebox, ttk
import random
import os

#Klass som innehåller alla funktioner för Memory-spelet. Inklusive logik, gränssnitt och highscore-hantering.
class MemoryGame:

    #Initierar spelet genom att sätta upp nödvändiga variabler och visa startlayouten.
    def __init__(self, root, ord_fil="memo.txt", highscore_fil="highscore.txt"):
        self.root = root
        self.ord_fil = ord_fil #Fil för ordlistan
        self.highscore_fil = highscore_fil #Fil för highscores
        self.namn = ""  #Spelarens namn
        self.matris = []  #Spelbrädsmatrisen 
        self.synlig = []  #Spårar vilka rutor som är synliga
        self.knappar = []  #Knappar för spelmatrisen
        self.försök = 0  #Räknar antal försök spelaren kör
        self.hittade_par = 0  #Antal matchade par
        self.storlek = (0, 0)  #Storlek på spelmatrisen (rader, kolumner)
        self.totala_par = 0  #Totala antalet par i spelet
        self.vald_första = None  #Koordinater för första valda rutan
        self.låst = False  #För att förhindra snabba klick
        self.startlayout()  #Visa startlayouten

    #Visar startlayouten där spelaren kan ange sitt namn och välja storlek på spelbrädet.
    def startlayout(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="🎮Välkommen till spelet Memory!🎮", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Ange ditt namn:").pack()
        namn_entry = tk.Entry(self.root)
        namn_entry.pack(pady=5)
            
        tk.Label(self.root, text="Välj storlek (t.ex. 4x3):").pack()
        storlek_entry = tk.Entry(self.root)
        storlek_entry.pack(pady=5)

        def starta_spel():
            namn = namn_entry.get().strip()
            if not namn:
                messagebox.showerror("Fel", "Du måste ange ett namn!")
                return

            storlek_text = storlek_entry.get().strip()
            try:
                rader, kolumner = map(int, storlek_text.split("x"))
                if rader * kolumner % 2 != 0:
                    raise ValueError("Matrisstorleken måste vara jämn!")
                if rader * kolumner > self.läs_max_ord():
                    raise ValueError("Matrisstorleken kräver fler ord än vad som finns!")
            except Exception as e:
                messagebox.showerror("Fel", f"Ogiltig storlek: {e}")
                return

            self.namn = namn
            self.storlek = (rader, kolumner)
            self.totala_par = (rader * kolumner) // 2
            self.initiera_spel()

        start_knapp = tk.Button(self.root, text="Starta spelet", command=starta_spel)
        start_knapp.pack(pady=20)

        highscore_knapp = tk.Button(self.root, text="Visa Highscore", command=self.visa_highscore)
        highscore_knapp.pack(pady=5)

    #Läser in det maximala antalet ord från ordlistfilen.
    def läs_max_ord(self):
        try:
            with open(self.ord_fil, 'r', encoding='utf-8') as f:
                return len(f.readlines())
        except FileNotFoundError:
            messagebox.showerror("Fel", f"Filen '{self.ord_fil}' hittades inte.")
            self.root.quit()

    #Initierar spelet genom att läsa ordlistan, skapa spelmatrisen och bygga gränssnittet.
    def initiera_spel(self):
        ordlista = self.läs_ord()
        self.skapa_matris(ordlista)
        self.bygg_gränssnitt()

    def läs_ord(self):
        try:
            with open(self.ord_fil, 'r', encoding='utf-8') as f:
                ordlista = [rad.strip() for rad in f.readlines()]
            return random.sample(ordlista, self.totala_par) * 2
        except FileNotFoundError:
            messagebox.showerror("Fel", f"Filen '{self.ord_fil}' hittades inte.")
            self.root.quit()

    #Skapar en matris för spelet genom att slumpa och arrangera orden i rader och kolumner.
    def skapa_matris(self, ordlista):
        random.shuffle(ordlista)
        rader, kolumner = self.storlek
        self.matris = [ordlista[i * kolumner:(i + 1) * kolumner] for i in range(rader)]
        self.synlig = [[False] * kolumner for _ in range(rader)]

    #Bygger gränssnittet för spelet med knappar för varje cell.
    def bygg_gränssnitt(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.knappar = []
        rader, kolumner = self.storlek
        for rad in range(rader):
            rad_knappar = []
            for kol in range(kolumner):
                knapp = tk.Button(
                    self.root, text="---", width=10, height=3,
                    command=lambda r=rad, k=kol: self.valj_ruta(r, k)
                )
                knapp.grid(row=rad, column=kol)
                rad_knappar.append(knapp)
            self.knappar.append(rad_knappar)

    #Hanterar spelarens klick på en ruta, visar ordet och kontrollerar om det bildar ett par.
    def valj_ruta(self, rad, kol):
        if self.låst or self.synlig[rad][kol]:
            return

        self.synlig[rad][kol] = True
        self.knappar[rad][kol].config(text=self.matris[rad][kol])

        if not self.vald_första:
            self.vald_första = (rad, kol)
        else:
            self.låst = True
            self.root.after(1000, lambda: self.utvärdera_par(rad, kol))

    #Utvärderar om de två valda rutorna bildar ett par och hanterar resultatet
    def utvärdera_par(self, rad2, kol2):
        if not self.vald_första:
            return

        rad1, kol1 = self.vald_första

        if self.matris[rad1][kol1] == self.matris[rad2][kol2]:
            self.hittade_par += 1
            if self.hittade_par == self.totala_par:
                self.avsluta_spel()
        else:
            self.synlig[rad1][kol1] = False
            self.synlig[rad2][kol2] = False
            self.knappar[rad1][kol1].config(text="---")
            self.knappar[rad2][kol2].config(text="---")

        self.vald_första = None
        self.låst = False
        self.försök += 1

    def avsluta_spel(self):
        messagebox.showinfo("Grattis!", f"Du klarade spelet på {self.försök} försök!")
        self.spara_highscore()
        self.visa_highscore()
        self.root.destroy()
    
    #Sparar spelarens resultat i highscore-filen.
    def spara_highscore(self):
        rader, kolumner = self.storlek
        ny_post = f"{self.namn},{self.försök},{rader}x{kolumner}\n"

        if not os.path.exists(self.highscore_fil):
            with open(self.highscore_fil, 'w', encoding='utf-8') as f:
                f.write(ny_post)
        else:
            with open(self.highscore_fil, 'a', encoding='utf-8') as f:
                f.write(ny_post)

    #Visar highscore-listan i ett nytt fönster, sorterad efter antal drag och svårighetsgrad.
    def visa_highscore(self):
        if not self.highscore_fil:
            messagebox.showinfo("Highscore", "Ingen highscore hittades ännu!")
            return

        highscore_window = tk.Toplevel(self.root)
        highscore_window.title("Highscore")

        tree = ttk.Treeview(highscore_window, columns=("Namn", "Drag", "Storlek"), show="headings")
        tree.heading("Namn", text="Namn")
        tree.heading("Drag", text="Drag")
        tree.heading("Storlek", text="Storlek")

        with open(self.highscore_fil, 'r', encoding='utf-8') as f:
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

if __name__ == "__main__":
    rot = tk.Tk()
    rot.title("Memory-spel")
    spel = MemoryGame(rot)
    rot.mainloop()
