from trace import Trace

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


class snake:
    tete = []

    corp = []

    def __init__(self):
        self.tete = [4, 1]
        self.corp = [[1, 1], [2, 1], [3, 1]]

    def addElemCorp(self):
        self.corp.append([self.corp[len(self.corp)-1][0], self.corp[len(self.corp)-1][1]])

    def move(self, dir): #dificulty --> 2 easy, 1 medium, 0 hard
        touch = False
        for posList in range(len(self.corp)-1, 0, -1):
            self.corp[posList][0] = self.corp[posList - 1][0]
            self.corp[posList][1] = self.corp[posList - 1][1]
            #print self.corp[posList]
        '''self.corp[2][0] = self.corp[1][0]
        self.corp[2][1] = self.corp[1][1]

        self.corp[1][0] = self.corp[0][0]
        self.corp[1][1] = self.corp[0][1]'''

        self.corp[0][0] = self.tete[0]
        self.corp[0][1] = self.tete[1]
        #self.corp[0] = self.tete

        '''print self.corp[0]
        print self.corp[1]
        print self.corp[2]'''

        if dir == 0:
            self.tete[0] += 1 #droite
            if(self.tete[0] == 64):
                self.tete[0] = 0
        elif dir == 1:
            self.tete[1] -= 1 #haut
            if (self.tete[1] == -1):
                self.tete[1] = 31
        elif dir == 2:
            self.tete[0] -= 1 #gauche
            if (self.tete[0] == -1):
                self.tete[0] = 63
        elif dir == 3:
            self.tete[1] += 1 #bas
            if (self.tete[1] == 32):
                self.tete[1] = 0
        return self.touch()

    def touch(self):
        for i in range(0, len(self.corp)-1):
            if self.tete[0] == self.corp[i][0] and self.tete[1] == self.corp[i][1]:
                return True



    def getTeteX(self):
        return self.tete[0]

    def getTeteY(self):
        return self.tete[1]

    def getCorp(self):
        return self.corp

    def getCorpX(self, pos):
        return self.corp[pos][0]

    def getCorpY(self, pos):
        return self.corp[pos][1]




