from tkinter import *

def add(a,b):
    return a+b

def minus(a,b):
    if a>b:
        return a-b
    elif a<b:
        return b-a
    else:
        return a-b

def product(a,b):
    return a*b

def division(a,b):
    print("remainder is", a%b)
    return a/b

def factorial(num):
    # Python program to find the factorial of a number provided by the user.

    factorial = 1

    # check if the number is negative, positive or zero
    if num < 0:
        print("Sorry, factorial does not exist for negative numbers")
    elif num == 0:
        print("The factorial of 0 is 1")
    else:
        for i in range(1,num + 1):
            factorial = factorial*i
            print("The factorial of",num,"is",factorial)

def stone_paper_scissor():

    import random
    options = ["Rock", "Paper", "Scissors"]
    user_choice = input("Choose Rock, Paper, or Scissors: ")

    computer_choice = random.choice(options)

    print("You chose: ", user_choice)

    print("Computer chose: ", computer_choice)

    if user_choice == computer_choice:
        print("It's a tie!")

    elif user_choice == "Rock" and computer_choice == "Scissors":
        print("You win!")

    elif user_choice == "Paper" and computer_choice == "Rock":
        print("You win!")

    elif user_choice == "Scissors" and computer_choice == "Paper":
        print("You win!")

    else:
        print("Please choose a correct option")

def random_number_generater():
    import random as r
    rnum = r.randint(1,100)
    print("Random Number between 1 to 100 is:",rnum)

def random_number_picker():
    import random as r

    rnumber = r.randint(1,100)
    attempts = 0
    while True:
        number = int(input("Enter the random number: "))
        print("Your input is:",number)

        if number==rnumber:
            print(f"You did it right in {attempts} attempts")

        elif number<rnumber:
            print("Please type a large number")
            attempts = attempts+1

        elif number>rnumber:
            print("Please type a small number")
            attempts=attempts+1

        else:
            print("Please type a right number")


def circle(a):
    import turtle as t
    t.circle(a)
    t.done()

def square(a):
    import turtle as t
    t.forward(a)
    t.left(90)
    t.forward(a)
    t.left(90)
    t.forward(a)
    t.left(90)
    t.forward(a)
    t.mainloop()

def rectangle(a,b):
    import turtle as t
    t.forward(a)
    t.left(90)
    t.forward(b)
    t.left(90)
    t.forward(a)
    t.left(90)
    t.forward(b)

def root_of_quadratic_equation():
    import math as m

    a = float(input("Enter the value of a: "))
    b = float(input("Enter the value of b: "))
    c = float(input("Enter the value of c: "))

    D = (b*b)-(4*a*c)
    rd = m.sqrt(D)


    def one_zero():
        us = -b + rd
        fs = us/(2*a)
        print(fs)

    def sec_zero():
        us2 = -b - rd
        fs2 = us2 / (2*a)
        print(fs2)

    one_zero()
    sec_zero()

def quadratic_equation_formation():
    
    a = float(input("Enter the value of first zero: "))
    b = float(input("Enter the value of second zero: "))

    sum = a+b
    prod = a*b

    var1 = 'x'
    var2 = 'x^2'
    if sum<0:
        sn2 = '-'
    else:
        sn2 = '+'
    if prod<0:
        print(var2, sn2 ,sum,var1 , prod)
    else:
        print(var2, sn2 ,sum,var1,'+' , prod)

def name_of_colour_of_word_game():
    # import the modules
	import tkinter
	import random

	# list of possible colour.
	colours = ['Red','Blue','Green','Pink','Black',
			'Yellow','Orange','White','Purple','Brown']
	score = 0

	# the game time left, initially 30 seconds.
	timeleft = 30

	# function that will start the game.
	def startGame(event):
		
		if timeleft == 30:
			
			# start the countdown timer.
			countdown()
			
		# run the function to
		# choose the next colour.
		nextColour()

	# Function to choose and
	# display the next colour.
	def nextColour():

		# use the globally declared 'score'
		# and 'play' variables above.
		global score
		global timeleft

		# if a game is currently in play
		if timeleft > 0:

			# make the text entry box active.
			e.focus_set()

			# if the colour typed is equal
			# to the colour of the text
			if e.get().lower() == colours[1].lower():
				
				score += 1

			# clear the text entry box.
			e.delete(0, tkinter.END)
			
			random.shuffle(colours)
			
			# change the colour to type, by changing the
			# text _and_ the colour to a random colour value
			label.config(fg = str(colours[1]), text = str(colours[0]))
			
			# update the score.
			scoreLabel.config(text = "Score: " + str(score))


	# Countdown timer function
	def countdown():

		global timeleft

		# if a game is in play
		if timeleft > 0:

			# decrement the timer.
			timeleft -= 1
			
			# update the time left label
			timeLabel.config(text = "Time left: "
								+ str(timeleft))
									
			# run the function again after 1 second.
			timeLabel.after(1000, countdown)


	# Driver Code

	# create a GUI window
	root = tkinter.Tk()

	# set the title
	root.title("COLORGAME")

	# set the size
	root.geometry("375x200")

	# add an instructions label
	instructions = tkinter.Label(root, text = "Type in the colour"
							"of the words, and not the word text!",
										font = ('Helvetica', 12))
	instructions.pack()

	# add a score label
	scoreLabel = tkinter.Label(root, text = "Press enter to start",
										font = ('Helvetica', 12))
	scoreLabel.pack()

	# add a time left label
	timeLabel = tkinter.Label(root, text = "Time left: " +
				str(timeleft), font = ('Helvetica', 12))
					
	timeLabel.pack()

	# add a label for displaying the colours
	label = tkinter.Label(root, font = ('Helvetica', 60))
	label.pack()

	# add a text entry box for
	# typing in colours
	e = tkinter.Entry(root)

	# run the 'startGame' function
	# when the enter key is pressed
	root.bind('<Return>', startGame)
	e.pack()

	# set focus on the entry box
	e.focus_set()

	# start the GUI
	root.mainloop()

def halloween_wish_and_pumpkin_creation():

    import turtle
    import time

    window = turtle.Screen()
    window.bgcolor("black")

    # Whole pumpkin
    pumpkin = turtle.Turtle()
    pumpkin.hideturtle()
    pumpkin.color("orange")
    pumpkin.dot(200)

    # The turtle to "carve" the pumpkin
    carver = turtle.Turtle()

    # "Flatten" the lower part of the pumpkin
    carver.penup()
    carver.setposition(-200, -100)
    carver.pensize(60)
    carver.pendown()
    carver.forward(600)
    carver.pensize(2)

    def carve_pumpkin(colour):
        carver.color(colour)

        # Make eyes
    def make_eye(start, orientation):
        carver.setheading(0)
        carver.penup()
        carver.setposition(*start)
        carver.pendown()
        carver.begin_fill()
        carver.forward(orientation * 40)
        carver.setheading(orientation * 135)
        carver.forward(orientation * 70)
        carver.end_fill()
    
    make_eye((-50, 20), 1)
    make_eye((50, 20), -1)
    
    # Make mouth
    carver.penup()
    carver.setposition(-50, -30)
    carver.setheading(45)
    carver.pendown()
    carver.pensize(1)
    carver.begin_fill()
    for _ in range(5):
        carver.forward(15)
        carver.right(90)
        carver.forward(15)
        carver.left(90)
    carver.setheading(260)
    carver.forward(20)
    carver.setheading(180)
    carver.forward(99)
    carver.end_fill()

    # Make nose
    carver.penup()
    carver.setposition(0, 0)
    carver.setheading(90)
    carver.shape("triangle")
    carver.stamp()

    carve_pumpkin("black")
    
    # Write text on animation
    text = turtle.Turtle()
    text.hideturtle()
    text.color("orange")
    text.penup()
    text.sety(175)
    text.write("Happy Halloween", font=("Trattatello", 60, "bold"), align="center")

    window.tracer(0)
    start = time.time()
    count = 0
    colours = "yellow", "black"
    while True:
        if time.time() - start > 1:
            carve_pumpkin(colours[count % 2])
            window.update()
            count += 1
            start = time.time() # Reset timer


        turtle.done()


def text_to_speech():
    import pyttsx3
    text = input("Enter the text which you want the computer to speak")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_system_name_and_ip_address():
    import socket    
    hostname = socket.gethostname()    
    IPAddr = socket.gethostbyname(hostname)    
    print("Your Computer Name is:" + hostname)    
    print("Your Computer IP Address is:" + IPAddr) 
    #How to get the IP address of a client using socket

def eye_track_and_mouse_control_with_eye():
    import cv2
    import mediapipe as mp
    import pyautogui as pg

    c = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w,screen_h = pg.size()

    while True:
        _,frame = c.read()
        frame = cv2.flip(frame,1)
        rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h,frame_w,_ = frame.shape

        if landmark_points:
            landmarks = landmark_points[0].landmark

            for id,landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)

                cv2.circle(frame, (x,y),3,(0,255,0))
                if id==1:
                    screen_x = screen_w * landmark.x
                    screen_y = screen_h * landmark.y
                    pg.moveTo(screen_x,screen_y)

            left = [landmarks[145],landmarks[159]]

            for landmark in left:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame,(x,y),3,(0,255,255))

            if (left[0].y-left[1].y)<0.004:
                pg.click()
                pg,exit(1)

        cv2.imshow('eye controlled mouse', frame)
        cv2.waitKey(1)

def stopwatch():
    import os    
    import time as t
    second = 0    
    minute = 0    
    hours = 0    
    while(True):    
        print('\n\n\n\n\n\n\n')    
        print('\t\t\t\t-------------')    
        print('\t\t\t\t  %d : %d : %d '%(hours,minute,second))    
        print('\t\t\t\t-------------')    
        t.sleep(1)    
        second+=1    
        if(second == 60):    
            second = 0    
            minute+=1    
        if(minute == 60):    
            minute = 0    
            hour+=1;    
        os.system('cls')              

def forest_adventure_game():
    def start_game():
        print("Welcome to the text adventure game!")
        print("You find yourself in a dark forest, lost and alone.")
        print("What would you like to do?")
        print("1. Look for a way out of the forest")
        print("2. Build a fire and stay put")
        choice = input("> ")
        if choice == "1":
            find_way_out()
        elif choice == "2":
            build_fire()
        else:
            print("Invalid choice, try again.")
            start_game()

    def find_way_out():
        print("You start looking for a way out of the forest.")
        print("After some time, you come across a fork in the path.")
        print("Which path do you take?")
        print("1. Left")
        print("2. Right")
        choice = input("> ")
        if choice == "1":
            print("You take the left path and eventually find a road leading out of the forest.")
            print("Congratulations, you've escaped the forest!")
        elif choice == "2":
            print("You take the right path and get deeper into the forest. You eventually get lost and starve.")
            print("Game Over.")
        else:
            print("Invalid choice, try again.")
            find_way_out()

    def build_fire():
        print("You build a fire and wait for rescue.")
        print("After some time, a rescue team finds you.")
        print("Congratulations, you've survived!")

    start_game()

def zero_cutties_game():
    import random

    def draw_board(board):
        print("\n".join(" ".join(row) for row in board))

    def play_game():
        # Initialize the board
        board = [["." for _ in range(3)] for _ in range(3)]

        # Play the game
        while True:
            draw_board(board)
            row = int(input("Enter row (0-2): "))
            col = int(input("Enter column (0-2): "))
            if board[row][col] == ".":
                board[row][col] = "X"
            else:
                print("Invalid move")
                continue
            computer_row = random.randint(0, 2)
            computer_col = random.randint(0, 2)
            if board[computer_row][computer_col] == ".":
                board[computer_row][computer_col] = "O"
            else:
                print("Invalid move")
                continue

    play_game()

def tic_tac_tor_in_tkinter():


    root = Tk()
    root.geometry("330x550")
    root.title("Tic Tac Toe")

    root.resizable(0,0)

    frame1 = Frame(root)
    frame1.pack()
    titleLabel = Label(frame1 , text="Tic Tac Toe" , font=("Arial" , 26) , bg="orange" , width=16 )
    titleLabel.grid(row=0 , column=0)

    optionFrame = Frame(root , bg="grey")
    optionFrame.pack()

    frame2 = Frame(root , bg="yellow")
    frame2.pack()

    board = { 1:" " , 2:" " , 3:" ",
            4:" " , 5:" " , 6:" ",
            7:" " , 8:" " , 9:" " }

    turn = "x"
    game_end = False
    mode = "singlePlayer"

    def changeModeToSinglePlayer(): 
        global mode 
        mode = "singlePlayer"
        singlePlayerButton["bg"] = "lightgreen"
        multiPlayerButton["bg"] = "lightgrey"

    def changeModeToMultiplayer():
        global mode 
        mode = "multiPlayer"
        multiPlayerButton["bg"] = "lightgreen"
        singlePlayerButton["bg"] = "lightgrey"

    def updateBoard():
        for key in board.keys():
            buttons[key-1]["text"] = board[key]

    def checkForWin(player):
        # rows
        if board[1] == board[2] and board[2] == board[3] and board[3] == player:
            return True
        
        elif board[4] == board[5] and board[5] == board[6] and board[6] == player:
            return True
        
        elif board[7] == board[8] and board[8] == board[9] and board[9] == player:
            return True

        # columns
        elif board[1] == board[4] and board[4] == board[7] and board[7] == player:
            return True
        
        elif board[2] == board[5] and board[5] == board[8] and board[8] == player:
            return True
        
        elif board[3] == board[6] and board[6] == board[9] and board[9] == player:
            return True
        
        # diagonals
        elif board[1] == board[5] and board[5] == board[9] and board[9] == player:
            return True
        
        elif board[3] == board[5] and board[5] == board[7] and board[7] == player:
            return True
        

        return False

    def checkForDraw():
        for i in board.keys():
            if board[i] == " ":
                return False
        
        return True

    def restartGame():
        global game_end
        game_end = False
        for button in buttons:
            button["text"] = " "

        for i in board.keys():
            board[i] = " "

        titleLabel = Label(frame1 , text="Tic Tac Toe" , font=("Arial" , 30) , bg="orange" , width=15 )
        titleLabel.grid(row=0 , column=0)

    def minimax(board , isMaximizing):
        
        if checkForWin("o"):
            return 1 
        
        if checkForWin("x"):
            return -1
        
        if checkForDraw():
            return 0
        
        if isMaximizing:
            bestScore = -100

            for key in board.keys():
                if board[key] == " ":
                    board[key] = "o"
                    score = minimax(board , False) # minimax
                    board[key] = " "
                    if score > bestScore : 
                        bestScore = score 
            
            return bestScore
        
        else:
            bestScore = 100

            for key in board.keys():
                if board[key] == " ":
                    board[key] = "x"
                    score = minimax(board , True) # minimax
                    board[key] = " "
                    if score < bestScore : 
                        bestScore = score 
            
            return bestScore

    def playComputer():
        bestScore = -100
        bestMove = 0

        for key in board.keys():
            if board[key] == " ":
                board[key] = "o"
                score = minimax(board , False) # minimax
                board[key] = " "
                if score > bestScore : 
                    bestScore = score 
                    bestMove = key

        board[bestMove] = "o"

    # Function to play
    def play(event):
        global turn,game_end
        if game_end:
            return
        
        button = event.widget
        buttonText = str(button)
        clicked = buttonText[-1]
        if clicked == "n" :
            clicked = 1
        else :
            clicked = int(clicked)
        
        if button["text"] == " ":
            if turn == "x" :
                board[clicked] = turn
                if checkForWin(turn):
                    winningLabel = Label(frame1 , text=f"{turn} wins the game", bg="orange", font=("Arial" , 26),width=16 )
                    winningLabel.grid(row = 0 , column=0 , columnspan=3)
                    game_end = True

                turn = "o"

                updateBoard()

                if mode == "singlePlayer":

                    playComputer()

                    if checkForWin(turn):
                        winningLabel = Label(frame1 , text=f"{turn} wins the game", bg="orange", font=("Arial" , 26),width=16   )
                        winningLabel.grid(row = 0 , column=0 , columnspan=3)
                        game_end = True

                    turn = "x"

                    updateBoard()

            
                
            else:
                board[clicked] = turn
                updateBoard()
                if checkForWin(turn):
                    winningLabel = Label(frame1 , text=f"{turn} wins the game" , bg="orange", font=("Arial" , 26),width=16)
                    winningLabel.grid(row = 0 , column=0 , columnspan=3)
                    game_end = True
                turn = "x"

            
            if checkForDraw():
                drawLabel = Label(frame1 , text=f"Game Draw" , bg="orange", font=("Arial" , 26), width = 16)
                drawLabel.grid(row = 0 , column=0 , columnspan=3)
            
    # ------ UI --------

    # Change Mode options 

    singlePlayerButton = Button(optionFrame , text="SinglePlayer" , width=13 , height=1 , font=("Arial" , 15) , bg="lightgrey" , relief=RAISED , borderwidth=5 , command=changeModeToSinglePlayer)
    singlePlayerButton.grid(row=0 , column=0 , columnspan=1 , sticky=NW)

    multiPlayerButton = Button(optionFrame , text="Multiplayer" , width=13 , height=1 , font=("Arial" , 15) , bg="lightgrey" , relief=RAISED , borderwidth=5 , command=changeModeToMultiplayer )
    multiPlayerButton.grid(row=0 , column=1 , columnspan=1 , sticky=NW)

    # Tic Tac Toe Board 

    #  First row 

    button1 = Button(frame2 , text= " " , width=4 , height=2  , font=("Arial" , 30) , bg="yellow" , relief=RAISED , borderwidth=5)
    button1.grid(row = 0 , column=0)
    button1.bind("<Button-1>" , play)

    button2 = Button(frame2 , text= " " , width=4 , height=2  , font=("Arial" , 30), bg="yellow" , relief=RAISED , borderwidth=5 )
    button2.grid(row = 0 , column=1)
    button2.bind("<Button-1>" , play)

    button3 = Button(frame2 , text= " " , width=4 , height=2  , font=("Arial" , 30), bg="yellow" , relief=RAISED , borderwidth=5 )
    button3.grid(row = 0 , column=2)
    button3.bind("<Button-1>" , play)

    #  second row 

    button4 = Button(frame2 , text= " " , width=4 , height=2  , font=("Arial" , 30), bg="yellow" , relief=RAISED , borderwidth=5 )
    button4.grid(row = 1 , column=0)
    button4.bind("<Button-1>" , play)

    button5 = Button(frame2 , text= " " , width=4 , height=2  , font=("Arial" , 30), bg="yellow" , relief=RAISED , borderwidth=5 )
    button5.grid(row = 1 , column=1)
    button5.bind("<Button-1>" , play)

    button6 = Button(frame2 , text= " " , width=4 , height=2  , font=("Arial" , 30), bg="yellow" , relief=RAISED , borderwidth=5 )
    button6.grid(row = 1 , column=2)
    button6.bind("<Button-1>" , play)

    #  third row 

    button7 = Button(frame2 , text= " " , width=4 , height=2  , font=("Arial" , 30) , bg="yellow" , relief=RAISED , borderwidth=5)
    button7.grid(row = 2 , column=0)
    button7.bind("<Button-1>" , play)

    button8 = Button(frame2 , text= " " , width=4 , height=2  , font=("Arial" , 30), bg="yellow" , relief=RAISED , borderwidth=5 )
    button8.grid(row = 2 , column=1)
    button8.bind("<Button-1>" , play)

    button9 = Button(frame2 , text= " " , width=4 , height=2  , font=("Arial" , 30) , bg="yellow" , relief=RAISED , borderwidth=5)
    button9.grid(row = 2 , column=2)
    button9.bind("<Button-1>" , play)

    restartButton = Button(frame2 , text="Restart Game" , width=19 , height=1 , font=("Arial" , 20) , bg="Green" , relief=RAISED , borderwidth=5 , command=restartGame )
    restartButton.grid(row=4 , column=0 , columnspan=3)

    buttons = [button1 , button2 , button3 , button4 , button5 , button6 , button7 , button8, button9]

    root.mainloop()

