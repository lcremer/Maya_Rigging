"""
Creates Clavicle, Shoulder, Elbow, Wrist Joints
"""

import maya.cmds as mc

from ..Utils import String as String


class Arm:
    def __init__(self,
                 characterName = '',
                 suffix = '',
                 clavicleName = 'Clavicle',
                 shoulderName = 'Shoulder', 
                 elbowName = 'Elbow', 
                 wristName = 'Hand',
                 clavicle = True,
                 shoulderTwist = False, 
                 foreTwist = False,
                 parent = ''):
        
        self.characterName = characterName
        self.suffix = suffix
        self.clavicleName = clavicleName
        self.shoulderName = shoulderName
        self.elbowName = elbowName
        self.wristName = wristName
        self.clavicle = clavicle      
        self.shoulderTwist = shoulderTwist
        self.foreTwist = foreTwist
        self.parent = parent
        self.joints = []
                                    
        if parent:
            # selecting parent
            mc.select(parent)

        self.topJoint = ''
        if clavicle:                
            # creating clavicle
            self.topJoint =  mc.joint(n = String.combineWith_((characterName, clavicleName, suffix)), relative=True, p = (0.25,0.75,0))
            self.joints.append(self.topJoint)            

        # creating shoulder joint
        shoulder = mc.joint(n = String.combineWith_((characterName, shoulderName, suffix)), relative=True, p = (0.75,0,0))
        self.joints.append(shoulder)
        if not clavicle:
            self.topJoint = shoulder
            
        # creating elbow joint
        elbow = mc.joint(n = String.combineWith_((characterName, elbowName, suffix)), relative=True, p = (1,0,-0.5))
        self.joints.append(elbow)
        
        # creating hand joint
        self.endJoint = mc.joint(n = String.combineWith_((characterName, wristName, suffix)), relative=True, p = (1.1,0,0.5))
        self.joints.append(self.endJoint)        
        
        # clearing selection
        mc.select(cl = True)                