from tkinter import *
import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt

# Create main customtkinter window
win = ctk.CTk()
win.title("Main Menu")
win.geometry("300x500")
win_widgets = []

#Read the csv file
def read_csv():
    global df, subjects
    df = pd.read_csv('project.csv')
    subjects = df['Subject'].tolist()

read_csv()

subj_buttons = []

#Function to save changes to the dataframe
def save_changes(subject, mark_textboxes, mark_textboxes_outof, rank_textboxes, rank_textboxes_outof, edit_win, toplevel):
    index = subjects.index(subject)
    for i in range(4):
        df.iloc[index, i*4+1] = mark_textboxes[i].get("1.0", "end-1c")  #This bit is ai - I couldn't figure out how to properly edit
        df.iloc[index, i*4+3] = rank_textboxes[i].get("1.0", "end-1c")  # the values in the dataframe
        df.iloc[index, i*4+2] = mark_textboxes_outof[i].get("1.0", "end-1c")
        df.iloc[index, i*4+4] = rank_textboxes_outof[i].get("1.0", "end-1c")

    df.to_csv('project.csv', index=False)
    edit_win.destroy()
    toplevel.deiconify()

#Function to open an edit window
def open_edit_window(subject, toplevel):
    index = subjects.index(subject)
    edit_win = ctk.CTkToplevel(toplevel)
    edit_win.title(str(subject) + ' Marks/Ranks')
    edit_win.geometry("350x400")

    toplevel.withdraw()

    mark_textboxes = []
    mark_textboxes_outof = []
    rank_textboxes = []
    rank_textboxes_outof = []

    for i in range(4):
        ctk.CTkLabel(edit_win, text='Task ' + str(i+1)).place(x=10,y=10+80*i)
        ctk.CTkLabel(edit_win, text='Mark').place(x=75,y=10+80*i)
        ctk.CTkLabel(edit_win, text='Rank').place(x=75,y=50+80*i)
        ctk.CTkLabel(edit_win, text='Out Of').place(x=200,y=10+80*i)
        ctk.CTkLabel(edit_win, text='Out Of').place(x=200,y=50+80*i)

        mark_textbox = ctk.CTkTextbox(edit_win, height=1, width=50)
        mark_textbox.place(x=125,y=10+80*i)
        mark_textbox.insert(END, df.iloc[index, i*4+1])
        mark_textboxes.append(mark_textbox)

        mark_textbox_outof = ctk.CTkTextbox(edit_win, height=1, width=50)
        mark_textbox_outof.place(x=250,y=10+80*i)
        mark_textbox_outof.insert(END, df.iloc[index, i*4+2])
        mark_textboxes_outof.append(mark_textbox_outof)

        rank_textbox = ctk.CTkTextbox(edit_win, height=1, width=50)
        rank_textbox.place(x=125,y=50+80*i)
        rank_textbox.insert(END, df.iloc[index, i*4+3])
        rank_textboxes.append(rank_textbox)

        rank_textbox_outof = ctk.CTkTextbox(edit_win, height=1, width=50)
        rank_textbox_outof.place(x=250,y=50+80*i)
        rank_textbox_outof.insert(END, df.iloc[index, i*4+4])
        rank_textboxes_outof.append(rank_textbox_outof)

    # Create a button to save the changes
    save_button = ctk.CTkButton(edit_win, text='Save Changes', command= lambda: save_changes(subject, mark_textboxes, mark_textboxes_outof, rank_textboxes, rank_textboxes_outof, edit_win, toplevel))
    save_button.place(x=125,y=350)

#Function to close a toplevel and restore main window
def close_window(toplevel, win):
    toplevel.destroy()
    win.deiconify()

#Function to delete a subject
def delete_subject(subject, toplevel):
    global subjects, win, subj_buttons
    index = subjects.index(subject)
    df.drop(index, inplace=True)
    df.to_csv('project.csv', index=False)
    read_csv()
    subj_buttons[index].destroy()
    subjects = df['Subject'].tolist()
    toplevel.destroy()
    win.deiconify()

#Function to add a new goal
def add_goal(goaltextboxes, goalcheckboxes, scrollframe):
    goaltxt = ctk.CTkTextbox(scrollframe, height=75, width=200)
    goaltxt.pack(pady=10)
    goaltxt.insert(END, 'New Goal')
    goaltextboxes.append(goaltxt)
    check_var = ctk.StringVar(value='False')
    checkbox = ctk.CTkCheckBox(scrollframe, text='Goal Achieved', variable=check_var, onvalue='True', offvalue='False')
    checkbox.pack(pady=10)
    goalcheckboxes.append(check_var)

#Function to save changes to the goals
def save_goals(subject, goaltextboxes, goalcheckboxes, goals_win, toplevel):
    index = subjects.index(subject)
    goals = ''
    for i in range(len(goaltextboxes)):
        goal = goaltextboxes[i].get("1.0", "end-1c")
        goal_check = goalcheckboxes[i].get()
        goal += '#' + goal_check
        if i == len(goaltextboxes)-1:
            goals += goal
        else:
            goals += goal + '$'
    df.iloc[index, -1] = goals
    df.to_csv('project.csv', index=False)
    goals_win.destroy()
    toplevel.deiconify()

#Function to open a goals window
def open_goals_window(subject, toplevel):
    goals_win = ctk.CTkToplevel(toplevel)
    goals_win.title(str(subject) + ' Goals')
    goals_win.geometry("300x500")

    index = subjects.index(subject)

    toplevel.withdraw()

    ctk.CTkLabel(goals_win, text=(str(subject)+' Goals'), font=('Calibri', 40, 'bold', 'underline')).pack(pady=10)

    goaltextboxes = []
    goalcheckboxes = []
    goals = str(df.iloc[index, -1])
    goals = list(goals.split("$"))
    scrollframe = ctk.CTkScrollableFrame(goals_win, width=300, height=300)
    scrollframe.pack()
    for i in range(len(goals)):
        goaltxt = ctk.CTkTextbox(scrollframe, height=75, width=200)
        goalandcheck = goals[i].split("#")
        goaltxt.insert(END, goalandcheck[0])
        goaltxt.pack(pady=10)
        goaltextboxes.append(goaltxt)
        check_var = ctk.StringVar(value=goalandcheck[1])
        checkbox = ctk.CTkCheckBox(scrollframe, text='Goal Achieved', variable=check_var, onvalue='True', offvalue='False')
        checkbox.pack(pady=10)
        goalcheckboxes.append(check_var)

    new_goal_button = ctk.CTkButton(goals_win, text='Add New Goal', command= lambda : add_goal(goaltextboxes, goalcheckboxes, scrollframe))
    new_goal_button.pack(pady=10)

    close_button = ctk.CTkButton(goals_win, text='Close', command= lambda : save_goals(subject, goaltextboxes, goalcheckboxes, goals_win, toplevel))
    close_button.pack(pady=10)

def open_graphs(subject, toplevel):
    index = subjects.index(subject)
    graph_win = ctk.CTkToplevel(toplevel)
    graph_win.title(str(subject) + ' Graphs')
    graph_win.geometry("300x300")

    toplevel.withdraw()

    ctk.CTkLabel(graph_win, text=(str(subject)+' Graphs'), font=('Calibri', 40, 'bold', 'underline')).pack(pady=10)

    tasks = 0
    for task in df.iloc[index, 1:17:4]:
        if task != 'none':
            tasks += 1
    
    task_marks = []
    for i in range(4):
        mark = df.iloc[index, i*4+1]
        if mark != 'none':
            task_marks.append(float(int(mark)/int(df.iloc[index, i*4+2]))*100)
    tasks = []
    for i in range(len(task_marks)):
        tasks.append('Task ' + str(i+1))
    
    plt.figure(figsize=(9, 3))
    plt.plot(tasks, task_marks, color='skyblue')
    plt.ylim(0, 100)
    plt.show()

    # Create a button to save the changes
    close_button = ctk.CTkButton(graph_win, text='Close', command= lambda : close_window(graph_win, toplevel))
    close_button.pack(pady=10)

#Function to open a subject homepage
def open_subject(index):
    subject = subjects[index]

    toplevel = ctk.CTkToplevel(win)
    toplevel.title(subject)
    toplevel.geometry("300x400")

    win.withdraw()

    ctk.CTkLabel(toplevel, text=subject, font=('Calibri', 40, 'bold', 'underline')).pack(pady=10)

    edit_button = ctk.CTkButton(toplevel, text='Edit Marks/Ranks', command= lambda subject=subject: open_edit_window(subject, toplevel))
    edit_button.pack(pady=10)

    goals_button = ctk.CTkButton(toplevel, text='Goals', command= lambda subject=subject: open_goals_window(subject, toplevel))
    goals_button.pack(pady=10)

    graph_button = ctk.CTkButton(toplevel, text='Graphs', command= lambda subject=subject: open_graphs(subject, toplevel))
    graph_button.pack(pady=10)

    close_button = ctk.CTkButton(toplevel, text='Close', command= lambda toplevel=toplevel: close_window(toplevel, win))
    close_button.pack(pady=10)

    delete_button = ctk.CTkButton(toplevel, text='Delete Subject', command= lambda : delete_subject(subject, toplevel))
    delete_button.pack(pady=10)

# Create a button for each existing subject
def set_page(new_subject, add_button):
    subjects.append(new_subject)
    index = subjects.index(new_subject)
    add_button.destroy()
    new_button = ctk.CTkButton(win, text=new_subject, command= lambda index=index: open_subject(index))
    new_button.pack(pady=10)
    subj_buttons.append(new_button)
    # Create a button to add a new subject
    add_button = ctk.CTkButton(win, text='Add New Subject', command=lambda : add_subject(df, add_button))
    add_button.pack(pady=10)
    win_widgets.append(subj_buttons)
    win_widgets.append(add_button)

#Function to save a new subject
def save_subject(new_subject, add_win, df, add_button):
    if new_subject != '':
        global win
        data = [new_subject, 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none','New Goal#False']
        df = pd.concat([df, pd.DataFrame([data], columns=df.columns)], ignore_index=True)
        df.to_csv('project.csv', index=False)
        read_csv()
        set_page(new_subject, add_button)
    add_win.destroy()
    win.deiconify()

#Function to add a new subject
def add_subject(df, add_button):
    add_win = ctk.CTkToplevel(win)
    add_win.title('Add New Subject')
    add_win.geometry("300x300")

    win.withdraw()

    ctk.CTkLabel(add_win, text='Enter New Subject Name').pack(pady=10)
    new_subject = ctk.CTkEntry(add_win, height=20, width=150, placeholder_text='Subject Name')
    new_subject.pack(pady=10)

    save_subj_button = ctk.CTkButton(add_win, text='Save and Exit', command= lambda : save_subject(new_subject.get(), add_win, df, add_button)) 
    save_subj_button.pack(pady=10)

# Set the page
index = 0
for subject in subjects:
    button = ctk.CTkButton(win, text=subject, command= lambda index=index: open_subject(index))
    button.pack(pady=10)
    subj_buttons.append(button)
    index += 1    
# Create a button to add a new subject
add_button = ctk.CTkButton(win, text='Add New Subject', command=lambda : add_subject(df, add_button))
add_button.pack(pady=10)

win.mainloop()