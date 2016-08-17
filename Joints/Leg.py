"""
Creates Hip, Knee, Ankle Joints
"""

import maya.cmds as mc

from ..Utils import String as String

class Leg():
    def __init__(self,
                 characterName = '', 
                 suffix = '',           
                 hipName = 'Hip', 
                 kneeName = 'Knee', 
                 ankleName = 'Ankle',            
                 thighTwist = False, 
                 shinTwist = False,
                 position = (0.5,0,0),
                 parent = ''):
        """
        @return: returns end joint
        """
        
        self.characterName = characterName
        self.suffix = suffix
        self.hipName = hipName
        self.kneeName = kneeName
        self.ankleName = ankleName
        self.thighTwist = thighTwist
        self.shinTwist = shinTwist
        self.position = position
        self.parent = parent
                    
        if parent:
            # selecting parent
            mc.select(parent)        
                
        #TODO: position knee and ankle based on length and depth
        self.joints = []
        
        # creating hip joint
        self.topJoint = mc.joint(n = String.combineWith_((characterName, hipName, suffix)), relative=True, p = position)
        self.joints.append(self.topJoint)
        
        # creating knee joint
        knee = mc.joint(n = String.combineWith_((characterName, kneeName, suffix)), relative=True, p = (0,position[1]-1.25,0.5))    
        self.joints.append(knee)
        
        # creating ankle joint
        self.endJoint = mc.joint(n = String.combineWith_((characterName, ankleName, suffix)), relative=True, p = (0,position[1]-1.55,position[2]-0.5))
        self.joints.append(self.endJoint)        

        # clearing selection
        mc.select(cl = True)        
