#Dags och skapa spelet Memory som min p_uppgift

import random
import tkinter as tk
import os

# Ladda ord från filen och välj slumpmässigt ett visst antal ord
def load_words(filename="memo.txt", word_count=18):
    with open(filename, 'r') as file:
        words = [line.strip() for line in file.readlines()]
    selected_words = random.sample(words, word_count)
    words_to_place = selected_words * 2
    random.shuffle(words_to_place)
    return words_to_place

# Skapa matrisen med ord
def create_board(words, size=6):
    board = []
    idx = 0
    for row in range(size):
        board.append(words[idx:idx + size])
        idx += size
    return board

# Skapa en matris för att hålla koll på avslöjade celler.
def create_hidden_board(size=6, max_word_len=3):
    return [['_' * max_word_len for _ in range(size)] for _ in range(size)]

# Skriv ut brädet
def print_board(board):
    for row in board:
        print(" ".join(row))
    print("\n")

# Kontrollera om spelet är över
def is_game_won(hidden_board):
    for row in hidden_board:
        if '_' in ''.join(row):  # Kontrollera om några ord är dolda
            return False
    return True

# Uppdatera och spara highscore-listan i en fil
def update_highscore(attempts, size, filename="highscores.txt"):
    highscores = []

    # Läs existerande highscore från fil
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                entry = line.strip().split(",")
                highscores.append((int(entry[0]), int(entry[1])))

    # Lägg till den nuvarande poängen
    highscores.append((attempts, size))
    highscores.sort(key=lambda x: (x[0], x[1]))  # Sortera efter försök och storlek

    # Spara de fem bästa resultaten
    with open(filename, 'w') as file:
        for score in highscores[:5]:
            file.write(f"{score[0]},{score[1]}\n")
    
    # Visa highscore
    print("\nHighscore-lista:")
    for idx, (attempt, size) in enumerate(highscores[:5], start=1):
        print(f"{idx}. Försök: {attempt}, Storlek: {size}")

# Funktion för att hantera spelet i textläge
def play_memory_game():
    size = 6
    words = load_words(word_count=18)
    max_word_len = max(len(word) for word in words)
    board = create_board(words, size)
    hidden_board = create_hidden_board(size, max_word_len)
    attempts = 0

    while not is_game_won(hidden_board):
        print_board(hidden_board)
        try:
            r1, c1 = map(int, input("Välj första cell (rad kolumn): ").split())
            r2, c2 = map(int, input("Välj andra cell (rad kolumn): ").split())
            attempts += 1

            if (r1, c1) == (r2, c2):
                print("Du valde samma cell två gånger. Försök igen!")
                continue
            
            hidden_board[r1][c1] = board[r1][c1]
            hidden_board[r2][c2] = board[r2][c2]
            print_board(hidden_board)
            
            if board[r1][c1] == board[r2][c2]:
                print("Matchning!")
            else:
                print("Ingen matchning.")
                hidden_board[r1][c1] = '_' * max_word_len
                hidden_board[r2][c2] = '_' * max_word_len
        except (ValueError, IndexError):
            print("Ogiltig inmatning. Ange rad och kolumn mellan 0 och 5.")

    print(f"Grattis! Du har matchat alla ord på {attempts} försök.")
    update_highscore(attempts, size)

# Grafisk version med tkinter
class MemoryGameGUI:
    def __init__(self, root, size=6):
        self.root = root
        self.size = size
        self.attempts = 0
        self.first_click = None
        self.words = load_words(word_count=(size * size) // 2)
        self.board = create_board(self.words, size)
        self.hidden_board = create_hidden_board(size, max(len(word) for word in self.words))
        self.buttons = [[None for _ in range(size)] for _ in range(size)]
        self.create_widgets()

    def create_widgets(self):
        for r in range(self.size):
            for c in range(self.size):
                btn = tk.Button(self.root, text=self.hidden_board[r][c], width=10, height=3,
                                command=lambda r=r, c=c: self.cell_click(r, c))
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn

    def cell_click(self, r, c):
        if self.hidden_board[r][c] != '_' * len(self.board[r][c]):  # Om cellen redan är synlig
            return

        self.hidden_board[r][c] = self.board[r][c]
        self.buttons[r][c].config(text=self.board[r][c])

        if self.first_click is None:
            self.first_click = (r, c)
        else:
            r1, c1 = self.first_click
            self.attempts += 1
            if self.board[r1][c1] == self.board[r][c]:  # Om matchning
                self.first_click = None
            else:
                self.root.after(1000, self.hide_cells, r1, c1, r, c)  # Göm om ej match
                self.first_click = None

        if is_game_won(self.hidden_board):
            self.show_winner()

    def hide_cells(self, r1, c1, r2, c2):
        self.hidden_board[r1][c1] = '_' * len(self.board[r1][c1])
        self.hidden_board[r2][c2] = '_' * len(self.board[r2][c2])
        self.buttons[r1][c1].config(text=self.hidden_board[r1][c1])
        self.buttons[r2][c2].config(text=self.hidden_board[r2][c2])

    def show_winner(self):
        print(f"Grattis! Du vann spelet på {self.attempts} försök.")
        update_highscore(self.attempts, self.size)
        self.root.quit()

if __name__ == "__main__":
    mode = input("Välj läge: 1 för textläge, 2 för grafiskt läge: ")
    if mode == "1":
        play_memory_game()
    elif mode == "2":
        root = tk.Tk()
        root.title("Memory Game")
        game = MemoryGameGUI(root)
        root.mainloop()