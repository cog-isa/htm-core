# -*- coding: utf8 -*-
__author__ = 'AVPetrov'

class HTMSettings:

    def __init__(self):
        self.debug=False
        self.activationThreshold = 0
        self.minOverlap = 0
        self.desiredLocalActivity = 0
        self.connectedPct = 0
        self.connectedPerm = 0
        self.xInput = 0
        self.yInput = 0
        self.potentialRadius = 0
        self.xDimension = 0
        self.yDimension = 0
        self.initialInhibitionRadius = 0
        self.permanenceInc = 0
        self.permanenceDec = 0
        self.cellsPerColumn=0
        self.maxBoost=0
        self.debug=True
        minDutyCycleFraction=0

    @staticmethod
    def getDefaultSettings():
        setting = HTMSettings()
        setting.activationThreshold = 1;
        setting.minOverlap = 1;
        setting.desiredLocalActivity = 3;
        setting.connectedPct=1;
        setting.connectedPerm=0.01;
        setting.potentialRadius=4;
        setting.xDimension=10;
        setting.yDimension=10;
        setting.initialInhibitionRadius=1;
        setting.permanenceInc=0.1;
        setting.permanenceDec=0.1;
        setting.cellsPerColumn=2
        setting.minDutyCycleFraction=2
        setting.maxBoost=1
        setting.debug=True
        return setting

