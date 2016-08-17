from Head import Head
from Head import Neck
from Head import HeadNeck
from Arm import Arm
from Leg import LegBiped
from Leg import LegQuad
from Spine import Spine
from Tentacle import Tentacle
from Fingers import createFingers

class DummyBuild:
    def __init__(self):
        pass

    @staticmethod
    def Head(name, side, moduleName, colorIndex):
        Head(name=name,side=side,moduleName=moduleName,colorIndex=colorIndex)

    @staticmethod
    def Neck(name, side, moduleName, numCon, axis, dis, colorIndex):
        Neck(name=name, side=side, moduleName=moduleName, numCon=numCon, colorIndex=colorIndex)

    # TODO: clean this up so Head and Neck can be used separately
    @staticmethod
    def HeadNeck(name, side, moduleName, numCon, axis, dis, colorIndex):
        HeadNeck(name=name, side=side, moduleName=moduleName, numCon=numCon, axis=axis, dis=dis, colorIndex=colorIndex)

    @staticmethod
    def Arm(name, side, numJoints, fingers, numFingers, numSegment, colorIndex):
        Arm(name=name, side=side, numJoints=numJoints, fingers=fingers, numFingers=numFingers, numSegment=numSegment, colorIndex=colorIndex)

    @staticmethod
    def LegBiped(name, side, numJoints, fingers, numFingers, numSegment, colorIndex):
        LegBiped(name=name, side=side, numJoints=numJoints, fingers=fingers, numFingers=numFingers, numSegment=numSegment, colorIndex=colorIndex)

    @staticmethod
    def LegQuad(name, side, numJoints, fingers, numFingers, numSegment, colorIndex):
        LegQuad(name=name, side=side, numJoints=numJoints, fingers=fingers, numFingers=numFingers, numSegment=numSegment, colorIndex=colorIndex)

    @staticmethod
    def Spine(name, side, moduleName, numCon, axis, dis, colorIndex):
        Spine(name=name, side=side, moduleName=moduleName, numCon=numCon, axis=axis, dis=dis, colorIndex=colorIndex)

    @staticmethod
    def Tentacle(name, side, moduleName, numCon, axis, dis, colorIndex):
        Tentacle(name=name, side=side, moduleName=moduleName, numCon=numCon, axis=axis, dis=dis, colorIndex=colorIndex)

    @staticmethod
    def Fingers(name, fingerName, side, numCon, axis, dis, colorIndex):
        createFingers(name=name, fingerName=fingerName, side=side, numCon=numCon, axis=axis, val=dis, colorIndex=colorIndex)

