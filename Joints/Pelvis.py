"""
Creates Pelvis
"""

import maya.cmds as mc

from ..Utils import String as String

class Pelvis():
    def __init__(self,
                 characterName = '', 
                 suffix = '',
                 name = 'Pelvis',
                 parent = ''):
        """
        @return: returns end joint
        """
        
        self.characterName = characterName
        self.suffix = suffix
        self.name = name
            
        mc.select(cl = True)
        self.topJoint = mc.joint(n = String.combineWith_((characterName, name, suffix)), p = (0,3,0))
        self.endJoint = self.topJoint
               
        if parent:
            mc.delete(mc.pointConstraint(parent, self.topJoint))
            mc.delete(mc.orientConstraint(parent, self.topJoint))
            mc.parent(self.topJoint, parent)
        
        mc.select(cl = True)
        #return {'topJoint':topJoint, 'endJoint':topJoint}