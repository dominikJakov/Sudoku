from sudoku import Sudoku
from tkinter import *
import random

global player_sudoku # 2D array containg numbers that the player put inisde the sudoku
global puzzle # containing both the original (starting) sudoku and the finished sudoku
global difficulty # the difficulty that the player choose

# Function for game buttons
def get_hint(): # get hint button
    p = []
    for x in range(len(player_sudoku)):
        for y in range(len(player_sudoku[x])):
            if player_sudoku[x][y].get() == "":
                p.append([player_sudoku[x][y],puzzle.solve().board[x][y]])
    n = random.randint(0, len(p)-1)
    p[n][0].insert(0,p[n][1])
    check_if_game_finished()

def clear_input(): # clear values button
    for x in range(len(player_sudoku)):
        for y in range(len(player_sudoku[x])):
            if puzzle.board[x][y] == None:    
                    player_sudoku[x][y].delete(0,"end")
    check_entered_value()


def load_from_file(): # load from file button
    load_sudoku_from_file()
    reset_player_sudoku()

def generate_new(): # generate new button
    create_sudoku_puzzle(random.randint(1, 9))
    reset_player_sudoku()
    
def show_solution(): # show solution
    for x in range(len(player_sudoku)):
        for y in range(len(player_sudoku[x])):
            player_sudoku[x][y].delete(0,"end")
            player_sudoku[x][y].insert(0,puzzle.solve().board[x][y])
    finish_window()


def value_entered(e): # called when value entered
    check_entered_value()
    check_if_game_finished()
        
def finish_window(): # Win window
    win_root = Tk()
    win_root.title("Confirmation")
    win_root.geometry("250x150")
    win_root.resizable(False, False)
    label = Label(win_root, text="Congratulation")
    label.place(x= 30 , y = 15, height = 25, width =200)
    # main menu Button 
    main_menu_button = Button (win_root, text= "OK",command=lambda:[win_root.destroy()])
    main_menu_button.place(x= 113 , y = 60, height = 25, width = 70)
     
def reset_player_sudoku(): # reset the sudoku
    solved = puzzle.solve().board
    for x in range(len(player_sudoku)):
        for y in range(len(player_sudoku)):
            player_sudoku[x][y].config({"state": "normal"})
            player_sudoku[x][y].delete(0,"end") 
            if puzzle.board[x][y] != None:
                player_sudoku[x][y].insert(0,puzzle.board[x][y])
                player_sudoku[x][y].config({"state": "readonly"})
            else:
                player_sudoku[x][y].insert(0,"")
    check_entered_value()

                      
def user_confirmation(opt): # user confirmation window 
    cof_root = Tk()
    cof_root.title("Confirmation")
    cof_root.geometry("250x150")
    cof_root.resizable(False, False)
    time_label = Label(cof_root, text="Do you want to load a new puzzle?")
    time_label.place(x= 30 , y = 15, height = 25, width =200)
    # get_hint Button 
    if opt == 1:
        yes_button = Button (cof_root, text= "Yes",command= lambda:[load_from_file(), cof_root.destroy()]) 
    else:
        yes_button = Button (cof_root, text= "Yes",command= lambda:[generate_new(), cof_root.destroy()]) 
    yes_button.place(x= 40 , y = 60, height = 25, width = 50)
    # solution Button 
    no_button = Button (cof_root, text= "No",command=cof_root.destroy) 
    no_button.place(x= 160 , y = 60, height = 25, width = 50)

def check_entered_value(): # check entered value
    d = puzzle.solve().board
    for x in range(len(player_sudoku)):
        for y in range(len(player_sudoku[x])):
            if player_sudoku[x][y].get() != "":
                if int(player_sudoku[x][y].get()) != d[x][y]:
                    player_sudoku[x][y].config({"background": "red"})
                else:
                    player_sudoku[x][y].config({"background": "white"})
            else:
                player_sudoku[x][y].config({"background": "white"})

def check_if_game_finished(): # check if game finished
    for x in range(len(player_sudoku)):
        for y in range(len(player_sudoku[x])):
                if player_sudoku[x][y].get() == "" or int(player_sudoku[x][y].get()) != puzzle.solve().board[x][y]:
                    return False
    finish_window()
            
def main_game_loop(): # main game window
    global difficulty
    def timer(count): # timer function
        s = str(count%60)
        if int(s) < 10:
            s = "0"+str(count%60)
        m = str(count // 60)
        if int(m) < 10:
            m = "0"+str(m)
        h = str(int(m) // 60)
        if int(h) < 10:
            h = "0"+str(h)
            
        time = h +":"+m+":"+s
        time_label.config({"text": "Timer: " + time})
        game_root.after(1000, timer,count+1)
        
    game_root = Tk()
    game_root.title("Play Sudoku")
    game_root.geometry("600x650")
    game_root.resizable(False, False)
    #playing label
    lab = Label(game_root, text="You are now playing sudoku")
    lab.grid(row= 0, column= 0, sticky= E)
    # difficulty level label
    difficulty_label = Label(game_root, text="  difficulty level = " + str(difficulty))
    difficulty_label.grid(row= 0, column= 1, sticky= E)
    # time label
    time_label = Label(game_root, text="Time: ")
    time_label.grid(row= 0, column= 4, sticky= W+E)
    # get_hint Button 
    get_hint_button = Button (game_root, text= "Get Hint",command = get_hint) 
    get_hint_button.grid(row=1,column=0,padx = 30,pady = (20,10),ipady= 10)
    # solution Button 
    solution_button = Button (game_root, text= "Show solution",command = show_solution) 
    solution_button.grid(row=1,column=1,padx = 10,pady = (20,10),ipady= 10)
    # load from file Button 
    load_file_button = Button (game_root, text= "Load from file",command = lambda : user_confirmation(1)) 
    load_file_button.grid(row=1,column=2,padx = 10,pady = (20,10),ipady= 10)
    # Generate new Button 
    generate_new_button = Button (game_root, text= "Generate new",command=lambda : user_confirmation(2)) 
    generate_new_button.grid(row=1,column=3,padx = 10,pady = (20,10),ipady= 10)
    # Clear input Button 
    clear_button = Button (game_root, text= "Clear input",command=clear_input) 
    clear_button.grid(row=1,column=4,padx = 10,pady = (20,10),ipady= 10)
    display_the_board(game_root)
    game_root.bind("<KeyPress>", value_entered)
        
    timer(0)
    mainloop()
    

# Game window
def display_the_board(game_root):
    global player_sudoku
    global puzzle
    player_sudoku = []
    x_offset = 0
    y_offset = 0
    x_start_pos = 50
    y_start_pos = 100
    width_size = 45
    height_size = 45
    creating_player_sudoku()
    for i in range(9):
        if (i) % 3 == 0:
                x_offset += 15
        y_offset = 0
        for j in range(9):
            if j % 3 == 0:
                y_offset += 15
            name = StringVar(game_root, value=puzzle.board[j][i])
            if puzzle.board[j][i] == None:
                player_sudoku[j][i] = Entry(game_root,font=("Calibri 16"),justify='center')
            else:
                player_sudoku[j][i] = Entry(game_root,font=("Calibri 16"),textvariable=name,state='readonly',justify='center')
            player_sudoku[j][i].place(x = x_start_pos + x_offset + width_size * i,
                                      y = y_start_pos + y_offset + height_size * j,
                                      height = height_size, width = width_size)
             
def creating_player_sudoku(): # create player sudoku
    global player_sudoku
    for i in range(9):
        player_sudoku.append([])
        for j in range(9):
            player_sudoku[i].append(j)
    
def start_sudoku_from_file(): # start game with loaded sudoku file
    load_sudoku_from_file()
    main_game_loop()
    
def load_sudoku_from_file(): # load sudoku from file
    global puzzle
    global difficulty
    puzzle = []
    difficulty = 0
    with open("sudoku.txt") as f:
        for line in f:
            l = [ None if int(x) == 0 else int(x) for x in line.strip()]
            puzzle.append(l)
    puzzle = Sudoku(3,3, board=puzzle)
    
def create_sudoku_puzzle(diff): # create generated sudoku
    global puzzle
    global difficulty
    difficulty = diff
    puzzle = Sudoku(3, seed = random.randint(0, 100)).difficulty(diff/10)
    
def start_sudoku_puzzle(diff): # start game with generated sudoku
    create_sudoku_puzzle(diff)
    main_game_loop()


def main():
    root = Tk()
    root.title("Play Sudoku")
    root.geometry("250x250")
    root.resizable(False, False)
    # Generate label
    label = Label(root, text="Generate a new puzzle",font =("Calibri 13"))
    label.grid(row=0,column=0,columnspan = 2,sticky=E+W)
    # Slider label
    slider_label = Label(root, text="Difficulty:",font =("Calibri 13"))
    slider_label.grid(row=1,column=0,padx = 0,pady = (20,10),ipady= 10)
    # Slider
    difficulty_slider = Scale(root, from_=1, to=9,orient=HORIZONTAL)
    difficulty_slider.set(5)
    difficulty_slider.grid(row=1,column=1,sticky=W)
    # PLay Button 
    play_button = Button (root, text= "Generate and play",font =("Calibri 10"),command =lambda : start_sudoku_puzzle(difficulty_slider.get())) 
    play_button.grid(row=2,column=0,padx = 80,columnspan = 2,pady = (10,10),sticky=E+W)
    # or label
    or_label = Label(root, text="Or")
    or_label.grid(row=3,column=0,columnspan = 2,sticky=E+W)
    # Import puzzle 
    import_puzzle_button = Button (root, text= "Load puzzle from a text file",font =("Calibri 10"),command = start_sudoku_from_file) 
    import_puzzle_button.grid(row=4,column=0,padx = 55,columnspan = 3,pady = (10,10),sticky=W)
    # Settings value
    mainloop()

main()


