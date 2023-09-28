import turtle
from math import *

win = turtle.Screen()
chuck = turtle.Turtle()
chuck.turtlesize(3.6)

#Makes the outline around the board
chuck.penup()
chuck.backward(300)
chuck.pendown()
chuck.right(90)
chuck.forward(297)
chuck.left(90)
for i in range(4):
    chuck.forward(600)
    chuck.left(90)
chuck.width(75)
chuck.penup()

#Creates the first square
chuck.shape('square')
chuck.forward(37.5)
chuck.left(90)
chuck.forward(37.5)
chuck.color("grey")
grey = True
chuck.stamp()

#Creates the first checker
chuck.shape('circle')
chuck.color('darkred')
chuck.turtlesize(3)
chuck.stamp()
chuck.shape('square')
chuck.color('grey')
chuck.turtlesize(3.6)

#The spots that the checkers are in
redSpots = [3,15,17,19,31,33,35,47,49,51,63]
blackSpots = [7,9,11,23,25,27,39,41,43,55,57,59]

#Creates the board
i = 1
while i < 64:
    if i in redSpots or i in blackSpots:
        chuck.shape('circle')
        if i in redSpots:
            chuck.color('darkred')
        else:
            chuck.color('black')
        chuck.turtlesize(3)
        chuck.stamp()
        chuck.shape('square')
        if grey:
            chuck.color('grey')
        else:
            chuck.color('red')
        chuck.turtlesize(3.6)

    if grey:
        chuck.color("red")
        grey = False
    else:
        chuck.color("grey")
        grey = True
    chuck.forward(75)
    chuck.stamp()
    i += 1

    if i % 16 == 0 and i % 64 != 0:
        chuck.left(90)
        if grey:
            chuck.color("red")
            grey = False
        else:
            chuck.color("grey")
            grey = True
        chuck.forward(75)
        chuck.stamp()
        i += 1
        chuck.left(90)
    elif i % 8 == 0 and i % 64 != 0:
        chuck.right(90)
        if grey:
            chuck.color("red")
            grey = False
        else:
            chuck.color("grey")
            grey = True
        chuck.forward(75)
        chuck.stamp()
        i += 1
        chuck.right(90)

#Moves the turtle to the center of the screen
chuck.shape('circle')
chuck.left(45)
chuck.backward(371.231060123)
chuck.left(45)
chuck.turtlesize(0.1)


def Moving(newX, newY, oldX, oldY, current, blackTurn, king):
    #Calculates distance
    dis = ((75*newX - 75*oldX)**2 + (75*newY - 75*oldY)**2)**0.5
    #If the distance moved forward needs to be negative
    if newX < oldX:
        leftAd = -1
    else:
        leftAd = 1

    #Calculates the angle to get to spot
    if (oldX > newX and oldY > newY) or (oldX < newX and oldY < newY):
        chuck.left(degrees(atan(abs((75*(newY-oldY))/(75*(newX-oldX))))))
    else:
        chuck.right(degrees(atan(abs((75*(newY-oldY))/(75*(newX-oldX))))))

    #Kill check
    if abs(oldY - newY) == 2 and abs(oldX - newX) == 2: #Kill
        chuck.forward((leftAd * dis)/2)
        chuck.color('grey')
        chuck.stamp()
        chuck.forward((leftAd * dis)/2)
    else: #No kill
        chuck.forward(leftAd * dis)

    #Determines which color to use
    if current:
        chuck.color('grey')
        chuck.stamp()
    else:
        if blackTurn == 1:
            chuck.color('black')
        else:
            chuck.color('darkred')
        chuck.stamp()
        if king:
            chuck.turtlesize(1.5)
            chuck.color('yellow')
            chuck.stamp()
            chuck.turtlesize(3)

    #Realigns the turtle
    if (oldX > newX and oldY > newY) or (oldX < newX and oldY < newY):
        chuck.right(degrees(atan(abs((75*(newY-oldY))/(75*(newX-oldX))))))
    else:
        chuck.left(degrees(atan(abs((75*(newY-oldY))/(75*(newX-oldX))))))

    return [newX,newY]

def BoardUpdate(rawCurX, rawCurY, rawSelX, rawSelY, blackTurn, king):
    curDis = ((75*rawCurX - 337.5)**2 + (75*rawCurY - 337.5)**2)**0.5
    selDis = ((75*rawSelX - 337.5)**2 + (75*rawSelY - 337.5)**2)**0.5
    chuck.turtlesize(3)

    if curDis <= selDis: #If the current distance is less
        Moving(rawCurX, rawCurY, 4.5, 4.5, True, blackTurn, king)
        coord = Moving(rawSelX, rawSelY, rawCurX, rawCurY, False, blackTurn, king)
    else:
        Moving(rawSelX, rawSelY, 4.5, 4.5, False, blackTurn, king)
        coord = Moving(rawCurX, rawCurY, rawSelX, rawSelY, True, blackTurn, king)

    chuck.forward(75*(4.5-coord[0]))
    chuck.left(90)
    chuck.forward(75*(4.5-coord[1]))
    chuck.right(90)
    chuck.turtlesize(0.1)




#Variables
board = [["B","B","B","B"],\
         ["B","B","B","B"],\
         ["B","B","B","B"],\
         ["N","N","N","N"],\
         ["N","N","N","N"],\
         ["R","R","R","R"],\
         ["R","R","R","R"],\
         ["R","R","R","R"]]

blackTurn = -1

def CoordValidate(coordType, endSentence):
    expression = "Enter " + coordType + " value of " + endSentence
    coord = input(expression)
    if coord.upper() == "BACK":
        return -1
    while not coord.isdigit():
        coord = input("Error. Enter a number: ")
    coord = int(coord)
    while coord < 1 or coord > 8:
        coord = input("Error. Enter a number in range: ")
        while not coord.isdigit():
            coord = input("Error. Enter a number: ")
        coord = int(coord)
    return coord

def newArray(oldArray,oldX,oldY,newPiece,newX,newY,killX,killY):
    newArray = [[],[],[],[],[],[],[],[]]
    for num in range(8):
        for i in range(4):
            if oldY == num and oldX == i:
                newArray[num].append("N")
            elif newY == num and newX == i:
                newArray[num].append(newPiece)
            elif killY == num and killX == i:
                newArray[num].append("N")
            else:
                newArray[num].append(oldArray[num][i])
    return newArray

def GeneralMoveAvailable(blackTurn,array):
    if blackTurn == 1:
        char = "B"
        opp = "R"
    else:
        char = "R"
        opp = "B"

    for num in range(len(array)): #Loops through rows
        for i in range(len(array[num])): #Loops through columns
            if num%2 == 0:
                ladd = 1
            else:
                ladd = -1
            if array[num][i] == char:
                it = 1
            elif array[num][i] == "K" + char:
                it = 2
            #When the loop finds a char
            if char in array[num][i]:
                for itera in range(it):
                    #Makes sure there is no error
                    if num+blackTurn > -1 and num+blackTurn < 8:
                        #If there is more space to move to (basic forward)
                        if (i-1 > -1 or ladd == 1) and (i+1 < 4 or ladd == -1):
                            if array[num+blackTurn][i+ladd] == "N":
                                return True
                        if array[num+blackTurn][i] == "N":
                                return True
                        #Checking before evaluating
                        elif num+2*blackTurn > -2 and num+2*blackTurn < 9:
                            #Basic kills
                            #Forward in the array
                            if opp in array[num+blackTurn][i]\
                               and array[num+2*blackTurn][i] == "N":
                                return True
                            elif i+2*blackTurn > -2 and i+2*blackTurn < 5:
                                #Across the array
                                if opp in array[num+blackTurn][i]\
                                     and array[num+2*blackTurn][i-ladd] == "N":
                                         return True
                                elif opp in array[num+blackTurn][i+ladd]\
                                     and array[num+2*blackTurn][i+ladd] == "N":
                                         return True
                    blackTurn *= -1
    return False

def DoubleJumpAvailable(arrayX,arrayY,blackTurn,array):
    if "K" in array[arrayY][arrayX]:
        it = 2
    else:
        it = 1
    if arrayY % 2 == 0:
        ladd = 1
    else:
        ladd = -1
    if blackTurn == 1:
        char = "B"
        opp = "R"
    else:
        char = "R"
        opp = "B"
    for num in range(it):
        #Makes sure there is no error
        if arrayY+blackTurn > -1 and arrayY+blackTurn < 8:
            #If there is more space to move to (basic forward)
            if (arrayX > 0 or ladd == 1) and (arrayX < 3 or ladd == -1):
                if array[arrayY+blackTurn][arrayX+ladd] == "N":
                    return True
            if array[arrayY+blackTurn][arrayX] == "N":
                    return True
            #Checking before evaluating
            if arrayY+2*blackTurn > -1 and arrayY+2*blackTurn < 8:
                #Basic kills
                #Forward in the array
                if arrayX+2*blackTurn > -2 and arrayX+2*blackTurn < 5:
                    #Across the array
                    if opp in array[arrayY+blackTurn][arrayX]\
                         and array[arrayY+2*blackTurn][arrayX-ladd] == "N":
                        return True
                    elif opp in array[arrayY+blackTurn][arrayX+ladd]\
                         and array[arrayY+2*blackTurn][arrayX+ladd] == "N":
                        return True
        blackTurn *= -1
    return False

def DaMove(blackTurn, board):
    goAhead = True
    rawCurX = -1; newCurX = -1
    rawCurY = -1; newCurY = -1
    rawSelX = -1; newSelX = -1
    rawSelY = -1; newSelY = -1
    change = ""
    invalidCoords = [[1,2],[1,4],[1,6],[1,8],\
                     [2,1],[2,3],[2,5],[2,7],\
                     [3,2],[3,4],[3,6],[3,8],\
                     [4,1],[4,3],[4,5],[4,7],\
                     [5,2],[5,4],[5,6],[5,8],\
                     [6,1],[6,3],[6,5],[6,7],\
                     [7,2],[7,4],[7,6],[7,8],\
                     [8,1],[8,3],[8,5],[8,7]]

    if blackTurn == 1:
        print("Black's move.")
    else:
        print("Red's move.")
    #Move validation
    validPiece = False
    while validPiece == False:
        validPiece = False
        while validPiece == False:
            #Gathering raw current coords
            rawCurX = CoordValidate("x","current: ")

            #User changing mind
            while rawCurX == -1:
                rawCurX = CoordValidate("x","current: ")

            rawCurY = CoordValidate("y","current: ")

            #User changing mind
            while rawCurX == -1 or rawCurY == -1:
                rawCurX = CoordValidate("x","current: ")
                if rawCurX != -1:
                    rawCurY = CoordValidate("y","current: ")

            #Converting coords for array
            newCurX = (1+rawCurX)//2 -1
            newCurY = 8 - rawCurY

            #Checks that a black piece is picked on a black turn & vice versa
            if blackTurn == 1 and (board[newCurY][newCurX] == "B" or board[newCurY][newCurX] == "KB") and [rawCurX,rawCurY] not in invalidCoords:
                validPiece = True
            elif blackTurn == -1 and (board[newCurY][newCurX] == "R" or board[newCurY][newCurX] == "KR") and [rawCurX,rawCurY] not in invalidCoords:
                validPiece = True
            else:
                print("Choose a valid checker.")

    #Determines if the user can change the current coords (can't if they just killed)
    curChange = True
    while goAhead:
            #Validating that the user chose an empty spot to go to
            validPiece = False
            while validPiece == False:
                #Gathering x selected coord
                rawSelX = CoordValidate("x", "target: ")

                #User changing mind
                while rawCurX == -1 or rawCurY == -1 or rawSelX == -1:
                    if curChange:
                        rawCurX = CoordValidate("x","current: ")
                    if curChange and rawCurX != -1:
                        rawCurY = CoordValidate("y","current: ")
                    if rawCurX != -1 and rawCurY != -1:
                        rawSelX = CoordValidate("x","target: ")

                #Gathering y selected coord
                rawSelY = CoordValidate("y", "target: ")

                #User changing mind
                while rawCurX == -1 or rawCurY == -1 or rawSelX == -1 or rawSelY == -1:
                    if curChange:
                        rawCurX = CoordValidate("x","current: ")
                    if curChange and rawCurX != -1:
                        rawCurY = CoordValidate("y","current: ")
                    if rawCurX != -1 and rawCurY != -1:
                        rawSelX = CoordValidate("x","target: ")
                    if rawCurX != -1 and rawCurY != -1 and rawSelX != -1:
                        rawSelY = CoordValidate("y", "target: ")

                #Converting board coords to array coords
                newSelX = (1 + rawSelX)//2 - 1
                newSelY = 8 - rawSelY

                if board[newSelY][newSelX] == "N":
                    validPiece = True
                else:
                    print("Space is already occupied.")

            avX = (1+(rawCurX+rawSelX)//2)//2 - 1
            avY = 8-(rawCurY+rawSelY)//2
            if blackTurn == 1:
                if "K" in board[newCurY][newCurX]:
                    piece = "KB"
                    royal = True
                else:
                    piece = "B"
                    royal = False
            else:
                if "K" in board[newCurY][newCurX]:
                    piece = "KR"
                    royal = True
                else:
                    piece = "R"
                    royal = False

            #Basic move
            if (newSelY - newCurY == blackTurn or royal) and abs(rawSelX - rawCurX) == 1:
                #Yay! It's valid!
                validPiece = True
                if newSelY == 0 and blackTurn == -1:
                    piece = "KR"
                    royal = True
                elif newSelY == 7 and blackTurn == 1:
                    piece = "KB"
                    royal = True
                board = newArray(board,newCurX,newCurY,piece,newSelX,newSelY,-1,-1)
                BoardUpdate(rawCurX, rawCurY, rawSelX, rawSelY, blackTurn, royal)
                goAhead = False

            #Kill Move
            elif newSelY - newCurY == 2*blackTurn and abs(rawSelX - rawCurX) == 2\
                 and board[avY][avX] != "N":
                if board[avY][avX] == "R" and blackTurn == 1:
                    validPiece = True
                    if newSelY == 0 and blackTurn == -1:
                        piece = "KR"
                        royal = True
                    elif newSelY == 7 and blackTurn == 1:
                        piece = "KR"
                        royal = True

                    #Changes to board
                    board = newArray(board,newCurX,newCurY,piece,newSelX,newSelY,avX,avY)
                    BoardUpdate(rawCurX, rawCurY, rawSelX, rawSelY, blackTurn, royal)
                    goAhead = DoubleJumpAvailable(newSelX,newSelY,blackTurn,board)

                    if goAhead:
                        rawCurX = rawSelX;rawCurY = rawSelY
                        newCurX = newSelX;newCurY = newSelY
                        curChange = False
                elif board[avY][avX] == "B" and blackTurn == -1:
                    validPiece = True
                    if newSelY == 0 and blackTurn == -1:
                        piece = "KR"
                        royal = True
                    elif newSelY == 7 and blackTurn == 1:
                        piece = "KR"
                        royal = True
                    board = newArray(board,newCurX,newCurY,piece,newSelX,newSelY,avX,avY)
                    BoardUpdate(rawCurX, rawCurY, rawSelX, rawSelY, blackTurn, royal)
                    goAhead = DoubleJumpAvailable(newSelX,newSelY,blackTurn,board)

                    if goAhead:
                        rawCurX = rawSelX;rawCurY = rawSelY
                        newCurX = newSelX;newCurY = newSelY
                        curChange = False
                else:
                    print("You cannot kill your own piece.")
                    validPiece = False
            else:
                print("Illegal move.")
                validPiece = False
    return board

moreMoves = True
while moreMoves:
    if "KB" not in board[0] and "B" not in board[0] and \
       "KB" not in board[1] and "B" not in board[1] and \
       "KB" not in board[2] and "B" not in board[2] and \
       "KB" not in board[3] and "B" not in board[3] and \
       "KB" not in board[4] and "B" not in board[4] and \
       "KB" not in board[5] and "B" not in board[5] and \
       "KB" not in board[6] and "B" not in board[6] and \
       "KB" not in board[7] and "B" not in board[7]:
        moreMoves = False
        print("Red wins!")
    elif "RB" not in board[0] and "R" not in board[0] and \
       "KR" not in board[1] and "R" not in board[1] and \
       "KR" not in board[2] and "R" not in board[2] and \
       "KR" not in board[3] and "R" not in board[3] and \
       "KR" not in board[4] and "R" not in board[4] and \
       "KR" not in board[5] and "R" not in board[5] and \
       "KR" not in board[6] and "R" not in board[6] and \
       "KR" not in board[7] and "R" not in board[7]:
        moreMoves = False
        print("Black wins!")
    elif GeneralMoveAvailable(blackTurn,board) == False:
        if blackTurn == 1:
            print("Red wins!")
        else:
            print("Black wins!")
        moreMoves = False
    else:
        #INCLUDE NO MORE MOVES POSSIBLE [check]
        board = DaMove(blackTurn,board)
        blackTurn *= -1