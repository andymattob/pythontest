import tkinter as tk
import subprocess
import os

def starta_spel(sokvag):
    try:
        # Startar processen i bakgrunden
        subprocess.Popen(sokvag)
    except Exception as e:
        print(f"Kunde inte starta spelet: {e}")

# Skapa huvudfönstret
root = tk.Tk()
root.title("Min Gaming Launcher")
root.geometry("400x300")

# Lista på dina spel (Namn, Sökväg till .exe)
spel_lista = [
    ("Age Of Empires  1", "C:/games/aoe/empires.exe"),
    ("Age Of Empires  1: The Rise OF Rome", "C:/games/aoe/empiresx.exe"),
    ("Age Of Empires  2", "C:/games/aoe2/empires2.exe"),
    ("Backpacker 3", "C:/games/bp3/bp3.exe")
]

tk.Label(root, text="Välj ett spel att starta", font=("Arial", 16)).pack(pady=20)

# Skapa en knapp för varje spel
for namn, path in spel_lista:
    btn = tk.Button(root, text=namn, width=20, command=lambda p=path: starta_spel(p))
    btn.pack(pady=5)

root.mainloop()