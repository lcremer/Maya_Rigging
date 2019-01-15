import maya.mel as mel
import pymel.core as pc

# import re

from Maya_Rigging.Core import BuildWorld as bw
from Maya_Rigging.Utils import CharUtilsLib as chUL
from Maya_Rigging.Utils import CurveUtilLib as cuUL
from Maya_Rigging.Core import JointStretchNetworkLib as js


def buildTentacleSetup(name,
                       startJoint,
                       endJoint,
                       controlType,
                       offsetControls,
                       offControlType,
                       dynamics,
                       type,
                       stretchType,
                       stretch,
                       numJoints,
                       volume,
                       world,
                       scale,
                       controlColor):
    cleanGrp = []

    nonScaleGrp = (name+'non_scale_grp')
    scaleNode = (name+'worldScaleCon_grp')

    partGrp = pc.group(em=True, n=(name + startJoint + 'Parts_grp'))
    chUL.lockAndHide(partGrp, 'locknHide', 'trans rot scale')

    if world:
        cleanGrp = bw.build_world (name, scale)
        pc.parent(partGrp, cleanGrp[0])
    else:
        scaleNode = bw.create_scale_grp(name)

    list = chUL.findJointArray(startJoint, endJoint)
    size = len(list)
    pc.select(startJoint, r=True)
    tempControl = cuUL.curveControl(controlType, 'joint', controlColor)
    tempControl[0] = pc.rename(tempControl[0], name + startJoint + '_ctrl')
    pc.parentConstraint(tempControl, startJoint, mo=True, w=1)
    pc.select(cl=True)
    allControls = []
    for i in range(1,size-1):
        allControls.append(tempControl[0])
        pc.select(list[i], r=True)
        tempControl = cuUL.curveControl(controlType, 'joint', controlColor)
        tempControl[0] = pc.rename(tempControl[0], name + list[i] + '_ctrl')
        pc.parentConstraint(tempControl, list[i], mo=True, w=1)
        pc.select(cl=True)
        pc.parent(tempControl[0], allControls[i-1])
            
    allControls.append(tempControl[0]) #add last created control in the array
    pc.select(allControls, r=True)
    controlGrp = chUL.quickZeroOut('')
    pc.select(allControls, r=True)
    chUL.lockAndHide('', 'locknHide', 'trans scale vis')

    #int numJoints = `getAttr (startJoint + '.twistJoints')`

    curve = chUL.jointCurve(startJoint,endJoint)
    curve = pc.rename(curve, (name + startJoint + '_crv'))
    pc.setAttr((curve + '.visibility'), 0)
    chUL.lockAndHide(curve, 'lock', 'trans rot scale vis')

    stretchAxis = chUL.getStretchAxis(endJoint, 'translate')
    orientAxis = ''
    if stretchAxis[0] == 'tx': 
        orientAxis = 'xyz'
        facingAxis = 'X'        
        scaleCmd = cuUL.resizeCurves(None,0,1,1,2.5)
    elif stretchAxis[0] == 'ty':
        orientAxis = 'yzx' 
        facingAxis = 'Y'         
        scaleCmd = cuUL.resizeCurves(None,1,0,1,2.5)
    elif stretchAxis[0] == 'tz':
        orientAxis = 'zxy' 
        facingAxis = 'Z'         
        scaleCmd = cuUL.resizeCurves(None,1,1,0,2.5)

    curveJoints = chUL.jointsOnCurve(curve, orientAxis, 'zup', numJoints, (name+type+'Def'))
    ikHandle = pc.ikHandle(name=(name + startJoint + '_ikh'), startJoint=curveJoints[0], endEffector=curveJoints[numJoints], solver='ikSplineSolver', curve=curve, createCurve=False, parentCurve=False)
    pc.setAttr((ikHandle[0] + '.visibility'), 0)
    chUL.lockAndHide(ikHandle[0],'lock','trans rot scale vis')
    pc.parent(ikHandle[0], nonScaleGrp)

    # create two locator for twist distribution
    pc.select(curveJoints[0], r=True)
    startTwistLoc = cuUL.curveControl('locator', 'curve', controlColor)
    startTwistLoc[0] = pc.rename(startTwistLoc[0], name + 'startTwist_loc')
    pc.hide(startTwistLoc[0])
    chUL.lockAndHide(startTwistLoc[0], 'locknHide', 'scale vis')
    pc.select(cl=True)
  
    pc.select(curveJoints[numJoints-1], r=True)
    endTwistLoc = cuUL.curveControl('locator', 'curve', controlColor)
    endTwistLoc[0] = pc.rename(endTwistLoc[0], name + 'endTwist_loc')
    pc.hide(endTwistLoc[0])
    chUL.lockAndHide(endTwistLoc[0], 'locknHide', 'scale vis')
    pc.select(cl=True)

    #connect ik handle twist
    pc.setAttr((ikHandle[0] + '.dTwistControlEnable'), 1)
    pc.setAttr((ikHandle[0] + '.dWorldUpType'), 4)

    pc.connectAttr((startTwistLoc[0] + '.worldMatrix[0]'), (ikHandle[0] + '.dWorldUpMatrix'), f=True)
    pc.connectAttr((endTwistLoc[0] + '.worldMatrix[0]'), (ikHandle[0] + '.dWorldUpMatrixEnd'), f=True)

    pc.parent(startTwistLoc[0], allControls[0])
    pc.parent(endTwistLoc[0], allControls[size-2])
    pc.parent(curveJoints[0], startJoint)

    parentJoint = chUL.getParent(startJoint)
    if parentJoint != '':
        pc.parentConstraint(parentJoint, controlGrp[0], mo=True, weight=1)
        if offsetControls:
            pc.select(startJoint, r=True)
            tempControl = cuUL.curveControl(offControlType, 'joint', controlColor)
            tempControl[0] = pc.rename(tempControl[0], name + startJoint + 'Offset_ctrl')
            pc.parent(tempControl[0], allControls[0])
            pc.select(cl=True)
            allOffControls = []
            for i in range(1,size-1):
                allOffControls.append(tempControl[0])
                pc.select(list[i], r = True)
                tempControl = cuUL.curveControl(offControlType, 'joint', controlColor)
                tempControl[0] = pc.rename(tempControl[0], name + list[i] + 'Offset_ctrl')
                pc.select(cl=True)
                pc.parent(tempControl[0], allControls[i])
            allOffControls.append(tempControl[0])#add last created control offset in the array
            pc.select(endJoint, r=True)
            tempControl = cuUL.curveControl(offControlType, 'joint', controlColor)
            tempControl[0] = pc.rename(tempControl[0], name + endJoint + 'Offset_ctrl')
            endOffGrp = chUL.quickZeroOut(tempControl[0])
            pc.select(cl=True)
            allOffControls.append(tempControl[0])
            pc.parent(endOffGrp[0], allControls[len(allControls)-1])
            pc.select(allOffControls, r=True)
            chUL.lockAndHide('', 'locknHide', 'rot scale vis')
            chUL.lockAndHide(endOffGrp[0], 'lock', 'trans rot scale vis')
            pc.skinCluster(allOffControls, curve, tsb=True, mi=4, dr=7)

            pc.select(allOffControls, r=True)
            cuUL.resizeCurves(None, 1, 1, 1, scale)
            pc.select(cl=True)        
        else:
            pc.skinCluster(list, curve, tsb=True, mi=4, dr=7)

    if stretch:
        js.stretchySpline (name, '', allControls[0], stretchType, curve, 1, volume, scaleNode)

    if dynamics:
        pc.select(curve, r=True)
        dynamicCurve = makeDynamicCurve(name, type, pc.ls(sl=True), allControls[0])
        pc.delete(ikHandle)
        ikHandle = pc.ikHandle(name=(name + startJoint + '_ikh'), startJoint=curveJoints[0], endEffector=curveJoints[numJoints], solver='ikSplineSolver', curve=dynamicCurve[0], createCurve=False, parentCurve=False)
        pc.setAttr((ikHandle[0] + '.visibility'), 0)
        chUL.lockAndHide(ikHandle[0], 'lock', 'trans rot scale vis')
        pc.parent(ikHandle[0], nonScaleGrp)
    else:
        pc.parent(curve, nonScaleGrp)

    pc.parent(controlGrp[0], partGrp)

    #lock all tentacle control zeroOut grps
    for c in controlGrp:    
        chUL.lockAndHide(c, 'lock', 'trans rot scale vis')

    #add tentacle rig info for future update...
    charRigInfo = chUL.getcharRigInfoNode(name)
    pc.addAttr(charRigInfo, ln=type, dt='string')
    pc.setAttr((charRigInfo + '.' + type), (allControls[0]), type='string')

    #parent skeleton 
    pc.select(cl=True)
    chUL.parentSkeletonTo(startJoint, cleanGrp[1])

    # createskinJointset
    set = chUL.createSkinJointSet(name)
    chUL.addSkinJointToSet(set, curveJoints )

    #scale controls to global value
    pc.select(allControls, r=True)
    cuUL.resizeCurves(None, 1, 1, 1, scale)
    pc.select(cl=True)


def makeDynamicCurve(name, type, curves, controller):
    #string name = ''
    #string curves[] = `ls -sl`
    #string controller = 'locator1'

    parentFollicle = ''
    newCurve = []
    connections = []
    nonScaleGrp = (name+'non_scale_grp')

    nonScaleGrp = bw.create_non_scale_grp(name)

    pc.select(curves, r=True)    
    # TODO: convert to python
    mel.eval('makeCurvesDynamicHairs %d %d %d' % (0, 0, 1)) #attach, snap, match

    for i in range(len(curves)):
        #first find parent follicle
        parentFollicle = chUL.getParent(curves[i])
        #now find shape node 
        follicleShape = pc.listRelatives(parentFollicle, shapes=True)
        connections = pc.listConnections(follicleShape[0], d=True, s=False)
        newCurve.append(connections[1])
        #ok now we found all information lets create dynamic setup..
        pc.setAttr((follicleShape[0] + '.pointLock'), 1)

    #get which hairSystem is created  
    pc.addAttr(controller, ln=(type + 'Dynamics'), at='enum', en='-------------', keyable=True)
    pc.setAttr((controller + '.' + (type + 'Dynamics')), lock=True)
    pc.addAttr(controller, ln=(type + 'DynamicsSwitch'), at='enum', en='off:on:', keyable=True)
    pc.addAttr(controller, ln=(type + 'DynamicAttract'), at='double', min=0, max=1, dv=0.5, keyable=True)
    pc.addAttr(controller, ln=(type + 'AttractionDamp'), at='double', min=0, max=1, dv=0, keyable=True)

    dynOnCondition = pc.createNode('condition', n='dynamicState_cnd')
    pc.setAttr((dynOnCondition + '.colorIfTrueR'), 1)
    pc.setAttr((dynOnCondition + '.colorIfFalseR'), 4)

    dynRev = pc.createNode('reverse', n='dynamicAttract_rev')

    pc.connectAttr((controller + '.' + (type + 'DynamicsSwitch')), (dynOnCondition + '.firstTerm'))
    pc.connectAttr((controller + '.' + (type + 'DynamicAttract')), (dynRev + '.inputX'))

    pc.connectAttr((dynOnCondition + '.outColorR'), (connections[0] + '.simulationMethod'))
    pc.connectAttr((dynRev + '.outputX'), (connections[0] + '.startCurveAttract'))
    pc.connectAttr((controller + '.' + (type + 'AttractionDamp')), (connections[0] + '.attractionDamp'))

    follicleParent = chUL.getParent(parentFollicle)
    dynCurveParent = chUL.getParent(connections[1])
    pc.hide(follicleParent, dynCurveParent, connections[0])
    pc.select(follicleParent, dynCurveParent, connections[0], r=True)
    chUL.lockAndHide('', 'lock', 'trans rot scale vis')

    partGrp = pc.group(em=True, n=(type + 'DynamicsParts_grp'))
    pc.parent(partGrp, nonScaleGrp)

    pc.parent(follicleParent, partGrp)
    pc.parent(dynCurveParent, partGrp)
    pc.parent(connections[0], partGrp)
    return newCurve