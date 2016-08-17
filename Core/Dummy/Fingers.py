import pymel.core as pc
from Util import *

def createFingers(name, fingerName, side, numCon, axis, val, colorIndex):
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