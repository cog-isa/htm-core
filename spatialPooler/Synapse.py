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
    #  * ��������� �������� �������������� ������ ���� �� ������ ��������� ����� connectedPerm
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


    # /* connectToIndex - ��� ���� ����� ���� �� ������� �����, ���� ����� ������ (�����) ��� ����������� ����� */
    def getIndexConnectTo(self):
        return self.indexConnectTo


    # /* �������� ������� ����������� ����� ������� � ���������. */
    def getPermanence(self):
        return self.permanence

    # /* ���������� ������� ����������� ����� ������� � ���������. */
    def setPermanence(self,permanence):
        self.permanence = permanence