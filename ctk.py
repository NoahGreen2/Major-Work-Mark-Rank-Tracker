from tkinter import *
import customtkinter as ctk
import pandas as pd

# Create customtkinter window
win = ctk.CTk()
win.title("File Edit")
win.geometry("200x300")

# Create input box for name
name = ctk.CTkEntry(win, placeholder_text="Enter your name")
name.pack(pady=10)
age = ctk.CTkEntry(win, placeholder_text="Enter your age")
age.pack(pady=10)
school = ctk.CTkEntry(win, placeholder_text="Enter your school")
school.pack(pady=10)
sport = ctk.CTkEntry(win, placeholder_text="Enter your favourite sport")
sport.pack(pady=10)
gender = ctk.CTkEntry(win, placeholder_text="Enter your gender")
gender.pack(pady=10)

def enter_data():
    data = [str(name.get()), str(age.get()), str(school.get()), str(sport.get()), str(gender.get())]
    print(data)
    dad = pd.DataFrame(columns=data)
    dad.to_csv('myfile.csv', mode='a', index=False)
    df = pd.read_csv('myfile.csv')
    print(df)

# Create button to submit
submit = ctk.CTkButton(win, text="Submit and add to file", command=enter_data)
submit.pack(pady=10)


win.mainloop()