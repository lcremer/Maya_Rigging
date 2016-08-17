"""
Creates Foot, Ball, Toes Joints
"""

import maya.cmds as mc

from ..Utils import String as String

class Foot():
    def __init__(self,
                 characterName = '', 
                 suffix = '',           
                 footName = 'Foot', 
                 ballName = 'ball', 
                 toesName = 'toes',
                 position = (0,0,0),
                 parent = ''):
        """
        @return: returns end joint
        """
        
        self.characterName = characterName
        self.suffix = suffix
        self.footName = footName
        self.ballName = ballName
        self.toesName = toesName        
        self.position = position
        self.parent = parent
                    
        if parent:
            # selecting parent
            mc.select(parent)        
                
        #TODO: position knee and ankle based on length and depth
        self.joints = []
        
        # creating foot joint
        self.topJoint = mc.joint(n = String.combineWith_((characterName, footName, suffix)), relative=True, p = position)
        self.joints.append(self.topJoint)
        
        # creating ball joint
        ball = mc.joint(n = String.combineWith_((characterName, ballName, suffix)), relative=True, p = (0,-.35,0.25))    
        self.joints.append(ball)
        
        # creating toes joint
        self.endJoint = mc.joint(n = String.combineWith_((characterName, toesName, suffix)), relative=True, p = (0,0,0.5))
        self.joints.append(self.endJoint)        

        # clearing selection
        mc.select(cl = True)
