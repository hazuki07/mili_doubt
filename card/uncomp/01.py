from tkinter import *
import random

def callback():
    print("callback")

class Card:
    def __init__(self, suit, rank, image, image2):
        self.suit = suit
        self.rank = rank
        self.image = image
        self.backimage = image2
    def getSuit(self):
        return self.suit
    def getRank(self):
        return self.rank
    def setSuit(self, s):
        self.suit = s
    def setRank(self, r):
        self.rank = r
carddeck = []
comHand = []
userHand = []
Yama = []
getCom = []
getUser = []
gameOverP = False
comPlayP = False
dispCom = []

WW = 10
HH = 10
trump = 0

def card_set():
    back_image = PhotoImage(file= "b1fv.gif")
    global carddeck
    for s in range(4):
        for r in range(13):
            name = ""
            if s == 0:
                name = "c"
            elif s == 1:
                name = "d"
            elif s == 2:
                name = "h"
            else:
                name = "s"
            if r < 10:
                name += str(r+1)
            elif r == 11:
                name += "j"
            elif r == 12:
                name += "q"
            else:
                name += "k"
            name += ".gif"
            image = PhotoImage(file=name)
            card = Card(s, r, image, back_image)
            carddeck.append(card)

def card_initialize():
    for i in range(104):
        s = random.randrange(0, 52)
        t = random.randrange(0, 52)
        temp = carddeck[s]
        carddeck[s] = carddeck[t]
        carddeck[t] = temp

def gameInitialize():
    global carddeck, comHand, userHand, Yama, getCom, getUser, dispCom
    global gameOverP, comPlayP, trump
    comHand = []
    userHand = []
    Yama = []

    card_initialize()
    index = 0
    for i in range(13):
        comHand.append(carddeck[index])
        index += 1
    for i in range(13):
        userHand.append(carddeck[index])
        index += 1
    for i in range(26):
        Yama.append(carddeck[index])
        index += 1
    getCom = []
    getUser = []
    dispCom = []
    gameOverP = False
    comPlayP = False
    trump = Yama[len(Yama)-1].getSuit()

def ShowBan():
    canvas.create_rectangle(0, 0, 1000, 600, fill="white")
    pos = 45
    for i in range(len(comHand)):
        canvas.create_image(pos, 65, image=comHand[i].backimage)
        pos += 72
    pos = 45
    for i in range(len(getCom)):
        canvas.create_image(pos, 165, image=getCom[i].image)
        pos += 18
    pos = 45
    if len(Yama) > 0:
        canvas.create_image(pos, 265, image=Yama[len(Yama)-1].image)
    pos = 145
    if len(dispCom) > 0:
        canvas.create_image(pos, 265, image=dispCom[0].image)

    pos = 45
    for i in range(len(getUser)):
        canvas.create_image(pos, 365, image=getUser[i].image)
        pos += 18
    pos = 45
    for i in range(len(userHand)):
        canvas.create_image(pos, 465, image=userHand[i].image)
        pos += 72
    f1, f2 = "courier 24", "courier 12"
    c1, c2, c3 = "blue", "red", "black"
    if gameOverP == False:
        canvas.create_text(400, 265, text=u"カードを選んで下さい", font=f1, fill=c1)
    else:
        comValue = len(getCom)/2
        userValue = len(getUser)/2
        drawString = "Game Over "
        drawString += str(userValue)
        drawString += " : "
        drawString += str(comValue)
        if comValue > userValue:
            drawString += u" コンピュータの勝ちです。頑張ってね！"
            canvas.create_text(500, 265, text=drawString, font=f1, fill=c1)
        elif comValue < userValue:
            drawString += u" あなたの勝ちです。強いですね！"
            canvas.create_text(500, 265, text=drawString, font=f1, fill=c1)
        else:
            drawString += u"　引き分けです。もう一度しませんか？"
            canvas.create_text(500, 265, text=drawString, font=f1, fill=c1)

def buttonPress(event):
    global carddeck, comHand, userHand, Yama, getCom, getUser, dispCom
    global gameOverP, comPlayP, trump
    mX = event.x
    mY = event.y
    userIndex = -1
    pos = 10
    for i in range(len(userHand)):
        if mX > pos and mX < pos+72 and mY > 415 and mY < 515:
            userIndex = i
            break
        pos += 72
    if userIndex < 0:
        return
    if comPlayP == False:
        suit = userHand[userIndex].suit
        rank = userHand[userIndex].rank
        comIndex = -1
        for i in range(len(comHand)):
            if comHand[i].suit == suit:
                comIndex = i
                break
        if comIndex < 0:
            for i in range(len(comHand)):
                if comHand[i].suit == trump:
                    comIndex = i
                    break
            if comIndex < 0:
                comindex = random.randrange(0, len(comHand))
        if comHand[comIndex].suit == userHand[userIndex].suit:
            if comHand[comIndex].rank == 0:
                getCom.append(userHand[userIndex])
                getCom.append(comHand[comIndex])
                comPlayP = True
            elif userHand[userIndex].rank == 0:
                getUser.append(userHand[userIndex])
                getUser.append(comHand[comIndex])
                comPlayP = False
            elif comHand[comIndex].rank > userHand[userIndex].rank:
                getCom.append(userHand[userIndex])
                getCom.append(comHand[comIndex])
                comPlayP = True
            else:
                getUser.append(userHand[userIndex])
                getUser.append(comHand[comIndex])
                comPlayP = False
        elif comHand[comIndex].suit == trump:
            getCom.append(userHand[userIndex])
            getCom.append(comHand[comIndex])
            comPlayP = True
        elif userHand[userIndex].suit == trump:
            getUser.append(userHand[userIndex])
            getUser.append(comHand[comIndex])
            comPlayP = False
        else:
            getUser.append(userHand[userIndex])
            getUser.append(comHand[comIndex])
            comPlayP = False
        del userHand[userIndex]
        del comHand[comIndex]
    else:
        suit = userHand[userIndex].suit
        rank = userHand[userIndex].rank
        if suit != dispCom[0].suit:
            flag = False
            for i in range(len(userHand)):
                if userHand[i].suit == dispCom[0].suit:
                    flag = True
                    break
            if flag == True:
                s = "リードは"
                if dispCom[0].suit == 0:
                    s += "クラブ"
                elif dispCom[0].suit == 1:
                    s += "ダイヤ"
                elif dispCom[0].suit == 2:
                    s += "ハート"
                else:
                    s += "スペード"
                s += "です"
                sub_win = Toplevel()
                Message(sub_win, text=s).pack()
                return
        if dispCom[0].suit == userHand[userIndex].suit:
            if dispCom[0].rank == 0:
                getCom.append(userHand[userIndex])
                getCom.append(dispCom[0])
                comPlayP = True
            elif userHand[userIndex].rank == 0:
                getUser.append(userHand[userIndex])
                getUser.append(dispCom[0])
                comPlayP = False
            elif dispCom[0].rank > userHand[userIndex].rank:
                getCom.append(userHand[userIndex])
                getCom.append(dispCom[0])
                comPlayP = True
            else:
                getUser.append(userHand[userIndex])
                getUser.append(dispCom[0])
                comPlayP = False
        elif dispCom[0].suit == trump:
            getCom.append(userHand[userIndex])
            getCom.append(dispCom[0])
            comPlayP = True
        elif userHand[userIndex].suit == trump:
            getUser.append(userHand[userIndex])
            getUser.append(dispCom[0])
            comPlayP = False
        else:
            getCom.append(userHand[userIndex])
            getCom.append(dispCom[0])
            comPlayP = True
        del userHand[userIndex]
    if len(Yama) > 0:
        if comPlayP == True:
            comHand.append(Yama[len(Yama)-1])
            del Yama[len(Yama)-1]
            userHand.append(Yama[len(Yama)-1])
            del Yama[len(Yama)-1]
        else:
            userHand.append(Yama[len(Yama)-1])
            del Yama[len(Yama)-1]
            comHand.append(Yama[len(Yama)-1])
            del Yama[len(Yama)-1]
    if len(comHand) == 0:
        gameOverP = True
        dispCom = []
    elif comPlayP == True:
        comIndex = random.randrange(0, len(comHand))
        dispCom = [comHand[comIndex]]
        del comHand[comIndex]
    else:
        dispCom = []
    ShowBan()

def game_start():
    random.seed()
    card_set()
    gameInitialize()
    ShowBan()

root = Tk()
canvas = Canvas(root, width=1000, height=600)
canvas.pack()
canvas.bind("<ButtonPress-1>", buttonPress)
button = Button(root, text="Game Start", command=game_start)
button.pack()
root.mainloop()
