import random

__author__ = 'AVPetrov'

class Synapse:
    def __init__(self,settings,indexConnectTo,initPermanence):
        self.settings = settings;
        self.indexConnectTo = indexConnectTo;
        self.permanence = initPermanence;
        self.rand=random.Random()
        self.rand.seed=10


    # /**
    #  * Случайные значения преманентности должны быть из малого диапазона около connectedPerm
    #  */
    def initPermanence(self,k):
        if self.settings.debug==True:
            self.permanence = self.settings.connectedPerm
            self.permanence=self.permanence*(1/(k==0 if 0.5 else k))
        else:
            if random.nextDouble() <= self.settings.initConnectedPct:
                self.permanence = self.settings.connectedPerm + self.rand.random() * self.settings.permanenceInc / 4.0
            else:
                self.permanence = self.settings.connectedPerm - self.random.random() * self.settings.permanenceInc / 4.0
                self.permanence=self.permanence*(1/(k==0 if 0.5 else k))

    def increasePermanence(self):
        self.permanence = self.permanence + self.settings.permanenceInc
        self.permanence = self.permanence > 1 if 1 else self.permanence


    def decreasePermanence(self):
        self.permanence = self.permanence - self.settings.permanenceDec
        self.permanence = self.permanence < 0 if 0 else self.permanence


    def isConnected(self):
        return self.permanence > self.settings.connectedPerm


    # /* connectToIndex - это либо номер бита из сигнала снизу, либо номер клетки (аксон) при латеральной связи */
    def getIndexConnectTo(self):
        return self.indexConnectTo


    # /* Получить степени связанности между аксоном и дендритом. */
    def getPermanence(self):
        return self.permanence

    # /* Установить степени связанности между аксоном и дендритом. */
    def setPermanence(self,permanence):
        self.permanence = permanence