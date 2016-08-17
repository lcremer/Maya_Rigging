"""
Creates GlobalRoot And Or BodyRoot Joints
"""

import maya.cmds as mc

from ..Utils import String as String

class Root():
    def __init__(self,
                 characterName = '',           
                 bodyName = 'Body', 
                 addGlobal = True, 
                 globalName = 'Root'):
        """
        @return: returns end joint
        """
        
        self.characterName = characterName
        self.bodyName = bodyName
        self.addGlobal = addGlobal
        self.globalName = globalName
        
        characterName = String.add_((characterName))
        
        self.topJoint = ''
        if addGlobal:
            self.topJoint = mc.joint(n=characterName + globalName, p = (0,0,0))
            
        self.endJoint = mc.joint(n=characterName + bodyName, p = (0,3.3,0))        
