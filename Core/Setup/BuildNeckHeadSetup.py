import pymel.core as pc
from BuildSpaceSwitchSetup import buildSpaceSwitchSetup
from Maya_Rigging.Core.BuildWorld import buildWorld
from ..JointStretchNetworkLib import buildIkStretch
from ..JointStretchNetworkLib import stretchySpline
from ...Utils.CharUtilsLib import addSkinJointToSet
from ...Utils.CharUtilsLib import createSkinJointSet
from ...Utils.CharUtilsLib import findJointArray
from ...Utils.CharUtilsLib import getChildJoint
from ...Utils.CharUtilsLib import getStretchAxis
from ...Utils.CharUtilsLib import getcharRigInfoNode
from ...Utils.CharUtilsLib import jointCurve
from ...Utils.CharUtilsLib import jointsOnCurve
from ...Utils.CharUtilsLib import lockAndHide
from ...Utils.CharUtilsLib import parentSkeletonTo
from ...Utils.CharUtilsLib import quickZeroOut
from ...Utils.CurveUtilLib import curveControl
from ...Utils.CurveUtilLib import resizeCurves
from ...Utils.Transform import Snap

def buildNeckHeadSetup(name,
                       side,
                       neckJoint,
                       headJoint,
                       stretchType,
                       stretch,
                       numJoints,
                       volume,
                       world,
                       scale,
                       controlColor):
    list = findJointArray(neckJoint,headJoint)
    size = len(list)
    sknJoints = []
    if size>2:
        sknJoints = multiBoneHeadNeckSetup(name,side,neckJoint,headJoint,stretchType,numJoints,stretch,volume,world,scale,controlColor)
    else:
        sknJoints = headNeckSetup(name,side,neckJoint,headJoint,stretchType,numJoints,stretch,volume,world,scale,controlColor)

    # createskinJointset
    set = createSkinJointSet(name)
    addSkinJointToSet(set, sknJoints)

#multiBoneNeckHeadSetup '' '' joint1 joint4 scale 7 1 1 1
def multiBoneHeadNeckSetup(name, side, neckJoint, headJoint, stretchType, numJoints, stretch, volume, world, scale, controlColor):
    stretchAxis = []
    curveJoints = []
    ikHandle = []
    list = []
    orientAxis = ''
    facingAxis = ''
    curve = ''
    scaleCmd = ''
    nonScaleGrp = (name+'non_scale_grp')
    scaleNode = (name+'worldScaleCon_grp')
    cleanGrp = []
    sknJoints = []

    partGrp = pc.group(em=True, n=(name + side + 'neckParts_grp'))
    lockAndHide(partGrp, 'locknHide', 'trans rot scale')

    if world:
        cleanGrp = buildWorld(name, scale)
        pc.parent(partGrp, cleanGrp[0])
    else:
        scaleNode = buildWorld.createScaleGrp(name)

    #get no neck joints btween first neck joint to head joint
    list = findJointArray(neckJoint,headJoint)
    curve = jointCurve(neckJoint,headJoint)
    #rebuildCurve -ch 0 -rpo 1 -rt 0 -end 1 -kr 0 -kcp 0 -kep 1 -kt 0 -s 2 -d 3 -tol 0.001 curve
    curve = pc.rename(curve, (name + side + 'neck_crv')) #remember to change the name of curve
    pc.setAttr((curve + '.visibility'), 0)
    lockAndHide(curve,'lock','trans rot scale vis')

    stretchAxis = getStretchAxis(headJoint, 'translate')

    if stretchAxis[0] == 'tx': 
        orientAxis = 'xyz' 
        facingAxis = 'X' 
        scaleCmd = pc.Callback(resizeCurves, None,0,1,1,2.5)
    elif stretchAxis[0] == 'ty':
        orientAxis = 'yzx' 
        facingAxis = 'Y' 
        scaleCmd = pc.Callback(resizeCurves, None, 0,1,1,2.5)
    elif stretchAxis[0] == 'tz':
        orientAxis = 'zxy' 
        facingAxis = 'Z' 
        scaleCmd = pc.Callback(resizeCurves, None, 1,1,0,2.5)

    curveJoints = jointsOnCurve(curve, orientAxis, 'zup', numJoints,(name+side+'neckDef'))
    ikHandle = pc.ikHandle(name=(headJoint + '_ikh'), startJoint=curveJoints[0], endEffector=curveJoints[numJoints], solver='ikSplineSolver', curve=curve, createCurve=0)
    pc.setAttr((ikHandle[0] + '.visibility'),0)
    lockAndHide(ikHandle[0],'lock','trans rot scale vis')
    pc.parent(curveJoints[0], neckJoint)

    pc.parent(ikHandle[0],nonScaleGrp)
    pc.parent(curve,nonScaleGrp)
    pc.select(cl=True)

    # create two locator for twist distribution
    pc.select(curveJoints[0], r=True)
    startTwistLoc = curveControl('locator', 'curve', controlColor)
    startTwistLoc[0] = pc.rename(startTwistLoc[0], name + side + 'startTwist_loc')
    pc.hide(startTwistLoc[0])
    lockAndHide(startTwistLoc[0],'locknHide','scale vis')
    pc.select(cl=True)
  
    pc.select(curveJoints[numJoints-1], r=True)
    endTwistLoc = curveControl('locator', 'curve', controlColor)
    endTwistLoc[0] = pc.rename(endTwistLoc[0], name + side + 'endTwist_loc')
    pc.hide(endTwistLoc[0])
    lockAndHide(endTwistLoc[0], 'locknHide', 'scale vis')
    pc.select(cl=True)

    #connect ik handle twist
    pc.setAttr((ikHandle[0] + '.dTwistControlEnable'), 1)
    pc.setAttr((ikHandle[0] + '.dWorldUpType'), 4)

    pc.connectAttr((startTwistLoc[0] + '.worldMatrix[0]'), (ikHandle[0] + '.dWorldUpMatrix'), f=True)
    pc.connectAttr((endTwistLoc[0] + '.worldMatrix[0]'), (ikHandle[0] + '.dWorldUpMatrixEnd'), f=True)

    #create controls
    pc.select(headJoint, r=True)
    headControl = curveControl('cube1', 'joint', controlColor)
    resizeCurves(None, 1, 1, 1, 2.5)
    headControl[0] = pc.rename(headControl[0], name + side + 'head_ctrl')
    headGrp = quickZeroOut(headControl[0])
    lockAndHide(headControl[0], 'locknHide', 'scale vis')
    pc.parentConstraint(headControl[0], headJoint, mo=True, w=1)
    pc.select(cl=True)
    
    child = getChildJoint(headJoint)
    if child != '':
        tempSpaceGrp = pc.group(em=True)
        pc.pointConstraint(headJoint, child, tempSpaceGrp, offset=(0,0,0), weight=1)
        pc.select((headControl[0] + '.cv[*]'), r=True)
        tempClts = pc.cluster()
        pc.pointConstraint(tempSpaceGrp, tempClts[1], offset=(0,0,0), weight=1)
        pc.scale(tempClts[1],(scale,scale,scale))
        pc.select(headControl[0], r=True)
        pc.runtime.DeleteHistory()
        pc.delete(tempSpaceGrp)
        	
    #creating neck control....
    pc.select(neckJoint, r=True)
    tempControl = curveControl('square', 'joint', controlColor)
    tempControl[0] = pc.rename(tempControl[0], name + side + 'neck_ctrl')
    pc.parentConstraint(tempControl, neckJoint, mo=True, w=1)
    pc.select(cl=True)
    allControls = []

    size = len(list)
    for i in range(1,size-1):
        allControls.append(tempControl[0])
        pc.select(list[i], r=True)
        tempControl = curveControl('square', 'joint', controlColor)
        tempControl[0] = pc.rename(tempControl[0], name + side + list[i] + '_ctrl')
        pc.parentConstraint(tempControl, list[i], mo=True, w=1)
        pc.select(cl=True)
        pc.parent(tempControl[0], allControls[i-1])
    
    allControls.append(tempControl[0]) # add last created control in the array
    pc.select(allControls, r=True)
    controlGrp = quickZeroOut('')

    pc.select(allControls, r=True)
    lockAndHide('', 'locknHide', 'trans scale vis')

    #parent Twiat locators
    pc.parent(startTwistLoc[0], allControls[0])
    pc.parent(endTwistLoc[0], headControl[0])
    pc.parent(headGrp[0], allControls[len(allControls)-1])
    lockAndHide(headGrp[0],'lock','trans rot scale vis')

    pc.skinCluster(allControls, headControl[0], curve, tsb=True, mi=4, dr=7)

    if stretch:
        stretchySpline(name, side, headControl[0], stretchType, curve, 1, volume, scaleNode)

    parentJoint = pc.listRelatives(neckJoint, parent=True)
    if parentJoint[0] != '':
        pc.parentConstraint(parentJoint[0], controlGrp[0], mo=True, weight=1)

    pc.parent(controlGrp[0],partGrp)
    #lock all neck control zeroOut grps
    for x in range(len(controlGrp)):
        lockAndHide(controlGrp[x],'lock','trans rot scale vis')

    #add neckHead rig info for future update...
    charRigInfo = getcharRigInfoNode(name)
    pc.addAttr(charRigInfo , ln=(side+'neckHeadRig'), dt='string')
    pc.setAttr((charRigInfo + '.' + (side+'neckHeadRig')), (headControl[0]+' '+allControls[0]), type='string')

    #create space switch
    if world:
        if pc.attributeQuery('spineRig', n=charRigInfo, ex=True):
            spineRigPart = pc.getAttr(charRigInfo+'.spineRig')
            spineRigArray = spineRigPart.split(' ')
            buildSpaceSwitchSetup(headControl[0], headGrp[0],[allControls[len(allControls)-1],spineRigArray[1],(name+'worldB_ctrl')], ['neck','chest','world'], 2)
            pc.setAttr((headControl[0]+'.rotateLock'),2)

    #parent skeleton 
    pc.select(cl=True)
    parentSkeletonTo(neckJoint, cleanGrp[1])

    #scale controls to global value
    pc.select(allControls, r=True)
    resizeCurves(None, 1, 1, 1, scale)
    pc.select(cl=True)
    listA = [headJoint]
    
    sknJoints.extend(curveJoints)
    sknJoints.extend(listA)
    return sknJoints

#headNeckSetup '' '' joint1 joint2 scale 3 0 0 1
def headNeckSetup(name, side, neckJoint, headJoint, stretchType, numJoints, stretch, volume, world, scale, controlColor):

    print('Head Scale: ')
    print(scale)

    stretchAxis = []
    orientAxis = ''
    facingAxis = ''
    curve = ''
    scaleCmd = ''
    nonScaleGrp = (name+'non_scale_grp')
    scaleNode = (name+'worldScaleCon_grp')
    cleanGrp = []
    curveJoints = []

    partGrp = pc.group(em=True, n=(name + side + 'headParts_grp'))
    lockAndHide(partGrp, 'locknHide', 'trans rot scale')

    if world:
        cleanGrp = buildWorld (name, scale)
        pc.parent(partGrp, cleanGrp[0])
    else:
        scaleNode = buildWorld.createScaleGrp(name)

    stretchAxis = getStretchAxis(headJoint,'translate')

    pc.select(neckJoint, r=True)
    neckControl = curveControl('square', 'joint', controlColor)
    neckControl[0] = pc.rename(neckControl[0], name + side + 'neck_ctrl')
    neckGrp = quickZeroOut(neckControl[0])
    lockAndHide(neckControl[0], 'locknHide', 'scale vis')
    pc.select(cl=True)

    pc.select(headJoint, r=True)
    headControl = curveControl('cube1', 'joint', controlColor)
    resizeCurves(None, 1, 1, 1, 2.5)
    headControl[0] = pc.rename(headControl[0], name + side + 'head_ctrl')
    headGrp = quickZeroOut(headControl[0])
    lockAndHide(headControl[0],'locknHide','scale vis')
    pc.select(cl=True)

    child = getChildJoint(headJoint)
    if child != '':
        tempSpaceGrp = pc.group(em=True)
        pc.pointConstraint(headJoint, child, tempSpaceGrp, offset=[0,0,0], weight=1)
        pc.select((headControl[0] + '.cv[*]'), r=True)
        tempClts = pc.cluster()
        pc.pointConstraint(tempSpaceGrp, tempClts[1], offset=[0,0,0], weight=1)
        pc.scale(tempClts[1],(scale, scale, scale))
        pc.select(headControl[0], r=True)        
        pc.runtime.DeleteHistory()
        pc.delete(tempSpaceGrp)

    pc.parent(headGrp[0],neckControl[0])

    if numJoints>1:
        curve = jointCurve(neckJoint,headJoint)
        curve = pc.rename(curve, (name + side + 'neck_crv')) #remember to change the name of curve
        pc.setAttr((curve + '.visibility'), 0)
        lockAndHide(curve,'lock','trans rot scale vis')
        
        if stretchAxis[0] == 'tx':
            orientAxis = 'xyz'
            facingAxis = 'X'
            scaleCmd = pc.Callback(resizeCurves, None, 0, 1, 1, 2.5)
        elif stretchAxis[0] == 'ty':
            orientAxis = 'yzx'
            facingAxis = 'Y'
            scaleCmd = pc.Callback(resizeCurves, None, 1, 0, 1, 2.5)
        elif stretchAxis[0] == 'tz':
            orientAxis = 'zxy'
            facingAxis = 'Z'
            scaleCmd = pc.Callback(resizeCurves, None, 1, 1, 0, 2.5)

        curveJoints = jointsOnCurve(curve, orientAxis, 'zup', numJoints,(name+side+'neckDef'))        
        ikHandle = pc.ikHandle(name=(headJoint + '_ikh'), startJoint=curveJoints[0], endEffector=curveJoints[numJoints-1], solver='ikSplineSolver', curve=curve, createCurve=0)
        pc.setAttr((ikHandle[0] + '.visibility'), 0)
        lockAndHide(ikHandle[0],'lock','trans rot scale vis')
        pc.parent(curveJoints[0], neckJoint)

        pc.parent(ikHandle[0],nonScaleGrp)
        pc.parent(curve, nonScaleGrp)
        pc.select(cl=True)
        
        pc.select(curveJoints[0], r=True)
        startTwistLoc = curveControl('locator', 'curve', controlColor)
        startTwistLoc[0] = pc.rename(startTwistLoc[0], name + side + 'startTwist_loc')
        pc.hide(startTwistLoc[0])
        lockAndHide(startTwistLoc[0],'locknHide','scale vis')
        pc.select(cl=True)
  
        pc.select(curveJoints[numJoints-1], r=True)
        endTwistLoc = curveControl('locator', 'curve', controlColor)
        endTwistLoc[0] = pc.rename(endTwistLoc[0], name + side + 'endTwist_loc')
        pc.hide(endTwistLoc[0])
        lockAndHide(endTwistLoc[0], 'locknHide', 'scale vis')
        pc.select(cl=True)
        
        pc.setAttr((ikHandle[0] + '.dTwistControlEnable'), 1)
        pc.setAttr((ikHandle[0] + '.dWorldUpType'),4)
        
        pc.connectAttr((startTwistLoc[0] + '.worldMatrix[0]'), (ikHandle[0] + '.dWorldUpMatrix'), f=True)
        pc.connectAttr((endTwistLoc[0] + '.worldMatrix[0]'), (ikHandle[0] + '.dWorldUpMatrixEnd'), f=True)
        
        pc.parent(startTwistLoc[0], neckControl[0])
        pc.parent(endTwistLoc[0], headControl[0])	

    if stretch:	
        ikNeckJoint = curveControl('joint', 'curve', controlColor)
        ikNeckJoint[0] = pc.rename(ikNeckJoint[0], name + side + '_ik_' + neckJoint)
        Snap(neckJoint, ikNeckJoint[0])
        pc.makeIdentity(ikNeckJoint[0], apply=True, t=1, r=1, s=1)
        pc.select(cl=True)
        
        ikHeadJoint = curveControl('joint', 'curve', controlColor)
        ikHeadJoint[0] = pc.rename(ikHeadJoint[0], name + side + '_ik_' + headJoint)
        Snap(headJoint, ikHeadJoint[0])
        pc.makeIdentity(ikHeadJoint[0], apply=True, t=1, r=1, s=1)
        pc.select(cl=True)
        
        ikHeadEndJoint = curveControl('joint', 'curve', controlColor)
        ikHeadEndJoint[0] = pc.rename(ikHeadEndJoint[0], name + side + '_ik_' + headJoint + 'End')
        Snap(headJoint, ikHeadEndJoint[0])
        pc.makeIdentity(ikHeadEndJoint[0], apply=True, t=1, r=1, s=1)
        pc.select(cl=True)
        
        pc.parent(ikHeadEndJoint[0], ikHeadJoint[0])
        pc.parent(ikHeadJoint[0], ikNeckJoint[0])
        pc.parent(ikNeckJoint, neckControl[0])
               
        rad = pc.getAttr(headJoint + '.radius')
        val = pc.getAttr(headJoint + '.' + stretchAxis[0])
        pc.setAttr((ikNeckJoint[0] + '.radius'), rad)
        pc.setAttr((ikHeadJoint[0] + '.radius'), rad)
        pc.setAttr((ikHeadEndJoint[0] + '.radius'), rad)
        
        if val < 0.00001:
            if stretchAxis[0] == 'tx':
                pc.move(-0.7,0,0, ikHeadEndJoint[0], r=True, ls=True, wd=True)
            elif stretchAxis[0] == 'ty':
                pc.move(0,-0.7,0, ikHeadEndJoint[0], r=True, ls=True, wd=True)
            elif stretchAxis[0] == 'tz':
                pc.move(0,0,-0.7, ikHeadEndJoint[0], r=True, ls=True, wd=True)
        else:
            if stretchAxis[0] == 'tx':
                pc.move(0.7, 0, 0, ikHeadEndJoint[0], r=True, ls=True, wd=True)
            elif stretchAxis[0] == 'ty':
                pc.move(0,0.7,0, ikHeadEndJoint[0], r=True, ls=True, wd=True)
            elif stretchAxis[0] == 'tz':
                pc.move(0,0,0.7, ikHeadEndJoint[0], r=True, ls=True, wd=True)
                
        ikHandle = pc.ikHandle(name=(name + side + headJoint + '_ikhandle'), startJoint=ikHeadJoint[0], endEffector=ikHeadEndJoint[0], solver='ikSCsolver')
        pc.parent(ikHandle[0], headControl[0])
        pc.setAttr((ikHandle[0] + '.visibility'), 0)
        lockAndHide(ikHandle[0],'lock','trans rot scale vis')
        pc.setAttr((ikNeckJoint[0] + '.visibility'),0)
        lockAndHide(ikNeckJoint[0],'lock','vis')
        
        sScmd = buildIkStretch(name,side,ikNeckJoint[0], ikHeadJoint[0], headControl[0], stretchType)
        pc.parent(sScmd[0], neckControl[0])
        
        parentJoint = pc.listRelatives(neckJoint, parent=True)
        if parentJoint[0] != '':
            pc.parentConstraint(parentJoint[0], neckGrp[0], mo=True, weight=1)

        pc.parentConstraint(neckControl[0], neckJoint, mo=True, w=1)
        pc.parentConstraint(headControl[0], headJoint, mo=True, w=1)
        if numJoints>1:
            stretchySpline(name, side, headControl[0], stretchType, curve, 1, volume, scaleNode)
            pc.skinCluster(ikNeckJoint[0], ikHeadJoint[0], curve, tsb=True, mi=4, dr=7)

    else:
        pc.parentConstraint(headControl[0], headJoint, mo=True, skipTranslate=['x','y','z'], weight=1)
        pc.parentConstraint(neckControl[0], neckJoint, mo=True, weight=1)
        lockAndHide(headControl[0],'locknHide','trans')
        if numJoints>1:
            pc.skinCluster(neckControl[0], headControl[0], curve, mi=4, dr=7)

    pc.parent(neckGrp[0], partGrp)

    #lock all neck control zeroOut grps
    lockAndHide(headGrp[0],'lock','trans rot scale vis')
    lockAndHide(neckGrp[0],'lock','trans rot scale vis')

    #add neckHead rig info for future update...
    charRigInfo = getcharRigInfoNode(name)
    pc.addAttr(charRigInfo, ln=(side+'neckHeadRig'), dt='string')
    pc.setAttr((charRigInfo + '.' + (side+'neckHeadRig')), (headControl[0]+' '+neckControl[0]), type='string')

    #create space switch
    if world:
        if pc.attributeQuery('spineRig', n=charRigInfo, ex=True):
            spineRigPart = pc.getAttr(charRigInfo+'.spineRig')
            spineRigArray = spineRigPart.split(' ')
            buildSpaceSwitchSetup(headControl[0], headGrp[0],[neckControl[0],spineRigArray[1],(name+'worldB_ctrl')], ['neck','chest','world'], 2)
            pc.setAttr((headControl[0]+'.rotateLock'),2)

    #parent skeleton 
    pc.select(cl=True)
    parentSkeletonTo(neckJoint, cleanGrp[1])

    #scale controls to global value
    pc.select(neckControl, r=True)
    resizeCurves(None, 1, 1, 1, scale)
    pc.select(cl=True)
    listA = [headJoint]
    sknJoints = []
    sknJoints.extend(curveJoints)
    sknJoints.extend(listA)
    return sknJoints