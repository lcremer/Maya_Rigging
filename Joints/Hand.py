"""
Creates Hand Joints
"""

import maya.cmds as mc

from ..Utils import String as String

# TODO: Mirror creation on given axis
# TODO: create hand using joint chain, to allow for naming digits more specifically

class Hand():
    def __init__(self,
                 characterName = '', 
                 suffix = '',
                 wristName = 'Wrist',
                 fingerName = 'Finger',
                 thumbName = 'Thumb',
                 metaCarpalName = 'MetaCarpal',
                 fingers = 4, 
                 fingerJoints = 4, 
                 metaCarpal = True, 
                 thumb = True, 
                 thumbJoints = 4,
                 wristEndJoint = True,
                 parent = ''):
        """
        @return: returns end joint
        """
        
        self.characterName = characterName
        self.suffix = suffix
        self.wristName = wristName
        self.fingerName = fingerName
        self.thumbName = thumbName
        self.metaCarpalName = metaCarpalName
        self.fingers = fingers
        self.fingerJoints = fingerJoints
        self.metaCarpal = metaCarpal
        self.thumb = thumb
        self.thumbJoints = thumbJoints
        self.wristEndJoint = wristEndJoint
        self.parent = parent
                
        # clearing selection
        mc.select(cl = True)
        self.joints = []
        
        self.topJoint = mc.joint(n = String.combineWith_((characterName, 
                                                          wristName, 
                                                          suffix)), 
                                                          relative=True,
                                                          p = (0, 0, 0))
        self.joints.append(self.topJoint)
        
        self.endJoint = ''
        if wristEndJoint:
            self.endJoint = mc.joint(n = String.combineWith_((characterName, 
                                                              wristName + 'End', 
                                                              suffix)), 
                                                              relative=True,
                                                              p = (1, 0, 0))
            mc.select(self.topJoint)
            self.joints.append(self.endJoint)               
        
        fingerZPos = -0.5
        for i in range(fingers):
            mc.select(self.topJoint)            
            if metaCarpal:
                # creating meta carpal joints
                j = mc.joint(n = String.combineWith_((characterName, 
                                                      metaCarpalName, 
                                                      String.intToAlpha(i+1), 
                                                      suffix)),
                                                      relative=True,
                                                      p=(0.3, 0, fingerZPos+(i*0.24)),
                                                      radius=0.5)
                self.joints.append(j)
            for j in range(fingerJoints):
                x = 0.3    
                y = 0           
                z = 0              
                if j == 0:
                    y = 0.125
                    x = 0.4
                    if not metaCarpal:                       
                        z = fingerZPos+(i*0.24)
                # creating finger joints
                j = mc.joint(n = String.combineWith_((characterName, 
                                                      fingerName, 
                                                      String.intToAlpha(i+1), 
                                                      String.intToAlpha(j+1), 
                                                      suffix)), 
                                                      relative=True,
                                                      p=(x, y, z),
                                                      radius=0.5)
                self.joints.append(j)
        
        if thumb:
            mc.select(self.topJoint)
            for i in range(thumbJoints):
                # creating thumb joints
                j = mc.joint(n = String.combineWith_((characterName, 
                                                      thumbName, 
                                                      String.intToAlpha(i+1), 
                                                      suffix)), 
                                                      relative=True,
                                                      p=(0.2, 0, 0.2),
                                                      radius=0.5)
                self.joints.append(j)
                
        if parent:
            mc.delete(mc.pointConstraint(parent, self.topJoint))
            mc.delete(mc.orientConstraint(parent, self.topJoint))
            mc.parent(self.topJoint, parent)
                
        mc.select(cl = True)                