#!/usr/bin/env python

import sys
sys.path.insert(0, "/home/pi/tictactoe/dependencies/Adafruit_Python_LED_Backpack")
sys.path.insert(0, "/home/pi/tictactoe/dependencies/Adafruit_Python_GPIO")
sys.path.insert(0, "/home/pi/tictactoe/dependencies/Adafruit_Python_PureIO")
sys.path.insert(0, "/home/pi/tictactoe/dependencies/Adafruit_Python_CharLCD")

import RPi.GPIO as GPIO

import time
import math
from Adafruit_LED_Backpack import Matrix8x8
import Adafruit_CharLCD as LCD
import os
import random

# Call this only when there is a change. 
# i.e. curr_input and new_input are different.
def find_change(curr_input, new_input):
    assert curr_input != new_input

    for i in range(9):
        a = curr_input[i]
        b = new_input[i]

        if a>b:
            return "Close", i+1

        if a<b:
            return "Open", i+1

    raise Exception("Should not have come here")

GPIO.setmode(GPIO.BCM)

# This is a list of GPIO pins connected to squares as numbered
# in the original project. 
gpio_list = [26, 19, 13, 12, 5, 22, 27, 17, 4]
for pin in gpio_list:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def init_input():
    global curr_input

    curr_input = [1] * 9

# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDPlate()

# create some custom characters
lcd.create_char(1, [2, 3, 2, 2, 14, 30, 12, 0])
lcd.create_char(2, [0, 1, 3, 22, 28, 8, 0, 0])
lcd.create_char(3, [0, 14, 21, 23, 17, 14, 0, 0])
lcd.create_char(4, [31, 17, 10, 4, 10, 17, 31, 0])
lcd.create_char(5, [8, 12, 10, 9, 10, 12, 8, 0])
lcd.create_char(6, [2, 6, 10, 18, 10, 6, 2, 0])
lcd.create_char(7, [31, 17, 21, 21, 21, 21, 17, 31])
lcd.clear()
lcd.message('RPI NOX game\nWelcome')

# Create display instance on default I2C address (0x70) and bus number.
display = Matrix8x8.Matrix8x8(address=0x70, busnum=1)
# check using I2cdetect -y 1  to make sure the address is 70, if not edit the line above to change it
# the correct address

# Initialize the display. Must be called once before using the display.
display.begin()
display.clear()
display.write_display()
   
# global constants
X = "X"
O = "O"
EMPTY = " "
TIE = "TIE"
NUM_SQUARES = 9

# Global variables for LCD Keypad
# Make list of button value, text, and backlight color.
buttons = ( (LCD.SELECT, 'Shutdown', (1,1,1)),  # Select
            (LCD.LEFT,   'No'  , (1,0,0)),    # Left
            (LCD.UP,     'Yes'    , (0,0,1)),  # Up
            (LCD.DOWN,   'No'  , (0,1,0)),   # Down
            (LCD.RIGHT,  'No' , (1,0,1)) )  # Right

level= 2 # expert
def ledon(sq):
    w=sq+1 # different numbering system
    x =int((w-1)/3)+1   # anodes numbers starts 1
    y =  (2+w)%3   # cathodes number start 0
    display.set_pixel(x, y, 1)  # switch on the LED
    display.write_display()

def ledoff(sq):
    w=sq+1 # different numbering system
    x =int((w-1)/3)+1   # anodes numbers starts 1
    y =  (2+w)%3   # cathodes number start 0
    display.set_pixel(x, y, 0)  # switch on the LED
    display.write_display()

def display_instruct():
    """Display game instructions."""

    lcd.clear()
    lcd.message(' Tic Tac Toe')
    time.sleep(1)  #give time to read message
    for l in range(9):
        ledon(l)
        time.sleep(0.25)
        ledoff(l)

    return
    
def get_LCD_button(question):
    lcd.clear()
    lcd.message(question)
    pressed = False
    print "in Question"
    time.sleep(1)  #give time to read message
    while pressed == False:
        # Loop through each button and check if it is pressed.
        for button in buttons:
            if lcd.is_pressed(button[0]):
                # Button is pressed, change the message and backlight.
                lcd.clear()
                lcd.message(button[1]) # prints button name
                but=button[1]
                time.sleep(1)  #give time to read message
                pressed = True 
    print but
    return but # sends name back

def get_level():
    global level
    lcd.clear()  
    print "in level"
    chlev =["Novice","Good","Expert"]  # level labels   
    while True:
        mess=" Level = "+str(chlev[level]) +"\n Yes or No?"
        getl = get_LCD_button(mess)
        if getl == "Shutdown": os.system("sudo shutdown -h now")
        if getl == "Yes": return
        level=(level+1)%3

    time.sleep(1)  #give time to read message

    while pressed == False:
        # Loop through each button and check if it is pressed.
        for button in buttons:
            if lcd.is_pressed(button[0]):
                # Button is pressed, change the message and backlight.
                lcd.clear()
                lcd.message(button[1]) # prints button name
                but=button[1]
                time.sleep(1)  #give time to read message
                pressed = True 

    print but
    return but # sends name back

def pieces():
    global mbrd 
    print "pieces"
    # mbrd = [0xFF,0xFF] 
    """Determine if player or computer goes first."""
    go_first = get_LCD_button(" Yes to go 1st\n any other I go ")
    print " go_first", go_first

    if go_first == "Yes":
        lcd.clear()
        lcd.message(' Yes\n')
        time.sleep(1) 
        human = X
        computer = O

    elif go_first == "Shutdown": os.system("sudo shutdown -h now")

    else:
        lcd.clear()
        lcd.message(' Me to go first')
        time.sleep(1) 
        computer = X
        human = O
    return computer, human

def new_board():
    """Create new game board."""
    board = []
    for square in range(NUM_SQUARES):
        board.append(EMPTY)
    return board

def check_clear():
    # checks that the board is clear before starting a game
    clrboard = False
    while not clrboard:
        clrboard = True 
        new_input = [GPIO.input(x) for x in gpio_list]
        if 0 in new_input:
            clrboard = False
            lcd.clear()
            lcd.message('  Please clear\n  The board')
            time.sleep(1)         

    lcd.clear()
    return

def legal_moves(board):
    """Create list of legal moves."""
    moves = []
    for square in range(NUM_SQUARES):
        if board[square] == EMPTY:
            moves.append(square)
    return moves

def make(move):
#Flash LED on square move +1 until registers
# light LED
    global curr_input

    w2=10
    print "led on move ", move
    ledon(move)
    # time.sleep(1)
    # Check to see if piece placed
    movecomp = False
    while movecomp != True :
        new_input = [GPIO.input(x) for x in gpio_list]
        if curr_input != new_input:
            # There has been a state change.
            dirx, w2 = find_change(curr_input, new_input)
            if dirx == "Close" and (w2-1) == move :
                movecomp = True  # if the square is closed in the right place we're done
                curr_input = new_input

    ledoff(move) # switch off the LED
    lcd.clear()
    lcd.message('    Thanks\n')
            
    return 

def winner(board):
    """Determine the game winner."""
    WAYS_TO_WIN = ((0, 1, 2),
                   (3, 4, 5),
                   (6, 7, 8),
                   (0, 3, 6),
                   (1, 4, 7),
                   (2, 5, 8),
                   (0, 4, 8),
                   (2, 4, 6))
    
    for row in WAYS_TO_WIN:
        if board[row[0]] == board[row[1]] == board[row[2]] != EMPTY:
            winner = board[row[0]]
            return winner

    if EMPTY not in board:
        return TIE

    return None

def human_move(board, human):
    global curr_input

    chcol =["A","B","C"]  # column labels
    print "in Human Move"
    lcd.clear()
    lcd.message(' Make Your Move')
    #time.sleep(1)  #give time to read message
    legal = legal_moves(board)
    move = None

    while move not in legal:
        new_input = [GPIO.input(x) for x in gpio_list]
        if curr_input != new_input:
            # There has been a state change.
            dirx, y = find_change(curr_input, new_input)
            if dirx == "Open":
                lcd.clear()
                print "Square: ", y, " is open"
                lcd.message('\nNo!, put it back')
                time.sleep(1)  #give time to read message
                lcd.clear()
                lcd.message(' Make Your Move')
            else:
                move=y-1 # different from test prog as need numbers 0-8
                curr_input = new_input
   
    print "Hmove " , move
    ledon(move)
    time.sleep(1)
    ledoff(move)
    lcd.clear()
    
    lcd.message(' Your move\n ')
    mess = chcol[move%3] + str(int(move/3)+1) 
    lcd.message(mess)
    
    time.sleep(1)  #give time to read message
    return move

def ranmove():
    rmove=random.randint(0,8)
    return rmove

def computer_move(board, computer, human):
    global mbrd,level
    print "in computer move."
    # make a copy to work with since function will be changing list
    board = board[:]
    # the best positions to have, in order
    BEST_MOVES = (4, 0, 2, 6, 8, 1, 3, 5, 7)

    lcd.clear()
    lcd.message(' Making my Move\n Place piece')
    time.sleep(1)  #give time to read message

    # Novice level moves randomly ignores win
    if level==0:
        while True:
            move= random.randint(0,8)
            if move in legal_moves(board):
                print move
                make(move)
                return move
   
    # if computer can win, take that move
    for move in legal_moves(board):
        board[move] = computer
        if winner(board) == computer:
            print move
            make(move)
            return move
        # done checking this move, undo it
        board[move] = EMPTY

    # if human can win, block that move
    for move in legal_moves(board):
        board[move] = human
        if winner(board) == human:
            print move
            make(move)
            return move
        # done checkin this move, undo it
        board[move] = EMPTY

# good level, blocks your winning move, but then moves randomly
    if level==1:
        while True:
            move= random.randint(0,8)
            if move in legal_moves(board):
                print move
                make(move)
                return move

    # since no one can win on next move, pick best open square
    for move in BEST_MOVES:
        if move in legal_moves(board):
            print move
            make(move)
            return move

def next_turn(turn):
    """Switch turns."""
    if turn == X:
        return O
    else:
        return X
    
def congrat_winner(the_winner, computer, human):
    """Congratulate the winner."""
    lcd.clear()
    if the_winner != TIE:       
        lcd.message("won!\n")
        
    else:
           lcd.message("It's a tie!\n")

    if the_winner == computer:
           lcd.message("I Win!!!!")

    elif the_winner == human:
       lcd.message("No, no! You won!")
    elif the_winner == TIE:
        lcd.message("Its a Tie!")
    time.sleep(5)  #give time to read message       

def main():
    global mbrd
    while True:
        init_input()

        display_instruct()
        
        check_clear()
        get_level()
        computer, human = pieces()
        turn = X
        board = new_board()

        while not winner(board):
            if turn == human:
                move = human_move(board, human)
                board[move] = human
            else:
                move = computer_move(board, computer, human)
                board[move] = computer
            
            turn = next_turn(turn)

        the_winner = winner(board)
        congrat_winner(the_winner, computer, human)


# start the program
main()
# raw_input("\n\nPress the enter key to quit.")
