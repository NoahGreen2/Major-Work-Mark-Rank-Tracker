from tkinter import *
import customtkinter as ctk
import pandas as pd

# Create main customtkinter window
win = ctk.CTk()
win.title("Main Menu")
win.geometry("200x300")

df = pd.read_csv('project.csv')
subjects = df['Subject'].tolist()

def print_name(index):
    subjects = df['Subject'].tolist()
    print(subjects[index])

# Create a button for each existing subject
for subject in subjects:
    ctk.CTkButton(win, text=subject, command=lambda: print_name(subjects.index(subject))).pack(pady=10)

# Create button to add a subject
add_subject = ctk.CTkButton(win, text="Add a subject", command=lambda: add_subject())
add_subject.pack(pady=10)

win.mainloop()