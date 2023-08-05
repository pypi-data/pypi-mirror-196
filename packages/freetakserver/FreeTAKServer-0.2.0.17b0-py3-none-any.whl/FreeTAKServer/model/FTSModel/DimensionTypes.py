from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
#######################################################
# 
# DimensionTypes.py
# Python implementation of the Class DimensionTypes
# Generated by Enterprise Architect
# Created on(FTSProtocolObject):    11Feb2020 11:08:09 AM
# Original author: Corvo
# 
#######################################################


class DimensionTypes(FTSProtocolObject):
# default constructor    def __init__(self):  

    space = "p" 
    # space getter 
    def getspace(self): 
        return self.space 
 
    # space setter 
    def setspace(self,space=0):  
        self.space=space 
 
    air = "A" 
    # air getter 
    def getair(self): 
        return self.air 
 
    # air setter 
    def setair(self,air=0):  
        self.air=air 
 
    landunit = "G" 
    # landunit getter 
    def getlandunit(self): 
        return self.landunit 
 
    # landunit setter 
    def setlandunit(self,landunit=0):  
        self.landunit=landunit 
 
    landequipment = "G" 
    # landequipment getter 
    def getlandequipment(self): 
        return self.landequipment 
 
    # landequipment setter 
    def setlandequipment(self,landequipment=0):  
        self.landequipment=landequipment 
 
    landinstallation = "G" 
    # landinstallation getter 
    def getlandinstallation(self): 
        return self.landinstallation 
 
    # landinstallation setter 
    def setlandinstallation(self,landinstallation=0):  
        self.landinstallation=landinstallation 
 
    seasurface = "S" 
    # seasurface getter 
    def getseasurface(self): 
        return self.seasurface 
 
    # seasurface setter 
    def setseasurface(self,seasurface=0):  
        self.seasurface=seasurface 
 
    seasubsurface = "U" 
    # seasubsurface getter 
    def getseasubsurface(self): 
        return self.seasubsurface 
 
    # seasubsurface setter 
    def setseasubsurface(self,seasubsurface=0):  
        self.seasubsurface=seasubsurface 
 
    subsurface = "U" 
    # subsurface getter 
    def getsubsurface(self): 
        return self.subsurface 
 
    # subsurface setter 
    def setsubsurface(self,subsurface=0):  
        self.subsurface=subsurface 
 
    other = "X" 
    # other getter 
    def getother(self): 
        return self.other 
 
    # other setter 
    def setother(self,other=0):  
        self.other=other 
    