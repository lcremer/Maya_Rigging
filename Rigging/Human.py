"""
Creates human skeleton
"""

import maya.cmds as mc

from ..Utils import String as String

from ..Joints.Root import Root as sRoot
from ..Joints.Pelvis import Pelvis as sPelvis
from ..Joints.Leg import Leg as sLeg
from ..Joints.Foot import Foot as sFoot
from ..Joints.Chain import Chain as sChain
from ..Joints.Chest import Chest as sChest
from ..Joints.Arm import Arm as sArm
from ..Joints.Hand import Hand as sHand
from ..Joints.Head import Head as sHead

def Create(characterName = 'human'):
    
    root = sRoot(characterName = characterName)
    
    pelvis = sPelvis(characterName = characterName, parent = root.endJoint)
    
    lLeg = sLeg(characterName = characterName, suffix = 'Lt', parent = pelvis.endJoint)    
    lFoot = sFoot(characterName = characterName, suffix = 'Lt', parent = lLeg.endJoint)
    mc.mirrorJoint(lLeg.topJoint, mirrorYZ = True, mirrorBehavior = True, searchReplace=('_Lt','_Rt'))
    
    spine = sChain(characterName = characterName, count = 4, length = 0.4, parent = root.endJoint, n = (0,1,0), posToParent=True)
    
    chest = sChest(characterName = characterName, parent = spine.endJoint)
    
    lArm = sArm(characterName = characterName, suffix = 'Lt', parent = chest.topJoint)
    lHand = sHand(characterName = characterName, suffix = 'Lt', parent = lArm.endJoint)
    mc.mirrorJoint(lArm.topJoint, mirrorYZ = True, mirrorBehavior = True, searchReplace=('_Lt','_Rt'))
    
    neck = sChain(characterName = characterName, name = 'Neck', count = 3, length = 0.25, parent = chest.topJoint, n = (0,1,0))
    head = sHead(characterName = characterName, parent = neck.endJoint)    

    return root