import pymel.core as pc

# from ..Utils.CharUtilsLib import charLib.lockAndHide

from ..Utils import CurveUtilLib as cuLib
from ..Utils import CharUtilsLib as charLib
from ..Utils import List
import ModuleSymmetryLib as modSymLib


def createDummyBone(name, side, startDummyJoint, endDummyJoint):
    # creating parent grp
    boneCrvGrp = (side + name + 'BoneCurves_grp')

    # some error checking
    if not pc.objExists(boneCrvGrp):
        boneCrvGrp = pc.group(em=True, n=(side + name + 'BoneCurves_grp'))

    startDummySp = pc.getAttr(startDummyJoint + '.startPos')
    startDummyEp = pc.getAttr(startDummyJoint + '.endPos')
    endDummySp = pc.getAttr(endDummyJoint + '.startPos')
    endDummyEp = pc.getAttr(endDummyJoint + '.endPos')

    temp = []
    shape = []

    temp = charLib.createDistance(startDummySp, startDummyEp)
    shape = pc.listRelatives(temp[0], s=True)

    startSphereRad = pc.getAttr(shape[0] + '.distance')
    pc.delete(temp)

    temp = charLib.createDistance(endDummySp, endDummyEp)
    shape = pc.listRelatives(temp[0], s=True)

    endSphereRad = pc.getAttr(shape[0] + '.distance')
    pc.delete(temp)

    # creating dummy bone rig
    pc.select(startDummyJoint, r=True)
    startLoc1 = cuLib.curveControl('loc', 'curve')
    startLoc1[0] = pc.rename(startLoc1[0], startDummyJoint + 'Aim_loc#')
    startLoc2 = cuLib.curveControl('loc', 'curve')
    startLoc2[0] = pc.rename(startLoc2[0], startDummyJoint + 'AimPos_loc#')
    pc.parent(startLoc2[0], startLoc1[0])
    pc.setAttr((startLoc2[0] + '.tx'), startSphereRad)
    pc.parent(startLoc1[0], startDummyJoint)

    pc.select(endDummyJoint, r=True)
    endLoc1 = cuLib.curveControl('loc', 'curve')
    endLoc1[0] = pc.rename(endLoc1[0], endDummyJoint + 'Aim_loc#')
    endLoc2 = cuLib.curveControl('loc', 'curve')
    endLoc2[0] = pc.rename(endLoc2[0], endDummyJoint + 'AimPos_loc#')
    pc.parent(endLoc2[0], endLoc1[0])
    pc.setAttr((endLoc2[0] + '.tx'), (-endSphereRad))
    pc.parent(endLoc1[0], endDummyJoint)

    pc.aimConstraint(endDummyJoint, startLoc1[0], offset=[0, 0, 0], weight=1, aimVector=[1, 0, 0], upVector=[0, 1, 0],
                     worldUpType='vector', worldUpVector=[0, 1, 0])
    pc.aimConstraint(startDummyJoint, endLoc1[0], offset=[0, 0, 0], weight=1, aimVector=[-1, 0, 0], upVector=[0, 1, 0],
                     worldUpType='vector', worldUpVector=[0, 1, 0])

    pc.select(cl=True)
    connect = cuLib.curveControl('cone', 'curve')
    connect[0] = pc.rename(connect[0], startDummyJoint + 'Bone_crv#')
    pc.select((connect[0] + '.cv[0:1]'), (connect[0] + '.cv[3:4]'), (connect[0] + '.cv[6:7]'),
              (connect[0] + '.cv[9:10]'), (connect[0] + '.cv[12:13]'), (connect[0] + '.cv[15:16]'), r=True)
    posAClts = pc.cluster()
    pc.select(cl=True)
    pc.select((connect[0] + '.cv[2]'), (connect[0] + '.cv[5]'), (connect[0] + '.cv[8]'), (connect[0] + '.cv[11]'),
              (connect[0] + '.cv[14]'), r=True)
    posBClts = pc.cluster()
    pc.select(cl=True)
    pc.setAttr((connect[0] + '.overrideEnabled'), 1)
    pc.setAttr((connect[0] + '.overrideDisplayType'), 2)

    pc.pointConstraint(startLoc2[0], posAClts[1], offset=[0, 0, 0], weight=1)
    pc.parent(posAClts[1], startLoc1[0])
    boneScale = pc.getAttr(startDummyJoint + '.s')
    pc.setAttr((posAClts[1] + '.r'), (0, 0, 0))
    pc.setAttr((posAClts[1] + '.s'), (boneScale[0], boneScale[1], boneScale[2]))

    pc.pointConstraint(endLoc2[0], posBClts[1], offset=[0, 0, 0], weight=1)
    pc.parent(posBClts[1], endLoc1[0])
    pc.hide(startLoc1[0], endLoc1[0])

    charLib.lockAndHide(startLoc1[0], 'lock', 'trans rot scale vis')
    charLib.lockAndHide(endLoc1[0], 'lock', 'trans rot scale vis')
    pc.parent(connect[0], boneCrvGrp)
    return boneCrvGrp


def createDummyJoint(colorIndex):
    # TODO: change dummy shapes here
    impSphere = pc.createNode('implicitSphere')
    pc.setAttr((impSphere + '.rd'), 0.7)
    parent = pc.listRelatives(impSphere, p=True)
    sph = pc.sphere(p=[0, 0, 0], ax=[0, 1, 0], ssw=0, esw=360, r=0.6, d=3, ut=0, tol=0.01, s=8, nsp=4, ch=1)
    sphShape = pc.listRelatives(sph[0], s=True)

    distanation = pc.listConnections(sphShape[0], s=1, p=1)
    source = pc.listConnections(distanation[0], s=1, p=1)
    pc.disconnectAttr(source[0], distanation[0])

    shapeColorOverride(sph[0], colorIndex)
    pc.parent(sphShape[0], parent[0], r=True, s=True)
    cuLib.shapeRename(parent[0])

    startDis = cuLib.curveControl('loc', 'curve')
    startDis[0] = pc.rename(startDis[0], parent[0] + 'Sp_loc#')

    endDis = cuLib.curveControl('loc', 'curve')
    endDis[0] = pc.rename(endDis[0], parent[0] + 'Ep_loc#')

    pc.parent(endDis[0], startDis[0])
    pc.setAttr((endDis[0] + '.tx'), 0.7)
    pc.parent(startDis[0], parent[0])
    pc.hide(startDis[0], endDis[0])

    charLib.lockAndHide(startDis[0], 'lock', 'trans rot scale vis')
    charLib.lockAndHide(endDis[0], 'lock', 'trans rot scale vis')

    pc.addAttr(parent[0], ln='startPos', dt='string')
    pc.addAttr(parent[0], ln='endPos', dt='string')

    pc.setAttr((parent[0] + '.startPos'), startDis[0], type='string')
    pc.setAttr((parent[0] + '.endPos'), endDis[0], type='string')

    pc.delete(sph[0])
    return parent


def shapeColorOverride(n, colorIndex):
    # color index
    # 6 = blue
    # 13 = red
    # 14 = green
    # 17 = yellow
    # int colorIndex = 17;

    sel = []
    shape = []

    if n == '':
        sel = pc.ls(sl=True)
    else:
        sel.append(n)

    for s in sel:
        shape = pc.listRelatives(s, f=True, s=True)
        for x in shape:
            pc.setAttr((x + '.overrideEnabled'), 1)
            pc.setAttr((x + '.overrideColor'), colorIndex)


# string name = '';
# string side = '';
# string fingerName = 'index';
# int numCon = 5;
# string axis = 'x';
# float val = 5;
# int colorIndex = 3;
# fingerSegmentDummyBoneCreator(name, side, numCon, axis, dis, colorIndex)

def fingerSegmentDummyBoneCreator(name, fingerName, side, numCon, axis, val, colorIndex):
    tentacleDummyJnt = []
    control = []
    list = ''
    dummyBoneGrp = ''
    lock = ''
    pos = val
    tentMainPos = cuLib.curveControl('cube1', 'curve')
    tentMainPos[0] = pc.rename(tentMainPos[0], name + side + fingerName + 'Main_ctrl')
    shapeColorOverride(tentMainPos[0], colorIndex)
    cuLib.resizeCurves(None, 1, 1, 1, 1.5)
    # module tags
    pc.addAttr(tentMainPos[0], ln='moduleTag', dt='string')
    pc.addAttr(tentMainPos[0], ln='buildTag', dt='string')
    pc.addAttr(tentMainPos[0], ln='jointPosList', dt='string')

    pc.setAttr((tentMainPos[0] + '.moduleTag'), 'finger', type='string')

    for i in range(numCon):
        tentacleDummyJnt = createDummyJoint(colorIndex)
        tentacleDummyJnt[0] = pc.rename(tentacleDummyJnt[0], (name + side + fingerName + str(i + 1) + '_loc'))
        control.append(tentacleDummyJnt[0])
        if i > 0:
            if axis == 'x':
                pc.move(val, 0, 0, control[i])
                lock = 'z'
            elif axis == 'y':
                pc.move(0, val, 0, control[i])
                lock = 'x'
            elif axis == 'z':
                pc.move(0, 0, val, control[i])
                lock = 'x'
            dummyBoneGrp = createDummyBone(fingerName, side, control[i - 1], control[i])
            val = (val + pos)

        pc.parent(tentacleDummyJnt, tentMainPos[0])
        list = list + (tentacleDummyJnt[0] + ' ')

    for x in range(numCon):
        pc.setAttr((control[x] + '.t' + lock), lock=True)

    pc.setAttr((dummyBoneGrp + '.inheritsTransform'), 0)
    pc.parent(dummyBoneGrp, tentMainPos[0], r=True)
    pc.setAttr((tentMainPos[0] + '.jointPosList'), list, type='string')
    # select -r control;
    # scale -r 0.5 0.5 0.5;
    return tentMainPos[0]


# string name = '';
# string side = '';
# string moduleName = 'spine';
# int numCon = 4;
# string axis = 'y';
# float dis = 15;
# int colorIndex = 3;
# linearDisDummyBoneCreator(name, side, numCon, axis, dis, colorIndex)

def linearDisDummyBoneCreator(name, side, moduleName, numCon, axis, dis, colorIndex):
    tentacleDummyJnt = []
    control = []
    list = ''
    dummyBoneGrp = ''
    lock = ''
    split = dis / (numCon - 1)
    pos = 0
    tentMainPos = cuLib.curveControl('cube1', 'curve')
    tentMainPos[0] = pc.rename(tentMainPos[0], name + side + moduleName + 'Main_ctrl')
    shapeColorOverride(tentMainPos[0], colorIndex)
    cuLib.resizeCurves(None, 1, 1, 1, 1.5)
    pc.addAttr(tentMainPos[0], ln='jointPosList', dt='string')
    pc.select(cl=True)

    for i in range(numCon):
        tentacleDummyJnt = createDummyJoint(colorIndex)
        tentacleDummyJnt[0] = pc.rename(tentacleDummyJnt[0], (name + side + moduleName + str(i + 1) + '_loc'))
        control.append(tentacleDummyJnt[0])
        pc.scale(tentacleDummyJnt[0], (0.7, 0.7, 0.7))
        if i > 0:
            if axis == 'x':
                pc.move(pos, 0, 0, control[i])
                lock = 'z'
            elif axis == 'y':
                pc.move(0, pos, 0, control[i])
                lock = 'x'
            elif axis == 'z':
                pc.move(0, 0, pos, control[i])
                lock = 'x'
            dummyBoneGrp = createDummyBone(moduleName, side, control[i - 1], control[i])
        pos = (pos + split)
        pc.parent(tentacleDummyJnt, tentMainPos[0])
        list = list + (tentacleDummyJnt[0] + ' ')
        pc.select(cl=True)

    for x in range(numCon):
        pc.setAttr((control[x] + '.t' + lock), lock=True)

    pc.setAttr((dummyBoneGrp + '.inheritsTransform'), 0)
    pc.parent(dummyBoneGrp, tentMainPos[0], r=True)
    pc.setAttr((tentMainPos[0] + '.jointPosList'), list, type='string')
    pc.select(cl=True)
    return tentMainPos[0]


def getDummyBoneLimbPos(curve, numJoints):
    dummyJointPos = []

    curveInfo = pc.pointOnCurve(curve, constructionHistory=1)
    pc.setAttr((curveInfo + '.turnOnPercentage'), 1)

    i = 0
    for i in range(numJoints):
        parameter = i * (1.0 / (numJoints - 1))
        pc.setAttr((curveInfo + '.parameter'), parameter)
        tempJointPos = pc.getAttr(curveInfo + '.position')
        dummyJointPos.append(tempJointPos)

    pc.delete(curveInfo)
    return dummyJointPos


# string name = '';
# string side = '';
# int numJoints = 3;
# int fingers = 1;
# int numFingers = 5;
# int numSegment = 4;
# int colorIndex = 3;
# buildArmDummySkeletonModule (name, side, numJoints, fingers, numFingers, numSegment, colorIndex)

def buildArmDummySkeletonModule(name, side, numJoints, fingers, numFingers, numSegment, colorIndex):
    list = ''
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

    list = list + (clavDummyJoint[0] + ' ')
    for n in range(len(allArmDummyJoints)):
        list = list + (allArmDummyJoints[n] + ' ')
        pc.setAttr((allArmDummyJoints[n] + '.ty'), lock=True)

    list = list + (wristDummyJoint[0] + ' ' + wristEndDummyJoint[0])
    pc.setAttr((mainArmPlacer[0] + '.jointPosList'), list, type='string')

    pc.parent(allArmDummyJoints, mainArmPlacer[0])
    pc.parent(mainWristPlacer[0], mainArmPlacer[0])
    pc.setAttr((wristDummyJoint[0] + '.ty'), lock=True)
    pc.setAttr((wristEndDummyJoint[0] + '.ty'), lock=True)
    pc.setAttr((wristEndDummyJoint[0] + '.tz'), lock=True)
    pc.setAttr((mainWristPlacer[0] + '.ty'), lock=True)

    pc.select(clavDummyJoint[0], allArmDummyJoints, wristDummyJoint[0], wristEndDummyJoint[0], r=True)
    pc.scale((0.7, 0.7, 0.7))
    pc.select(cl=True)

    if fingers:
        # declaring position for fingers
        fingerlist = ''

        fingerPos = [(17.7, -0.35, 1), (18.3, 0.15, 0.9), (18.2, 0.3, 0.1), (18.15, 0.15, -0.5), (18.1, 0, -1)]
        fingerRot = [(85, -35, -30), (0, -3, 0), (0, 0, 0), (0, 5, 0), (0, 10.25, 0)]
        scale = [0.35, 0.35, 0.4, 0.35, 0.3]
        fingerNames = ['thumb', 'index', 'middle', 'ring', 'pinky']

        pc.select(cl=True)
        for j in range(numFingers):
            if j == 0:  # idea here is that thumb joints will have one less segment compare to other fingers
                finger = fingerSegmentDummyBoneCreator(name, fingerNames[j], side, numSegment, 'x', 3, colorIndex)
            else:
                finger = fingerSegmentDummyBoneCreator(name, fingerNames[j], side, (numSegment + 1), 'x', 3, colorIndex)

            fingerlist = fingerlist + (finger + ' ')

            position = fingerPos[j]
            pc.move(position[0], position[1], position[2], finger)

            rotation = fingerRot[j]
            pc.rotate(finger, rotation[0], rotation[1],
                      rotation[2])  # NOTE: for some reason pymel rotate does not follow the pattern that move does

            modSymLib.connectModuleComponants(wristDummyJoint[0], finger)

            pc.scale(finger, (scale[j], scale[j], scale[j]))

            pc.parent(finger, mainWristPlacer[0])

            pc.setAttr((finger + '.buildTag'), mainArmPlacer[0], type='string')

            pc.select(cl=True)

        pc.addAttr(mainArmPlacer[0], ln='child', dt='string')
        pc.setAttr((mainArmPlacer[0] + '.child'), fingerlist, type='string')

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


# string name = '';
# string side = '';
# int numJoints = 3;
# int fingers = 1;
# int numFingers = 5;
# int numSegment = 4;
# int colorIndex = 3;
# buildBipedLegDummySkeletonModule (name, side, numJoints, fingers, numFingers, numSegment, colorIndex)

def buildBipedLegDummySkeletonModule(name, side, numJoints, fingers, numFingers, numSegment, colorIndex):
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
    pc.scale((0.7, 0.7, 0.7))
    pc.select(cl=True)

    if fingers:
        # declaring position for fingers
        pc.addAttr(mainLegPlacer[0], ln='child', dt='string')
        fingerJointList = ''
        fingerPos = [(1, 0, 2), (1.7, 0, 2), (2.4, 0, 2), (3.1, 0, 2), (3.8, 0, 2)]
        scale = [0.35, 0.32, 0.30, 0.27, 0.25]
        fingerName = ['bigToe', 'indexToe', 'midToe', 'ringToe', 'pinkyToe']

        for i in range(numFingers):
            finger = fingerSegmentDummyBoneCreator(name, fingerName[i], side, numSegment, 'z', 2, colorIndex)
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


# string name = '';
# string side = '';
# int numJoints = 3;
# int fingers = 1;
# int numFingers = 5;
# int numSegment = 4;
# int colorIndex = 3;
# buildQuadLegDummySkeletonModule(name, side, numJoints, fingers, numFingers, numSegment, colorIndex);

def buildQuadLegDummySkeletonModule(name, side, numJoints, fingers, numFingers, numSegment, colorIndex):
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
    pc.scale((0.7, 0.7, 0.7))
    pc.select(cl=True)

    if fingers:
        # declaring position for fingers
        pc.addAttr(mainLegPlacer[0], ln='child', dt='string')
        fingerJointList = ''
        fingerPos = [(1, 0, 1.5), (1.7, 0, 1.5), (2.4, 0, 1.5), (3.1, 0, 1.5), (3.8, 0, 1.5)]
        scale = [0.35, 0.385, 0.385, 0.35, 0.35]
        fingerName = ['bigToe', 'indexToe', 'midToe', 'ringToe', 'pinkyToe']

        for i in range(numFingers):
            finger = fingerSegmentDummyBoneCreator(name, fingerName[i], side, numSegment, 'z', 2, colorIndex)
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


# string name = '';
# string side = 'l_';
# string moduleName = 'spine';
# int numCon = 4;
# string axis = 'y';
# float dis = 15;
# int colorIndex = 3;

# buildSpineDummySkeletonModule(name, side, moduleName, numCon, axis, dis, colorIndex);

# TODO: continue
def buildSpineDummySkeletonModule(name, side, moduleName, numCon, axis, dis, colorIndex):
    lock = ''
    dummyBoneGrp = ''
    jointPosList = ''
    jointPosLists = []
    # create spineModule
    spinePalcer = linearDisDummyBoneCreator(name, side, moduleName, numCon, axis, dis, colorIndex)
    createModuleAnnotation((name + side + moduleName), spinePalcer)
    chest = createModuleAnnotation((name + side + 'chest'), (name + side + moduleName + str(numCon) + '_loc'))
    pc.setAttr((chest + '.t'), (0, 0, 0))

    # negate pos value in order to get hips position opposite to the spine joint
    pos = (dis / dis) * -1

    hipsDummyJnt = createDummyJoint(colorIndex)
    hipsDummyJnt[0] = pc.rename(hipsDummyJnt[0], (name + side + moduleName + 'Hips_loc'))
    pc.scale(hipsDummyJnt[0], (0.7, 0.7, 0.7))
    pc.addAttr(hipsDummyJnt[0], ln='jointPosList', dt='string')
    pc.setAttr((hipsDummyJnt[0] + '.jointPosList'), hipsDummyJnt[0], type='string')
    hips = createModuleAnnotation((name + side + 'hips'), hipsDummyJnt[0])
    pc.setAttr((hips + '.t'), (0, -1, 0))

    pc.parent(hipsDummyJnt[0], spinePalcer)

    jointPosList = pc.getAttr(spinePalcer + '.jointPosList')
    jointPosLists = List.seperate(jointPosList)
    dummyBoneGrp = createDummyBone(side, moduleName, jointPosLists[0], hipsDummyJnt[0]);

    pc.addAttr(hipsDummyJnt[0], ln='parent', dt='string')
    pc.setAttr((hipsDummyJnt[0] + '.parent'), jointPosLists[0], type='string')

    pc.addAttr(spinePalcer, ln='child', dt='string')
    pc.setAttr((spinePalcer + '.child'), hipsDummyJnt[0], type='string')

    if axis == 'x':
        pc.move(pos, 0, 0, hipsDummyJnt[0])
        lock = 'z'
    elif axis == 'y':
        pc.move(0, pos, 0, hipsDummyJnt[0])
        lock = 'x'
    elif axis == 'z':
        pc.move(0, 0, pos, hipsDummyJnt[0])
        lock = 'x'

    pc.setAttr((hipsDummyJnt[0] + '.t' + lock), lock=True)

    pc.setAttr((dummyBoneGrp + '.inheritsTransform'), 0)
    try:
        pc.parent(dummyBoneGrp, spinePalcer, r=True)
    except:
        pass
    pc.select(cl=True)

    # create world pos loc and parent main arm placer ctrl...
    worldPosLoc = buildWorldPosLoc(name)
    if not pc.attributeQuery('spine', n=worldPosLoc, ex=True):
        pc.addAttr(worldPosLoc, ln='spine', dt='string')

    moduleParts = pc.getAttr(worldPosLoc + '.' + 'spine')
    pc.setAttr((worldPosLoc + '.' + 'spine'), (str(moduleParts or '') + ' ' + spinePalcer), type='string')

    pc.parent(spinePalcer, worldPosLoc)

    # module tags
    pc.addAttr(spinePalcer, ln='moduleTag', dt='string')
    pc.addAttr(spinePalcer, ln='buildTag', dt='string')

    pc.setAttr((spinePalcer + '.moduleTag'), 'spine', type='string')
    pc.setAttr((spinePalcer + '.buildTag'), worldPosLoc, type='string')

    # rig info Attr
    spineList = pc.getAttr(spinePalcer + '.jointPosList')
    spineJointsList = List.seperate(spineList)
    size = len(spineJointsList)

    pc.addAttr(spinePalcer, ln='name', dt='string')
    pc.setAttr((spinePalcer + '.name'), name, type='string')
    pc.addAttr(spinePalcer, ln='side', dt='string')
    pc.setAttr((spinePalcer + '.side'), side, type='string')
    pc.addAttr(spinePalcer, ln=(side + 'rootJoint'), dt='string')
    pc.setAttr((spinePalcer + '.' + (side + 'rootJoint')), spineJointsList[0], type='string')
    pc.addAttr(spinePalcer, ln=(side + 'chestJoint'), dt='string')
    pc.setAttr((spinePalcer + '.' + (side + 'chestJoint')), spineJointsList[size - 1], type='string')
    pc.addAttr(spinePalcer, ln=(side + 'hipJoint'), dt='string')
    pc.setAttr((spinePalcer + '.' + (side + 'hipJoint')), hipsDummyJnt[0], type='string')

    pc.select(cl=True)


# string name = '';
# string side = '';
# string moduleName = 'head';
# int colorIndex = 3;
# buildHeadDummySkeletonModule(name, side, moduleName, colorIndex)

def buildHeadDummySkeletonModule(name, side, moduleName, colorIndex):
    dummyBoneGrp = ''
    jointPosList = ''
    jointPosLists = []

    headPalcer = linearDisDummyBoneCreator(name, side, moduleName, 2, 'y', 7, colorIndex)

    # create head annotation
    head = createModuleAnnotation((name + side + moduleName), headPalcer)

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
    pc.parent(lEyeDummyJnt[0], rEyeDummyJnt[0], headPalcer)

    pc.addAttr(headPalcer, ln='child', dt='string')
    pc.setAttr((headPalcer + '.child'), (lEyeDummyJnt[0] + ' ' + rEyeDummyJnt[0]), type='string')
    pc.addAttr(headPalcer, ln='side', dt='string')
    pc.setAttr((headPalcer + '.side'), side, type='string')

    jointPosList = pc.getAttr(headPalcer + '.jointPosList')
    jointPosLists = List.seperate(jointPosList)
    dummyBoneGrp = createDummyBone(side, moduleName, jointPosLists[0], lEyeDummyJnt[0])
    dummyBoneGrp = createDummyBone(side, moduleName, jointPosLists[0], rEyeDummyJnt[0])

    pc.addAttr(lEyeDummyJnt[0], ln='parent', dt='string')
    pc.setAttr((lEyeDummyJnt[0] + '.parent'), jointPosLists[0], type='string')
    pc.addAttr(rEyeDummyJnt[0], ln='parent', dt='string')
    pc.setAttr((rEyeDummyJnt[0] + '.parent'), jointPosLists[0], type='string')

    pc.setAttr((dummyBoneGrp + '.inheritsTransform'), 0)
    try:
        pc.parent(dummyBoneGrp, headPalcer, r=True)
    except:
        pass
    pc.select(cl=True)

    ##create world pos loc and parent main arm placer ctrl...
    # string worldPosLoc[] = buildWorldPosLoc(name);
    # if(!`attributeExists 'head' worldPosLoc[0]`)
    # addAttr -ln 'head'  -dt 'string' worldPosLoc[0];

    # string moduleParts = `getAttr (worldPosLoc[0] + '.' +'head')`;
    # setAttr -type 'string' (worldPosLoc[0] + '.' +'head') (moduleParts+' '+headPalcer);

    # parent headPalcer worldPosLoc[0];

    ##module tags
    # addAttr -ln 'moduleTag' -dt 'string' headPalcer;
    # addAttr -ln 'buildTag' -dt 'string' headPalcer;

    # setAttr -type 'string' (headPalcer + '.moduleTag') 'head';
    # setAttr -type 'string' (headPalcer + '.buildTag') worldPosLoc[0];

    pc.select(cl=True)


# string name = '';
# string side = '';
# string moduleName = 'neck1';
# int numCon = 2;
# string axis = 'y';
# float dis = 3;
# int colorIndex = 3;
# buildNeckDummySkeletonModule(name, side, moduleName, numCon, axis, dis, colorIndex);

def buildNeckDummySkeletonModule(name, side, moduleName, numCon, axis, dis, colorIndex):
    neckPlacer = ''

    if numCon > 1:
        neckPlacer = linearDisDummyBoneCreator(name, side, moduleName, numCon, axis, dis, colorIndex)
    else:
        mainNeckPlacer = cuLib.curveControl('cube1', 'curve')
        mainNeckPlacer[0] = pc.rename(mainNeckPlacer[0], name + side + moduleName + 'Main_ctrl')
        shapeColorOverride(mainNeckPlacer[0], colorIndex)
        cuLib.resizeCurves(None, 1, 1, 1, 1.5)
        pc.addAttr(mainNeckPlacer[0], ln='jointPosList', dt='string')

        neckDummyJoint = createDummyJoint(colorIndex)
        neckDummyJoint[0] = pc.rename(neckDummyJoint[0], (name + side + 'neck_loc'))
        pc.scale(neckDummyJoint[0], (0.7, 0.7, 0.7))

        pc.parent(neckDummyJoint[0], mainNeckPlacer[0])

        pc.setAttr((mainNeckPlacer[0] + '.jointPosList'), neckDummyJoint[0], type='string')
        neckPlacer = mainNeckPlacer[0]

    # create neck annotation
    neck = createModuleAnnotation((name + side + moduleName), neckPlacer)

    ##create world pos loc and parent main arm placer ctrl...
    # string worldPosLoc[] = buildWorldPosLoc(name);
    # if(!`attributeExists 'neck' worldPosLoc[0]`)
    #	addAttr -ln 'neck'  -dt 'string' worldPosLoc[0];

    # string moduleParts = `getAttr (worldPosLoc[0] + '.' +'neck')`;
    # setAttr -type 'string' (worldPosLoc[0] + '.' +'neck') (moduleParts+' '+neckPlacer);

    # parent neckPlacer worldPosLoc[0];

    ##module tags
    # addAttr -ln 'moduleTag' -dt 'string' neckPlacer;
    # addAttr -ln 'buildTag' -dt 'string' neckPlacer;

    # setAttr -type 'string' (neckPlacer + '.moduleTag') 'neck';
    # setAttr -type 'string' (neckPlacer + '.buildTag') worldPosLoc[0];

    pc.select(cl=True)


# string name = '';
# string side = '';
# string moduleName = 'neck';
# int numCon = 1;
# string axis = 'y';
# float dis = 3;
# int colorIndex = 3;
# buildHeadNeckDummySkeletonModule(name, side, moduleName, numCon, axis, dis, colorIndex);

def buildHeadNeckDummySkeletonModule(name, side, moduleName, numCon, axis, dis, colorIndex):
    buildNeckDummySkeletonModule(name, side, moduleName, numCon, axis, dis, colorIndex)
    buildHeadDummySkeletonModule(name, side, 'head', colorIndex)

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

    if numCon > 1:
        size = len(neckJointList)
        modSymLib.connectModuleComponants(neckJointList[size - 1], headPlacer)
        headPos = (dis / (numCon - 1))
        pc.move(0, (dis + headPos), 0, headPlacer)
    else:
        modSymLib.connectModuleComponants(neckJointList[0], headPlacer)
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


# string name = '';
# string side = '';
# string moduleName = 'tail';
# int numCon = 2;
# string axis = 'y';
# float dis = 3;
# int colorIndex = 3;
# buildTentacleDummySkeletonModule(name, side, moduleName, numCon, axis, dis, colorIndex);

def buildTentacleDummySkeletonModule(name, side, moduleName, numCon, axis, dis, colorIndex):
    tentaclePlacer = linearDisDummyBoneCreator(name, side, moduleName, numCon, axis, dis, colorIndex)

    # create tentacle annotation
    tentacle = createModuleAnnotation((name + side + moduleName), tentaclePlacer)
    pc.setAttr((tentacle + '.t'), (0, 1, 0))

    # create world pos loc and parent main arm placer ctrl...
    worldPosLoc = buildWorldPosLoc(name)
    if not pc.attributeQuery('tentacle', n=worldPosLoc, ex=True):
        pc.addAttr(worldPosLoc, ln='tentacle', dt='string')

    moduleParts = pc.getAttr(worldPosLoc + '.' + 'tentacle')
    pc.setAttr((worldPosLoc + '.' + 'tentacle'), (str(moduleParts or '') + ' ' + tentaclePlacer), type='string')

    pc.parent(tentaclePlacer, worldPosLoc)

    # module tags
    pc.addAttr(tentaclePlacer, ln='moduleTag', dt='string')
    pc.addAttr(tentaclePlacer, ln='buildTag', dt='string')

    pc.setAttr((tentaclePlacer + '.moduleTag'), 'tentacle', type='string')
    pc.setAttr((tentaclePlacer + '.buildTag'), worldPosLoc, type='string')

    # rig info Attr
    tentacleList = pc.getAttr(tentaclePlacer + '.jointPosList')
    tentacleJointsList = List.seperate(tentacleList)
    size = len(tentacleJointsList)

    pc.addAttr(tentaclePlacer, ln='name', dt='string')
    pc.setAttr((tentaclePlacer + '.name'), name, type='string')
    pc.addAttr(tentaclePlacer, ln='side', dt='string')
    pc.setAttr((tentaclePlacer + '.side'), side, type='string')
    pc.addAttr(tentaclePlacer, ln=(side + 'startJoint'), dt='string')
    pc.setAttr((tentaclePlacer + '.' + (side + 'startJoint')), tentacleJointsList[0], type='string')
    pc.addAttr(tentaclePlacer, ln=(side + 'endJoint'), dt='string')
    pc.setAttr((tentaclePlacer + '.' + (side + 'endJoint')), tentacleJointsList[size - 1], type='string')
    pc.addAttr(tentaclePlacer, ln=(side + 'types'), dt='string')
    pc.setAttr((tentaclePlacer + '.' + (side + 'types')), moduleName, type='string')

    pc.select(cl=True)


# This proc will create world pos loc for position dummy modules
def buildWorldPosLoc(name):
    worldPosLoc = (name + 'worldPos_loc')

    if not pc.objExists(worldPosLoc):
        worldPosLoc = pc.spaceLocator(p=(0, 0, 0), n=(name + 'worldPos_loc'))
        pc.setAttr((worldPosLoc + 'Shape.localScaleX'), 7)
        pc.setAttr((worldPosLoc + 'Shape.localScaleY'), 7)
        pc.setAttr((worldPosLoc + 'Shape.localScaleZ'), 7)
    return worldPosLoc


def createModuleAnnotation(name, obj):
    annotation = pc.annotate(obj, tx=name, p=(0, 0, 0))
    pc.setAttr((annotation + '.displayArrow'), 0)
    pc.setAttr((annotation + '.overrideEnabled'), 1)
    pc.setAttr((annotation + '.overrideDisplayType'), 2)

    annotationShape = pc.listRelatives(annotation, p=True)
    annotationShape[0] = pc.rename(annotationShape[0], (name + '_annotate'))
    pc.parent(annotationShape[0], obj)

    return annotationShape[0]