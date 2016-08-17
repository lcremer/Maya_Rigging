"""
Creates Joint chains, Tail/Spine/Neck
"""

import maya.cmds as mc

from ..Utils import String as String
from ..Utils import Vector as Vector

#TODO: add attribute for LimbType IE Root, Chain, Limb, Hand, Foot
#TODO: freeze transforms, give option to point or orient to Parent
class Chain():
    def __init__(self,
                 characterName = '',            
                 name = 'Spine', 
                 suffix = '',
                 count = 5, 
                 length = 0.5,
                 n=(0,1,0),                 
                 topOffset = (0,0.25,0),
                 parent = '',                 
                 posToParent = False):
        """
        @return: returns end joint
        """
        
        self.characterName = characterName
        self.name = name
        self.suffix = suffix
        self.count = count
        self.length = length
        self.n = n
        self.parent = parent
        
        if parent:
            # selecting parent
            mc.select(parent)
                   
        self.joints = []
        # creating spine joints
        v = (n[0] * length, n[1] * length, n[2] * length)
        for i in range(count):            
            j = mc.joint(n=String.combineWith_((characterName, name, String.intToAlpha(i+1), suffix)), relative = True, p = v)
            self.joints.append(j)        

        self.topJoint = self.joints[0]
        self.endJoint = self.joints[-1]

        offset = Vector.addVec3toVec3(v,topOffset)
        mc.xform(self.topJoint,r=1,t=offset)
        
        if posToParent:
            mc.delete(mc.parentConstraint(parent,self.topJoint))                   
        
        # clearing selection
        mc.select(cl = True)