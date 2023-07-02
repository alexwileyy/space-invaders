class Invader:

    #Set the initial variables for the X and Y position.
    def __init__(self):
        self.__alienPosX = 100
        self.__alienPosY = 100

    #Set position of invader for X
    def setPosX(self, x):
        self.__alienPosX = x

    #Set position of invader for Y
    def setPosY(self, y):
        self.__alienPosY = y

    #Access method for invader X position
    def getPosX(self):
        return self.__alienPosX

    #Access method for invader Y position
    def getPosY(self):
        return self.__alienPosY

    #Access method to get position of invader X and Y
    def getPosition(self):
        return (self.__alienPosX, self.__alienPosY)

    #Method for horizontal movement
    def moveHorizontal(self, amount):
        self.__alienPosX = self.__alienPosX + amount

    #Method for vertical movement
    def moveVertical(self,amount):
        self.__alienPosY = self.__alienPosY + amount
