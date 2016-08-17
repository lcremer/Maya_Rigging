import pymel.core as pc
import re

from RiggingSystem.Utils import AttrUtil as atu
from ...Utils import *
from RiggingSystem.Utils.CharUtilsLib import *
from RiggingSystem.Core import JointStretchNetworkLib as js

def buildTwistJointSetup(name, side, joint, stretchType, ikFkType, rotConnect, wristJoint, controller, stretch, volume, scale, controlColor = ''):
    transNode = []
    transNodePath = ''
    rotNode = []
    rotNodePath = ''
    childJoint = ''
    transConnection = []
    rotConnection = []
    jointCount = 0
    newJoints = []
    twistAxis = []
    stretchAxis = []
    tempJoint = []
    axis = ''
    color = ''
    rotAdd = ''
    jointRotAdd = ''
    fullchain = []
    transMd = ''
        
    if pc.attributeQuery('twistJoints', n=joint, ex=True):
        jointCount = (pc.getAttr(joint + '.twistJoints')+1)
        if jointCount == 1:
            # TODO: clean this up, shouldn't have to be resetting value to 0
            jointCount = 0
        stretchAxis = getStretchAxis(joint, stretchType)
        twistAxis = getTwistAxis(joint)
        # determine twist axis for further info distribution
        if twistAxis[0] == 'rx':
            axis = 'X'
            color = 'R'
        elif twistAxis[0] == 'ry':
            axis = 'Y'
            color = 'G'
        elif twistAxis[0] == 'rz':
            axis = 'Z'
            color = 'B'
            
        pc.select(joint, r=True)
        atu.removeTwistJointsAttr('twistJoints')
        pc.select(cl=True)
        if jointCount > 0:
            childJoint = getChildJoint(joint)
            if not pc.attributeQuery('twistFixVis', n=controller,ex=True):
                pc.addAttr(controller, ln='twistFixVis', at='bool', keyable=True)
            pc.setAttr((controller + '.twistFixVis'), 1)
        
            if stretch:
                transMd = pc.createNode('multiplyDivide', n=(name + side + joint + '_posSplit_md'))
                pc.setAttr((transMd + '.operation'), 2)
            
                if stretchType == 'translate':
                    transConnection = pc.listConnections((childJoint + '.' + stretchAxis[0]), d=False, s=True, plugs=True, skipConversionNodes=True)
                    transNodePath = transConnection[0]
                    match = re.search('[^.]*', str(transNodePath))
                    if match:
                        transNode.append(match.group())
                    elif transNodePath:
                        transNode.append(transNodePath)
                    pc.setAttr((transMd + '.input2X'), jointCount)
                    pc.setAttr((transMd + '.input2Y'), jointCount)
                    pc.setAttr((transMd + '.input2Z'), jointCount)
                elif stretchType == 'scale':
                    transConnection = pc.listConnections((joint + '.' + stretchAxis[0]), d=False, s=True, plugs=True, skipConversionNodes=True)
                    transNodePath = transConnection[0]                
                    match = re.search('[^.]*', str(transNodePath))
                    if match:
                        transNode.append(match.group())
                    elif transNodePath:
                        transNode.append(transNodePath)
                pc.connectAttr((transNode[0] + '.outputR'), (transMd + '.input1X'))
                pc.connectAttr((transNode[0] + '.outputG'), (transMd + '.input1Y'))
                pc.connectAttr((transNode[0] + '.outputB'), (transMd + '.input1Z'))
        
            rotMd = pc.createNode('multiplyDivide', n=(name + side + joint + '_rotSplit_md'))
            pc.setAttr((rotMd + '.operation'), 2)
        
            if rotConnect == 'parent':
                rotConnection = pc.listConnections((joint + '.' + twistAxis[0]), d=False, s=True, plugs=True, skipConversionNodes=True)
                rotNodePath = rotConnection[0]
                match = re.search('[^.]*', str(rotNodePath))
                if match:
                    rotNode.append(match.group())
                elif rotNodePath:
                    rotNode.append(rotNodePath)
            
                if ikFkType == 'utilNode':
                    pc.setAttr((rotMd + '.input2X'),jointCount)
                    pc.setAttr((rotMd + '.input2Y'),jointCount)
                    pc.setAttr((rotMd + '.input2Z'),jointCount)
                    pc.connectAttr((rotNode[0] + '.outputR'), (rotMd + '.input1X'))
                    pc.connectAttr((rotNode[0] + '.outputG'), (rotMd + '.input1Y'))
                    pc.connectAttr((rotNode[0] + '.outputB'), (rotMd + '.input1Z'))
                
                elif ikFkType == 'constrain':
                    pc.setAttr((rotMd + '.input2X'), jointCount)
                    pc.setAttr((rotMd + '.input2Y'), jointCount)
                    pc.setAttr((rotMd + '.input2Z'), jointCount)
                    pc.connectAttr((rotNode[0] + '.constraintRotate.constraintRotateX'), (rotMd + '.input1X'))
                    pc.connectAttr((rotNode[0] + '.constraintRotate.constraintRotateY'), (rotMd + '.input1Y'))
                    pc.connectAttr((rotNode[0] + '.constraintRotate.constraintRotateZ'), (rotMd + '.input1Z'))
                
                pc.select(cl=True)
                twistCtrl = curveControl('plus', 'curve', controlColor)
                resizeCurves(None, 1, 1, 1, scale)
                twistCtrl[0] = pc.rename(twistCtrl[0], name + side + joint + '_twist_ctrl')                
                Snap(joint, twistCtrl[0])
                zeroGrp = quickZeroOut(twistCtrl[0])
                pc.parentConstraint(joint, zeroGrp[0], weight=1)
                partGrp = pc.listRelatives(controller, parent=True)
                pc.parent(zeroGrp[0], partGrp[0])
                pc.connectAttr((controller + '.twistFixVis'), (twistCtrl[0] + '.visibility'))
                lockAndHide(twistCtrl[0], locknHide, 'trans scale vis')
                pc.setAttr((twistCtrl[0] + '.' + twistAxis[1]),lock=True, keyable=False)
                pc.setAttr((twistCtrl[0] + '.' + twistAxis[2]), lock=True, keyable=False)
            
                rotMulti = pc.createNode('multiplyDivide', n=(name + side + joint + '_addTwist_md'))
                pc.setAttr((rotMulti + '.operation'), 2)
                pc.setAttr((rotMulti + '.input2X'), jointCount)
                pc.setAttr((rotMulti + '.input2Y'), jointCount)
                pc.setAttr((rotMulti + '.input2Z'), jointCount)
            
                rotMultiDouble = pc.createNode('multDoubleLinear', n=(name + side + joint + '_addTwist_mdl'))
                rotAdd = pc.createNode('addDoubleLinear', n=(name + side + joint + '_addTwist_adl'))
                rotBlend = pc.createNode('blendTwoAttr', n=(name + side + joint + '_addTwist_bta'))
                jointRotAdd = pc.createNode('addDoubleLinear', n=(name + side + joint + '_addRot_adl'))
                jointRotBlend = pc.createNode('blendTwoAttr', n=(name + side + joint + '_addRot_bta'))
            
                pc.addAttr(twistCtrl[0], ln='nullifyTwist',  at='double', min=0, max=1, keyable=True)
                pc.connectAttr((twistCtrl[0] + '.' + twistAxis[0]), (rotMulti + '.input1X'))
                pc.connectAttr((rotMulti + '.outputX'), (rotMultiDouble + '.input1'))
                pc.setAttr((rotMultiDouble + '.input2'), -1)
                pc.connectAttr((twistCtrl[0] + '.nullifyTwist'), (rotBlend + '.attributesBlender'))
                pc.connectAttr((rotMd + '.output' + axis), (rotBlend + '.input[0]'))
                pc.setAttr((rotBlend + '.input[1]'), 0)
                pc.connectAttr((rotBlend + '.output'), (rotAdd + '.input1'))
                pc.connectAttr((rotMultiDouble + '.output'), (rotAdd + '.input2'))
            
                pc.connectAttr((twistCtrl[0] + '.nullifyTwist'), (jointRotBlend + '.attributesBlender'))
                pc.connectAttr((rotMd + '.output' + axis), (jointRotBlend + '.input[0]'))

                if ikFkType == 'utilNode':
                    pc.connectAttr((rotNode[0] + '.output' + color), (jointRotBlend + '.input[1]'))
                elif ikFkType == 'constraint':
                    pc.connectAttr((rotNode[0] + '.constraintRotate.constraintRotate' + axis), (jointRotBlend + '.input[1]'))

                pc.connectAttr((jointRotBlend + '.output'), (jointRotAdd + '.input1'))
                pc.connectAttr((twistCtrl[0] + '.' + twistAxis[0]), (jointRotAdd + '.input2'))
            
            elif rotConnect == 'child':
                # create new joint same position as wrist joint and constraint to the ikfk joints
                pc.select(cl=True)
                tempJoint = curveControl('joint', 'curve', controlColor)
                tempJoint[0] = pc.rename(tempJoint[0], name + side + joint + 'Rot_jnt')
                Snap(wristJoint, tempJoint[0])
                rad = pc.getAttr(wristJoint + '.radius')
                pc.setAttr((tempJoint[0] + '.radius'), rad)
                pc.select(cl=True)
                pc.makeIdentity(tempJoint[0], apply=True, t=0, r=1, s=0, n=0)
            
                ikFkCon = pc.parentConstraint(('fk_' + wristJoint), ('ik_' + wristJoint), tempJoint[0], skipTranslate=['x', 'y', 'z'], weight=1)
                rev = pc.createNode('reverse', n=(tempJoint[0] + '_rot_rev'))
                pc.connectAttr((controller + '.FK_IK'), (rev + '.ix'), f=True)
                pc.connectAttr((rev + '.ox'), (ikFkCon + '.w0'), f=True)
                pc.connectAttr((controller + '.FK_IK'), (ikFkCon + '.w1'), f=True)
            
                pc.setAttr((rotMd + '.input2X'), jointCount)
                pc.setAttr((rotMd + '.input2Y'), jointCount)
                pc.setAttr((rotMd + '.input2Z'), jointCount)
                pc.connectAttr((tempJoint[0] + '.rotateX'), (rotMd + '.input1X'))
                pc.connectAttr((tempJoint[0] + '.rotateY'), (rotMd + '.input1Y'))
                pc.connectAttr((tempJoint[0] + '.rotateZ'), (rotMd + '.input1Z'))
            
                pc.select(cl=True)
                twistCtrl = curveControl('plus', 'curve', controlColor)
                resizeCurves(None, 1, 1, 1, scale)
                twistCtrl[0] = pc.rename(twistCtrl[0], name + side + childJoint + '_twist_ctrl')
                Snap(childJoint,twistCtrl[0])
                zeroGrp = quickZeroOut(twistCtrl[0])
                pc.parentConstraint(childJoint, zeroGrp[0], weight=1)
                partGrp = pc.listRelatives(controller, parent=True)
                pc.parent(zeroGrp[0], partGrp[0])
                pc.connectAttr((controller + '.twistFixVis'), (twistCtrl[0] + '.visibility'))
                lockAndHide( twistCtrl[0], 'locknHide', 'trans scale vis')
                pc.setAttr((twistCtrl[0] + '.' + twistAxis[1]), lock=True, keyable=False)
                pc.setAttr((twistCtrl[0] + '.' + twistAxis[2]), lock=True, keyable=False)
            
                rotMulti = pc.createNode('multiplyDivide', n=(name + side + joint + '_addTwist_mdl'))
                pc.setAttr((rotMulti + '.operation'), 2)
                pc.setAttr((rotMulti + '.input2X'), jointCount)
                pc.setAttr((rotMulti + '.input2Y'), jointCount)
                pc.setAttr((rotMulti + '.input2Z'), jointCount)
            
                rotAdd = pc.createNode('addDoubleLinear', n=(name + side + joint + '_addTwist_adl'))
                rotBlend = pc.createNode('blendTwoAttr', n=(name + side + joint + '_addTwist_bta'))
            
                pc.addAttr(twistCtrl[0], ln='nullifyTwist', at='double', min=0, max=1, keyable=True)
                pc.connectAttr((twistCtrl[0] + '.nullifyTwist'), (rotBlend + '.attributesBlender'))
                pc.connectAttr((rotMd + '.output' + axis), (rotBlend + '.input[0]'))
                pc.setAttr((rotBlend + '.input[1]'), 0)
                pc.connectAttr((twistCtrl[0] + '.' + twistAxis[0]), (rotMulti + '.input1X'))
                pc.connectAttr((rotBlend + '.output'), (rotAdd + '.input1'))
                pc.connectAttr((rotMulti + '.outputX'), (rotAdd + '.input2'))
            
            pc.select(joint, r=True)
            newJoints = splitSelJoint(jointCount)
            for j in newJoints:
                if stretch:
                    if stretchType == 'translate':
                        pc.connectAttr((transMd + '.outputX'), (j + '.translateX'))
                        pc.connectAttr((transMd + '.outputY'), (j + '.translateY'))
                        pc.connectAttr((transMd + '.outputZ'), (j + '.translateZ'))
                
                    elif stretchType == 'scale':
                        pc.connectAttr((transMd + '.output' + axis), (j + '.scale' + axis))
                pc.connectAttr((rotAdd + '.output'), (j + '.' + twistAxis[0]))

            if rotConnect == 'parent':
                if stretch:
                    if stretchType == 'translate':
                        pc.connectAttr((transMd + '.outputX'), (childJoint + '.translateX'), f=True)
                        pc.connectAttr((transMd + '.outputY'), (childJoint + '.translateY'), f=True)
                        pc.connectAttr((transMd + '.outputZ'), (childJoint + '.translateZ'), f=True)		     
                pc.connectAttr((jointRotAdd + '.output'), (joint + '.' + twistAxis[0]), f=True)		
            elif rotConnect == 'child':
                if stretch:
                    if stretchType == 'translate':
                        pc.connectAttr((transMd + '.outputX'), (childJoint + '.translateX'), f=True)
                        pc.connectAttr((transMd + '.outputY'), (childJoint + '.translateY'), f=True)
                        pc.connectAttr((transMd + '.outputZ'), (childJoint + '.translateZ'), f=True)
                        # connecting temp joint translate
                        pc.connectAttr((transNode[0] + '.outputR'), (tempJoint[0] + '.translateX'))
                        pc.connectAttr((transNode[0] + '.outputG'), (tempJoint[0] + '.translateY'))
                        pc.connectAttr((transNode[0] + '.outputB'), (tempJoint[0] + '.translateZ'))
                # parent new twist help joint to elbow
                pc.parent(tempJoint[0], joint)

            # insert joint into split joint array
            if volume:
                newJoints.insert(0, joint)
                pc.refresh
                js.makeJointVolumeSetup(name, side, controller, stretchType, newJoints)
    return newJoints

# based of Jason Schleifer's code
def splitSelJoint(numSegments):
    if numSegments < 2:
        pc.error('The number of segments has to be more than 1.. ')

    joints = []
    joint = ''
    newJoints = []
    newChildJoints = []
    count = 0
    joints = pc.ls(sl=True, type='joint')
    for joint in joints:        
        child = getFirstChildJoint(joint)

        if not child:
            pc.error('Joint: ' + joint + ' has no children joints.\n')
        else:
            axis = ''
            rotationOrder = ''
            firstChar = ''
            radius = pc.getAttr(joint + '.radius')
            axis = getJointAxis(child)
            rotOrderIndex = pc.getAttr(joint + '.rotateOrder')
            rotationOrder = getRotOrder(joint)
            childT = 0.0
            tVal = 0.0            
            attr = ('t'+axis)
            childT = pc.getAttr(child + '.' + attr)
            space = childT/numSegments
            locators = []
            for x in range(numSegments-1):
                tmp = pc.spaceLocator()
                locators.append(tmp)
                pc.parent(locators[x], joint)
                pc.setAttr((locators[x] + '.t'), 0, 0, 0)
                pc.setAttr((locators[x] + '.' + attr), (space * (x+1)))

            prevJoint = joint            
            for x in range(len(locators)):
                newJoint = pc.insertJoint(prevJoint)
                pos = pc.xform(locators[x], q=True, ws=True, rp=True)
                pc.move(pos[0], pos[1], pos[2], (newJoint + '.scalePivot'), (newJoint + '.rotatePivot'), a=True, ws=True)
                newJoint = pc.rename((newJoint), (joint + '_seg_'+str(x+1)+'_joint'))
                pc.setAttr((newJoint + '.radius'), radius)
                pc.setAttr((newJoint + '.rotateOrder'), rotOrderIndex)
                prevJoint = newJoint
                newJoints.append(newJoint)
            pc.delete(locators)
    return newJoints

def getRotOrder(joint):
    r = ''
    ro = pc.getAttr(joint + '.ro')
    
    if ro == 0:
        return 'xyz'
    if ro == 1:
        return 'yzx'
    if ro == 2:
        return 'zxy'            
    if ro == 3:
        return 'xzy'
    if ro == 4:
        return 'yxz'
    if ro == 5:
        return 'zyx'
    return r

def getJointAxis(child):
    axis = ''
    t = pc.getAttr(child + '.t')
    tol = 0.0001
    for x in range(2):        
        if ((t[x] > tol) or (t[x] < (-1 *tol))):
            if x == 0:
                axis = 'x'
            if x == 1:
                axis = 'y'
            if x == 2:
                axis = 'z'
                
    if axis == '':
        pc.error('The child joint is too close to the parent joint. Cannot determine the proper axis to segment.')
    return axis

def getFirstChildJoint(joint):
    tmp = pc.listRelatives(joint, f=True, c=True, type='joint')
    return tmp[0]