from tkinter import *
import customtkinter as ctk
import pandas as pd

# Create main customtkinter window
win = ctk.CTk()
win.title("Main Menu")
win.geometry("500x500")

df = pd.read_csv('project.csv')
subjects = df['Subject'].tolist()
subj_buttons = []

#Function to open a subject homepage
def open_subject(index):
    mark = df['Mark'][index]
    subject = subjects[index]

    toplevel = ctk.CTkToplevel(win)
    toplevel.title(subject)
    toplevel.geometry("500x500")

    win.withdraw()

    tabview = ctk.CTkTabview(toplevel)
    tabview.pack(padx=20, pady=20)
    tabview.add("Assessment 1")
    tabview.add("Assessment 2")

    ctk.CTkLabel(tabview.tab("Assessment 1"), text=str("Mark=" + mark)).pack(pady=10)

    ctk.CTkLabel(toplevel, text=subject).pack(pady=10)

# Create a button for each existing subject
index = 0

for subject in subjects:
    subj_buttons.append(ctk.CTkButton(win, text=subject, command= lambda index=index: open_subject(index)).pack(pady=10))
    index += 1

win.mainloop()