"""
Creates Head Joints
"""

import maya.cmds as mc

from ..Utils import String as String

class Head():
    def __init__(self,
                 characterName = '', 
                 suffix = '',
                 headName = 'Head',
                 jawName = 'Jaw',
                 eyeName = 'Eye',           
                 jaw = True,
                 jawEnd = True,
                 lEye = True,
                 rEye = True,
                 headEnd = True,
                 parent = ''):
        """
        @return: returns end joint
        """
        
        self.characterName = characterName
        self.suffix = suffix
        self.headName = headName
        self.jawName = jawName
        self.eyeName = eyeName
        self.jaw = jaw
        self.jawEnd = jawEnd
        self.lEye = lEye
        self.rEye = rEye
        self.parent = parent
                                
        if parent:
            # selecting parent
            mc.select(parent)
        
        # creating head joint
        self.topJoint = mc.joint(n = String.combineWith_((characterName, headName, suffix)), relative=True, p = (0, 0.25, 0))
        self.endJoint = self.topJoint
        if jaw:
            mc.joint(n = String.combineWith_((characterName, jawName, suffix)), relative=True, p = (0, -0.15, 0.2))
            if jawEnd:
                mc.joint(n = String.combineWith_((characterName, jawName + 'End', suffix)), relative=True, p = (0, 0, 0.55))
                                
        # selecting head joint        
        mc.select(self.topJoint)
        
        if headEnd:
            mc.joint(n = String.combineWith_((characterName, headName+'End',suffix)), relative=True, p = (0, 0.75, 0))
            # re-selecting head joint        
            mc.select(self.topJoint)        
        
        if lEye:
            # creating lEye joint
            mc.joint(n = String.combineWith_((characterName, eyeName,suffix,'Lt')), relative=True, p = (0.35, 0.45, 0.75))
            
        mc.select(self.topJoint)
        if rEye:
            # creating lEye joint
            mc.joint(n = String.combineWith_((characterName, eyeName,suffix,'Rt')), relative=True, p = (-0.35, 0.45, 0.75))
                        
        # clearing selection
        mc.select(cl = True)        