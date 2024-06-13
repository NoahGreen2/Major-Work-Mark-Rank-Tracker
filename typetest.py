from tkinter import *
import random
win = Tk()
win.title("Type Test")
win.geometry("200x200")
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
lbl = Label(win, text=random.choice(letters), font=("Arial", 20))
lbl.pack()
def check_key(event):
    if event.char.upper() == lbl.cget("text"):
        lbl.config(text=random.choice(letters))
win.bind("<Key>", check_key)
win.mainloop()