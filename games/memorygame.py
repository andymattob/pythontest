import random
import tkinter as tk
from tkinter import Toplevel, Label, Frame
from PIL import Image, ImageTk
import sys, os

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Game")
        self.size = 4  # 4x4
        self.buttons = []
        self.images = []
        self.cover_image = None
        self.first_choice = None
        self.second_choice = None
        self.matches = 0
        self.pulse_states = {}

        # -----------------------------
        # Fönsterikon
        # -----------------------------
        icon_path = "memimg/icon.png"  # byt till din ikon
        icon_img = Image.open(icon_path)
        self.icon_photo = ImageTk.PhotoImage(icon_img)
        self.root.iconphoto(True, self.icon_photo)

        self.load_images()
        self.create_board()

    # -----------------------------------------
    # Säker resize-funktion
    # -----------------------------------------
    def safe_resize(self, image_path, size=(120, 120)):
        img = Image.open(image_path)
        try:
            resample_method = Image.LANCZOS # type: ignore
        except AttributeError:
            resample_method = Image.BICUBIC # type: ignore
        return ImageTk.PhotoImage(img.resize(size, resample=resample_method))

    # -----------------------------------------
    # Ladda bilder
    # -----------------------------------------
    def load_images(self):
        self.images = []
        for i in range(1, 9):  # img-1.png - img-8.png
            img_path = f"memimg/img-{i}.png"
            resized_img = self.safe_resize(img_path)
            self.images.append(resized_img)
            self.images.append(resized_img)

        self.cover_image = self.safe_resize("memimg/back.png")
        random.shuffle(self.images)

    # -----------------------------------------
    # Skapa spelplan
    # -----------------------------------------
    def create_board(self):
        for r in range(self.size):
            row = []
            for c in range(self.size):
                index = r * self.size + c

                frame = Frame(self.root, highlightthickness=4, highlightbackground="black")
                frame.grid(row=r, column=c, padx=2, pady=2)

                btn = tk.Button(
                    frame,
                    image=self.cover_image, # type: ignore
                    command=lambda idx=index: self.reveal(idx),
                    relief="flat"
                )
                btn.grid(row=0, column=0)

                row.append(frame)
            self.buttons.append(row)

    # -----------------------------------------
    # Klicka kort
    # -----------------------------------------
    def reveal(self, index):
        r, c = divmod(index, self.size)
        frame = self.buttons[r][c]
        button = frame.winfo_children()[0]

        if button["state"] == "disabled" or self.second_choice is not None:
            return

        button.config(image=self.images[index])

        if self.first_choice is None:
            self.first_choice = index
        elif self.second_choice is None:
            self.second_choice = index
            self.root.after(500, self.check_match)

    # -----------------------------------------
    # Kontrollera match
    # -----------------------------------------
    def check_match(self):
        r1, c1 = divmod(self.first_choice, self.size) # type: ignore
        r2, c2 = divmod(self.second_choice, self.size) # type: ignore

        btn1 = self.buttons[r1][c1].winfo_children()[0]
        btn2 = self.buttons[r2][c2].winfo_children()[0]

        if self.images[self.first_choice] == self.images[self.second_choice]: # type: ignore
            # MATCH – färgglad ram
            self.start_pulse(self.buttons[r1][c1])
            self.start_pulse(self.buttons[r2][c2])

            btn1.config(state="disabled")
            btn2.config(state="disabled")

            self.matches += 1
            if self.matches == 8:
                self.show_win_screen()
        else:
            btn1.config(image=self.cover_image)
            btn2.config(image=self.cover_image)

        self.first_choice = None
        self.second_choice = None

    # -----------------------------------------
    # Pulserande ram på match
    # -----------------------------------------
    def start_pulse(self, frame):
        self.pulse_states[frame] = True
        self.pulse(frame, True)

    def pulse(self, frame, state):
        if frame not in self.pulse_states:
            return

        frame.config(highlightbackground="lime" if state else "green")
        self.root.after(200, lambda: self.pulse(frame, not state))

    # -----------------------------------------
    # You Win-skärm
    # -----------------------------------------
    def show_win_screen(self):
        win = Toplevel(self.root)
        win.title("Du Vann!")
        win.geometry("600x400")
        win.resizable(False, False)

        bg_photo = self.safe_resize("memimg/you_win.jpg", (600, 400))
        bg_label = Label(win, image=bg_photo)
        bg_label.image = bg_photo # type: ignore
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = Label(win, text="🎉 Du  Vann! 🎉", font=("Arial", 40, "bold"),
                     fg="yellow", bg="black")
        text.place(relx=0.5, rely=0.5, anchor="center")

        btn_close = tk.Button(win, text="Stäng Spelet", font=("Arial", 14),
                              command=self.root.destroy)
        btn_close.place(relx=0.5, rely=0.8, anchor="center")


# -----------------------------------------
# Starta spelet
# -----------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()


