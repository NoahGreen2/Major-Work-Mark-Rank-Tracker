from tkinter import *
import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter.messagebox as messagebox

# Create main customtkinter window
win = ctk.CTk()
win.title("Main Menu")
win.geometry("300x400")

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
    # Check if the values entered are valid
    valid = True
    for i in range(4):
        if not mark_textboxes[i].get("1.0", "end-1c").isdigit():
            if mark_textboxes[i].get("1.0", "end-1c") != 'none':
                valid = False
        if not mark_textboxes_outof[i].get("1.0", "end-1c").isdigit():
            if mark_textboxes_outof[i].get("1.0", "end-1c") != 'none':
                valid = False
        if not rank_textboxes[i].get("1.0", "end-1c").isdigit():
            if rank_textboxes[i].get("1.0", "end-1c") != 'none':
                valid = False
        if not rank_textboxes_outof[i].get("1.0", "end-1c").isdigit():
            if rank_textboxes_outof[i].get("1.0", "end-1c") != 'none':
                valid = False
        if mark_textboxes[i].get("1.0", "end-1c").isdigit() and mark_textboxes_outof[i].get("1.0", "end-1c").isdigit() and rank_textboxes[i].get("1.0", "end-1c").isdigit() and rank_textboxes_outof[i].get("1.0", "end-1c").isdigit():
            if int(mark_textboxes[i].get("1.0", "end-1c")) > int(mark_textboxes_outof[i].get("1.0", "end-1c")) or int(rank_textboxes[i].get("1.0", "end-1c")) > int(rank_textboxes_outof[i].get("1.0", "end-1c")):
                valid = False
            if int(mark_textboxes[i].get("1.0", "end-1c")) < 0 or int(mark_textboxes_outof[i].get("1.0", "end-1c")) <= 0 or int(rank_textboxes[i].get("1.0", "end-1c")) <= 0 or int(rank_textboxes_outof[i].get("1.0", "end-1c")) <= 0:
                valid = False
    if valid:
        # Loop through the four assessments to save the edited values to the dataframe
        for i in range(4):
            df.iloc[index, i*4+1] = mark_textboxes[i].get("1.0", "end-1c")  #This bit is ai - I couldn't figure out how to properly edit
            df.iloc[index, i*4+3] = rank_textboxes[i].get("1.0", "end-1c")  # the values in the dataframe
            df.iloc[index, i*4+2] = mark_textboxes_outof[i].get("1.0", "end-1c")
            df.iloc[index, i*4+4] = rank_textboxes_outof[i].get("1.0", "end-1c")
        # Save the changes to the csv file
        df.to_csv('project.csv', index=False)
        # Close the edit window and restore the main window
        edit_win.destroy()
        toplevel.deiconify()
    else: #Show error message if values aren't valid
        messagebox.showerror("Error", "Please enter valid numbers for marks and ranks")

#Function to open an edit window
def open_edit_window(subject, toplevel):
    index = subjects.index(subject)
    # Create a new window for editing the marks and ranks
    edit_win = ctk.CTkToplevel(toplevel)
    edit_win.title(str(subject) + ' Marks/Ranks')
    edit_win.geometry("350x400")
    edit_win.resizable(False, False)

    toplevel.withdraw()

    mark_textboxes = []
    mark_textboxes_outof = []
    rank_textboxes = []
    rank_textboxes_outof = []
    # Place the labels and textboxes for each assessment
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
    # Remove the subject from the dataframe and save the changes
    df.drop(index, inplace=True)
    df.to_csv('project.csv', index=False)
    read_csv()
    subjects = df['Subject'].tolist()
    toplevel.destroy()
    set_homepage()
    win.deiconify()

#Function to add a new goal
def add_goal(goaltextboxes, goalcheckboxvals, scrollframe):
    goaltxt = ctk.CTkTextbox(scrollframe, height=75, width=200)
    goaltxt.pack(pady=10)
    goaltxt.insert(END, 'New Goal')
    goaltextboxes.append(goaltxt)
    # Variable to store the value of the checkbox
    check_var = ctk.StringVar(value='False')
    checkbox = ctk.CTkCheckBox(scrollframe, text='Goal Achieved', variable=check_var, onvalue='True', offvalue='False')
    checkbox.pack(pady=10)
    goalcheckboxvals.append(check_var)

#Function to save changes to the goals
def save_goals(subject, goaltextboxes, goalcheckboxvals, goals_win, toplevel):
    index = subjects.index(subject)
    goals = ''
    # Loop through the goals to save the edited data to the dataframe including checkboxes
    for i in range(len(goaltextboxes)):
        goal = goaltextboxes[i].get("1.0", "end-1c")
        goal_check = goalcheckboxvals[i].get()
        goal += '#' + goal_check
        if i == len(goaltextboxes)-1:
            goals += goal
        else:
            goals += goal + '$'
    df.iloc[index, -1] = goals
    df.to_csv('project.csv', index=False)
    goals_win.destroy()
    toplevel.deiconify()

#Function to delete a goal
def delete_goal(i, goaltextboxes, goalcheckboxes, delete_goal_buttons):
    goaltextboxes[i].destroy()
    goalcheckboxes[i].destroy()
    goaltextboxes.pop(i)
    goalcheckboxes.pop(i)
    for i in range(len(goaltextboxes)):
        goaltextboxes[i].pack(pady=10)
        goalcheckboxes[i].pack(pady=10)
    delete_goal_buttons[i].destroy()
    delete_goal_buttons.pop(i)

#Function to open a goals window
def open_goals_window(subject, toplevel):
    goals_win = ctk.CTkToplevel(toplevel)
    goals_win.title(str(subject) + ' Goals')
    goals_win.geometry("300x500")
    goals_win.resizable(False, False)

    index = subjects.index(subject)

    toplevel.withdraw()

    ctk.CTkLabel(goals_win, text=(str(subject)+' Goals'), font=('Calibri', 40, 'bold')).pack(pady=10)

    goaltextboxes = []
    goalcheckboxvals = []
    goalcheckboxes = []
    delete_goal_buttons = []
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
        goalcheckboxes.append(checkbox)
        goalcheckboxvals.append(check_var)
        delete_goal_button = ctk.CTkButton(scrollframe, text='Delete Goal', command= lambda i=i: delete_goal(i, goaltextboxes, goalcheckboxes, delete_goal_buttons))
        delete_goal_button.pack(pady=10)
        delete_goal_buttons.append(delete_goal_button)

    new_goal_button = ctk.CTkButton(goals_win, text='Add New Goal', command= lambda : add_goal(goaltextboxes, goalcheckboxvals, scrollframe))
    new_goal_button.pack(pady=10)

    close_button = ctk.CTkButton(goals_win, text='Close', command= lambda : save_goals(subject, goaltextboxes, goalcheckboxvals, goals_win, toplevel))
    close_button.pack(pady=10)

#Function to open a graph window
def open_graphs(subject, toplevel):
    index = subjects.index(subject)
    graph_win = ctk.CTkToplevel(toplevel)
    graph_win.title(str(subject) + ' Graphs')
    graph_win.geometry("700x550")
    graph_win.resizable(False, False)

    toplevel.withdraw()

    ctk.CTkLabel(graph_win, text=(str(subject)+' Graphs'), font=('Calibri', 40, 'bold')).pack(pady=10)

    tasks = 0
    for task in df.iloc[index, 1:17:4]:
        if task != 'none' and task != '':
            tasks += 1
    
    task_marks = []
    for i in range(4):
        mark = df.iloc[index, i*4+1]
        if mark != 'none' and df.iloc[index, i*4+2] != 'none':
            task_marks.append(float(int(mark)/int(df.iloc[index, i*4+2]))*100)
        elif mark == 'none' or df.iloc[index, i*4+2] == 'none':
            task_marks.append(0)
    task_ranks = []
    for i in range(4):
        rank = df.iloc[index, i*4+3]
        if rank != 'none':
            task_ranks.append(float(rank))
        elif rank == 'none':
            task_ranks.append(0)
    tasks = []
    for i in range(len(task_marks)):
        tasks.append('Task ' + str(i+1))
    
    # Create a button to save the changes
    close_button = ctk.CTkButton(graph_win, text='Close', command= lambda : close_window(graph_win, toplevel))
    close_button.pack(pady=10)

    fig = Figure(figsize=(8, 5), dpi=100)
    plot1 = fig.add_subplot(121)
    plot2 = fig.add_subplot(122)

    plot1.plot(tasks, task_marks, 'r', linewidth=5)
    plot1.set_title('Marks Graph')
    plot1.set_xlabel('Tasks')
    plot1.set_ylabel('Mark %')

    plot2.plot(tasks, task_ranks, 'g', linewidth=5)
    plot2.set_title('Ranks Graph')
    plot2.set_xlabel('Tasks')
    plot2.set_ylabel('Rank')
    plot2.invert_yaxis()

    # Create a canvas to display the plot
    canvas = FigureCanvasTkAgg(fig, master=graph_win)
    canvas.draw()
    canvas.get_tk_widget().pack()

#Function to open a subject homepage
def open_subject(index):
    subject = subjects[index]

    toplevel = ctk.CTkToplevel(win)
    toplevel.title(subject)
    toplevel.geometry("300x400")
    toplevel.resizable(False, False)

    win.withdraw()

    ctk.CTkLabel(toplevel, text=subject, font=('Calibri', 40, 'bold')).pack(pady=10)

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

#Function to save a new subject
def save_subject(new_subject, add_win, df, add_button, instructions_button):
    # Check if the subject name is valid
    if new_subject != '':
        global win
        # Create empty subject
        data = [new_subject, 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none','New Goal#False']
        df = pd.concat([df, pd.DataFrame([data], columns=df.columns)], ignore_index=True)
        df.to_csv('project.csv', index=False)
        read_csv()
        set_homepage()
    add_win.destroy()
    win.deiconify()

#Function to add a new subject
def add_subject(df, add_button, instructions_button):
    add_win = ctk.CTkToplevel(win)
    add_win.title('Add New Subject')
    add_win.geometry("300x300")
    add_win.resizable(False, False)

    win.withdraw()

    ctk.CTkLabel(add_win, text='Enter New Subject Name').pack(pady=10)
    new_subject = ctk.CTkEntry(add_win, height=20, width=150, placeholder_text='Subject Name')
    new_subject.pack(pady=10)

    save_subj_button = ctk.CTkButton(add_win, text='Save and Exit', command= lambda : save_subject(new_subject.get(), add_win, df, add_button, instructions_button)) 
    save_subj_button.pack(pady=10)

#Function to open the instructions window
def open_instructions():
    instructions_win = ctk.CTkToplevel(win)
    instructions_win.title('Instructions')
    instructions_win.geometry("650x400")
    instructions_win.resizable(False, False)

    win.withdraw()

    ctk.CTkLabel(instructions_win, text='Instructions', font=('Calibri', 40, 'bold')).pack(pady=10)

    instructions = ctk.CTkLabel(instructions_win, text='Welcome to the Student Progress Tracker! \nTo get started, click on a subject to view the marks, ranks, goals and graphs. \nTo edit the marks and ranks, click on the Edit Marks/Ranks button. \nTo add or delete goals, click on the Goals button. \nTo view the graphs, click on the Graphs button. \nTo delete a subject, click on the Delete Subject button. \nTo add a new subject, click on the Add New Subject button. \nTo view these instructions again, click on the Instructions button. \nWhen you open and close the program, all your information will be saved,\n so that you may come back another day to review your results.', font=('Calibri', 20))
    instructions.pack(pady=10)

    close_button = ctk.CTkButton(instructions_win, text='Close', command= lambda : close_window(instructions_win, win))
    close_button.pack(pady=10)

# Set the page
def set_homepage():
    global homescrollframe, subjects
    subj_buttons = []
    for widget in win.winfo_children():
        widget.destroy()
    homescrollframe = ctk.CTkScrollableFrame(win, width=300, height=400)
    homescrollframe.pack()
    index = 0
    for subject in subjects:
        button = ctk.CTkButton(homescrollframe, text=subject, command= lambda index=index: open_subject(index))
        button.pack(pady=10)
        subj_buttons.append(button)
        index += 1    
    # Create a button to add a new subject
    add_button = ctk.CTkButton(homescrollframe, text='Add New Subject', command=lambda : add_subject(df, add_button, instructions_button))
    add_button.pack(pady=10)

    instructions_button = ctk.CTkButton(homescrollframe, text='Instructions', command= lambda : open_instructions())
    instructions_button.pack(pady=10)

set_homepage()

win.mainloop()