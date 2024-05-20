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

#Function to make sure that the user wishes to delete a subject
def check_delete_subject(subject, toplevel):
    # Create a message box to confirm the deletion
    answer = messagebox.askyesno("Delete", "Are you sure you want to delete " + str(subject) + "?")
    if answer:
        delete_subject(subject, toplevel)
    else:
        toplevel.deiconify()

#Function to add a new goal
def add_goal(goaltextboxes, goalcheckboxvals, scrollframe):
    # Create a new textbox and set its contents to 'New Goal'
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
        # Only add a $ to separate the goals if it is not the last goal
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

    delete_button = ctk.CTkButton(toplevel, text='Delete Subject', fg_color='red', hover_color='tomato', command= lambda : check_delete_subject(subject, toplevel))
    delete_button.pack(pady=10)
    
    close_button = ctk.CTkButton(toplevel, text='Back', fg_color='grey', hover_color='darkgrey', command= lambda toplevel=toplevel: close_window(toplevel, win))
    close_button.pack(pady=10)

#Function to save a new subject
def save_subject(new_subject, add_win, df, add_button, instructions_button):
    if new_subject == 'linegame':
        run_secret_game()
    # Check if the subject name is valid
    elif new_subject != '':
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
    # Establish the window
    instructions_win = ctk.CTkToplevel(win)
    instructions_win.title('Instructions')
    instructions_win.geometry("650x400")
    instructions_win.resizable(False, False)

    win.withdraw()

    # Create text for the instructions
    ctk.CTkLabel(instructions_win, text='Instructions', font=('Calibri', 40, 'bold')).pack(pady=10)

    instructions = ctk.CTkLabel(instructions_win, text='Welcome to the Student Progress Tracker! \nTo get started, click on a subject to view the marks, ranks, goals and graphs. \nTo edit the marks and ranks, click on the Edit Marks/Ranks button. \nTo add or delete goals, click on the Goals button. \nTo view the graphs, click on the Graphs button. \nTo delete a subject, click on the Delete Subject button. \nTo add a new subject, click on the Add New Subject button. \nTo view these instructions again, click on the Instructions button. \nWhen you open and close the program, all your information will be saved,\n so that you may come back another day to review your results.', font=('Calibri', 20))
    instructions.pack(pady=10)

    # Create a button to close the window
    close_button = ctk.CTkButton(instructions_win, fg_color='grey', hover_color='darkgrey', text='Close', command= lambda : close_window(instructions_win, win))
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
    add_button = ctk.CTkButton(homescrollframe, fg_color='green', hover_color='mediumseagreen', text='Add New Subject', text_color='black', command=lambda : add_subject(df, add_button, instructions_button))
    add_button.pack(pady=10)

    instructions_button = ctk.CTkButton(homescrollframe, fg_color='yellow', hover_color='lightgoldenrodyellow', text='Instructions', text_color='black', command= lambda : open_instructions())
    instructions_button.pack(pady=10)

# Easter egg - check line 300
def run_secret_game():
    import winsound
    import random
    import time
    import pygame

    pygame.mixer.init()

    ctk.set_appearance_mode("light")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

    linesound = pygame.mixer.Sound('Place line.wav')
    gamesound = pygame.mixer.Sound('Game over.wav')


    app = ctk.CTk()
    app.geometry("400x400")
    app.title("CustomTkinter simple_example.py")

    frame_1 = ctk.CTkFrame(master=app)
    frame_1.pack(pady=20, padx=60, fill="both", expand=True)

    label = ctk.CTkLabel(frame_1, text="Line Game", fg_color="transparent", font=("Helvetica", 20))
    label.place(y=50, x=100)

    optionmenu_1 = ctk.CTkOptionMenu(frame_1, values=["Player vs Player", "AI - Easy", "AI - Medium", "AI - Hard"])
    optionmenu_1.place(y=100, x=75)
    optionmenu_1.set("Pick a gamemode")

    start_button = ctk.CTkButton(frame_1, text="Start", command=lambda: start_game(optionmenu_1.get(), optionmenu_2.get(), sound_switch_var.get()))
    start_button.place(y=150, x=75)

    instructions_button = ctk.CTkButton(frame_1, text="Instructions/Rules", command=lambda: open_instructions())
    instructions_button.place(y=200, x=75)

    options_button = ctk.CTkButton(frame_1, text="Options", command=lambda: option_window(optionmenu_2))
    options_button.place(y=250, x=75)

    optionmenu_2 = ctk.StringVar(value='4x4 (classic)')

    sound_switch_var = ctk.StringVar(value='on')

    appearance_switch_var = ctk.StringVar(value='light')

    def option_window(modemenu):
        options_window = ctk.CTk()
        options_window.geometry("400x400")
        options_window.title("Options")

        frame_3 = ctk.CTkFrame(master=options_window)
        frame_3.pack(pady=20, padx=60, fill="both", expand=True)

        label = ctk.CTkLabel(frame_3, text="Options", fg_color="transparent", font=("Helvetica", 20))
        label.pack(pady=25)

        def sound_switch_event():
            sound_switch.configure(text="Sound: " + sound_switch_var.get().capitalize())

        def appearance_switch_event():
            appearance_switch.configure(text="Appearance: " + appearance_switch_var.get().capitalize())
            ctk.set_appearance_mode(appearance_switch_var.get())

        sound_switch = ctk.CTkSwitch(frame_3, text="Sound: " + sound_switch_var.get().capitalize(), command=lambda: sound_switch_event(), variable=sound_switch_var, onvalue="on", offvalue="off")
        sound_switch.pack(pady=15)

        
        appearance_switch = ctk.CTkSwitch(frame_3, text="Appearance: " + appearance_switch_var.get().capitalize(), command=lambda: appearance_switch_event(), variable=appearance_switch_var, onvalue="light", offvalue="dark")
        appearance_switch.pack(pady=15)

        modemenu = ctk.CTkOptionMenu(frame_3, values=["3x3", "4x4 (classic)", "5x5"])
        modemenu.pack(pady=10)
        modemenu.set("4x4 (classic)")

        apply_button = ctk.CTkButton(frame_3, text="Apply", command=lambda: apply_options(modemenu, options_window))
        apply_button.pack(pady=15)

        options_window.mainloop()

    def apply_options(modemenu, options_window):
        optionmenu_2.set(modemenu.get())
        sound_switch_var.set(sound_switch_var.get())
        options_window.destroy()

    def start_game(mode, size, sound):
        if size == ('3x3'):
            boardsize = 3
        elif size == ('4x4 (classic)'):
            boardsize = 4
        elif size == ('5x5'):
            boardsize = 5
        elif size == ('6x6'):
            boardsize = 6
        if mode  == ('Player vs Player'):
            print('Player vs Player')
            open_pvp_window(boardsize, sound)
        elif mode == ('AI - Easy'):
            print('AI - Easy')
            gamemode = 'easy'
            open_new_window(gamemode, boardsize, sound)
        elif mode == ('AI - Medium'):
            print('AI - Medium')
            gamemode = 'medium'
            open_new_window(gamemode, boardsize, sound)
        elif mode == ('AI - Hard'):
            print('AI - Hard')
            gamemode = 'hard'
            open_new_window(gamemode, boardsize, sound)

    def open_pvp_window(size, sound):
        new_window = ctk.CTk()
        geometry = str(size*100)
        new_window.geometry(geometry + 'x' + geometry)
        new_window.title("Line Game - Player vs Player")

        c = Canvas(new_window, width=size*100+100, height=size*100+100, bg='white')
        c.pack()

        # Create the dotted lines and bind them to a function that changes their color
        lines = []
        count_red_lines = []
        count_blue_lines = []
        changed_lines = []

        for y in range(105, size*100 +6, 100):
            for i in range(size - 1):
                line = c.create_line(105 + 100 * i, y, 205 + 100 * i, y, width=10, fill='white', activefill='light grey')
                lines.append(line)
                c.tag_bind(line, "<Button-1>", lambda event, line=line: take_turn(line, changed_lines))

        for x in range(105, size*100 +6, 100):
            for i in range(size - 1):
                line = c.create_line(x, 105 + 100 * i, x, 205 + 100 * i, width=10, fill='white', activefill='light grey')
                lines.append(line)
                c.tag_bind(line, "<Button-1>", lambda event, line=line: take_turn(line, changed_lines))

        for i in range(size):
            for j in range(size):
                x, y = 100 + i * 100, 100 + j * 100
                c.create_oval(x, y, x + 10, y + 10, fill='black', width=5)

        # Function to change the color of a line red, run random blue move
        def take_turn(line, changed_lines):
            if c.itemcget(line, 'fill') == 'white':
                if sound == 'on':
                    linesound.play()
                line_red(line, changed_lines)
                if not lines:

                    if sound == 'on':
                        winsound.PlaySound("Game over.wav", winsound.SND_FILENAME|winsound.SND_ASYNC)
                    
                    longest_red_line = count_longest(count_red_lines)
                    longest_blue_line = count_longest(count_blue_lines)

                    c.create_text((size*100 + 100)//2, 50, text="GAME OVER", fill="black", font=('Helvetica 15 bold'))

                    print('The longest red line is ' + str(longest_red_line))
                    print('The longest blue line is ' + str(longest_blue_line))

                    c.create_text((size*100 + 100)//4, 60, text="Red: " + str(longest_red_line), fill="red", font=('Helvetica 15 bold'))
                    c.create_text((size*100 + 100)//4*3, 60, text="Blue: " + str(longest_blue_line), fill="blue", font=('Helvetica 15 bold'))

                    if longest_red_line > longest_blue_line:
                        c.create_text((size*100 + 100)//2, 75, text="Red wins", fill="red", font=('Helvetica 15 bold'))
                    if longest_red_line < longest_blue_line:
                        c.create_text((size*100 + 100)//2, 75, text="Blue wins", fill="blue", font=('Helvetica 15 bold'))
                    if longest_red_line == longest_blue_line:
                        c.create_text((size*100 + 100)//2, 75, text="Tie", fill="black", font=('Helvetica 15 bold'))
                    

        def line_red(line, changed_lines):
            if c.itemcget(line, 'fill') == 'white':
                if not changed_lines:
                    c.itemconfig(line, fill='Red', activefill='red')
                    lines.remove(line)
                    count_red_lines.append(line)
                    changed_lines.append(line)
                elif c.itemcget(changed_lines[-1], 'fill') == 'Blue':
                    c.itemconfig(line, fill='Red', activefill='red')
                    lines.remove(line)
                    count_red_lines.append(line)
                    changed_lines.append(line)
                elif c.itemcget(changed_lines[-1], 'fill') == 'Red':
                    c.itemconfig(line, fill='Blue', activefill='blue')
                    lines.remove(line)
                    count_blue_lines.append(line)
                    changed_lines.append(line)

        def return_end_open(list):
            i = list[-1]
            n = list[-2]
            ax1, ay1 = c.coords(i)[0], c.coords(i)[1]
            bx1, by1 = c.coords(i)[2], c.coords(i)[3]
            ax2, ay2 = c.coords(n)[0], c.coords(n)[1]
            bx2, by2 = c.coords(n)[2], c.coords(n)[3]
            if ax2 == ax1 and ay2 == ay1 or bx2 == ax1 and by2 == ay1:
                return 2
            elif ax2 == bx1 and ay2 == by1 or bx2 == bx1 and by2 == by1:
                return 1
            
        def loop_count(lists, lengths, count_lines):
            new_lists = []
            for list in lists:
                last = list[-1]
                if return_end_open(list) == 1:
                    for i in count_lines:
                            if i not in list:
                                x1, y1 = c.coords(last)[0], c.coords(last)[1]
                                ax2, ay2 = c.coords(i)[0], c.coords(i)[1]
                                bx2, by2 = c.coords(i)[2], c.coords(i)[3]
                                if ax2 == x1 and ay2 == y1 or bx2 == x1 and by2 == y1:
                                    globals()[str(i)] = []
                                    for l in list:
                                        globals()[str(i)].append(l)
                                    globals()[str(i)].append(i)
                                    new_lists.append(globals()[str(i)])
                                    lengths.append(globals()[str(i)])
                if return_end_open(list) == 2:
                    for i in count_lines:
                            if i not in list:
                                x1, y1 = c.coords(last)[2], c.coords(last)[3]
                                ax2, ay2 = c.coords(i)[0], c.coords(i)[1]
                                bx2, by2 = c.coords(i)[2], c.coords(i)[3]
                                if ax2 == x1 and ay2 == y1 or bx2 == x1 and by2 == y1:
                                    globals()[str(i)] = []
                                    for l in list:
                                        globals()[str(i)].append(l)
                                    globals()[str(i)].append(i)
                                    new_lists.append(globals()[str(i)])
                                    lengths.append(globals()[str(i)])
            if new_lists:
                loop_count(new_lists, lengths, count_lines)
                                
                                    

        def count_longest(count_lines):
            lists = []
            
            for end in count_lines:
                for i in count_lines:
                    current_count = []
                    current_count.append(end)
                    if i not in current_count:
                        for j in range(2):
                            for k in range(2): 
                                if abs(c.coords(i)[j * 2 - 1] - c.coords(end)[k * 2 - 1]) < 2 and \
                                    abs(c.coords(i)[j * 2] - c.coords(end)[k * 2]) < 2:
                                    if i != end:
                                        current_count.append(i)
                                        if current_count:
                                            lists.append(current_count)
            lengths = []
            loop_count(lists, lengths, count_lines)
            longest = 0
            longest_line = []
            for i in lengths:
                if len(i) > longest:
                    longest = len(i)
                    longest_line = i
            for i in count_lines:
                if i not in longest_line:
                    c.itemconfig(i, dash=(5,3), width=5)
            return longest
        new_window.mainloop()

    def open_new_window(i, size, sound):
        new_window = ctk.CTk()
        geometry = str(size*100+100)
        new_window.geometry(geometry+'x'+geometry)
        new_window.title("Line Game - " + str(i))

        c = Canvas(new_window, width=size*100+100, height=size*100+100, bg='white')
        c.pack()

        # Create the dotted lines and bind them to a function that changes their color
        lines = []
        count_red_lines = []
        count_blue_lines = []
        end_blue_lines = []

        difficulty = i

        for y in range(105, size*100 +6, 100):
            for i in range(size-1):
                line = c.create_line(105 + 100 * i, y, 205 + 100 * i, y, width=10, fill='white', activefill='light grey')
                lines.append(line)
                c.tag_bind(line, "<Button-1>", lambda event, line=line: take_turn(line))

        for x in range(105, size*100+6, 100):
            for i in range(size-1):
                line = c.create_line(x, 105 + 100 * i, x, 205 + 100 * i, width=10, fill='white', activefill='light grey')
                lines.append(line)
                c.tag_bind(line, "<Button-1>", lambda event, line=line: take_turn(line))

        for i in range(size):
            for j in range(size):
                x, y = 100 + i * 100, 100 + j * 100
                c.create_oval(x, y, x + 10, y + 10, fill='black', width=5)

        # Function to change the color of a line red, run random blue move
        def take_turn(line):
            if c.itemcget(line, 'fill') == 'white':
                if sound == 'on':
                    winsound.PlaySound("Place line.wav", winsound.SND_FILENAME|winsound.SND_ASYNC)
                line_red(line)
                get_line_blue(difficulty)
                if not lines:
                    if sound == 'on':
                        winsound.PlaySound("Game over.wav", winsound.SND_FILENAME|winsound.SND_ASYNC)
                    
                    longest_red_line = count_longest(count_red_lines)
                    longest_blue_line = count_longest(count_blue_lines)

                    c.create_text((size*100+100)//2, 50, text="GAME OVER", fill="black", font=('Helvetica 15 bold'))

                    print('The longest red line is ' + str(longest_red_line))
                    print('The longest blue line is ' + str(longest_blue_line))

                    c.create_text((size*100+100)//4, 60, text="Red: " + str(longest_red_line), fill="red", font=('Helvetica 15 bold'))
                    c.create_text((size*100+100)*3//4, 60, text="Blue: " + str(longest_blue_line), fill="blue", font=('Helvetica 15 bold'))

                    if longest_red_line > longest_blue_line:
                        c.create_text((size*100+100)//2, 75, text="Player wins", fill="red", font=('Helvetica 15 bold'))
                    elif longest_red_line < longest_blue_line:
                        c.create_text((size*100+100)//2, 75, text="AI wins", fill="blue", font=('Helvetica 15 bold'))
                    if longest_red_line == longest_blue_line:
                        c.create_text((size*100+100)//2, 75, text="Tie", fill="black", font=('Helvetica 15 bold'))

                    button = Button(c, text = 'Exit', font='bold', relief='flat', bg='blue', activebackground = 'blue', command = new_window.destroy)
                    button.place(x=size*100+50, y=size*100+50)

                    restart_button = Button(c, text = 'Restart', font='bold', relief='flat', bg='blue', activebackground = 'blue', command = lambda: restart_game(difficulty, size, sound))
                    restart_button.place(x=50, y=size*100+50)

                    def restart_game(difficulty, size, sound):
                        new_window.destroy()
                        open_new_window(difficulty, size, sound)

        def line_red(line):
            if c.itemcget(line, 'fill') == 'white':
                c.itemconfig(line, fill='red', width=10, activefill='red')
                lines.remove(line)
                count_red_lines.append(line)          

        def find_end_lines(count_lines, end_lines):
            for i in count_lines:
                ax1, ay1 = c.coords(i)[0], c.coords(i)[1]
                bx1, by1 = c.coords(i)[2], c.coords(i)[3]
                first_point = []
                for other in count_lines:
                    ax2, ay2 = c.coords(other)[0], c.coords(other)[1]
                    bx2, by2 = c.coords(other)[2], c.coords(other)[3]
                    if ax2 == ax1 and ay2 == ay1 or bx2 == ax1 and by2 == ay1:
                        if c.coords(other) != c.coords(i):
                            first_point.append(other)
                second_point = []
                for other in count_lines:
                    ax2, ay2 = c.coords(other)[0], c.coords(other)[1]
                    bx2, by2 = c.coords(other)[2], c.coords(other)[3]
                    if ax2 == bx1 and ay2 == by1 or bx2 == bx1 and by2 == by1:
                        if c.coords(other) != c.coords(i):
                            second_point.append(other)
                if not first_point or not second_point:
                    end_lines.append(i)

        def return_end_open(list):
            i = list[-1]
            n = list[-2]
            ax1, ay1 = c.coords(i)[0], c.coords(i)[1]
            bx1, by1 = c.coords(i)[2], c.coords(i)[3]
            ax2, ay2 = c.coords(n)[0], c.coords(n)[1]
            bx2, by2 = c.coords(n)[2], c.coords(n)[3]
            if ax2 == ax1 and ay2 == ay1 or bx2 == ax1 and by2 == ay1:
                return 2
            elif ax2 == bx1 and ay2 == by1 or bx2 == bx1 and by2 == by1:
                return 1
            
        def loop_count(lists, lengths, count_lines):
            new_lists = []
            for list in lists:
                last = list[-1]
                if return_end_open(list) == 1:
                    for i in count_lines:
                            if i not in list:
                                x1, y1 = c.coords(last)[0], c.coords(last)[1]
                                ax2, ay2 = c.coords(i)[0], c.coords(i)[1]
                                bx2, by2 = c.coords(i)[2], c.coords(i)[3]
                                if ax2 == x1 and ay2 == y1 or bx2 == x1 and by2 == y1:
                                    globals()[str(i)] = []
                                    for l in list:
                                        globals()[str(i)].append(l)
                                    globals()[str(i)].append(i)
                                    new_lists.append(globals()[str(i)])
                                    lengths.append(globals()[str(i)])
                if return_end_open(list) == 2:
                    for i in count_lines:
                            if i not in list:
                                x1, y1 = c.coords(last)[2], c.coords(last)[3]
                                ax2, ay2 = c.coords(i)[0], c.coords(i)[1]
                                bx2, by2 = c.coords(i)[2], c.coords(i)[3]
                                if ax2 == x1 and ay2 == y1 or bx2 == x1 and by2 == y1:
                                    globals()[str(i)] = []
                                    for l in list:
                                        globals()[str(i)].append(l)
                                    globals()[str(i)].append(i)
                                    new_lists.append(globals()[str(i)])
                                    lengths.append(globals()[str(i)])
            if new_lists:
                loop_count(new_lists, lengths, count_lines)
                                
                                    

        def count_longest(count_lines):
            lists = []
            for n in count_lines:
                for i in count_lines:
                    current_count = []
                    if i not in current_count:
                        for j in range(2):
                            for k in range(2): 
                                if abs(c.coords(i)[j * 2 - 1] - c.coords(n)[k * 2 - 1]) < 2 and \
                                    abs(c.coords(i)[j * 2] - c.coords(n)[k * 2]) < 2:
                                    if i != n:                  
                                        current_count.append(n)
                                        current_count.append(i)
                                        if current_count:
                                            lists.append(current_count)
            lengths = []
            loop_count(lists, lengths, count_lines)
            longest = 0
            longest_line = []
            for i in lengths:
                if len(i) > longest:
                    longest = len(i)
                    longest_line = i
            for i in count_lines:
                if i not in longest_line:
                    c.itemconfig(i, dash=(5,3), width=5)
            return longest

        def get_line_blue(difficulty):
            if difficulty == 'easy':
                usable_lines = []
                for i in lines:
                    if c.itemcget(i, 'fill') == 'white':
                        usable_lines.append(i)
                bline = random.choice(usable_lines)
                lines.remove(bline)
                c.itemconfig(bline, fill='blue', width=10, activefill='blue')
                count_blue_lines.append(bline)
            elif difficulty == 'medium':
                usable_lines = []
                for i in lines:
                    if c.itemcget(i, 'fill') == 'white':
                        usable_lines.append(i)
                find_end_lines(count_red_lines, end_blue_lines)
                moves = []
                for i in usable_lines:
                    for x in end_blue_lines:
                        for j in range(2):
                            for k in range(2): 
                                if abs(c.coords(i)[j * 2 - 1] - c.coords(x)[k * 2 - 1]) < 2 and \
                                    abs(c.coords(i)[j * 2] - c.coords(x)[k * 2]) < 2:
                                    moves.append(i)
                if moves:
                    bline = random.choice(moves)
                    lines.remove(bline)
                    c.itemconfig(bline, fill='blue', width=10, activefill='blue')
                    count_blue_lines.append(bline)
                elif not moves:
                    moves2 = []
                    find_end_lines(count_blue_lines, end_blue_lines)
                    for i in usable_lines:
                        for x in end_blue_lines:
                            for j in range(2):
                                for k in range(2): 
                                    if abs(c.coords(i)[j * 2 - 1] - c.coords(x)[k * 2 - 1]) < 2 and \
                                        abs(c.coords(i)[j * 2] - c.coords(x)[k * 2]) < 2:
                                        moves2.append(i)
                    if moves2:
                        bline = random.choice(moves2)
                        lines.remove(bline)
                        c.itemconfig(bline, fill='blue', width=10, activefill='blue')
                        count_blue_lines.append(bline)
                    elif not moves2:
                        bline = random.choice(usable_lines)
                        lines.remove(bline)
                        c.itemconfig(bline, fill='blue', width=10, activefill='blue')
                        count_blue_lines.append(bline)
            elif difficulty == 'hard':
                usable_lines = []
                moves = []
                for i in lines:
                    if c.itemcget(i, 'fill') == 'white':
                        usable_lines.append(i)
                recent_red = count_red_lines[-1]
                if count_blue_lines:
                    recent_blue = count_blue_lines[-1]
                for i in usable_lines:
                    for j in range(2):
                        for k in range(2): 
                            if abs(c.coords(i)[j * 2 - 1] - c.coords(recent_red)[k * 2 - 1]) < 2 and \
                                abs(c.coords(i)[j * 2] - c.coords(recent_red)[k * 2]) < 2:
                                moves.append(i)
                if moves:
                    bline = random.choice(moves)
                    lines.remove(bline)
                    c.itemconfig(bline, fill='blue', width=10, activefill='blue')
                    count_blue_lines.append(bline)
                elif not moves:
                    moves2 = []
                    for i in usable_lines:
                        for j in range(2):
                            for k in range(2): 
                                if abs(c.coords(i)[j * 2 - 1] - c.coords(recent_red)[k * 2 - 1]) < 2 and \
                                    abs(c.coords(i)[j * 2] - c.coords(recent_red)[k * 2]) < 2:
                                    moves2.append(i)
                    if moves2:
                        bline = random.choice(moves2)
                        lines.remove(bline)
                        c.itemconfig(bline, fill='blue', width=10, activefill='blue')
                        count_blue_lines.append(bline)
                    elif not moves2:
                        bline = random.choice(usable_lines)
                        lines.remove(bline)
                        c.itemconfig(bline, fill='blue', width=10, activefill='blue')
                        count_blue_lines.append(bline)
            

        new_window.mainloop()

    def open_instructions():
        ins = ctk.CTk()
        ins.geometry("400x400")
        ins.title("Instructions")

        frame_2 = ctk.CTkFrame(master=ins)
        frame_2.pack(pady=20, padx=60, fill="both", expand=True)

        label = ctk.CTkLabel(frame_2, text="Instructions", fg_color="transparent", font=("Helvetica", 20))
        label.place(y=25, x=90)

        label = ctk.CTkLabel(frame_2, text="The goal of the game is to make the longest line of your color.", fg_color="transparent", font=("Helvetica", 10))
        label.place(y=75, x=7)

        label = ctk.CTkLabel(frame_2, text="A line is only counted if it is unbroken and continuous.", fg_color="transparent", font=("Helvetica", 10))
        label.place(y=100, x=20)

        label = ctk.CTkLabel(frame_2, text="The game ends when all the lines have been placed.", fg_color="transparent", font=("Helvetica", 10))
        label.place(y=125, x=20)

        label = ctk.CTkLabel(frame_2, text="The player with the longest line wins.", fg_color="transparent", font=("Helvetica", 10))
        label.place(y=150, x=55)

        c = Canvas(frame_2, width=200, height=200, bg='white')
        c.place(y=225, x=75)

        lines = []
        unused_lines = []
        size = 7
        turn = 0

        for y in range(42, 163, 40):
            for i in range(3):
                line = c.create_line(42 + 40 * i, y, 82 + 40 * i, y, width=4, fill='white')
                lines.append(line)
                unused_lines.append(line)

        for x in range(42, 163, 40):
            for i in range(3):
                line = c.create_line(x, 42 + 40 * i, x, 82 + 40 * i, width=4, fill='white')
                lines.append(line)
                unused_lines.append(line)

        for i in range(4):
            for j in range(4):
                x, y = 40 + i * 40, 40 + j * 40
                c.create_oval(x, y, x + 4, y + 4, fill='black', width=5)
        
        while True:
            if turn >= 24:
                for i in lines:
                    c.itemconfig(i, fill='white')
                    ins.update()
                    time.sleep(0.04)
                    unused_lines.append(i)
                turn = 0
            line = random.choice(unused_lines)
            if turn%2 == 0:
                c.itemconfig(line, fill='red')
            else:
                c.itemconfig(line, fill='blue')
            ins.update()
            time.sleep(0.1)
            turn += 1
            unused_lines.remove(line)

    app.mainloop()

set_homepage()

win.mainloop()