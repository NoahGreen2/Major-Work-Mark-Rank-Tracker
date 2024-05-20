from tkinter import *

win = Tk()
win.title("Mega Tic Tac Toe")
win.geometry("600x600")
win.resizable(False, False)

# Create a canvas
c = Canvas(win, width=600, height=600, bg="white")
c.pack()

# Create a big board
for x in range(0, 600, 200):
    c.create_line(x, 0, x, 600, width=2)
    c.create_line(0, x, 600, x, width=2)

playable_box = 4

colours = ["red", "blue"]
go = 0

squares = []

def check_match(box):
    if c.itemcget(squares[box*9], "fill").strip() == c.itemcget(squares[box*9+1], "fill").strip() == c.itemcget(squares[box*9+2], "fill").strip() != "white":
        for i in range(9):
            c.itemconfig(squares[box*9+i], fill=colours[go%2])
    elif c.itemcget(squares[box*9], "fill").strip() == c.itemcget(squares[box*9+3], "fill").strip() == c.itemcget(squares[box*9+6], "fill").strip() != "white":
        for i in range(9):
            c.itemconfig(squares[box*9+i], fill=colours[go%2])
    elif c.itemcget(squares[box*9], "fill").strip() == c.itemcget(squares[box*9+4], "fill").strip() == c.itemcget(squares[box*9+8], "fill").strip() != "white":
        for i in range(9):
            c.itemconfig(squares[box*9+i], fill=colours[go%2])
    elif c.itemcget(squares[box*9+2], "fill").strip() == c.itemcget(squares[box*9+4], "fill").strip() == c.itemcget(squares[box*9+6], "fill").strip() != "white":
        for i in range(9):
            c.itemconfig(squares[box*9+i], fill=colours[go%2])
    elif c.itemcget(squares[box*9+1], "fill").strip() == c.itemcget(squares[box*9+4], "fill").strip() == c.itemcget(squares[box*9+7], "fill").strip() != "white":
        for i in range(9):
            c.itemconfig(squares[box*9+i], fill=colours[go%2])
    elif c.itemcget(squares[box*9+3], "fill").strip() == c.itemcget(squares[box*9+4], "fill").strip() == c.itemcget(squares[box*9+5], "fill").strip() != "white":
        for i in range(9):
            c.itemconfig(squares[box*9+i], fill=colours[go%2])
    elif c.itemcget(squares[box*9+6], "fill").strip() == c.itemcget(squares[box*9+7], "fill").strip() == c.itemcget(squares[box*9+8], "fill").strip() != "white":
        for i in range(9):
            c.itemconfig(squares[box*9+i], fill=colours[go%2])
    elif c.itemcget(squares[box*9+2], "fill").strip() == c.itemcget(squares[box*9+5], "fill").strip() == c.itemcget(squares[box*9+8], "fill").strip() != "white":
        for i in range(9):
            c.itemconfig(squares[box*9+i], fill=colours[go%2])

def play_square(rect):
    global playable_box, go
    c.itemconfig(rect, fill=colours[go%2], activefill=colours[go%2])
    check_match(playable_box)
    go += 1
    playable_box = squares.index(rect)%9


def check_click(rect):
    global playable_box
    if squares.index(rect)//9 == playable_box:
        if c.itemcget(rect, "fill") == "white":
            play_square(rect)

# Create the rectangles
for i in range(3):
    for j in range(3):
        for x in range(i*200+25, i*200+175, 50):
            for y in range(j*200+25, j*200+175, 50):
                rect = c.create_rectangle(x, y, x+50, y+50, fill="white", width=0, activefill="light blue")
                squares.append(rect)
                c.tag_bind(rect, "<Button-1>", lambda event, rect=rect: check_click(rect))
                

# Create a small board
for i in range(3):
    for j in range(3):
        for x in range(i*200+75, i*200+175, 50):
            c.create_line(x, j*200+25, x, j*200+175, width=1)
        for y in range(j*200+75, j*200+175, 50):
            c.create_line(i*200+25, y, i*200+175, y, width=1)

win.mainloop()