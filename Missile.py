class Missile:

    def __init__(self, xInitialPos, yInitialPos):
        self.__missilePosX = xInitialPos
        self.__missilePosY = yInitialPos

    def missileMove(self):
        self.__missilePosY -= 4

    def getPosX(self):
        return self.__missilePosX

    def getPosY(self):
        return self.__missilePosY

    def getPosition(self):
        return (self.__missilePosX, self.__missilePosY)
