import pymel.core as pc
from Util import *
from Fingers import createFingers
from RiggingSystem.Utils import DummyUtil as dU

def LegBiped(name, side, numJoints, fingers, numFingers, numSegment, colorIndex):
    list = ''
    dummyBoneGrp = ''
    curve = pc.curve(d=1, p=[(2, 15, 0), (2, 8, 1), (2, 1, 0)])

    legDummyBonePos = getDummyBoneLimbPos(curve, numJoints)
    pc.delete(curve)

    legSegmentNames = ['hip', 'knee']
    middleIndex = (numJoints / 2)
    allLegDummyJoints = []

    for i in range(numJoints - 1):
        tempDummyJoint = createDummyJoint(colorIndex)
        if numJoints == 3:
            if i <= middleIndex:
                tempDummyJoint[0] = pc.rename(tempDummyJoint[0], (name + side + legSegmentNames[0] + '_loc'))
            if i >= middleIndex:
                tempDummyJoint[0] = pc.rename(tempDummyJoint[0], (name + side + legSegmentNames[1] + '_loc'))
        else:
            if i <= middleIndex:
                tempDummyJoint[0] = pc.rename(tempDummyJoint[0],
                                              (name + side + legSegmentNames[0] + str(i + 1) + '_loc'))
            if i >= middleIndex:
                tempDummyJoint[0] = pc.rename(tempDummyJoint[0],
                                              (name + side + legSegmentNames[1] + (str(i + 1) - middleIndex) + '_loc'))

        tempPosition = legDummyBonePos[i]
        pc.move((tempPosition[0]), (tempPosition[1]), (tempPosition[2]), tempDummyJoint[0])
        allLegDummyJoints.append(tempDummyJoint[0])
        if i > 0:
            dummyBoneGrp = createDummyBone('leg', side, allLegDummyJoints[i - 1], allLegDummyJoints[i])

    ankleDummyJoint = createDummyJoint(colorIndex)
    ankleDummyJoint[0] = pc.rename(ankleDummyJoint[0], (name + side + 'ankle_loc'))
    ballDummyJoint = createDummyJoint(colorIndex)
    ballDummyJoint[0] = pc.rename(ballDummyJoint[0], (name + side + 'ball_loc'))
    toeDummyJoint = createDummyJoint(colorIndex)
    toeDummyJoint[0] = pc.rename(toeDummyJoint[0], (side + 'toe_loc'))

    mainLegPlacer = cuLib.curveControl('cube1', 'curve')
    mainLegPlacer[0] = pc.rename(mainLegPlacer[0], name + side + 'legPlacer_loc')
    cuLib.resizeCurves(None, 1, 1, 1, 1.5)
    shapeColorOverride(mainLegPlacer[0], colorIndex)
    pc.addAttr(mainLegPlacer[0], ln='jointPosList', dt='string')
    pc.addAttr(mainLegPlacer[0], ln='footPlacer', dt='string')

    # create leg annotation
    leg = createModuleAnnotation((name + side + 'leg'), mainLegPlacer[0])
    pc.setAttr((leg + '.t'), (0, 1, 0))

    mainFootPlacer = cuLib.curveControl('cube1', 'curve')
    mainFootPlacer[0] = pc.rename(mainFootPlacer[0], name + side + 'footPlacer_loc')
    cuLib.resizeCurves(None, 1, 1, 1, 1.5)
    shapeColorOverride(mainFootPlacer[0], colorIndex)
    pc.addAttr(mainFootPlacer[0], ln='jointPosList', dt='string')

    hipPosition = legDummyBonePos[0];
    pc.move((hipPosition[0]), (hipPosition[1]), (hipPosition[2]), mainLegPlacer[0])

    anklePosition = legDummyBonePos[numJoints - 1]
    pc.parent(ankleDummyJoint[0], mainFootPlacer[0])
    pc.setAttr((ankleDummyJoint[0] + '.t'), (0, 0, 0))
    pc.move((anklePosition[0]), (anklePosition[1]), (anklePosition[2]), mainFootPlacer[0])

    # create ankle annotation
    ankle = createModuleAnnotation((name + side + 'ankle'), mainFootPlacer[0])
    pc.setAttr((ankle + '.t'), (1, 0, 0))

    pc.move(2, 0, 2, ballDummyJoint, )
    pc.move(2, 0, 4, toeDummyJoint, )

    dummyBoneGrp = createDummyBone('leg', side, allLegDummyJoints[numJoints - 2], ankleDummyJoint[0])
    dummyBoneGrp = createDummyBone('leg', side, ankleDummyJoint[0], ballDummyJoint[0])
    dummyBoneGrp = createDummyBone('leg', side, ballDummyJoint[0], toeDummyJoint[0])

    pc.parent(ballDummyJoint, toeDummyJoint, mainFootPlacer[0])
    pc.parent(allLegDummyJoints, mainFootPlacer[0], mainLegPlacer[0])

    for n in allLegDummyJoints:
        list = list + (n + ' ')
        pc.setAttr(n + '.tx', lock=True)

    list = list + (ankleDummyJoint[0] + ' ' + ballDummyJoint[0] + ' ' + toeDummyJoint[0])
    pc.setAttr((mainLegPlacer[0] + '.jointPosList'), list, type='string')
    pc.setAttr((mainLegPlacer[0] + '.footPlacer'), mainFootPlacer[0], type='string')
    pc.setAttr((mainFootPlacer[0] + '.jointPosList'), ankleDummyJoint[0], type='string')

    pc.setAttr((dummyBoneGrp + '.inheritsTransform'), 0)
    pc.parent(dummyBoneGrp, mainLegPlacer[0], r=True)
    pc.select(cl=True)

    pc.select(allLegDummyJoints, ankleDummyJoint[0], ballDummyJoint, toeDummyJoint, r=True)
    # pc.scale((0.7, 0.7, 0.7))
    pc.select(cl=True)

    if fingers:
        # declaring position for fingers
        pc.addAttr(mainLegPlacer[0], ln='child', dt='string')
        fingerJointList = ''
        fingerPos = [(1, 0, 2), (1.7, 0, 2), (2.4, 0, 2), (3.1, 0, 2), (3.8, 0, 2)]
        scale = [0.35, 0.32, 0.30, 0.27, 0.25]
        fingerName = ['bigToe', 'indexToe', 'midToe', 'ringToe', 'pinkyToe']

        for i in range(numFingers):
            finger = createFingers(name, fingerName[i], side, numSegment, 'z', 2, colorIndex)
            fingerJointList = fingerJointList + (finger + ' ')
            pc.addAttr(finger, ln='parent', dt='string')
            pc.setAttr((finger + '.parent'), ballDummyJoint, type='string')
            position = fingerPos[i]
            pc.move((position[0]), (position[1]), (position[2]), finger)
            pc.scale(finger, (scale[i], scale[i], scale[i]))
            pc.parent(finger, mainFootPlacer[0])
            pc.select(cl=True)
            pc.setAttr((finger + '.buildTag'), mainLegPlacer[0], type='string')
        pc.setAttr((mainLegPlacer[0] + '.child'), fingerJointList, type='string')

    # lock Attrs
    pc.setAttr((ankleDummyJoint[0] + '.tx'), lock=True)
    pc.setAttr((ballDummyJoint[0] + '.tx'), lock=True)
    pc.setAttr((toeDummyJoint[0] + '.tx'), lock=True)
    pc.setAttr((mainFootPlacer[0] + '.tx'), lock=True)
    pc.setAttr((mainFootPlacer[0] + '.rz'), lock=True)
    pc.setAttr((mainLegPlacer[0] + '.rz'), lock=True)

    # create world pos loc and parent main leg placer ctrl..
    worldPosLoc = buildWorldPosLoc(name)
    if not pc.attributeQuery('leg', n=worldPosLoc, ex=True):
        pc.addAttr(worldPosLoc, ln='leg', dt='string')

    moduleParts = pc.getAttr(worldPosLoc + '.leg')
    pc.setAttr((worldPosLoc + '.leg'), (str(moduleParts or '') + ' ' + mainLegPlacer[0]), type='string')

    pc.parent(mainLegPlacer[0], worldPosLoc)

    # module tags
    pc.addAttr(mainLegPlacer[0], ln='moduleTag', dt='string')
    pc.addAttr(mainLegPlacer[0], ln='buildTag', dt='string')

    pc.setAttr((mainLegPlacer[0] + '.moduleTag'), 'bipedLeg', type='string')
    pc.setAttr((mainLegPlacer[0] + '.buildTag'), worldPosLoc, type='string')

    # rig info Attr
    pc.addAttr(mainLegPlacer[0], ln='name', dt='string')
    pc.setAttr((mainLegPlacer[0] + '.name'), name, type='string')
    pc.addAttr(mainLegPlacer[0], ln='side', dt='string')
    pc.setAttr((mainLegPlacer[0] + '.side'), side, type='string')
    pc.addAttr(mainLegPlacer[0], ln=(side + 'hipJoint'), dt='string')
    pc.setAttr((mainLegPlacer[0] + '.' + (side + 'hipJoint')), allLegDummyJoints[0], type='string')
    pc.addAttr(mainLegPlacer[0], ln=(side + 'ankleJoint'), dt='string')
    pc.setAttr((mainLegPlacer[0] + '.' + (side + 'ankleJoint')), ankleDummyJoint[0], type='string')
    pc.addAttr(mainLegPlacer[0], ln=(side + 'ballJoint'), dt='string')
    pc.setAttr((mainLegPlacer[0] + '.' + (side + 'ballJoint')), ballDummyJoint[0], type='string')
    pc.select(cl=True)

    # add dummy twist joints
    for i in range(0, len(allLegDummyJoints)):
        if i > 0:
            dU.add_dummy_twist_joints_attr(mainFootPlacer[0], allLegDummyJoints[i - 1], allLegDummyJoints[i], 2)
    dU.add_dummy_twist_joints_attr(mainFootPlacer[0], allLegDummyJoints[len(allLegDummyJoints) - 1], ankleDummyJoint[0],
                                   2)
    dU.add_dummy_twist_joints_attr(mainFootPlacer[0], ankleDummyJoint[0], ballDummyJoint[0], 0)


def LegQuad(name, side, numJoints, fingers, numFingers, numSegment, colorIndex):
    list = ''
    dummyBoneGrp = ''

    curve = pc.curve(d=1, p=[(2, 15, 0), (2, 9, 2), (2, 4, -1), (2, 1, 0)])
    legDummyBonePos = getDummyBoneLimbPos(curve, numJoints)
    pc.delete(curve)

    legSegmentNames = ['hip', 'knee']
    middleIndex = (numJoints / 2)
    allLegDummyJoints = []

    for i in range(numJoints - 1):
        tempDummyJoint = createDummyJoint(colorIndex)
        if numJoints == 3:
            if i <= middleIndex:
                tempDummyJoint[0] = pc.rename(tempDummyJoint[0], (name + side + legSegmentNames[0] + '_loc'))
            if i >= middleIndex:
                tempDummyJoint[0] = pc.rename(tempDummyJoint[0], (name + side + legSegmentNames[1] + '_loc'))
        else:
            if i <= middleIndex:
                tempDummyJoint[0] = pc.rename(tempDummyJoint[0],
                                              (name + side + legSegmentNames[0] + str(i + 1) + '_loc'))
            if i >= middleIndex:
                tempDummyJoint[0] = pc.rename(tempDummyJoint[0],
                                              (name + side + legSegmentNames[1] + (str(i + 1 - middleIndex)) + '_loc'))

        tempPosition = legDummyBonePos[i]

        pc.move((tempPosition[0]), (tempPosition[1]), (tempPosition[2]), tempDummyJoint[0])

        allLegDummyJoints.append(tempDummyJoint[0])
        if i > 0:
            dummyBoneGrp = createDummyBone('leg', side, allLegDummyJoints[i - 1], allLegDummyJoints[i])

    hockJoint = createModuleAnnotation((name + side + 'hockJoint'), allLegDummyJoints[numJoints - 2])
    pc.setAttr((hockJoint + '.t'), (0, 1, 0))

    ankleDummyJoint = createDummyJoint(colorIndex)
    ankleDummyJoint[0] = pc.rename(ankleDummyJoint[0], (name + side + 'ankle_loc'))
    ballDummyJoint = createDummyJoint(colorIndex)
    ballDummyJoint[0] = pc.rename(ballDummyJoint[0], (name + side + 'ball_loc'))
    toeDummyJoint = createDummyJoint(colorIndex)
    toeDummyJoint[0] = pc.rename(toeDummyJoint[0], (side + 'toe_loc'))

    mainLegPlacer = cuLib.curveControl('cube1', 'curve')
    mainLegPlacer[0] = pc.rename(mainLegPlacer[0], name + side + 'legPlacer_loc')
    cuLib.resizeCurves(None, 1, 1, 1, 1.5)
    shapeColorOverride(mainLegPlacer[0], colorIndex)
    pc.addAttr(mainLegPlacer[0], ln='jointPosList', dt='string')
    pc.addAttr(mainLegPlacer[0], ln='footPlacer', dt='string')

    # create leg annotation
    leg = createModuleAnnotation((name + side + 'leg'), mainLegPlacer[0])
    pc.setAttr((leg + '.t'), (0, 1, 0))

    mainFootPlacer = cuLib.curveControl('cube1', 'curve')
    mainFootPlacer[0] = pc.rename(mainFootPlacer[0], name + side + 'footPlacer_loc')
    cuLib.resizeCurves(None, 1, 1, 1, 1.5)
    shapeColorOverride(mainFootPlacer[0], colorIndex)
    pc.addAttr(mainFootPlacer[0], ln='jointPosList', dt='string')

    hipPosition = legDummyBonePos[0]
    pc.move((hipPosition[0]), (hipPosition[1]), (hipPosition[2]), mainLegPlacer[0])

    anklePosition = legDummyBonePos[numJoints - 1]
    pc.parent(ankleDummyJoint[0], mainFootPlacer[0])
    pc.setAttr((ankleDummyJoint[0] + '.t'), (0, 0, 0))
    pc.move((anklePosition[0]), (anklePosition[1]), (anklePosition[2]), mainFootPlacer[0])

    # create ankle annotation
    ankle = createModuleAnnotation((name + side + 'ankle'), mainFootPlacer[0])
    pc.setAttr((ankle + '.t'), (1, 0, 0))

    pc.move(2, 0, 2, ballDummyJoint)
    pc.move(2, 0, 4, toeDummyJoint)

    dummyBoneGrp = createDummyBone('leg', side, allLegDummyJoints[numJoints - 2], ankleDummyJoint[0])
    dummyBoneGrp = createDummyBone('leg', side, ankleDummyJoint[0], ballDummyJoint[0])
    dummyBoneGrp = createDummyBone('leg', side, ballDummyJoint[0], toeDummyJoint[0])

    pc.parent(ballDummyJoint, toeDummyJoint, mainFootPlacer[0])
    pc.parent(allLegDummyJoints, mainFootPlacer[0], mainLegPlacer[0])

    for a in allLegDummyJoints:
        list = list + (a + ' ')
        pc.setAttr((a + '.tx'), lock=True)

    list = list + (ankleDummyJoint[0] + ' ' + ballDummyJoint[0] + ' ' + toeDummyJoint[0])
    pc.setAttr((mainLegPlacer[0] + '.jointPosList'), list, type='string')
    pc.setAttr((mainLegPlacer[0] + '.footPlacer'), mainFootPlacer[0], type='string')
    pc.setAttr((mainFootPlacer[0] + '.jointPosList'), ankleDummyJoint[0], type='string')

    pc.setAttr((dummyBoneGrp + '.inheritsTransform'), 0)
    pc.parent(dummyBoneGrp, mainLegPlacer[0], r=True)
    pc.select(cl=True)

    pc.select(allLegDummyJoints, ankleDummyJoint[0], ballDummyJoint, toeDummyJoint, r=True)
    # pc.scale((0.7, 0.7, 0.7))
    pc.select(cl=True)

    if fingers:
        # declaring position for fingers
        pc.addAttr(mainLegPlacer[0], ln='child', dt='string')
        fingerJointList = ''
        fingerPos = [(1, 0, 1.5), (1.7, 0, 1.5), (2.4, 0, 1.5), (3.1, 0, 1.5), (3.8, 0, 1.5)]
        scale = [0.35, 0.385, 0.385, 0.35, 0.35]
        fingerName = ['bigToe', 'indexToe', 'midToe', 'ringToe', 'pinkyToe']

        for i in range(numFingers):
            finger = createFingers(name, fingerName[i], side, numSegment, 'z', 2, colorIndex)
            fingerJointList = fingerJointList + (finger + ' ')
            pc.addAttr(finger, ln='parent', dt='string')
            pc.setAttr((finger + '.parent'), ankleDummyJoint, type='string')
            position = fingerPos[i]
            pc.move(position[0], position[1], position[2], finger)
            pc.scale(finger, (scale[i], scale[i], scale[i]))
            pc.parent(finger, mainFootPlacer[0])
            pc.select(cl=True)
            pc.setAttr((finger + '.buildTag'), mainLegPlacer[0], type='string')
        pc.setAttr((mainLegPlacer[0] + '.child'), fingerJointList, type='string')

    # lock Attrs
    pc.setAttr((ankleDummyJoint[0] + '.tx'), lock=True)
    pc.setAttr((ballDummyJoint[0] + '.tx'), lock=True)
    pc.setAttr((toeDummyJoint[0] + '.tx'), lock=True)
    pc.setAttr((mainFootPlacer[0] + '.tx'), lock=True)
    pc.setAttr((mainFootPlacer[0] + '.rz'), lock=True)
    pc.setAttr((mainLegPlacer[0] + '.rz'), lock=True)

    # create world pos loc and parent main leg placer ctrl..
    worldPosLoc = buildWorldPosLoc(name)
    if not pc.attributeQuery('leg', n=worldPosLoc, ex=True):
        pc.addAttr(worldPosLoc, ln='leg', dt='string')

    moduleParts = pc.getAttr(worldPosLoc + '.' + 'leg')
    pc.setAttr((worldPosLoc + '.' + 'leg'), (str(moduleParts or '') + ' ' + mainLegPlacer[0]), type='string')

    pc.parent(mainLegPlacer[0], worldPosLoc)

    # module tags
    pc.addAttr(mainLegPlacer[0], ln='moduleTag', dt='string')
    pc.addAttr(mainLegPlacer[0], ln='buildTag', dt='string')

    pc.setAttr((mainLegPlacer[0] + '.moduleTag'), 'quadLeg', type='string')
    pc.setAttr((mainLegPlacer[0] + '.buildTag'), worldPosLoc, type='string')

    # rig info Attr
    pc.addAttr(mainLegPlacer[0], ln='name', dt='string')
    pc.setAttr((mainLegPlacer[0] + '.name'), name, type='string')
    pc.addAttr(mainLegPlacer[0], ln='side', dt='string')
    pc.setAttr((mainLegPlacer[0] + '.side'), side, type='string')
    pc.addAttr(mainLegPlacer[0], ln=(side + 'hipJoint'), dt='string')
    pc.setAttr((mainLegPlacer[0] + '.' + (side + 'hipJoint')), allLegDummyJoints[0], type='string')
    pc.addAttr(mainLegPlacer[0], ln=(side + 'hockJoint'), dt='string')
    pc.setAttr((mainLegPlacer[0] + '.' + (side + 'hockJoint')), allLegDummyJoints[numJoints - 2], type='string')
    pc.addAttr(mainLegPlacer[0], ln=(side + 'ankleJoint'), dt='string')
    pc.setAttr((mainLegPlacer[0] + '.' + (side + 'ankleJoint')), ankleDummyJoint[0], type='string')
    pc.addAttr(mainLegPlacer[0], ln=(side + 'ballJoint'), dt='string')
    pc.setAttr((mainLegPlacer[0] + '.' + (side + 'ballJoint')), ballDummyJoint[0], type='string')
    pc.select(cl=True)

    # add dummy twist joints
    for i in range(0, len(allLegDummyJoints)):
        if i > 0:
            dU.add_dummy_twist_joints_attr(mainLegPlacer[0], allLegDummyJoints[i - 1], allLegDummyJoints[i], 2)
    dU.add_dummy_twist_joints_attr(mainLegPlacer[0], allLegDummyJoints[len(allLegDummyJoints) - 1], ankleDummyJoint[0],
                                   2)
    dU.add_dummy_twist_joints_attr(mainLegPlacer[0], ankleDummyJoint[0], ballDummyJoint[0], 0)
