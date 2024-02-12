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
    subject = subjects[index]

    mark_1 = df['Mark 1'][index]
    rank_1 = df['Rank 1'][index]

    mark_2 = df['Mark 2'][index]
    rank_2 = df['Rank 2'][index]

    mark_3 = df['Mark 3'][index]
    rank_3 = df['Rank 3'][index]

    mark_4 = df['Mark 4'][index]
    rank_4 = df['Rank 4'][index]

    toplevel = ctk.CTkToplevel(win)
    toplevel.title(subject)
    toplevel.geometry("500x500")

    tabview = ctk.CTkTabview(toplevel)
    tabview.pack(padx=20, pady=20)
    tabview.add("Assessment 1")
    tabview.add("Assessment 2")
    tabview.add("Assessment 3")
    tabview.add("Assessment 4")
    
    lower_tab_1 = ctk.CTkTabview(tabview.tab("Assessment 1"))
    lower_tab_1.pack(padx=20, pady=20)
    ass1_m = lower_tab_1.add("Mark")
    ass1_r = lower_tab_1.add("Rank")

    lower_tab_2 = ctk.CTkTabview(tabview.tab("Assessment 2"))
    lower_tab_2.pack(padx=20, pady=20)
    ass2_m = lower_tab_2.add("Mark")
    ass2_r = lower_tab_2.add("Rank")

    lower_tab_3 = ctk.CTkTabview(tabview.tab("Assessment 3"))
    lower_tab_3.pack(padx=20, pady=20)
    ass3_m = lower_tab_3.add("Mark")
    ass3_r = lower_tab_3.add("Rank")

    lower_tab_4 = ctk.CTkTabview(tabview.tab("Assessment 4"))
    lower_tab_4.pack(padx=20, pady=20)
    ass4_m = lower_tab_4.add("Mark")
    ass4_r = lower_tab_4.add("Rank")

    ctk.CTkLabel(ass1_m, text=str("Mark=" + str(mark_1))).pack(pady=10)
    ctk.CTkLabel(ass1_r, text=str("Rank=" + str(rank_1))).pack(pady=10)
    ctk.CTkLabel(ass2_m, text=str("Mark=" + str(mark_2))).pack(pady=10)
    ctk.CTkLabel(ass2_r, text=str("Rank=" + str(rank_2))).pack(pady=10)
    ctk.CTkLabel(ass3_m, text=str("Mark=" + str(mark_3))).pack(pady=10)
    ctk.CTkLabel(ass3_r, text=str("Rank=" + str(rank_3))).pack(pady=10)
    ctk.CTkLabel(ass4_m, text=str("Mark=" + str(mark_4))).pack(pady=10)
    ctk.CTkLabel(ass4_r, text=str("Rank=" + str(rank_4))).pack(pady=10)


# Create a button for each existing subject
index = 0

for subject in subjects:
    subj_buttons.append(ctk.CTkButton(win, text=subject, command= lambda index=index: open_subject(index)).pack(pady=10))
    index += 1

win.mainloop()