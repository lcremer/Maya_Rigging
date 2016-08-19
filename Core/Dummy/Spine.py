import pymel.core as pc
from Util import *
from Maya_Rigging.Utils import List
from Maya_Rigging.Utils import DummyUtil as dU

def Spine(name, side, moduleName, numCon, axis, dis, colorIndex):
    print('building Spine Dummy Skeleton Module')
    lock = ''
    dummyBoneGrp = ''
    jointPosList = ''
    jointPosLists = []
    # create spineModule
    spinePlacer = linearDisDummyBoneCreator(name, side, moduleName, numCon, axis, dis, colorIndex)
    createModuleAnnotation((name+side+moduleName), spinePlacer)
    chest = createModuleAnnotation((name+side+'chest'), (name+side+moduleName+str(numCon)+'_loc'))
    pc.setAttr((chest+'.t'), (0, 0, 0))

    # negate pos value in order to get hips position opposite to the spine joint
    pos = (dis/dis)*-1

    hipsDummyJnt = createDummyJoint(colorIndex)
    hipsDummyJnt[0] = pc.rename(hipsDummyJnt[0], (name+side+moduleName+'Hips_loc'))
    # pc.scale(hipsDummyJnt[0], (0.7, 0.7, 0.7))
    pc.addAttr(hipsDummyJnt[0], ln='jointPosList', dt='string')
    pc.setAttr((hipsDummyJnt[0] + '.jointPosList'), hipsDummyJnt[0], type='string')
    hips = createModuleAnnotation((name+side+'hips'), hipsDummyJnt[0])
    pc.setAttr((hips+'.t'), (0, -1, 0))

    pc.parent(hipsDummyJnt[0], spinePlacer)

    jointPosList = pc.getAttr(spinePlacer + '.jointPosList')
    jointPosLists = List.seperate(jointPosList)
    dummyBoneGrp = createDummyBone(side, moduleName, jointPosLists[0], hipsDummyJnt[0])

    pc.addAttr(hipsDummyJnt[0], ln='parent', dt='string')
    pc.setAttr((hipsDummyJnt[0] + '.parent'), jointPosLists[0], type='string')

    pc.addAttr(spinePlacer, ln='child', dt='string')
    pc.setAttr((spinePlacer + '.child'), hipsDummyJnt[0], type='string')

    if axis == 'x' or axis == 'X':
        pc.move(pos,0,0, hipsDummyJnt[0])
        lock = 'z'
    elif axis == 'y' or axis == 'Y':
        pc.move(0,pos,0, hipsDummyJnt[0])
        lock = 'x'
    elif axis == 'z' or axis == 'Z':
        pc.move(0,0,pos, hipsDummyJnt[0])
        lock = 'x'

    pc.setAttr((hipsDummyJnt[0] + '.t' + lock), lock=True)

    pc.setAttr((dummyBoneGrp+'.inheritsTransform'), 0)
    try:
        pc.parent(dummyBoneGrp, spinePlacer, r=True)
    except:
        pass
    pc.select(cl=True)

    # create world pos loc and parent main arm placer ctrl...
    worldPosLoc = buildWorldPosLoc(name)
    if not pc.attributeQuery('spine', n=worldPosLoc, ex=True):
        pc.addAttr(worldPosLoc, ln='spine', dt='string')

    moduleParts = pc.getAttr(worldPosLoc + '.' + 'spine')
    pc.setAttr((worldPosLoc + '.' + 'spine'), (str(moduleParts or '')+' '+spinePlacer), type='string')

    pc.parent(spinePlacer, worldPosLoc)

    # module tags
    pc.addAttr(spinePlacer, ln='moduleTag', dt='string')
    pc.addAttr(spinePlacer, ln='buildTag', dt='string')

    pc.setAttr((spinePlacer + '.moduleTag'), 'spine', type='string')
    pc.setAttr((spinePlacer + '.buildTag'), worldPosLoc, type='string')

    # rig info Attr
    spineList = pc.getAttr(spinePlacer + '.jointPosList')
    spineJointsList = List.seperate(spineList)
    size = len(spineJointsList)

    pc.addAttr(spinePlacer, ln='name', dt='string')
    pc.setAttr((spinePlacer + '.name'), name, type='string')
    pc.addAttr(spinePlacer, ln='side', dt='string')
    pc.setAttr((spinePlacer + '.side'), side, type='string')
    pc.addAttr(spinePlacer, ln=(side+'rootJoint'), dt='string')
    pc.setAttr((spinePlacer + '.' + (side+'rootJoint')), spineJointsList[0], type='string')
    pc.addAttr(spinePlacer, ln=(side+'chestJoint'), dt='string')
    pc.setAttr((spinePlacer + '.' + (side+'chestJoint')), spineJointsList[size-1], type='string')
    pc.addAttr(spinePlacer, ln=(side+'hipJoint'), dt='string')
    pc.setAttr((spinePlacer + '.' + (side+'hipJoint')), hipsDummyJnt[0], type='string')
    pc.select(cl=True)

    dU.add_dummy_twist_joints_attr(spinePlacer, jointPosLists[0], spineJointsList[size-1], 7)
