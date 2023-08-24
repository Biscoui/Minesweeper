import sys
import json
import random
import pygame

pygame.init()

#repl link https://replit.com/@TomaszHealey/Minesweeper?v=1
#before you comment it, i know that putting just functions into the classes is useless and i can just put them outside the classes but it is for organization since im too lazy to switch between files.


colour_active = pygame.Color(('black'))# Colour for when the rect is interacted with (white)
colour, colour_passive = pygame.Color(('white')), pygame.Color(('white'))# Colour for when the rect is not being interacted with (black)
colour_active1 = pygame.Color(('white'))
colour_passive1 = (90,90,90) 

#fonts for user typed text
smallest_font = pygame.font.Font(None, 20)
smaller_font = pygame.font.Font(None, 24)
base_font = pygame.font.Font(None, 32)
large_font = pygame.font.Font(None, 100)
largest_font = pygame.font.Font(None, 200)

#loads pngs into variables flagged with "image"
imageLeaderboardIcon = pygame.image.load("Assets/LeaderboardIcon.png")
imageCross = pygame.image.load("Assets/Cross.png")
imageColourBox = pygame.image.load("Assets/ColourBox.png")
flags = {"FlagSmall": pygame.image.load("Assets/Flag40x.png"),
        "FlagLarge": pygame.image.load("Assets/Flag50x.png")}
bombs = {"BombSmall": pygame.image.load("Assets/Bomb40x.png"),
         "BombLarge": pygame.image.load("Assets/Bomb50x.png")}
mouse = [pygame.image.load("Assets/MouseStationary.png"), pygame.image.load("Assets/MouseLeft.png"), pygame.image.load("Assets/MouseRight.png")]
imageShovel = pygame.image.load("Assets/Shovel.png")

gameStage = 'signin'
finished = False
enableHuge = True
difficulties = ['Easy', 'Medium', 'Hard']
if enableHuge:
    difficulties.append('Huge')

user = None
userIndex = None

signedIn = False
minSize = 9 #for huge it is 100
difficulty = 'Easy'

def resetVars():
    global playing, minesPlaced, gameOver, winState, dugCheck, flagCheck, instancesOfCollision, startTile, failedAttempts, failureReason, passwordInput, usernameInput, gameBoard, iteration, gameBoardEasyEmpty, gameBoardMediumEmpty,gameBoardHardEmpty, gameBoardHugeEmpty, generated
    playing = False
    minesPlaced = 0
    gameOver = False
    winState = False
    dugCheck = False
    flagCheck = False
    instancesOfCollision = 0
    startTile = None
    failedAttempts = 0
    failureReason = ''
    passwordInput = ''
    usernameInput = ''
    gameBoard = None
    iteration = 0
    gameBoardEasyEmpty = [[],[],[],[],[],[],[],[],]
    gameBoardMediumEmpty = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],]
    gameBoardHardEmpty = [[],[],[],[],[],[],[],[],[],[],
                        [],[],[],[],[],[],[],[],[],[],]
    gameBoardHugeEmpty = [[],[],[],[],[],[],[],[],[],[],
                        [],[],[],[],[],[],[],[],[],[],
                        [],[],[],[],[],[],[],[],[],[],
                        [],[],[],[],[],[],[],[],[],[],
                        [],[],[],[],[],[],[],[]]
    generated = False

resetVars()
    
screen = pygame.display.set_mode((1000,1000))#sets screen resolution
pygame.display.set_caption("Minesweeper")#Title of window

clock = pygame.time.Clock()

signedIn = False
BG_colour = (90,90,90)

colour_active, colour_passive = 'black', 'white'

colourChangeBox = {"Active": False,
                "Minimised": pygame.Rect(950,150,50,50),
                "Large": pygame.Rect(950, 10, 50, 361),
                "GreyBox": pygame.Rect(955, 20, 40,40),
                "PreviewColour": (123,123,123),
                "PreviewBox": pygame.Rect(955,318, 40, 40),
                "LetterRPos": (955, 105),
                "InputBoxRed": pygame.Rect(955, 125, 40, 32),
                "InputBoxRedColour": None,
                "InputBoxRedColourInverse": None,
                "RedInput": '0',
                "RedInputActive": False,
                "LetterGPos": (955, 162),
                "InputBoxGreen": pygame.Rect(955, 182, 40, 32),
                "InputBoxGreenColour": None,
                "InputBoxGreenColourInverse": None,
                "GreenInput": '0',
                "GreenInputActive": False,
                "LetterBPos": (955, 219),
                "InputBoxBlue": pygame.Rect(955, 239, 40, 32),
                "InputBoxBlueColour": None,
                "InputBoxBlueColourInverse": None,
                "BlueInput": '0',
                "BlueInputActive": False,
                "ApplyBox" : pygame.Rect(955,275 , 40, 20),
                "ApplyAcive": False,
                "CrossRect": pygame.Rect(951,11,9,9),
                }

#the prefix 's' indicates it is for the 'signin' stage, and the prefix 'r' indicates it is for the 'register' stage, 'l' is for leaderboard
inputBoxes = {'Username': pygame.Rect(375, 550, 300, 32),
            'Password': pygame.Rect(375, 600, 300, 32),
            'sSignIn': pygame.Rect(475, 650, 85, 32),
            'sRegister': pygame.Rect(467, 950, 100,32),
            'rSignIn': pygame.Rect(475, 950, 85, 32),
            'rRegister': pygame.Rect(467, 650, 100,32),
            'Easy': pygame.Rect(470, 450, 60, 32),
            'Medium': pygame.Rect(457, 500, 90, 32),
            'Hard': pygame.Rect(470, 550, 62, 32),
            'Huge': pygame.Rect(470, 600, 62, 32),
            'Continue': pygame.Rect(440, 600, 110, 32),
            'SignOut': pygame.Rect(467, 950, 100,32),
            'SignInAsGuest': pygame.Rect(425, 700, 185, 32),
            "lCross": pygame.Rect(223, 166, 9, 9),
            "lSmallBox": pygame.Rect(3,165 , 50, 50),
            "lEasy": pygame.Rect(7, 168, 55, 40),
            "lMedium": pygame.Rect(57, 168, 55, 40),
            "lHard": pygame.Rect(128, 168, 55, 40),
            "lHuge": pygame.Rect(177, 168, 55, 40),
}

states = {'UsernameBox': False,
          'PasswordBox': False,
          'Leaderboard': False,
          'lActive': "Easy",
          'Easy': True,
          'Medium': False,
          'Hard': False,
          'Huge': False,
}

colours = {'Username': ['white', 'black'],
           'Password': ['white', 'black'],
}

titlePosition = {'Easy': (325, 50),
                 'Medium': (275, 50),
                 'Hard': (325, 50)}

tabLine = {"1x": 54,
        "2x": 123,
        "3x": 174,
}
leaderboardLines = [(15,230),
                 (15,260),
                 (15,290),
                 (15,320),
                 (15,350),
                 (15,380),] 

#class for tiles on the board, mostly self explanatory
class BoardTile():

    def __init__(self, rect):
        self.rect = rect
        self.mine = False
        self.dug = False
        self.flag = False
        self.invincible = False
        self.touchingMines = 0
        self.textColour = None
        #some tiles will have other attributes (touchingTiles) if they are not mines
    
    def setFlag(self):
        global flagMax
        if self.rect.collidepoint(event.pos):
            if self.flag == False and flagMax != 0:
                self.flag = True
                flagMax -= 1
            elif self.flag:
                self.flag = False
                flagMax += 1
    
    def ColourCheckAndRender(self, index, index1):
        if self.dug:
            col1 = (232,206,206)
            col2 = (166,146,146)
        else:
            col1 = (72,208,90)
            col2 = (46,166,62)

        if index1 % 2 == 0:
            if index % 2 == 0:
                Colour = col1    
            else:
                Colour = col2
        else:
            if index % 2 == 0:
                Colour = col2
            else:
                Colour = col1
        pygame.draw.rect(screen, Colour, self.rect)
    
    @staticmethod
    def initTouchingTiles():
        rowIndex = 0
        for row in gameBoard:
            colIndex =  0
            for tile in row:
                if tile.mine:
                    colIndex += 1
                    continue
                else:
                    if rowIndex == 0:
                        if colIndex == 0:
                            tile.touchingTiles = [gameBoard[rowIndex][colIndex+1], gameBoard[rowIndex+1][colIndex+1], gameBoard[rowIndex+1][colIndex]]
                        elif colIndex == boardLength-1:
                            tile.touchingTiles = [gameBoard[rowIndex][colIndex-1], gameBoard[rowIndex+1][colIndex-1], gameBoard[rowIndex+1][colIndex]]
                        else:
                            tile.touchingTiles = [gameBoard[rowIndex][colIndex-1],gameBoard[rowIndex][colIndex+1], gameBoard[rowIndex+1][colIndex-1],gameBoard[rowIndex+1][colIndex+1], gameBoard[rowIndex+1][colIndex]]
                    elif rowIndex == boardLength-1:
                        if colIndex == 0:
                            tile.touchingTiles = [gameBoard[rowIndex-1][colIndex], gameBoard[rowIndex-1][colIndex+1], gameBoard[rowIndex][colIndex+1]]
                        elif colIndex == boardLength-1:
                            tile.touchingTiles = [gameBoard[rowIndex-1][colIndex-1], gameBoard[rowIndex-1][colIndex], gameBoard[rowIndex][colIndex-1]]
                        else:
                            tile.touchingTiles = [gameBoard[rowIndex][colIndex-1],gameBoard[rowIndex][colIndex+1], gameBoard[rowIndex-1][colIndex-1],gameBoard[rowIndex-1][colIndex+1], gameBoard[rowIndex-1][colIndex]]
                    elif colIndex == 0:
                        tile.touchingTiles = [gameBoard[rowIndex+1][colIndex], gameBoard[rowIndex+1][colIndex+1], gameBoard[rowIndex-1][colIndex], gameBoard[rowIndex-1][colIndex+1], gameBoard[rowIndex][colIndex+1]]
                    elif colIndex == boardLength-1:
                        tile.touchingTiles = [gameBoard[rowIndex+1][colIndex], gameBoard[rowIndex+1][colIndex-1], gameBoard[rowIndex-1][colIndex], gameBoard[rowIndex-1][colIndex-1], gameBoard[rowIndex][colIndex-1]]

                    else:
                        tile.touchingTiles = [gameBoard[rowIndex+1][colIndex-1],gameBoard[rowIndex+1][colIndex],gameBoard[rowIndex+1][colIndex+1],gameBoard[rowIndex-1][colIndex-1],gameBoard[rowIndex-1][colIndex],gameBoard[rowIndex-1][colIndex+1],gameBoard[rowIndex][colIndex-1],gameBoard[rowIndex][colIndex+1]]
                    colIndex += 1
            rowIndex += 1
    
    @staticmethod
    def initTouchingMines():
        for row in gameBoard:
            for tile in row:
                if tile.mine:
                    continue
                else:
                    for item in tile.touchingTiles:
                        if item.mine:
                            tile.touchingMines += 1
                match tile.touchingMines:
                    case 1:
                        tile.textColour ='blue'
                    case 2:
                        tile.textColour = 'green'
                    case 3:
                        tile.textColour = 'red'
                    case 4:
                        tile.textColour = 'purple'
                    case 5:
                        tile.textColour = 'yellow'
                    case 6:
                        tile.textColour = (0,128,128)
                    case 7:
                        tile.textColour = 'black'
                    case 8:
                        tile.textColour = (167,191,196)

class inputBox:
    #renders input box
    def Render(input_rect, colour, inverseColour, user_text, type):
        global screen, base_font
        pygame.draw.rect(screen, colour, input_rect)
        text_surface = base_font.render(user_text, True, inverseColour)
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))# render at position stated in arguments
        if type:
            input_rect.w = max(300, text_surface.get_width()+10)# set width of textfield so that text cannot get outside of user's text input

    def RenderSmall(input_rect, colour, inverseColour, user_text):
        pygame.draw.rect(screen, colour, input_rect)
        text_surface = smallest_font.render(user_text, True, inverseColour)
        screen.blit(text_surface, (input_rect.x+1, input_rect.y+1))

    #Checks for what colour a input box should be (if it has been interacted with or not)
    def ColourChecker(active):
        global colour_active, colour_passive
        if active:
            colour = colour_active
            inverseColour = colour_passive
        else:
            colour = colour_passive
            inverseColour = colour_active
        return [colour, inverseColour]

    def ColourChecker1(active):
        global colour_active1, colour_passive1
        if active:
            colour = colour_active1
            inverseColour = colour_passive1
        else:
            colour = colour_passive1
            inverseColour = colour_active1
        return colour, inverseColour
    
    def DrawRectAlpha(surface, rect):
        #creates a new surface the size of the rect and makes it take alpha values
        shapeSurface = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shapeSurface, (0,0,0,0,), shapeSurface.get_rect())
        surface.blit(shapeSurface, rect)

    #checks whether the user has interacted with a rect
    def userInteractCheck(rect, active):
        if rect.collidepoint(event.pos):
            active = True
        else:
            active = False
        return active

class load:
    #possible args are 'easyWon,'hardWon', 'mediumWon', 'hugeWon'
    def Leaderboard(category):
        leaderboard = [{"Username": "", "Score": ""}, {"Username": "", "Score": ""}, 
                       {"Username": "", "Score": ""}, {"Username": "", "Score": ""}, 
                       {"Username": "", "Score": ""}]
        for index in range(0, len(userList)):
            for i in range(0,5):
                try:
                    if userList[index][category] > leaderboard[i]["Score"]:
                        leaderboard.insert(i , {"Username": userList[index]["Username"], "Score": userList[index][category]})
                        leaderboard.pop(5)
                        break
                except TypeError:
                    leaderboard.insert(i , {"Username": userList[index]["Username"], "Score": userList[index][category]})
                    leaderboard.pop(5)
                    break
        return leaderboard

    def allLeaderboards():
        global leaderboard_easy, leaderboard_medium, leaderboard_hard, leaderboard_huge
        leaderboard_easy = load.Leaderboard("easyWon")
        leaderboard_medium = load.Leaderboard("mediumWon")
        leaderboard_hard = load.Leaderboard("hardWon")
        leaderboard_huge = load.Leaderboard("hugeWon")

    def updateUserList(item: int, toUpdate: str):
        user[toUpdate] = item
        userList[userIndex][toUpdate] = item
        with open("users.json", "w") as f:
            json.dump(userList, f, indent=4)
            f.close()
    
    def updateLeaderboards():
        if enableHuge:
            match difficulty:
                case "Easy":
                    load.updateUserList(user['easyWon']+1, 'easyWon')
                case "Medium":
                    load.updateUserList(user['mediumWon']+1, 'mediumWon')
                case "Hard":
                    load.updateUserList(user['hardWon']+1, 'hardWon')
                case "Huge":
                    load.updateUserList(user['hugeWon']+1, 'hugeWon')
        else:
            match difficulty:
                case "Easy":
                    load.updateUserList(user['easyWon']+1, 'easyWon')
                case "Medium":
                    load.updateUserList(user['mediumWon']+1, 'mediumWon')
                case "Hard":
                    load.updateUserList(user['hardWon']+1, 'hardWon')

class check:
    #verifies if the log in in valid
    def LogIn(failedAttempts):
        global usernameInput, passwordInput, BG_colour
        for i in userList:
            if i["Username"] == usernameInput and i["Password"] == passwordInput:
                BG_colour = tuple(i["Colour"])
                iteration = 0
                for n in userList:
                    if n == i:
                        index = iteration
                        break
                    iteration += 1
                return 'menuselect', failedAttempts, i, index
            #people can have the same password but not the same username
            elif i["Username"] == usernameInput and i["Password"] != passwordInput:
                continue
            else:
                continue
        failedAttempts += 1
        return 'signin', failedAttempts, None, None

    #checks whether information to register is valid
    def Register():
        global usernameInput, passwordInput
        for i in userList:
            if i["Username"] == usernameInput:
                return 'register', "Username is taken."
        if len(passwordInput) < 8:
            return 'register', "Password must be more than 8 characters"
        specialCharacters = str("!@#$%^&*()-+?_=,<>/'""")
        if any(c in specialCharacters for c in passwordInput) == False:
            return 'register', "Password must contain a special character."
        if any(c.isdigit() for c in passwordInput) == False:
            return 'register', "Password must have a number"
        if any(c.isupper() for c in passwordInput) == False:
            return 'register', "Password must contain a capital."
        userList.append({"Username": usernameInput, "Password": passwordInput, "easyWon": 0, "mediumWon": 0, "hardWon": 0, "hugeWon": 0, "Colour": [90,90,90]})
        with open("users.json", "w") as f:
            json.dump(userList, f, indent=4)
            f.close()
        return 'signin', ''

class SignIn:

    def mainRender():
        SignIn.ColourCheck()
        screen.blit(large_font.render("Welcome to Minesweeper", True, ('white')), (85, 250))
        screen.blit(base_font.render("Username: ", True, ('white')), (250, 555))
        screen.blit(base_font.render("Password: ", True, ('white')), (257, 605))
        inputBox.Render(inputBoxes["Username"], colours['Username'][0], colours['Username'][1], usernameInput, True)
        inputBox.Render(inputBoxes["Password"], colours['Password'][0], colours["Password"][1], len(passwordInput)*"*", True)
        if gameStage == 'register':
            inputBox.Render(inputBoxes["rSignIn"], 'black', 'white', 'Sign In', False)
            inputBox.Render(inputBoxes["rRegister"], "black", 'white', 'Register', False)
            if failureReason != '':
                screen.blit(base_font.render(failureReason, True, ('red')), (330, 700))
        else:
            inputBox.Render(inputBoxes["sSignIn"], 'black', 'white', 'Sign In', False)
            inputBox.Render(inputBoxes["sRegister"], "black", 'white', 'Register', False)
            inputBox.Render(inputBoxes['SignInAsGuest'], 'black', 'white', 'Sign In As Guest', False)
            if failedAttempts > 0:
                screen.blit(base_font.render(f"You have failed {failedAttempts} times.", True, ('red')), (400, 750))
    
    def CollisionCheck():
        global gameStage, failedAttempts, user, userIndex, failureReason
        if gameStage == 'register':
            states['PasswordBox'] = inputBox.userInteractCheck(inputBoxes['Password'], states['PasswordBox'])
            states['UsernameBox'] = inputBox.userInteractCheck(inputBoxes['Username'], states["UsernameBox"])
            if inputBoxes["rSignIn"].collidepoint(event.pos):
                gameStage = 'signin'
            if inputBoxes['rRegister'].collidepoint(event.pos):
                gameStage, failureReason = check.Register()
        else:
            states['PasswordBox'] = inputBox.userInteractCheck(inputBoxes['Password'], states['PasswordBox'])
            states['UsernameBox'] = inputBox.userInteractCheck(inputBoxes['Username'], states["UsernameBox"])
            if inputBoxes["sSignIn"].collidepoint(event.pos):
                gameStage, failedAttempts, user, userIndex = check.LogIn(failedAttempts)
            elif inputBoxes['sRegister'].collidepoint(event.pos):
                gameStage, failedAttempts = 'register', 0
            elif inputBoxes['SignInAsGuest'].collidepoint(event.pos):
                gameStage = 'menuselect'
    
    def ColourCheck():
        colours['Password'] = inputBox.ColourChecker(states["PasswordBox"])
        colours['Username'] = inputBox.ColourChecker(states["UsernameBox"])
              
    #if backspace was pressed it removes the last letter of the string by making the orignial string the substring of itself the first posiotion the position one before last
    def BackspaceCheck1():
        global usernameInput, passwordInput
        if states["UsernameBox"]:
            usernameInput = usernameInput[:-1]
        elif states["PasswordBox"]:
            passwordInput = passwordInput[:-1]

    #I didn't really know what to name this so the name is a little inaccurate(this is what happens if the spacebar has NOT been pressed), if the user types in a key it adds the unicode value of that key to the end of the Input string 
    def BackspaceCheck2():
        global usernameInput, passwordInput
        if states["UsernameBox"]:
            usernameInput += event.unicode
        elif states["PasswordBox"]:
            passwordInput += event.unicode

class ColourBox:
    def CollisionCheck():
        global BG_colour
        if colourChangeBox["Active"] == False:
                colourChangeBox["Active"] = inputBox.userInteractCheck(colourChangeBox["Minimised"], colourChangeBox["Active"])
        if colourChangeBox["Active"]:
            if colourChangeBox["CrossRect"].collidepoint(event.pos):
                colourChangeBox["Active"] = False
            colourChangeBox["RedInputActive"] = inputBox.userInteractCheck(colourChangeBox["InputBoxRed"], colourChangeBox["RedInputActive"])
            colourChangeBox["GreenInputActive"] = inputBox.userInteractCheck(colourChangeBox["InputBoxGreen"], colourChangeBox["GreenInputActive"])
            colourChangeBox["BlueInputActive"] = inputBox.userInteractCheck(colourChangeBox["InputBoxBlue"], colourChangeBox["BlueInputActive"])
            if colourChangeBox["ApplyBox"].collidepoint(event.pos):
                if colourChangeBox["PreviewColour"] != (255,255,255):
                    BG_colour = colourChangeBox["PreviewColour"]
                    if gameStage != 'signin' and gameStage != 'register':
                        ColourBox.ApplyColourToJSON()
            if colourChangeBox["GreyBox"].collidepoint(event.pos):
                BG_colour = (90,90,90)
                if signedIn == True:
                    ColourBox.ApplyColourToJSON()
        else:
            colourChangeBox["Active"] = inputBox.userInteractCheck(colourChangeBox["Minimised"], colourChangeBox["Active"])

    def InputBox(colour):
        screen.blit(base_font.render(f'{colour[0]}:', True, (90,90,90)), colourChangeBox[f"Letter{colour[0]}Pos"])
        colourChangeBox[f"InputBox{colour}Colour"], colourChangeBox[f"InputBox{colour}ColourInverse"] = inputBox.ColourChecker1(colourChangeBox[f"{colour}InputActive"])
        pygame.draw.rect(screen, colourChangeBox[f"InputBox{colour}Colour"], colourChangeBox[f"InputBox{colour}"])
        text_surface = smaller_font.render(colourChangeBox[f"{colour}Input"], True, colourChangeBox[f"InputBox{colour}ColourInverse"])
        screen.blit(text_surface, (colourChangeBox[f"InputBox{colour}"].x+5, colourChangeBox[f"InputBox{colour}"].y+5))
    
    def Render():
        if colourChangeBox["Active"]:
            pygame.draw.rect(screen, 'black', colourChangeBox["Large"])
            screen.blit(imageCross,(951, 11))
            inputBox.DrawRectAlpha(screen, colourChangeBox["CrossRect"])
            pygame.draw.rect(screen, (90,90,90), colourChangeBox["GreyBox"])
            ColourBox.UpdatePreviewColour()
            pygame.draw.rect(screen, colourChangeBox["PreviewColour"], colourChangeBox["PreviewBox"])
            ColourBox.InputBox('Red')
            ColourBox.InputBox('Green')
            ColourBox.InputBox('Blue')
            inputBox.RenderSmall(colourChangeBox["ApplyBox"], "white", 'black', 'Apply')
        else:
            pygame.draw.rect(screen, 'black', colourChangeBox["Minimised"])
            screen.blit(imageColourBox, (955,155))


    #Checks if the user prassed backspace when using the cilour change boxes
    def BackspaceCheck1():
        if colourChangeBox["RedInputActive"]:
            colourChangeBox["RedInput"] = colourChangeBox["RedInput"][0:-1]
        if colourChangeBox["GreenInputActive"]:
            colourChangeBox["GreenInput"] = colourChangeBox["GreenInput"][0:-1]
        if colourChangeBox["BlueInputActive"]:
            colourChangeBox["BlueInput"] = colourChangeBox["BlueInput"][0:-1]

    #if the user didn't input backspace and inputs a number
    def BackspaceCheck2(colour):
        if colourChangeBox[f"{colour}InputActive"]:
            lengthOfInput= int(len(colourChangeBox[f"{colour}Input"]))
            if colourChangeBox[f"{colour}Input"] == '':
                strInput = '0'
            else:
                strInput = colourChangeBox[f"{colour}Input"]
            if event.unicode.isdigit() and lengthOfInput < 3:
                intUnicode = int(event.unicode)
                if lengthOfInput < 1: 
                    if intUnicode < 3:
                        colourChangeBox[f"{colour}Input"] += event.unicode
                        return
                    return
                if int(strInput[0]) < 2:
                    colourChangeBox[f"{colour}Input"] += event.unicode
                    return
                if int(strInput[0]) == 2 and int(event.unicode) < 6:
                    colourChangeBox[f"{colour}Input"] += event.unicode
                    return

    #updates the colour to be previewed in the preiview box in the ColourChangeBox
    def UpdatePreviewColour():
        if colourChangeBox["RedInput"] == '':
            tempRed = '0'
        else:
            tempRed = colourChangeBox["RedInput"]
        if colourChangeBox["GreenInput"] == '':
            tempGreen = '0'
        else:
            tempGreen = colourChangeBox["GreenInput"]
        if colourChangeBox["BlueInput"] == '':
            tempBlue = '0'
        else:
            tempBlue = colourChangeBox["BlueInput"]
        colourChangeBox["PreviewColour"] = (int(tempRed), int(tempGreen), int(tempBlue))

    def ApplyColourToJSON():
        if user != None:
            user["Colour"] = BG_colour
            userList[userIndex]["Colour"] = list(BG_colour)
            with open("users.json", "w") as f:
                json.dump(userList, f, indent=4)

class Animations:

    def LeftClick(pos: tuple):
        if frame < fpsCap/2:
            image = mouse[0]
        else:
            image = mouse[1]
        screen.blit(image, pos)
        screen.blit(imageShovel,(145, 800))
        pygame.draw.rect(screen, 'black', (200,810, 40, 10))
        pygame.draw.rect(screen, 'black', (200,830, 40, 10))
    
    def RightClick(pos: tuple):
        if frame < fpsCap/2:
            image = mouse[0]
        else:
            image = mouse[2]
        screen.blit(image, pos)
        screen.blit(flags["FlagLarge"],(645, 795))
        pygame.draw.rect(screen, 'black', (700,810, 40, 10))
        pygame.draw.rect(screen, 'black', (700,830, 40, 10))

class MenuSelect:

    def mainRender():
        screen.blit(large_font.render('Select your difficulty', True, 'white',), (175,250))
        inputBox.Render(inputBoxes["Easy"], 'black', 'white', 'Easy', False)
        inputBox.Render(inputBoxes["Medium"], 'black', 'white', 'Medium', False)
        inputBox.Render(inputBoxes["Hard"], 'black', 'white', 'Hard', False)
        inputBox.Render(inputBoxes["Huge"], 'black', 'white', 'Huge', False)
        inputBox.Render(inputBoxes['SignOut'], 'black', 'white', 'Sign Out', False)
        if enableHuge == False:
            screen.blit(base_font.render('Huge is disabled due to speed of repl', True, 'red'), (313, 637))
            screen.blit(base_font.render('and processing power of the CPU being too slow', True, 'red'), (255, 664))
            screen.blit(base_font.render('in times of trafic', True, 'red'), (421, 696))
        Animations.LeftClick((250, 750))
        Animations.RightClick((750,750))
        
    
    def CollisionCheck():
        global gameStage, difficulty, difficulties, boardTileStart, boardTileSize, playing, flag, flagMax, bomb, gameBoard, boardLength, generated, medium_font, textOffset, startSize,minSize, usernameInput, passwordInput, user, userIndex 
        for i in difficulties:
            if inputBoxes[i].collidepoint(event.pos):
                gameStage = 'game'
                difficulty = i
                if enableHuge:
                    match i:
                        case "Easy":
                            gameBoard, boardTileStart, boardTileSize, flag, flagMax, bomb, startSize, boardLength =  gameBoardEasyEmpty, [300, 300], 50, flags["FlagLarge"], 8, bombs["BombLarge"], 11, 8
                            textOffset = 10
                            minSize = 9
                        case "Medium":
                            gameBoard, boardTileStart, boardTileSize, flag, flagMax, bomb, startSize, boardLength   =  gameBoardMediumEmpty, [125,150], 50, flags["FlagLarge"], 30, bombs["BombLarge"], 18, 15
                            textOffset = 10
                            minSize = 9
                        case "Hard":
                            gameBoard, boardTileStart, boardTileSize, flag, flagMax, bomb, startSize, boardLength   = gameBoardHardEmpty, [100,150], 40, flags["FlagSmall"],90, bombs["BombSmall"], 18, 20
                            textOffset = 8
                            minSize = 9
                        case "Huge":
                            gameBoard, boardTileStart, boardTileSize, flag, flagMax, bomb, startSize, boardLength   = gameBoardHugeEmpty, [20,20], 20, flags["FlagSmall"],356, bombs["BombSmall"], 120, 48
                            textOffset = 4
                            minSize = 100
                else:
                    match i:
                        case "Easy":
                            gameBoard, boardTileStart, boardTileSize, flag, flagMax, bomb, startSize, boardLength =  gameBoardEasyEmpty, [300, 300], 50, flags["FlagLarge"], 8, bombs["BombLarge"], 11, 8
                            textOffset = 10
                        case "Medium":
                            gameBoard, boardTileStart, boardTileSize, flag, flagMax, bomb, startSize, boardLength   =  gameBoardMediumEmpty, [125,150], 50, flags["FlagLarge"], 30, bombs["BombLarge"], 18, 15
                            textOffset = 10
                        case "Hard":
                            gameBoard, boardTileStart, boardTileSize, flag, flagMax, bomb, startSize, boardLength   = gameBoardHardEmpty, [100,150], 40, flags["FlagSmall"],90, bombs["BombSmall"], 18, 20
                            textOffset = 8
                playing = True
                generated = False
                medium_font = pygame.font.Font(None, int(boardTileSize*1.5))
        if inputBoxes['SignOut'].collidepoint(event.pos):
            gameStage = 'signin'
            usernameInput = ''
            passwordInput = ''
            user = None
            userIndex = None

class Game:

    def mainRender():
        global iteration, gameOver, flagCheck, generated, instancesOfCollision
        try:
            screen.blit(large_font.render(f'{difficulty} Mode', True, 'white'), (titlePosition[difficulty]))
            screen.blit(flags["FlagLarge"], (10,10))
            pygame.draw.rect(screen, 'black', (65,23, 40, 10))
            pygame.draw.rect(screen, 'black', (65,48, 40, 10))
            screen.blit(large_font.render(str(flagMax), True, 'black'), (115, 5))
        except KeyError:
            screen.blit(smallest_font.render(f"Flags Left = {str(flagMax)}", True, 'black'), (20, 5))
        index = 0
        for row in gameBoard:
            index1 = 0
            if iteration == 0:
                for tile in range(0,boardLength):
                    if row == []:
                        if index == 0:
                            gameBoard[index].append(BoardTile(pygame.Rect(boardTileStart[0], boardTileStart[1],boardTileSize, boardTileSize)))
                        else:
                            gameBoard[index].append(BoardTile(pygame.Rect(boardTileStart[0], boardTileStart[1]+(boardTileSize*index),boardTileSize, boardTileSize)))
                    else:
                        gameBoard[index].append(BoardTile(pygame.Rect(boardTileStart[0]+(index1*boardTileSize), boardTileStart[1]+(index*boardTileSize),boardTileSize, boardTileSize)))
                    index1 += 1
            else:
                for tile in row:
                    tile.ColourCheckAndRender(index, index1)
                    if tile.flag:
                        screen.blit(flag, (tile.rect.x, tile.rect.y))
                    elif tile.mine == 1 and tile.dug:
                        screen.blit(bomb, (tile.rect.x, tile.rect.y+2))
                    elif tile.dug and tile.touchingMines != 0:
                        try:
                            screen.blit(medium_font.render(str(tile.touchingMines), True, tile.textColour), (tile.rect.x+textOffset, tile.rect.y+2))
                        except NameError:
                            screen.blit(smaller_font.render(str(tile.touchingMines), True, tile.textColour), (tile.rect.x+textOffset, tile.rect.y+2))
                    if tile.mine == 1 and gameOver and winState == False:
                        screen.blit(bomb, (tile.rect.x, tile.rect.y+2))
                    index1 += 1                               
            index += 1
        if instancesOfCollision == 1 and generated == False:
            BoardTile.initTouchingTiles()
            Game.GenerateStart()
            Game.PlaceBombs()
            BoardTile.initTouchingMines()
            instancesOfCollision += 1
            generated = True
        if difficulty == 'Huge':
            pygame.draw.rect(screen, BG_colour, pygame.Rect(0, 980, 20, 980))
            pygame.draw.rect(screen, BG_colour, pygame.Rect(980, 20, 980, 20))
        Game.ZeroCheckAll()
        Game.WinLogic()
        if gameOver:
            if winState:
                screen.blit(largest_font.render('GAME WON', True, 'white'), (90,400))
            else:
                screen.blit(largest_font.render('GAME OVER', True, 'red'), (75,400))
            inputBox.Render(inputBoxes['Continue'], 'black', 'white', 'Continue', False)
            
    def WinLogic():
        global flagCheck, gameOver, winState, playing
        if flagMax == 0:
            tempBreak = False
            for row in gameBoard:
                for tile in row:
                    if tile.mine and tile.flag:
                        flagCheck = True
                        continue
                    elif tile.mine == False and tile.dug:
                        dugCheck = True
                        continue
                    else:
                        tempBreak = True
                        flagCheck, dugCheck = False, False
                        break
                if tempBreak == True:
                    break   
        if flagCheck and dugCheck:
            gameOver, winState, playing = True, True, False

    def PlaceBombs():
        global flagMax, minesPlaced
        while True:
            for row in gameBoard:
                for tile in row:
                    if tile.mine == False and tile.invincible == False:
                        randInt = random.randint(1,flagMax)
                        if randInt == 1:
                            tile.mine = 1
                            minesPlaced += 1
                    if minesPlaced == flagMax:
                        break
                if minesPlaced == flagMax:
                    break
            if minesPlaced == flagMax:
                break
    
    def ZeroCheck(tile, start: bool):
        if tile.dug and tile.touchingMines == 0 and tile.mine == False:
                for newTile in tile.touchingTiles:
                    if start:
                        newTile.invincible = True
                    newTile.dug = True

    def ZeroCheckAll():
        for row in gameBoard:
            for tile in row:
                Game.ZeroCheck(tile, False)

    def GenerateStart():
        global startTilePos, startTile, startSize
        index = 0  
        breakLoop = False
        for row in gameBoard:
            index1 = 0
            for tile in row:
                if tile == startTile:
                    startTilePos = [index, index1]
                    breakLoop = True
                    break
                index1 += 1
            if breakLoop:
                break
            index += 1
        invincibleTiles = 0
        for tile in startTile.touchingTiles:
            tile.invincible, tile.dug = True, True
            Game.ZeroCheck(tile, True)
            invincibleTiles += 1
        startingTilesNumber = random.randint(minSize,startSize)
        while invincibleTiles <= startingTilesNumber:
            randInt = random.randint(0,2)
            startTile = startTile.touchingTiles[randInt]
            for tile in startTile.touchingTiles:
                tile.invincible, tile.dug = True, True
                invincibleTiles += 1
        
    def CollisionCheck():
        global playing, flagMax, gameOver, instancesOfCollision, startTile, gameStage
        for row in gameBoard:
            for tile in row: 
                if event.button == 1 and tile.dug == False and tile.flag == False:
                    if tile.rect.collidepoint(event.pos):
                        instancesOfCollision += 1
                        if instancesOfCollision == 1:
                            startTile = tile
                            tile.invincible = True
                            tile.dug = True
                        else:
                            tile.dug = True
                            if tile.mine:
                                gameOver = True
                                playing = False
                if event.button == 2 and tile.dug and tile.rect.collidepoint(event.pos):
                    flaggedTiles = 0
                    for newTile in tile.touchingTiles:
                        if newTile.flag:
                            flaggedTiles += 1
                    if flaggedTiles == tile.touchingMines:
                        for newTile in tile.touchingTiles:
                            if newTile.flag == False:
                                newTile.dug = True
                                if newTile.mine:
                                    gameOver = True
                                    playing = False
                if event.button == 3 and tile.dug == False:
                    tile.setFlag()

class Leaderboard:

    def DrawTab(rect, active, line1):
        inputBox.DrawRectAlpha(screen, rect)
        if active:
            screen.blit(smaller_font.render(line1, True, 'green'), (rect.x, rect.y))
        else:
            screen.blit(smaller_font.render(line1, True, 'white'), (rect.x, rect.y))

    def TabCollision():
        if inputBoxes["lEasy"].collidepoint(event.pos):
            states["Easy"], states["Medium"], states["Hard"], states["Huge"] = True,False,False,False
        if inputBoxes["lMedium"].collidepoint(event.pos):
            states["Medium"], states["Easy"], states["Hard"], states["Huge"] = True,False,False,False
        if inputBoxes["lHard"].collidepoint(event.pos):
            states["Hard"], states["Easy"], states["Medium"], states["Huge"] = True,False,False,False
        if inputBoxes["lHuge"].collidepoint(event.pos):
            states["Huge"], states["Hard"], states["Easy"], states["Medium"] = True,False,False,False
            
    def Render():
        if states["Leaderboard"] == False:
            inputBox.DrawRectAlpha(screen, inputBoxes["lSmallBox"])
            screen.blit(imageLeaderboardIcon, (3, 165))
        else:
            pygame.draw.rect(screen, 'black', (3, 165, 230, 250))
            screen.blit(imageCross, (223,166))
            inputBox.DrawRectAlpha(screen, inputBoxes["lCross"])
            Leaderboard.DrawTab(inputBoxes["lEasy"], states["Easy"], "Easy")
            Leaderboard.DrawTab(inputBoxes["lMedium"], states["Medium"], "Medium")
            Leaderboard.DrawTab(inputBoxes["lHard"], states["Hard"], "Hard")
            Leaderboard.DrawTab(inputBoxes["lHuge"], states["Huge"], "Huge")
            for i in range (1,4):
                pygame.draw.line(screen, 'white', (tabLine[f"{i}x"], 165), (tabLine[f"{i}x"] ,205), 2)
            pygame.draw.line(screen, 'white', (115, 222), (115, 402), 2)
            pygame.draw.line(screen,'white', (15,252), (215,252), 2)
            for i in range (2,6):
                pygame.draw.line(screen,'white', (15,222+(30*i)), (215,222+(30*i)), 2)

            screen.blit(smaller_font.render('Username', True, 'white'), (15, 230))
            screen.blit(smaller_font.render('Wins', True, 'white'), (125, 230))
            try:
                for i in range(0, 4):
                    if len(leaderboardDisplay[i]['Username']) > 7:
                        leaderboardDisplay[i]['Username'] = leaderboardDisplay[i]['Username'][0:8] +'...'
                    screen.blit(smaller_font.render(leaderboardDisplay[i]['Username'], True, 'white'), leaderboardLines[i+1])
                for i in range(0, 5):
                    screen.blit(smaller_font.render(str(leaderboardDisplay[i]['Score']), True, 'white'), (leaderboardLines[i+1][0]+110, leaderboardLines[i+1][1] ))
            except NameError:
                Leaderboard.CollisionCheck()

    def CollisionCheck():
        global leaderboardDisplay
        if states["Leaderboard"]:
            Leaderboard.TabCollision()

            if states["Easy"]:
                states["lActive"], leaderboardDisplay = 'Easy', leaderboard_easy
            elif states["Medium"]:
                states['lActive'], leaderboardDisplay = 'Medium', leaderboard_medium
            elif states["Hard"]:
                states['lActive'], leaderboardDisplay = 'Hard', leaderboard_hard
            elif states["Huge"]:
                states['lActive'], leaderboardDisplay = 'Huge', leaderboard_huge

            if inputBoxes["lCross"].collidepoint(event.pos):
                states["Leaderboard"] = False
                states["Huge"] = False
        
        else:
            if inputBoxes["lSmallBox"].collidepoint(event.pos):
                states["Leaderboard"] = True
                states["Easy"] = True
                load.allLeaderboards()


with open("users.json", "r") as f:
    userList = json.load(f)
    f.close()

frame = 0
#whether a new game has started. The iteration of the while loop if the gameStage is 'game'
iteration = 0

fpsCap = 30
while True:
    # clock.tick() limits the while loop to a max of 30 times per second. 
    clock.tick(fpsCap)

    if frame == fpsCap:
        frame = 0

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if gameStage == 'signin' or gameStage == 'register' or gameStage == 'menuselect' or difficulty != "Huge":
            if event.type == pygame.MOUSEBUTTONDOWN:
                ColourBox.CollisionCheck()
                Leaderboard.CollisionCheck()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    ColourBox.BackspaceCheck1()
                    ColourBox.BackspaceCheck1()

                elif event.key != pygame.K_BACKSPACE:
                    ColourBox.BackspaceCheck2('Red')
                    ColourBox.BackspaceCheck2('Green')
                    ColourBox.BackspaceCheck2('Blue')
        
        if gameStage == 'signin' or gameStage == 'register':
            if event.type == pygame.MOUSEBUTTONDOWN:
                SignIn.CollisionCheck()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    SignIn.BackspaceCheck1()

                elif event.key == pygame.K_RETURN:
                    if states['PasswordBox']:
                        gameStage, failedAttempts, user, userIndex = check.LogIn(failedAttempts)
                    elif states['UsernameBox']:
                        states['UsernameBox'], states['PasswordBox'] = False, True
                else:
                    SignIn.BackspaceCheck2()
        
        elif gameStage == 'menuselect':
            if event.type == pygame.MOUSEBUTTONDOWN:
                MenuSelect.CollisionCheck()
        
        #if gameStage == 'game' this just also keeps them on the game over screen withouth being able to continue the game.
        elif playing == True:
            if event.type == pygame.MOUSEBUTTONDOWN:
                Game.CollisionCheck()
        if gameStage == 'game' and playing == False:
            if inputBoxes['Continue'].collidepoint(event.pos) and event.type == pygame.MOUSEBUTTONDOWN:
                #add in leaderboard shananigans and json update shananginas here
                resetVars()
                if winState:
                    load.updateLeaderboards()
                    load.allLeaderboards()
                gameStage = 'menuselect'

    
    screen.fill(BG_colour)

    if gameStage == 'signin' or gameStage == 'register':
        SignIn.mainRender()
    elif gameStage == 'menuselect':
        MenuSelect.mainRender()
    elif gameStage == 'game':
        Game.mainRender()
        iteration = 1
    if difficulty != 'Huge':
        ColourBox.Render()
        if gameStage != 'game':
            Leaderboard.Render()
            
    pygame.display.flip()

    frame += 1