from ...Core import BuildWorld as bw
from ...Core import JointStretchNetworkLib as js
from ...Core.Setup import BuildSpaceSwitchSetup as bsss
from ...Core.Setup import BuildTwistJointSetup as btjs
from ...Utils import AttrUtil as atu
from ...Utils import CharUtilsLib as chUL
from ...Utils import CurveUtilLib as cuUL
from ...Utils import Transform as tr
from ...Utils.CharUtilsLib import *


def buildArmSetup(name,
                  side,
                  shoulderJoint,
                  wristJoint,
                  stretchType,
                  ikFkType,
                  stretch,
                  midLock,
                  volume,
                  world,
                  scale,
                  controlColor):
    FK = []  # array to hold fk joint chain
    IK = []  # array to hold fk joint chain
    list = []  # array to hold actual joint chain
    temp = []  # hold name unused joint to delete
    middleIndex = 0  # hold middle index of ik joint chain
    modPos = []  # hold mid postion for pole vectoe control
    ikHandle = []  # hold all created ik handle
    fkContrlList = []  # array to hold fk control joint chain
    fkCon = []  # array to hold newly creted fk control
    tempJoint = []  # array to hold temp created joint
    stretchAxis = []  # array to stretch axis info
    parentGrp = []  # holds name of parent grp of given object
    cleanGrp = []

    partGrp = pc.group(em=True, n=(name + side + 'armParts_grp'))
    chUL.lockAndHide(partGrp, 'locknHide', 'trans rot scale')

    if world:
        cleanGrp = bw.build_world(name, scale)
        pc.parent(partGrp, cleanGrp[0])

    # duplicate joint chain twice in order to create ik fk switch
    FK = chUL.dupId(shoulderJoint, 'prefix', 'fk')
    IK = chUL.dupId(shoulderJoint, 'prefix', 'ik')

    # delete twistAttr from FK and IK joint chains if it exists
    for x in range(len(FK)):
        if pc.attributeQuery('twistJoints', n=FK[x], ex=True):
            pc.setAttr((FK[x] + '.twistJointGrp'), ' ', type='string')
            pc.setAttr((IK[x] + '.twistJointGrp'), ' ', type='string')
            pc.select(FK[x], r=True)
            atu.removeTwistJointsAttr('twistJoints')
            pc.select(IK[x], r=True)
            atu.removeTwistJointsAttr('twistJoints')

    # check if duplicated joint has any child joints and delete them
    temp = pc.listRelatives(('ik_' + wristJoint), allDescendents=True)
    if temp[0] != '':
        pc.delete(temp)

    # check if duplicated joint has any child joints and delete them
    temp = pc.listRelatives(('fk_' + wristJoint), allDescendents=True)
    if temp[0] != '':
        pc.delete(temp)

    # get all joints in chain
    IK = chUL.listHierarchy(IK[0])
    FK = chUL.listHierarchy(FK[0])
    list = chUL.findJointArray(shoulderJoint, wristJoint)

    pc.select(cl=True)

    # create controls
    wristCtrl = cuUL.curveControl('cube1', 'joint', controlColor)
    wristCtrl[0] = pc.rename(wristCtrl[0], name + side + 'ik_wrist_ctrl')
    elbowCtrl = cuUL.curveControl('cone', 'curve', controlColor)
    elbowCtrl[0] = pc.rename(elbowCtrl[0], name + side + 'ik_elbow_ctrl')
    switchCtrl = cuUL.curveControl('pin1', 'curve', controlColor)
    switchCtrl[0] = pc.rename(switchCtrl[0], name + side + 'armSwitches_ctrl')

    # snap controls to respective joints
    tr.Snap(wristJoint, wristCtrl[0])
    pc.makeIdentity(wristCtrl[0], apply=True, t=1, r=1, s=1)
    tr.Snap(wristJoint, switchCtrl[0])
    pc.setAttr((switchCtrl[0] + '.r'), (0, 0, 0))
    pc.select(cl=True)

    pc.parent(wristCtrl[0], partGrp)
    pc.parent(elbowCtrl[0], partGrp)
    pc.parent(switchCtrl[0], partGrp)

    pc.parentConstraint(wristJoint, switchCtrl[0], mo=True, weight=1)
    chUL.lockAndHide(switchCtrl[0], 'locknHide', 'trans rot scale vis')

    # get middle index of ik joint for pole control placement
    middleIndex = len(IK) / 2
    modPos = chUL.zoofindPolePosition(shoulderJoint, IK[middleIndex], wristJoint, 0.7)
    pc.select(elbowCtrl[0], r=True)
    pc.setAttr((elbowCtrl[0] + '.t'), (modPos[0], modPos[1], modPos[2]))
    cuUL.fixFacingAxis('Z', 0)
    pc.select(cl=True)

    # create ik fk connections from given array
    chUL.fkIkConnect(list, IK, FK, ikFkType, switchCtrl[0])
    pc.select(cl=True)

    # fk controllers and rename them respectively
    fkCon = chUL.fkControl(FK[0], 'circleCross', 1, controlColor)
    fkContrlList = chUL.listHierarchy(fkCon[0])

    for f in fkContrlList:
        f = pc.rename(f, (name + side + f))

    # check stretch condition and create connections
    if stretch == 1:
        js.stretchNetwork(name, side, ('ik_' + shoulderJoint), ('ik_' + wristJoint), wristCtrl[0], stretchType, midLock,
                          elbowCtrl[0])
        chUL.stretchTypeConnect(list, IK, FK, stretchType, switchCtrl[0])

    # creating twist joint setup if attribute exists on given joint
    size = len(list) - 1
    twistJoints = []
    sknJoints = []
    wristRots = pc.listRelatives(wristJoint, parent=True)
    for i in range(size):
        if list[i] == wristRots[0]:
            twistJoints = btjs.buildTwistJointSetup(name,
                                                    side,
                                                    list[i],
                                                    stretchType,
                                                    ikFkType,
                                                    'child',
                                                    wristJoint,
                                                    switchCtrl[0],
                                                    stretch,
                                                    volume,
                                                    scale,
                                                    controlColor)
        else:
            twistJoints = btjs.buildTwistJointSetup(name,
                                                    side,
                                                    list[i],
                                                    stretchType,
                                                    ikFkType,
                                                    'parent',
                                                    wristJoint,
                                                    switchCtrl[0],
                                                    stretch,
                                                    volume,
                                                    scale,
                                                    controlColor)
        sknJoints.extend(twistJoints)

    # create ik handle for ik joint chain
    ikHandle = pc.ikHandle(name=(name + side + '_arm_ikhandle'), startJoint=IK[0], endEffector=IK[len(IK) - 1],
                           solver='ikRPsolver')
    # parent ik handle into wrist control and lock the transforms
    pc.parent(ikHandle[0], wristCtrl[0])
    pc.setAttr((ikHandle[0] + '.visibility'), 0)
    chUL.lockAndHide(ikHandle[0], 'lock', 'trans rot scale vis')

    # create pole vector constraint for ikhandle
    pc.poleVectorConstraint(elbowCtrl[0], ikHandle[0])
    # parentConstraint -mo -skipTranslate x -skipTranslate y -skipTranslate z -weight 1 wristCtrl[0] ('ik_' + wristJoint)
    stretchAxis = chUL.getStretchAxis(wristJoint, 'translate')
    pc.select(cl=True)
    tempJoint = cuUL.curveControl('joint', 'curve', controlColor)
    tempJoint[0] = pc.rename(tempJoint[0], 'ik_' + wristJoint + 'RotHelp')
    tr.Snap(('ik_' + wristJoint), tempJoint[0])
    pc.makeIdentity(tempJoint[0], apply=True, t=1, r=1, s=1)
    rad = pc.getAttr(wristJoint + '.radius')
    val = pc.getAttr(wristJoint + '.' + stretchAxis[0])
    pc.setAttr((tempJoint[0] + '.radius'), rad)
    pc.parent(tempJoint[0], ('ik_' + wristJoint))
    # print(tempJoint[99])
    if val < 0.00001:
        if stretchAxis[0] == 'tx':
            pc.move(-0.7, 0, 0, tempJoint[0], r=True, ls=True, wd=True)
        elif stretchAxis[0] == 'ty':
            pc.move(0, -0.7, 0, tempJoint[0], r=True, ls=True, wd=True)
        elif stretchAxis[0] == 'tz':
            pc.move(0, 0, -0.7, tempJoint[0], r=True, ls=True, wd=True)
    else:
        if stretchAxis[0] == 'tx':
            pc.move(0.7, 0, 0, tempJoint[0], r=True, ls=True, wd=True)
        elif stretchAxis[0] == 'ty':
            pc.move(0, 0.7, 0, tempJoint[0], r=True, ls=True, wd=True)
        elif stretchAxis[0] == 'tz':
            pc.move(0, 0, 0.7, tempJoint[0], r=True, ls=True, wd=True)
    # create ik handle for ik joint chain
    ikHandleA = pc.ikHandle(name=(name + side + '_wristRot_ikhandle'), startJoint=IK[len(IK) - 1],
                            endEffector=tempJoint[0], solver='ikSCsolver')
    # parent ik handle into wrist control and lock the transforms
    pc.parent(ikHandleA[0], wristCtrl[0])
    pc.setAttr((ikHandleA[0] + '.visibility'), 0)
    chUL.lockAndHide(ikHandleA[0], 'lock', 'trans rot scale vis')

    # create ik fk visibility connections
    pc.addAttr(switchCtrl[0], ln='autoVis', at='bool', keyable=True)
    pc.setAttr((switchCtrl[0] + '.autoVis'), 1)
    pc.addAttr(switchCtrl[0], ln='fkVis', at='bool', keyable=True)
    pc.addAttr(switchCtrl[0], ln='ikVis', at='bool', keyable=True)
    pc.setAttr((switchCtrl[0] + '.autoVis'), keyable=False, channelBox=True)

    fkIkCnd = pc.createNode('condition', n=(name + side + 'fkIkVis_cnd'))
    fkIkRev = pc.createNode('reverse', n=(name + side + 'fkIkVis_rev'))
    pc.connectAttr((switchCtrl[0] + '.FK_IK'), (fkIkRev + '.inputX'))
    pc.connectAttr((fkIkRev + '.outputX'), (fkIkCnd + '.colorIfFalseR'))
    pc.connectAttr((switchCtrl[0] + '.FK_IK'), (fkIkCnd + '.colorIfFalseG'))
    pc.connectAttr((switchCtrl[0] + '.autoVis'), (fkIkCnd + '.firstTerm'))
    pc.connectAttr((switchCtrl[0] + '.fkVis'), (fkIkCnd + '.colorIfTrueG'))
    pc.connectAttr((switchCtrl[0] + '.ikVis'), (fkIkCnd + '.colorIfTrueR'))

    pc.connectAttr((fkIkCnd + '.outColorR'), (fkContrlList[0] + '.visibility'))
    pc.connectAttr((fkIkCnd + '.outColorR'), (FK[0] + '.visibility'))
    pc.connectAttr((fkIkCnd + '.outColorG'), (wristCtrl[0] + '.visibility'))
    pc.connectAttr((fkIkCnd + '.outColorG'), (elbowCtrl[0] + '.visibility'))
    pc.connectAttr((fkIkCnd + '.outColorG'), (IK[0] + '.visibility'))

    # zero out all controllers and cleanup animation controller
    wristConGrp = chUL.quickZeroOut(wristCtrl[0])
    elbowConGrp = chUL.quickZeroOut(elbowCtrl[0])
    pc.select(cl=True)

    # create guide curve
    guideCurve = chUL.curveGuide(IK[middleIndex], elbowCtrl[0])
    pc.connectAttr((fkIkCnd + '.outColorG'), (guideCurve + '.visibility'))

    chUL.lockAndHide(wristCtrl[0], 'locknHide', 'scale vis')
    chUL.lockAndHide(elbowCtrl[0], 'locknHide', 'rot scale vis')

    if stretchType == 'translate':
        for f in fkContrlList:
            chUL.lockAndHide(f, 'locknHide', 'scale vis')

    if stretchType == 'scale':
        for f in fkContrlList:
            chUL.lockAndHide(f, 'locknHide', 'trans vis')

    # building clavicle setup
    parentJoint = pc.listRelatives(shoulderJoint, parent=True)
    if parentJoint[0] != '':
        buildClavSetup(name, side, parentJoint[0], shoulderJoint, stretch, scale, controlColor)

    parentGrp = pc.listRelatives(fkContrlList[0], parent=True)
    chUL.lockAndHide(parentGrp[0], 'unLock', 'trans rot')
    pc.parent(parentGrp[0], partGrp)

    if parentJoint[0] != '':
        pc.parentConstraint(parentJoint[0], parentGrp[0], mo=True, weight=1)
        chUL.lockAndHide(parentGrp[0], 'lock', 'trans rot')

    # add arm rig info for future update...
    charRigInfo = chUL.getcharRigInfoNode(name)
    pc.addAttr(charRigInfo, ln=(side + 'armRig'), dt='string')
    pc.setAttr((charRigInfo + '.' + (side + 'armRig')),
               (wristCtrl[0] + ' ' + elbowCtrl[0] + ' ' + switchCtrl[0] + ' ' + fkContrlList[0]), type='string')

    # create space switch
    if world:
        if pc.attributeQuery('spineRig', n=charRigInfo, ex=True):
            fkShoulderParent = chUL.quickZeroOut(fkContrlList[0])
            spineRigPart = pc.getAttr(charRigInfo + '.spineRig')
            spineRigArray = spineRigPart.split(' ')
            bsss.buildSpaceSwitchSetup(wristCtrl[0], wristConGrp[0],
                                       [spineRigArray[1], spineRigArray[0], (name + 'worldB_ctrl')],
                                       ['chest', 'root', 'world'], 1)
            bsss.buildSpaceSwitchSetup(elbowCtrl[0], elbowConGrp[0],
                                       [spineRigArray[1], spineRigArray[0], (name + 'worldB_ctrl')],
                                       ['chest', 'root', 'world'], 1)
            bsss.buildSpaceSwitchSetup(fkContrlList[0], fkShoulderParent[0],
                                       [parentJoint[0], spineRigArray[1], (name + 'worldB_ctrl')],
                                       ['clav', 'chest', 'world'], 2)
            pc.setAttr((fkContrlList[0] + '.rotateLock'), 2)

    # parent skeleton
    pc.select(cl=True)
    chUL.parentSkeletonTo(parentJoint[0], cleanGrp[1])

    # create skinJoint set
    set = chUL.createSkinJointSet(name)
    listA = []
    listA.append(parentJoint)
    listA.extend(list)
    sknJoints.extend(listA)
    addSkinJointToSet(set, sknJoints)

    # scale controls to global value
    pc.select(wristCtrl, elbowCtrl, switchCtrl, fkContrlList, r=True)
    cuUL.resizeCurves(None, 1, 1, 1, scale)
    pc.select(cl=True)


#   buildClavSetup 'arm_' 'l' 'joint1' 'joint2' 1
def buildClavSetup(name, side, clavJoint, shoulderJoint, stretch, scale, controlColor):
    # string clavJoint = 'joint1'
    # string shoulderJoint = 'joint2'
    # string name = 'arm_'
    # string side = 'l'
    # int stretch = 0

    partGrp = (name + side + 'armParts_grp')
    grp = []
    offControl = []

    if not pc.objExists(partGrp):
        partGrp = pc.group(em=True, n=(name + side + 'armParts_grp'))
    control = cuUL.curveControl('rotArrow', 'curve', controlColor)
    control[0] = pc.rename(control[0], name + side + 'clav_ctrl')
    if 'l' in str(side).lower():
        pc.scale(control[0], [1, -1, 1], absolute=True)
        pc.makeIdentity(control[0], apply=True, t=1, r=1, s=1, n=0)

    tr.Snap(clavJoint, control[0])

    grp = chUL.quickZeroOut(control[0])
    chUL.lockAndHide(control[0], 'locknHide', 'trans scale vis')

    if stretch:
        offControl = cuUL.curveControl('cube1', 'curve', controlColor)
        offControl[0] = pc.rename(offControl[0], name + side + 'shoulderOffset_ctrl')
        tr.Snap(shoulderJoint, offControl[0])
        pc.makeIdentity(offControl[0], apply=True, t=1, r=1, s=1)
        offGrp = chUL.quickZeroOut(offControl[0])
        chUL.lockAndHide(offControl[0], 'locknHide', 'rot scale vis')
        sScmd = js.buildIkStretch(name, side, clavJoint, shoulderJoint, offControl[0], 'scale')
        pc.parent(offGrp[0], control[0])
        pc.parent(sScmd[0], control[0])
        chUL.lockAndHide(offGrp[0], 'lock', 'trans rot scale vis')
    else:
        pc.parentConstraint(control[0], clavJoint, skipTranslate=['x', 'y', 'z'], weight=1)

    parentJoint = pc.listRelatives(clavJoint, parent=True)
    if parentJoint[0] != '':
        pc.parentConstraint(parentJoint, grp[0], mo=True, weight=1)
    pc.parent(grp[0], partGrp)
    chUL.lockAndHide(grp[0], 'lock', 'trans rot scale vis')

    pc.select(control, offControl, r=True)
    cuUL.resizeCurves(None, 1, 1, 1, scale)
    pc.select(cl=True)
