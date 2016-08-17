import pymel.core as pc
from RiggingSystem.Utils import CurveUtilLib as cuLib
from RiggingSystem.Utils import CharUtilsLib as charLib

def createDummyBone(name, side, startDummyJoint, endDummyJoint):

    # creating parent grp
    boneCrvGrp = (side+name+'BoneCurves_grp')

    # some error checking
    if not pc.objExists(boneCrvGrp):
        boneCrvGrp = pc.group(em=True, n=(side+name+'BoneCurves_grp'))

    startDummySp = pc.getAttr(startDummyJoint+'.startPos')
    startDummyEp = pc.getAttr (startDummyJoint+'.endPos')
    endDummySp = pc.getAttr(endDummyJoint+'.startPos')
    endDummyEp = pc.getAttr(endDummyJoint+'.endPos')

    temp = []
    shape = []

    temp = charLib.createDistance(startDummySp, startDummyEp)
    shape = pc.listRelatives(temp[0], s=True)

    startSphereRad = pc.getAttr(shape[0]+'.distance')
    pc.delete(temp)

    temp = charLib.createDistance(endDummySp, endDummyEp)
    shape = pc.listRelatives(temp[0], s=True)

    endSphereRad = pc.getAttr(shape[0]+'.distance')
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

    pc.aimConstraint(endDummyJoint, startLoc1[0], offset=[0, 0, 0], weight=1, aimVector=[1, 0, 0], upVector=[0, 1, 0], worldUpType='vector', worldUpVector=[0, 1, 0])
    pc.aimConstraint(startDummyJoint, endLoc1[0], offset=[0, 0, 0], weight=1, aimVector=[-1, 0, 0], upVector=[0, 1, 0], worldUpType='vector', worldUpVector=[0, 1, 0])

    pc.select(cl=True)
    connect = cuLib.curveControl('cone', 'curve')
    connect[0] = pc.rename(connect[0], startDummyJoint + 'Bone_crv#')
    pc.select((connect[0] + '.cv[0:1]'), (connect[0] + '.cv[3:4]'), (connect[0] + '.cv[6:7]'), (connect[0] + '.cv[9:10]'), (connect[0] + '.cv[12:13]'), (connect[0] + '.cv[15:16]'), r=True)
    posAClts = pc.cluster()
    pc.select(cl=True)
    pc.select((connect[0] + '.cv[2]'), (connect[0] + '.cv[5]'), (connect[0] + '.cv[8]'), (connect[0] + '.cv[11]'), (connect[0] + '.cv[14]'), r=True)
    posBClts = pc.cluster()
    pc.select(cl=True)
    pc.setAttr((connect[0] + '.overrideEnabled'), 1)
    pc.setAttr((connect[0] + '.overrideDisplayType'), 2)

    pc.pointConstraint(startLoc2[0], posAClts[1], offset=[0, 0, 0], weight=1)
    pc.parent(posAClts[1], startLoc1[0])

    pc.setAttr((posAClts[1] + '.r'), (0, 0, 0))
    pc.setAttr((posAClts[1] + '.s'), (1, 1, 1))

    pc.pointConstraint(endLoc2[0], posBClts[1], offset=[0, 0, 0], weight=1)
    pc.parent(posBClts[1], endLoc1[0])
    pc.hide(startLoc1[0], endLoc1[0])

    charLib.lockAndHide(startLoc1[0], 'lock', 'trans rot scale vis')
    charLib.lockAndHide(endLoc1[0], 'lock', 'trans rot scale vis')
    pc.parent(connect[0], boneCrvGrp)
    return boneCrvGrp

def createDummyJoint(colorIndex):
    impSphere = pc.createNode('implicitSphere')
    pc.setAttr((impSphere + '.rd'), 0.5)

    parent = pc.listRelatives(impSphere, p=True)

    shapeColorOverride(parent, colorIndex)
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
        pc.scale(tentacleDummyJnt[0], (1, 1, 1))
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

# TODO: should be moved into a global util
#This method will create world pos loc for position dummy modules
def buildWorldPosLoc(name):
    worldPosLoc = (name + 'worldPos_loc')

    if not pc.objExists(worldPosLoc):
        worldPosLoc = pc.spaceLocator(p=(0, 0, 0), n=(name + 'worldPos_loc'))
        pc.setAttr((worldPosLoc+'Shape.localScaleX'), 7)
        pc.setAttr((worldPosLoc+'Shape.localScaleY'), 7)
        pc.setAttr((worldPosLoc+'Shape.localScaleZ'), 7)
    return worldPosLoc

def createModuleAnnotation(name, obj):
    annotation = pc.annotate(obj, tx=name, p=(0, 0, 0))
    pc.setAttr((annotation + '.displayArrow'), 0)
    pc.setAttr((annotation + '.overrideEnabled'), 1)
    pc.setAttr((annotation + '.overrideDisplayType'), 2)

    annotationShape = pc.listRelatives(annotation,p=True)
    annotationShape[0] = pc.rename(annotationShape[0], (name+'_annotate'))
    pc.parent(annotationShape[0], obj)

    return annotationShape[0]