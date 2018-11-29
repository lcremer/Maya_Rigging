import pymel.core as pc
from Util import *
from Fingers import createFingers
from Maya_Rigging.Utils import DummyUtil as dU
from Maya_Rigging.Core import ModuleSymmetryLib as modSymLib


def Arm(name, side, numJoints, fingers, numFingers, numSegment, colorIndex):
    elementsList = ''
    dummyBoneGrp = ''
    clavDummyJoint = createDummyJoint(colorIndex)
    clavDummyJoint[0] = pc.rename(clavDummyJoint[0], (name + side + 'clav_loc'))
    pc.move(1, 0, 1, clavDummyJoint[0])

    curve = pc.curve(d=1, p=[(3, 0, 0), (10, 0, -1), (17, 0, 0)])
    armDummyBonePos = getDummyBoneLimbPos(curve, numJoints)
    pc.delete(curve)

    armSegmentNames = ['shoulder', 'elbow']
    middleIndex = (numJoints / 2)
    allArmDummyJoints = []

    for i in range(numJoints - 1):
        tempDummyJoint = createDummyJoint(colorIndex)
        if numJoints == 3:
            if i <= middleIndex:
                tempDummyJoint[0] = pc.rename(tempDummyJoint[0], (name + side + armSegmentNames[0] + '_loc'))
            if i >= middleIndex:
                tempDummyJoint[0] = pc.rename(tempDummyJoint[0], (name + side + armSegmentNames[1] + '_loc'))
        else:
            if i <= middleIndex:
                tempDummyJoint[0] = pc.rename(tempDummyJoint[0],
                                              (name + side + armSegmentNames[0] + str(i + 1) + '_loc'))
            if i >= middleIndex:
                tempDummyJoint[0] = pc.rename(tempDummyJoint[0],
                                              (name + side + armSegmentNames[1] + (str(i + 1) - middleIndex) + '_loc'))

        tempPosition = armDummyBonePos[i]
        pc.move((tempPosition[0]), (tempPosition[1]), (tempPosition[2]), tempDummyJoint[0])

        allArmDummyJoints.append(tempDummyJoint[0])

        if i > 0:
            dummyBoneGrp = createDummyBone('arm', side, allArmDummyJoints[i - 1], allArmDummyJoints[i])

    mainArmPlacer = cuLib.curveControl('cube1', 'curve')
    mainArmPlacer[0] = pc.rename(mainArmPlacer[0], name + side + 'armPlacer_loc')
    cuLib.resizeCurves(None, 1, 1, 1, 1.5)
    shapeColorOverride(mainArmPlacer[0], colorIndex)
    pc.addAttr(mainArmPlacer[0], ln='jointPosList', dt='string')

    # create arm annotation
    arm = createModuleAnnotation((name + side + 'arm'), mainArmPlacer[0])
    pc.setAttr((arm + '.t'), (0, 1, 0))

    # shoulderPosition
    shoulderPosition = armDummyBonePos[0]
    pc.move((shoulderPosition[0]), (shoulderPosition[1]), (shoulderPosition[2]), mainArmPlacer[0])
    wristDummyJoint = createDummyJoint(colorIndex)
    wristDummyJoint[0] = pc.rename(wristDummyJoint[0], (name + side + 'wrist_loc'))
    wristEndDummyJoint = createDummyJoint(colorIndex)
    wristEndDummyJoint[0] = pc.rename(wristEndDummyJoint[0], (name + side + 'wristEnd_loc'))

    mainWristPlacer = cuLib.curveControl('cube1', 'curve')
    mainWristPlacer[0] = pc.rename(mainWristPlacer[0], name + side + 'wristPlacer_loc')
    cuLib.resizeCurves(None, 1, 1, 1, 1.5)
    shapeColorOverride(mainWristPlacer[0], colorIndex)
    pc.addAttr(mainWristPlacer[0], ln='jointPosList', dt='string')
    pc.setAttr((mainWristPlacer[0] + '.jointPosList'), wristDummyJoint[0], type='string')

    # create wrist annotation
    wrist = createModuleAnnotation((name + side + 'wrist'), mainWristPlacer[0])
    pc.setAttr((wrist + '.t'), (0, 1, 0))

    pc.addAttr(mainArmPlacer[0], ln='wristPlacer', dt='string')
    pc.setAttr((mainArmPlacer[0] + '.wristPlacer'), mainWristPlacer[0], type='string')

    pc.move(0.7, 0, 0, wristEndDummyJoint)
    dummyBoneGrp = createDummyBone('arm', side, clavDummyJoint[0], allArmDummyJoints[0])
    dummyBoneGrp = createDummyBone('arm', side, allArmDummyJoints[numJoints - 2], wristDummyJoint[0])
    dummyBoneGrp = createDummyBone('arm', side, wristDummyJoint[0], wristEndDummyJoint[0])

    pc.parent(wristDummyJoint, wristEndDummyJoint, mainWristPlacer[0])

    # wristPosition
    wristPosition = armDummyBonePos[numJoints - 1]
    pc.move((wristPosition[0]), (wristPosition[1]), (wristPosition[2]), mainWristPlacer[0])

    elementsList = elementsList + (clavDummyJoint[0] + ' ')
    for n in range(len(allArmDummyJoints)):
        elementsList = elementsList + (allArmDummyJoints[n] + ' ')
        pc.setAttr((allArmDummyJoints[n] + '.ty'), lock=True)

    elementsList = elementsList + (wristDummyJoint[0] + ' ' + wristEndDummyJoint[0])
    pc.setAttr((mainArmPlacer[0] + '.jointPosList'), elementsList, type='string')

    pc.parent(allArmDummyJoints, mainArmPlacer[0])
    pc.parent(mainWristPlacer[0], mainArmPlacer[0])
    pc.setAttr((wristDummyJoint[0] + '.ty'), lock=True)
    pc.setAttr((wristEndDummyJoint[0] + '.ty'), lock=True)
    pc.setAttr((wristEndDummyJoint[0] + '.tz'), lock=True)
    pc.setAttr((mainWristPlacer[0] + '.ty'), lock=True)

    pc.select(clavDummyJoint[0], allArmDummyJoints, wristDummyJoint[0], wristEndDummyJoint[0], r=True)
    # pc.scale((0.7,0.7,0.7))
    pc.select(cl=True)

    if fingers:
        # declaring position for fingers
        fingerList = ''

        fingerPos = [(17.7, -0.35, 1), (18.3, 0.15, 0.9), (18.2, 0.3, 0.1), (18.15, 0.15, -0.5), (18.1, 0, -1)]
        fingerRot = [(85, -35, -30), (0, -3, 0), (0, 0, 0), (0, 5, 0), (0, 10.25, 0)]
        scale = [0.35, 0.35, 0.4, 0.35, 0.3]
        fingerNames = ['thumb', 'index', 'middle', 'ring', 'pinky']

        pc.select(cl=True)
        for j in range(numFingers):
            if j == 0:  # idea here is that thumb joints will have one less segment compare to other fingers
                finger = createFingers(name, fingerNames[j], side, numSegment, 'x', 3, colorIndex)
            else:
                finger = createFingers(name, fingerNames[j], side, (numSegment + 1), 'x', 3, colorIndex)

            fingerList = fingerList + (finger + ' ')

            position = fingerPos[j]
            pc.move(position[0], position[1], position[2], finger)

            rotation = fingerRot[j]
            pc.rotate(finger, rotation[0], rotation[1],
                      rotation[2])  # NOTE: for some reason pymel rotate does not follow the pattern that move does

            modSymLib.connectModuleComponents(wristDummyJoint[0], finger)

            pc.scale(finger, (scale[j], scale[j], scale[j]))

            pc.parent(finger, mainWristPlacer[0])

            pc.setAttr((finger + '.buildTag'), mainArmPlacer[0], type='string')

            pc.select(cl=True)

        pc.addAttr(mainArmPlacer[0], ln='child', dt='string')
        pc.setAttr((mainArmPlacer[0] + '.child'), fingerList, type='string')

    pc.setAttr((dummyBoneGrp + '.inheritsTransform'), 0)
    pc.parent(dummyBoneGrp, mainArmPlacer[0], r=True)

    # create world pos loc and parent main arm placer ctrl...
    worldPosLoc = buildWorldPosLoc(name)

    if not pc.attributeQuery('arm', n=worldPosLoc, ex=True):
        pc.addAttr(worldPosLoc, ln='arm', dt='string')

    moduleParts = pc.getAttr(worldPosLoc + '.' + 'arm')
    pc.setAttr((worldPosLoc + '.' + 'arm'), (str(moduleParts or '') + ' ' + mainArmPlacer[0]), type='string')

    pc.parent(clavDummyJoint[0], mainArmPlacer[0], worldPosLoc)

    # module tags
    pc.addAttr(mainArmPlacer[0], ln='moduleTag', dt='string')
    pc.addAttr(mainArmPlacer[0], ln='buildTag', dt='string')

    pc.setAttr((mainArmPlacer[0] + '.moduleTag'), 'arm', type='string')
    pc.setAttr((mainArmPlacer[0] + '.buildTag'), worldPosLoc, type='string')

    # rig info Attr
    pc.addAttr(mainArmPlacer[0], ln='name', dt='string')
    pc.setAttr((mainArmPlacer[0] + '.name'), name, type='string')
    pc.addAttr(mainArmPlacer[0], ln='side', dt='string')
    pc.setAttr((mainArmPlacer[0] + '.side'), side, type='string')
    pc.addAttr(mainArmPlacer[0], ln=(side + 'shoulderJoint'), dt='string')
    pc.setAttr((mainArmPlacer[0] + '.' + (side + 'shoulderJoint')), allArmDummyJoints[0], type='string')
    pc.addAttr(mainArmPlacer[0], ln=(side + 'wristJoint'), dt='string')
    pc.setAttr((mainArmPlacer[0] + '.' + (side + 'wristJoint')), wristDummyJoint[0], type='string')
    pc.select(cl=True)

    # add dummy twist joints
    for i in range(0, len(allArmDummyJoints)):
        if i > 0:
            dU.add_dummy_twist_joints_attr(mainArmPlacer[0], allArmDummyJoints[i - 1], allArmDummyJoints[i], 2)
    dU.add_dummy_twist_joints_attr(mainArmPlacer[0], allArmDummyJoints[len(allArmDummyJoints) - 1], wristDummyJoint[0],2)

