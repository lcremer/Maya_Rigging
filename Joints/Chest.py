"""
Creates Pelvis
"""

import maya.cmds as mc

from ..Utils import String as String

class Chest():
    def __init__(self,
                 characterName = '', 
                 name = 'Chest',
                 suffix = '',           
                 position = (0,0,0),
                 chestEnd = True,
                 parent = ''):
        """
        @return: returns end joint
        """      
        
        self.characterName = characterName
        self.name = name
        self.suffix = suffix
        self.position = position
        self.parent = parent
                        
        if parent:
            # selecting parent
            mc.select(parent)
        
        # creating chest joint
        self.topJoint = mc.joint(n = String.combineWith_((characterName, name, suffix)), relative=True, p = position)
        self.endJoint = self.topJoint
        
        if chestEnd:
            # creating chest end joint
            self.endJoint = mc.joint(n = String.combineWith_((characterName, name+'End', suffix)), relative=True, p = (0,0.75,0.15))

        # clearing selection
        mc.select(cl = True)        