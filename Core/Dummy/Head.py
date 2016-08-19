import pymel.core as pc

from Util import *
from Maya_Rigging.Utils import List
from Maya_Rigging.Utils import DummyUtil as dU
from Maya_Rigging.Core import ModuleSymmetryLib as modSymLib

def Head(name, side, moduleName, colorIndex):
    dummyBoneGrp = ''
    jointPosList = ''
    jointPosLists = []

    headPlacer = linearDisDummyBoneCreator(name, side, moduleName, 2, 'y', 7, colorIndex)

    # create head annotation
    head = createModuleAnnotation((name + side + moduleName), headPlacer)

    lEyeDummyJnt = createDummyJoint(colorIndex)
    lEyeDummyJnt[0] = pc.rename(lEyeDummyJnt[0], (name + side + 'l_' + moduleName + 'Eye_loc'))
    pc.scale(lEyeDummyJnt[0], (0.7, 0.7, 0.7))
    pc.addAttr(lEyeDummyJnt[0], ln='jointPosList', dt='string')
    pc.setAttr((lEyeDummyJnt[0] + '.jointPosList'), lEyeDummyJnt[0], type='string')

    # create l_eye annotation
    lEye = createModuleAnnotation((name + 'l_eye'), lEyeDummyJnt[0])
    pc.setAttr((lEye + '.t'), (0, 1, 0))
    pc.rename(lEye, (name + side + moduleName + 'LEye_annotate'))

    rEyeDummyJnt = createDummyJoint(colorIndex)
    rEyeDummyJnt[0] = pc.rename(rEyeDummyJnt[0], (name + side + 'r_' + moduleName + 'Eye_loc'))
    pc.scale(rEyeDummyJnt[0], (0.7, 0.7, 0.7))
    pc.addAttr(rEyeDummyJnt[0], ln='jointPosList', dt='string')
    pc.setAttr((rEyeDummyJnt[0] + '.jointPosList'), rEyeDummyJnt[0], type='string')

    # create r_eye annotation
    rEye = createModuleAnnotation((name + 'r_eye'), rEyeDummyJnt[0])
    pc.setAttr((rEye + '.t'), (0, 1, 0))
    pc.rename(rEye, (name + side + moduleName + 'REye_annotate'))

    modSymLib.moduleSymmetryConnector(lEyeDummyJnt[0], rEyeDummyJnt[0])
    pc.move(1, 3, 1.5, lEyeDummyJnt[0])
    pc.parent(lEyeDummyJnt[0], rEyeDummyJnt[0], headPlacer)

    pc.addAttr(headPlacer, ln='child', dt='string')
    pc.setAttr((headPlacer + '.child'), (lEyeDummyJnt[0] + ' ' + rEyeDummyJnt[0]), type='string')
    pc.addAttr(headPlacer, ln='side', dt='string')
    pc.setAttr((headPlacer + '.side'), side, type='string')

    jointPosList = pc.getAttr(headPlacer + '.jointPosList')
    jointPosLists = List.seperate(jointPosList)
    dummyBoneGrp = createDummyBone(side, moduleName, jointPosLists[0], lEyeDummyJnt[0])
    dummyBoneGrp = createDummyBone(side, moduleName, jointPosLists[0], rEyeDummyJnt[0])

    pc.addAttr(lEyeDummyJnt[0], ln='parent', dt='string')
    pc.setAttr((lEyeDummyJnt[0] + '.parent'), jointPosLists[0], type='string')
    pc.addAttr(rEyeDummyJnt[0], ln='parent', dt='string')
    pc.setAttr((rEyeDummyJnt[0] + '.parent'), jointPosLists[0], type='string')

    pc.setAttr((dummyBoneGrp + '.inheritsTransform'), 0)
    try:
        pc.parent(dummyBoneGrp, headPlacer, r=True)
    except:
        pass
    pc.select(cl=True)

def Neck(name, side, moduleName, numCon, axis, dis, colorIndex):
    neckPlacer = ''

    if numCon > 1:
        neckPlacer = linearDisDummyBoneCreator(name, side, moduleName, numCon, axis, dis, colorIndex)
        jointPosList = pc.getAttr(neckPlacer + '.jointPosList')
        jointPosLists = List.seperate(jointPosList)
        size = len(jointPosList)

    else:
        mainNeckPlacer = cuLib.curveControl('cube1', 'curve')
        mainNeckPlacer[0] = pc.rename(mainNeckPlacer[0], name + side + moduleName + 'Main_ctrl')
        shapeColorOverride(mainNeckPlacer[0], colorIndex)
        cuLib.resizeCurves(None, 1, 1, 1, 1.5)
        pc.addAttr(mainNeckPlacer[0], ln='jointPosList', dt='string')

        neckDummyJoint = createDummyJoint(colorIndex)
        neckDummyJoint[0] = pc.rename(neckDummyJoint[0], (name + side + 'neck_loc'))
        pc.scale(neckDummyJoint[0], (1, 1, 1))

        pc.parent(neckDummyJoint[0], mainNeckPlacer[0])

        pc.setAttr((mainNeckPlacer[0] + '.jointPosList'), neckDummyJoint[0], type='string')
        neckPlacer = mainNeckPlacer[0]

    # create neck annotation
    neck = createModuleAnnotation((name + side + moduleName), neckPlacer)

    pc.select(cl=True)

def HeadNeck(name, side, moduleName, numCon, axis, dis, colorIndex):
    Neck(name, side, moduleName, numCon, axis, dis, colorIndex)
    Head(name, side, 'head', colorIndex)

    neckPlacer = (name + side + moduleName + 'Main_ctrl')
    headPlacer = (name + side + 'headMain_ctrl')

    pc.addAttr(neckPlacer, ln='child', dt='string')
    pc.setAttr((neckPlacer + '.child'), headPlacer, type='string')

    headPos = 0.0

    neckJoint = pc.getAttr(neckPlacer + '.jointPosList')
    neckJointList = List.seperate(neckJoint)

    headJoint = pc.getAttr(headPlacer + '.jointPosList')
    headJointList = List.seperate(headJoint)

    eyeJoints = pc.getAttr(headPlacer + '.child')

    neckJoint = pc.getAttr(neckPlacer + '.jointPosList')
    neckJointList = List.seperate(neckJoint)

    size = 0

    if numCon > 1:
        size = len(neckJointList)
        modSymLib.connectModuleComponents(neckJointList[size - 1], headPlacer)
        headPos = (dis / (numCon - 1))
        pc.move(0, (dis + headPos), 0, headPlacer)
    else:
        modSymLib.connectModuleComponents(neckJointList[0], headPlacer)
        headPos = (dis / numCon)
        pc.move(0, headPos, 0, headPlacer)

    pc.parent(headPlacer, neckPlacer)

    # create world pos loc and parent main arm placer ctrl...
    worldPosLoc = buildWorldPosLoc(name)
    if not pc.attributeQuery('neckHead', n=worldPosLoc, ex=True):
        pc.addAttr(worldPosLoc, ln='neckHead', dt='string')

    moduleParts = pc.getAttr(worldPosLoc + '.neckHead')
    pc.setAttr((worldPosLoc + '.neckHead'), (str(moduleParts or '') + ' ' + neckPlacer), type='string')

    pc.parent(neckPlacer, worldPosLoc)

    # module tags
    pc.addAttr(headPlacer, ln='moduleTag', dt='string')
    pc.addAttr(headPlacer, ln='buildTag', dt='string')

    pc.setAttr((headPlacer + '.moduleTag'), 'head', type='string')
    pc.setAttr((headPlacer + '.buildTag'), worldPosLoc, type='string')

    pc.addAttr(neckPlacer, ln='moduleTag', dt='string')
    pc.addAttr(neckPlacer, ln='buildTag', dt='string')

    pc.setAttr((neckPlacer + '.moduleTag'), 'neck', type='string')
    pc.setAttr((neckPlacer + '.buildTag'), worldPosLoc, type='string')

    pc.addAttr(neckPlacer, ln='name', dt='string')
    pc.setAttr((neckPlacer + '.name'), name, type='string')
    pc.addAttr(neckPlacer, ln='side', dt='string')
    pc.setAttr((neckPlacer + '.side'), side, type='string')
    pc.addAttr(neckPlacer, ln=(side + 'neckJoint'), dt='string')
    pc.setAttr((neckPlacer + '.' + (side + 'neckJoint')), neckJointList[0], type='string')
    pc.addAttr(neckPlacer, ln=(side + 'headJoint'), dt='string')
    pc.setAttr((neckPlacer + '.' + (side + 'headJoint')), headJointList[0], type='string')
    pc.addAttr(neckPlacer, ln=(side + 'eyeJoints'), dt='string')
    pc.setAttr((neckPlacer + '.' + (side + 'eyeJoints')), eyeJoints, type='string')

    print('adding dummy joints')
    dU.add_dummy_twist_joints_attr(neckPlacer, neckJointList[0], headJointList[0], 3)