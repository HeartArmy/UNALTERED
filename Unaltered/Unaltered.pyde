
import os
import time
import unicodedata
import csv
from ast import literal_eval
from random import randint
path = os.getcwd() + "/"

item_path = []
for root, dirs, files in os.walk(".", topdown=False):
    #print(root, dirs, files)
    for name in files:
        path2 = os.path.join(root, name)
        if path2.endswith("png"):
            item_path.append(path2)
print(item_path)
start_point = 24
africa_path = item_path[start_point:5 + start_point]
eastAsia_path = item_path[5 + start_point:10 + start_point]
middleEast_path = item_path[10 + start_point:15 + start_point]
southAsia_path = item_path[15 + start_point:20 + start_point]

isUp = False
isDown = False
isLeft = False
isRight = False
isSpace = False
page = 0
continent = 0
mapW = 431
mapH = 287
duration = 20
gameover = False
num_bullet = 0
item_count = 0
finish = False
Time_left = 30
username = 0
instruct = 0
img1 = loadImage(path + "images/arcade-font-writer.png")
img2 = loadImage(path + "images/login.png")
timeImage = loadImage(path + "images/time.png")

class aimer:

    def __init__(self, xPos, yPos):
        self.aimer = loadImage(
            path + "images/" + "aimer.png")
        self.keyp = 0
        self.xPos = xPos
        self.yPos = yPos
        self.aimerSize = 100
        self.speed = 15

    def move(self):
        if isUp:
            self.yPos -= self.speed
            #print("move working")
        if isDown:
            self.yPos += self.speed
        if isRight:
            self.xPos += self.speed
        if isLeft:
            self.xPos -= self.speed

    def hit(self):
        self.ishit = True

    def display(self):
        #print("okay 7")
        image(self.aimer, self.xPos - self.aimerSize / 2,
              self.yPos - self.aimerSize / 2, self.aimerSize, self.aimerSize)
        #rint("okay 8")


class items:

    def __init__(self, image_path, xPos, yPos, Size):
        self.item = loadImage(image_path)
        self.itemSize = Size
        self.xPos = xPos
        self.yPos = yPos
        self.ishit = False

    def display(self):
        if not self.ishit:
            image(self.item, self.xPos - self.itemSize / 2,
                  self.yPos - self.itemSize / 2, self.itemSize, self.itemSize)


class shelf_items:

    def __init__(self, yPos, screenWidth, continentSel, direction):
        global item_count, num_bullet
        item_count = 0
        self.items = []
        self.label = []
        self.sw = screenWidth
        self.dir = direction
        self.speed = direction * 15
        self.finish = False
        for i in range(10):
            num = randint(0, 12)
            # print(num)
            if num < 4:
                self.items.append(items(
                    path + "items_img/" + "bomb.png", self.sw / 20 + self.sw / 10 * i, yPos, self.sw / 12.8))
                self.label.append(1)
            elif num > 3 and num < 8:
                self.items.append(items(
                    path + "items_img/" + "cropcoin.png", self.sw / 20 + self.sw / 10 * i, yPos, self.sw / 19.2))
                self.label.append(2)
            elif num > 7:
                self.label.append(3)
                item_count += 1
                if continentSel % 4 == 0:
                    pathA = africa_path[num % 4]
                elif continentSel % 4 == 1:
                    pathA = eastAsia_path[num % 4]
                elif continentSel % 4 == 2:
                    pathA = middleEast_path[num % 4]
                elif continentSel % 4 == 3:
                    pathA = southAsia_path[num % 4]
                self.items.append(
                    items(path + pathA, self.sw / 20 + self.sw / 10 * i, yPos, self.sw / 12.8))

    def checkHit(self, x, y):
        # for item in self.items:
        global item_count, num_bullet, finish
        for i in range(10):
            if isSpace:
                if (self.items[i].xPos - 50) < x < (self.items[i].xPos + 50) and (self.items[i].yPos - 50) < y < (self.items[i].yPos + 50):
                    self.items[i].ishit = True
                    if self.label[i] == 1:
                        num_bullet -= 1
                        self.label[i] = 0
                    elif self.label[i] == 2:
                        num_bullet += 1
                        self.label[i] = 0
                    elif self.label[i] == 3:
                        item_count -= 1
                        self.label[i] = 0
            if 3 not in self.label:
                self.finish = True

    def move(self):
        for item in self.items:
            item.xPos = (item.xPos + self.speed) % self.sw

    def display(self):
        for item in self.items:
            item.display()


class game:

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.title = loadImage(path + "images/arcade-font-writer.png")
        self.worldMap = loadImage(path + "images/worldMap.png")
        self.region = loadImage(path + "images/region.png")
        self.gameover = loadImage(path + "images/gameover.png")
        self.restart = loadImage(path + "images/restart.png")
        self.won = loadImage(path + "images/won.png")
        self.titlewidth = self.w / 4
        self.titleheight = 80
        self.mapAfrica = loadImage(path + "images/" + "worldmap_africa.png")
        self.mapEastasia = loadImage(
            path + "images/" + "worldmap_eastasia.png")
        self.mapMiddleeast = loadImage(
            path + "images/" + "worldmap_middleeast.png")
        self.mapSouthAsia = loadImage(
            path + "images/" + "worldmap_southasia.png")
        self.cork = cork()
        self.firsttwo = False

    # def start_menu(self):

    def mapPage(self, continentSel):
        background(40)
        mapWidth = self.w / 4.5 * 2
        mapHeight = self.h / 3.76 * 2
        image(self.worldMap, self.w / 2 - mapWidth / 2,
              100, mapWidth - 10, self.h / 12)
        image(self.region, self.w / 2 - mapWidth / 2,
              self.h - 150, mapWidth + 10, self.h / 21.6)
        if continentSel % 4 == 0:
            image(self.mapAfrica, self.w / 2 - mapWidth / 2,
                  self.h / 2 - mapHeight / 2, mapWidth, mapHeight)
        elif continentSel % 4 == 1:
            image(self.mapEastasia, self.w / 2 - mapWidth / 2,
                  self.h / 2 - mapHeight / 2, mapWidth, mapHeight)
        elif continentSel % 4 == 2:
            image(self.mapMiddleeast, self.w / 2 - mapWidth / 2,
                  self.h / 2 - mapHeight / 2, mapWidth, mapHeight)
        elif continentSel % 4 == 3:
            image(self.mapSouthAsia, self.w / 2 - mapWidth / 2,
                  self.h / 2 - mapHeight / 2, mapWidth, mapHeight)

    def mainGameInit(self, continentSel):
        background(15, 68, 122)
        global first_shelf, second_shelf, third_shelf, aimerr, timer1, gameover, num_bullet, finish, item_count
        item_count = 0
        first_shelf = shelf_items(self.h / 4, self.w, continentSel, 1)
        second_shelf = shelf_items(self.h / 2, self.w, continentSel, -1)
        third_shelf = shelf_items(self.h / 1.3, self.w, continentSel, 1)
        aimerr = aimer(self.w / 2, self.h / 2)
        gameover = False
        timer1.initialize()
        num_bullet = 2
        finish = False
        self.firsttwo = False

    def mainGamePlay(self):
        #background(15, 68, 122)
        global num_bullet, finish, first_shelf, second_shelf, third_shelf, finish
        background(15)
        image(self.title, self.w / 2 - self.titlewidth / 2,
              self.titleheight / 2, self.titlewidth, self.titleheight)

        if not gameover:

            if first_shelf.finish and second_shelf.finish:
                self.firsttwo = True

            if third_shelf.finish and self.firsttwo:
                finish = True
                first_shelf.display()
                second_shelf.display()
                third_shelf.display()
                filter(BLUR, 20)
                image(self.won, self.w / 2 - self.titlewidth, self.h / 2 -
                      self.titleheight * 1.5, self.titlewidth * 2, self.titleheight * 2)
                image(self.restart, self.w / 2 - self.titlewidth, self.h -
                      self.titleheight * 4, self.titlewidth * 2, self.titleheight)
            else:
                timer1.displayTime(self.w, self.h)
                aimerr.move()
                first_shelf.move()
                second_shelf.move()
                third_shelf.move()
                first_shelf.checkHit(aimerr.xPos, aimerr.yPos)
                second_shelf.checkHit(aimerr.xPos, aimerr.yPos)
                third_shelf.checkHit(aimerr.xPos, aimerr.yPos)
                first_shelf.display()
                second_shelf.display()
                third_shelf.display()
                aimerr.display()
                self.cork.display(num_bullet, self.w, self.h)

        elif gameover:
            first_shelf.display()
            second_shelf.display()
            third_shelf.display()
            filter(BLUR, 20)
            image(self.gameover, self.w / 2 - self.titlewidth, self.h / 2 -
                  self.titleheight * 1.5, self.titlewidth * 2, self.titleheight * 2)
            image(self.restart, self.w / 2 - self.titlewidth, self.h -
                  self.titleheight * 4, self.titlewidth * 2, self.titleheight)

class cork:

    def __init__(self):
        self.corkpic = loadImage(path + "images/cork.png")
        self.ammoLeft = loadImage(path + "images/corkammo.png")

    def display(self, ammo, w, h):
        image(self.ammoLeft, 10, h - 70, 300, 40)
        for i in range(ammo):
            image(self.corkpic, 320 + (i * 40), h - 70, 30, 40)

class timer:

    def __init__(self):
        self.starttime = millis()

    def initialize(self):
        self.starttime = millis()

    def displayTime(self, w, h):
        currentTime = millis() - self.starttime
        global gameover, Time_left
        sec = currentTime // 1000
        Time_left = duration - sec
        #print("seconds" +str(sec))
        textSize(50)
        text(str(Time_left), w - 90, h - 20)
        if Time_left < 0:
            gameover = True
        image(timeImage, w - 200, h - 50, 100, 40)

class Instruction:

    def __init__(self):
        self.img3 = loadImage(path + "images/instructionTitle.png")
        self.img4 = loadImage(path + "images/InstructionList.png")

    def screen(self):
        if keyPressed:
            if key == SHIFT:
                instruct = 1
        background(15)
        image(self.img3, 500, 50, 500, 100)
        image(self.img4, 350, 200, 800, 800)


class Login:

    def __init__(self):
        global list1, list2, string1, f
        list1 = []
        list2 = []

    def screen(self):
        global username
        if keyPressed:
            if key != CODED:
                time.sleep(0.3)
                list1.append(key)

        background(15)
        fill(15)
        image(img1, 500, 50, 500, 100)
        image(img2, 350, 200, 800, 100)
        # image(img3,650,250,400,200)
        # image(img4,650,450,200,200)
        rect(670, 450, 150, 50)
        fill(255)
        textSize(50)

        print(list1)

        list2 = map(str, list1)
        string1 = convert(list2)
        print(string1)
        text(string1, 670, 500)
        if len(string1) == 5:
            username = 1
            with open('scoreHistory.csv', 'wb') as file:
                file.write(',')
                file.write(str(Time_left))
                file.write('\n')
                file.write(string1)
                #file.write(',')

aimerr = aimer(0, 0)
first_shelf = shelf_items(400, 1500, 1, 1)
second_shelf = shelf_items(400, 1500, 1, -1)
third_shelf = shelf_items(400, 1500, 1, 1)
game1 = game(0, 0)
timer1 = timer()
login1 = Login()
instruction1 = Instruction()

def setup():
    frameRate(40)
    fullScreen()
    wsize = width
    hsize = height
    global first_shelf, second_shelf, third_shelf, aimerr, game1, page, continent
    game1 = game(wsize, hsize)
    background(15, 68, 122)
    print(wsize)
    print(hsize)
    #score_history = open("scoreHistory.csv", 'a')

def draw():
    # game1.mainGamePlay()
    if page == 0:
        login1.screen()
        if username == 1:
            instruction1.screen()
    elif page == 1:
        game1.mapPage(continent)
    elif page == 2:
        game1.mainGamePlay()

def keyPressed():
    global continent, page
    if page == 0:
        if keyCode == SHIFT:
            page = 1
    elif page == 1:
        if keyCode == UP:
            continent += 1
        elif keyCode == DOWN:
            continent -= 1
        elif keyCode == SHIFT:
            page = 2
            game1.mainGameInit(continent)
    elif page == 2:
        if not gameover:
            if not finish:
                setMove(keyCode, True)
            else:
                if keyCode == SHIFT:
                    page = 0
        elif gameover:
            if keyCode == SHIFT:
                page = 0
    # print(isUp)

def keyReleased():
    if page == 2:
        setMove(keyCode, False)

def setMove(k, b):
    global isUp, isDown, isLeft, isRight, isSpace, num_bullet
    if k == UP:
        isUp = b

    elif k == DOWN:
        isDown = b

    elif k == LEFT:
        isLeft = b

    elif k == RIGHT:
        isRight = b

    elif k == SHIFT:
        isSpace = b

def convert(s):
    new = ""
    for x in s:
        new += x
    return new
