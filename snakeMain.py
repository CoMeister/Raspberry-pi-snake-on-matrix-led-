import time
import smbus
import sys
import pygame
import random
import thread

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from snakeClass import snake
from PIL import Image
from webSocketSendPoints import WebSocketHandler
import tornado
from tornado import gen

pygame.init()
print pygame.joystick.get_count()
time.sleep(0.5)
j = pygame.joystick.Joystick(0)
j.init()

print 'Initialized Joystick : %s' % j.get_name()

#i2c
bus = smbus.SMBus(1)

# I2C address of Arduino Slave
address = 0x04

options = RGBMatrixOptions()
options.rows = 32           #32 de haut
options.chain_length = 2    #2X matrix 32 large
options.parallel = 1        #une seul matrix de branche
options.hardware_mapping = 'regular'    #sans shield

snakeObjet = snake()
matrix = RGBMatrix(options = options)   #creer la matrix

#for text
offscreen_canvas = matrix.CreateFrameCanvas()
font1 = graphics.Font()
font1.LoadFont("./fonts/7x13.bdf")
#font1.LoadFont("./fonts/tom-thumb.bdf")

font2 = graphics.Font()
font2.LoadFont("./fonts/6x13B.bdf")

font3 = graphics.Font()
font2.LoadFont("./fonts/5x8.bdf")

font = [font1, font2, font3]


# for image
image = Image.open('snake.png').convert('RGB')

print matrix.width
print matrix.height
oldHeadX = 0
oldHeadY = 0

apple = [random.randrange(0, 63), random.randrange(0, 31)]

dir = 0

speed = 0.3

pos = 2
hardObstacle = [[random.randrange(0, 63), random.randrange(0, 31)]]

play = True



'''pygame.mixer.init(48000, -16, 1, 1024)  #initializing audio mixer
audio1 = pygame.mixer.Sound("snakemusique.wav")
channel1 = pygame.mixer.Channel(1)'''

'''testString = ["one"]
testString.append("two")
testString.append("three")
testString.append("four")
print testString[0]
print testString[len(testString)-1]'''


'''def ws():
    time.sleep(5)
    app = tornado.web.Application(handlers=[(r"/", tornado.websocket.WebSocketHandler)])
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8888)
    # main_loop = tornado.ioloop.IOLoop.instance()
    tornado.ioloop.IOLoop.instance().start()
    tornado.websocket.WebSocketHandler.write_message("erwer")'''


#thread.start_new_thread( ws, () )

def getJoyStat():
    out = [0,0,0,0,0,0, 0, 0, 0, 0, 0]
    pygame.event.pump()
    #Read input from buttons
    for i in range(0, 2):
        out[i] = j.get_hat(0)[i]
    out[3] = j.get_button(8)
    out[4] = j.get_button(9)
    for i in range(6, 10):
        out[i] = j.get_button(i-6)
    return out

def eatApple():
    global speed
    global apple
    global pos
    if pos != 1:
        apple = [random.randrange(0, 63), random.randrange(0, 31)]  # pop Pomme
    else:
        apple = [random.randrange(1, 62), random.randrange(1, 30)]  # pop Pomme

    print "---------------------------------- manger apple ----------------------------------"
    print apple
    print "---------------------------------- ------------ ----------------------------------"
    snakeObjet.addElemCorp()
    #bus.write_i2c_block_data(address, 0, [len(snakeObjet.getCorp())])
    speed = speed * 0.95

def displayText(x, y, font_taille, textdislpay, r, g, b, clear):
    global offscreen_canvas
    global font
    global posText
    textColor = graphics.Color(r, g, b)
    if clear:
        offscreen_canvas.Clear()

    '''if level == 1:
        level = level*10+1
    else:
        level = level * 10'''
    graphics.DrawText(offscreen_canvas, font[font_taille], x, y, textColor, textdislpay)

def home():
    global offscreen_canvas
    global image
    img_width, img_height = image.size
    xpos = 0
    while True:
        try:
            xpos += 1
            if xpos > img_width:
                xpos = 0
            offscreen_canvas.SetImage(image, -xpos)
            offscreen_canvas.SetImage(image, -xpos + img_width)
            #displayText(17, 10, 0, "Start", 200, 100, 100, False)
            offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
            print getJoyStat()
            if getJoyStat()[4] == 1:  # start
                time.sleep(0.4)
                difficulty()
            time.sleep(0.02)
        except KeyboardInterrupt:
            pygame.joystick.quit()
            sys.exit(0)
            raise

def menuPos():
    global pos
    global offscreen_canvas
    filePoints = open("/var/www/html/snake/points", "r+")
    pointsTab = filePoints.readline().split(";")
    if pos == 2:
        displayText(1, 7, 1, ">Easy", 100, 100, 100, True)
        displayText(50, 7, 1, str(pointsTab[0]), 200, 50, 50, False)
        displayText(6, 18, 1, "Medium", 100, 100, 100, False)
        displayText(50, 18, 1, str(pointsTab[1]), 200, 50, 50, False)
        displayText(6, 27, 1, "Hard", 100, 100, 100, False)
        displayText(50, 27, 1, str(pointsTab[2]), 200, 50, 50, False)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
    elif pos == 1:
        displayText(6, 7, 1, "Easy", 100, 100, 100, True)
        displayText(50, 7, 1, str(pointsTab[0]), 200, 50, 50, False)
        displayText(1, 18, 1, ">Medium", 100, 100, 100, False)
        displayText(50, 18, 1, str(pointsTab[1]), 200, 50, 50, False)
        displayText(6, 27, 1, "Hard", 100, 100, 100, False)
        displayText(50, 27, 1, str(pointsTab[2]), 200, 50, 50, False)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
    elif pos == 0:
        displayText(6, 7, 1, "Easy", 100, 100, 100, True)
        displayText(50, 7, 1, str(pointsTab[0]), 200, 50, 50, False)
        displayText(6, 18, 1, "Medium", 100, 100, 100, False)
        displayText(50, 18, 1, str(pointsTab[1]), 200, 50, 50, False)
        displayText(1, 27, 1, ">Hard", 100, 100, 100, False)
        displayText(50, 27, 1, str(pointsTab[2]), 200, 50, 50, False)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

def difficulty():
    global pos
    menuPos()
    while True:
        if getJoyStat()[1] == 1 or getJoyStat()[9] == 1:  # up
            if pos < 2:
                pos += 1
            else:
                pos = 0
            menuPos()
            time.sleep(0.3)
        elif getJoyStat()[1] == -1 or getJoyStat()[7] == 1:  # bottom
            if pos > 0:
                pos -= 1
            else:
                pos = 2

            menuPos()
            time.sleep(0.3)
        elif getJoyStat()[4] == 1:  # start
            time.sleep(0.4)
            newGame(pos)

def popObstacles():
    global hardObstacle
    if len(hardObstacle) > 1:
        for i in range(0, len(snakeObjet.getCorp()) - 1):
            matrix.SetPixel(hardObstacle[i][0], hardObstacle[i][1], 0, 0, 0)
    for i in range(0, len(snakeObjet.getCorp())):
        x = random.randint(0, 63)
        y = random.randint(0, 31)
        while (True):
            if snakeObjet.getTeteX() - x >= 5 or snakeObjet.getTeteX() - x <= -5 and snakeObjet.getTeteY() - y >= 5 or snakeObjet.getTeteY() - y <= -5:
                break
            else:
                x = random.randint(0, 63)
                y = random.randint(0, 31)

        matrix.SetPixel(x, y, 52, 21, 193)
        try:
            hardObstacle[i] = [x, y]
        except IndexError:
            hardObstacle.append([x, y])

def gameOver():
    global play
    global pos
    global offscreen_canvas
    filePoints = open("/var/www/html/snake/points", "r+")
    pointsTab = filePoints.readline().split(";")

    points = (len(snakeObjet.getCorp()) - 3)

    displayText(1, 9, 0, "Game Over", 150, 10, 10, True)
    displayText(10, 18, 1, ("%02d points" % (points)), 100, 100, 100, False)
    displayText(5, 27, 1, "Press Start", 100, 100, 100, False)
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

    print "--- points ---"
    print points
    print pointsTab[0]
    print "pos"
    print pos

    if pos == 2:
        if points > int(pointsTab[0]):
            pointsTab[0] = len(snakeObjet.getCorp()) - 3
            print "Ui"
    elif pos == 1:
        if points > int(pointsTab[1]):
            pointsTab[1] = len(snakeObjet.getCorp()) - 3
    elif pos == 0:
        if points > int(pointsTab[2]):
            pointsTab[2] = len(snakeObjet.getCorp()) - 3

    filePoints.seek(0)
    print pointsTab
    filePoints.writelines((str(pointsTab[0]).rstrip() + ";") + (str(pointsTab[1]).rstrip() + ";") + (str(pointsTab[2]).rstrip() + ";"))
    filePoints.close()


    while True:
        global pos
        try:
            if getJoyStat()[4] == 1:  # start
                time.sleep(0.4)
                newGame(pos)
            elif getJoyStat()[3] == 1:
                difficulty()

        except KeyboardInterrupt:
            pygame.joystick.quit()
            sys.exit(0)
            raise

def pause():
    global pos
    global offscreen_canvas
    displayText(15, 10, 0, "Pause", 100, 100, 100, True)
    displayText(5, 18, 1, "Press Start", 20, 100, 20, False)
    displayText(5, 27, 1, "To continue", 100, 100, 100, False)
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
    while True:
        try:
            if getJoyStat()[4] == 1:  # start
                time.sleep(0.4)
                play(pos)
        except KeyboardInterrupt:
            pygame.joystick.quit()
            sys.exit(0)
            raise

def newGame(pos):
    global oldHeadX
    global oldHeadY
    global apple
    global dir
    global speed
    global play
    global snakeObjet
    global offscreen_canvas

    snakeObjet = snake()
    oldHeadX = 0
    oldHeadY = 0
    dir = 0
    speed = 0.3
    #channel1.play(audio1)
    matrix.Clear()
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)  # clear canva
    matrix.Clear()
    play(pos)

def play(pos): # 2 easy, 1 medium, 0 hard
    global offscreen_canvas
    global hardObstacle
    global apple
    global play
    global dir
    global oldHeadX
    global oldHeadY
    apple = [random.randrange(1, 62), random.randrange(1, 30)]

    if pos == 1:
        graphics.DrawLine(offscreen_canvas, 0, 0, 63, 0, graphics.Color(100, 100, 100))
        graphics.DrawLine(offscreen_canvas, 63, 1, 63, 30, graphics.Color(100, 100, 100))
        graphics.DrawLine(offscreen_canvas, 63, 31, 1, 31, graphics.Color(100, 100, 100))
        graphics.DrawLine(offscreen_canvas, 0, 31, 0, 1, graphics.Color(100, 100, 100))
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)  # clear canva
    eatApp = False
    matrix.SetPixel(apple[0], apple[1], 255, 20, 20)  # afficher la apple
    oldLastCorp = [5, 1]
    while True:
        print pos
        try:
            # time_now = time.time() - start_time
            # print("- %s seconds -" % (time_now))
            print getJoyStat()
            if getJoyStat()[0] == -1 or getJoyStat()[6] == 1:  # left
                dir = 2
            elif getJoyStat()[1] == -1 or getJoyStat()[7] == 1:  # bottom
                dir = 3
            elif getJoyStat()[0] == 1 or getJoyStat()[8] == 1:  # right
                dir = 0
            elif getJoyStat()[1] == 1 or getJoyStat()[9] == 1:  # up
                dir = 1
            elif getJoyStat()[4] == 1:  # pause
                time.sleep(0.4)
                pause()

            #matrix.Clear()
            matrix.SetPixel(oldLastCorp[0], oldLastCorp[1], 0, 0, 0)  # effacer le dernier ellement du corp

            matrix.SetPixel(snakeObjet.getTeteX(), snakeObjet.getTeteY(), 55, 43, 89)  # afficher la tete

            for unCorp in snakeObjet.getCorp():  # afficher le corp
                matrix.SetPixel(unCorp[0], unCorp[1], 37, 124, 0)

            oldHeadX = snakeObjet.getTeteX()
            oldHeadY = snakeObjet.getTeteY()

            oldLastCorp = [snakeObjet.getCorpX(len(snakeObjet.getCorp()) - 1),snakeObjet.getCorpY(len(snakeObjet.getCorp()) - 1)]

            print oldLastCorp



            if snakeObjet.move(dir) == True:
                gameOver()

            print snakeObjet.getTeteX(), snakeObjet.getTeteY()

            if pos == 1:
                if snakeObjet.getTeteY() == 0:
                    gameOver()
                elif snakeObjet.getTeteY() == 31:
                    gameOver()

                if snakeObjet.getTeteX() == 0:
                    gameOver()
                elif snakeObjet.getTeteX() == 63:
                    gameOver()

            matrix.SetPixel(apple[0], apple[1], 255, 20, 20)  # afficher la apple
            if eatApp == True:
                if pos == 0:
                    popObstacles()
                    eatApp = False

            if (snakeObjet.tete == apple):  # manger apple
                eatApple()
                eatApp = True
            else:
                if len(hardObstacle) > 1:
                    for i in range(0, len(hardObstacle) - 1):
                        if (snakeObjet.tete == hardObstacle[i]):
                            gameOver()




            # print("--- %s seconds ---" % (2))
            time.sleep(speed)
        except KeyboardInterrupt:
            pygame.joystick.quit()
            sys.exit(0)
            raise


home()

