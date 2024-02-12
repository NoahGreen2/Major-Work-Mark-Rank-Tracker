import pandas as pd
from tkinter import *
import customtkinter as ctk

data = [input("Enter your name: "), input("Enter your age: "), input("Enter your school: "), input("Enter your favourite sport: "), input("Enter your gender: ")]
print(data)
dad = pd.DataFrame(columns=data)
dad.to_csv('myfile.csv', mode='a', index=False)
df = pd.read_csv('myfile.csv')

# Print the name column
print(df)

