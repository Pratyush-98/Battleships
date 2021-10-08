"""
Battleship Project
Name:
Roll No:
"""

import battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["rows"]=10
    data["cols"]=10
    data["Board_Size"]=500
    data["CellSize"]=data["Board_Size"]/data["rows"]
    data["numShips"]=5
    data["User_Board"]=emptyGrid(data["rows"],data["cols"])
    data["Comp_Board"]= addShips(emptyGrid(data["rows"],data["cols"]),data["numShips"])
    data["TempShip"]= []
    data["Userships"]=0
    data["Winner"]=None
    data["Max_Turns"]=50
    data["Number_Of_Turns"]=0
    return 


'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data,userCanvas,data["User_Board"],True)
    drawShip(data,userCanvas,data["TempShip"])
    drawGrid(data,compCanvas,data["Comp_Board"],False)  
    drawGameOver(data,compCanvas)
    return


'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None

'''
def keyPressed(data, event):
    if event.keycode==13:
        makeModel(data)
    pass


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    if data["Winner"]!=None:
        return None
    mouse=getClickedCell(data,event)
    if board=="user":
        clickUserBoard(data,mouse[0],mouse[1])
    elif board=="comp":
        runGameTurn(data,mouse[0],mouse[1])
    pass

#### WEEK 1 ####

'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    grid=[]
    for i in range(rows):
        a=[]
        for j in range(cols):
            a.append(EMPTY_UNCLICKED)
        grid.append(a)
    return grid 




'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    rows=random.randint(1,8)
    cols=random.randint(1,8)
    a=random.randint(0,1)
    ship=[]
    if a==0:
        ship=[[rows-1,cols],[rows,cols],[rows+1,cols]]
    else:
        ship=[[rows,cols-1],[rows,cols],[rows,cols+1]]
    return ship

'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    for i in ship:
        if grid[i[0]][i[1]]!=EMPTY_UNCLICKED:
            return False
    return True

# grid = [ [1, 1, 2, 1], [1, 1, 2, 1], [1, 1, 2, 1], [2, 2, 2, 1] ]
# ship =[[0, 0], [1, 0], [2, 0]]

'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    ship_count=0
    while ship_count!=numShips:
        ship=createShip()
        if checkShip(grid,ship):
            for i in ship:
                grid[i[0]][i[1]]=SHIP_UNCLICKED
            ship_count+=1
    return grid


'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    size=data["CellSize"]
    for row in range(data["rows"]):
        for col in range(data["cols"]):
            if grid[row][col]==SHIP_UNCLICKED:
                canvas.create_rectangle(size*col,size*row,size*(col+1),size*(row+1),fill="yellow")
                if showShips==False:
                   canvas.create_rectangle(size*col,size*row,size*(col+1),size*(row+1),fill="blue")
            elif grid[row][col]==EMPTY_UNCLICKED:
                canvas.create_rectangle(size*col,size*row,size*(col+1),size*(row+1),fill="blue")
            elif grid[row][col]==SHIP_CLICKED:
                canvas.create_rectangle(size*col,size*row,size*(col+1),size*(row+1),fill="red")   
            elif grid[row][col]==EMPTY_CLICKED:
                canvas.create_rectangle(size*col,size*row,size*(col+1),size*(row+1),fill="white")
    return 



### WEEK 2 ###

'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    ship.sort()
    if ship[0][1]==ship[2][1] and ship[1][1]==ship[2][1]:
        if ship[0][0]==ship[1][0]-1 and ship[2][0]==ship[1][0]+1 :
            return True
    return False


'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    ship.sort()
    if ship[0][0]==ship[2][0] and ship[1][0]==ship[2][0]:
        if ship[0][1]==ship[1][1]-1 and ship[2][1]==ship[1][1]+1 :
            return True
    return False



'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    x=int(event.x//data["CellSize"])
    y=int(event.y//data["CellSize"])
    return [y,x]



'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    size=data["CellSize"]
    for row in ship:
        canvas.create_rectangle(size*(row[1]),size*(row[0]),size*(row[1]+1),size*(row[0]+1),fill="white")
    return


'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if checkShip(grid,ship):
        if isVertical(ship):
            return True
        elif isHorizontal(ship):
            return True
    return False

'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    Userboard=data["User_Board"]
    Tempship=data["TempShip"]
    if shipIsValid(Userboard,Tempship):
        for row in Tempship:
            Userboard[row[0]][row[1]]=SHIP_UNCLICKED
        data["Userships"]+=1
    else:
        print("ship is not valid")
    data["TempShip"]=[]
    return 


'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if data["Userships"]==5:
        print("start the game")
        return 
    if data["TempShip"]==[row,col]:
        return
    else:
        data["TempShip"].append([row,col])
    if len(data["TempShip"])==3:
        placeShip(data)
    return


### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col]==SHIP_UNCLICKED:
        board[row][col]=SHIP_CLICKED
    if board[row][col]==EMPTY_UNCLICKED:
        board[row][col]=EMPTY_CLICKED
    if isGameOver(board):
        data["Winner"]=player
    return


'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    comp=data["Comp_Board"][row][col]
    if comp==SHIP_CLICKED or comp==EMPTY_CLICKED:
        return
    else:
        updateBoard(data,data["Comp_Board"],row,col,"user")
    Guess=getComputerGuess(data["User_Board"])
    updateBoard(data,data["User_Board"],Guess[0],Guess[1],"comp")
    data["Number_Of_Turns"]+=1
    if data["Number_Of_Turns"]==data["Max_Turns"]:
        data["Winner"]="draw"
    return


'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    row=random.randint(0,9)
    col=random.randint(0,9)
    while board[row][col]==EMPTY_CLICKED or board[row][col]==SHIP_CLICKED:
        row=random.randint(0,9)
        col=random.randint(0,9)
    if board[row][col]==EMPTY_UNCLICKED or board[row][col]==SHIP_UNCLICKED:
        return [row,col]



'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col]==SHIP_UNCLICKED:
                return False
    return True


'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data["Winner"]=="user":
        canvas.create_text(300, 50, text="Congratulations! You won the game", fill="green", font=('Helvetica 25 bold'))
        canvas.create_text(300, 100, text="press Enter to restart the game", fill="green", font=('Helvetica 25 bold'))
    elif data["Winner"]=="comp":
        canvas.create_text(300, 50, text="sorry! You lost the game", fill="red", font=('Helvetica 25 bold'))
        canvas.create_text(300, 100, text="press Enter to restart the game", fill="red", font=('Helvetica 25 bold'))
    elif data["Winner"]=="draw":
        canvas.create_text(300, 50, text="out of moves! Its a draw", fill="orange", font=('Helvetica 25 bold'))
        canvas.create_text(300, 100, text="press Enter to restart the game", fill="orange", font=('Helvetica 25 bold'))
    return


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":



    ## Finally, run the simulation to test it manually ##

    runSimulation(500, 500) 
    # test.testIsGameOver()

