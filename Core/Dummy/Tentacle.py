import pymel.core as pc
from Util import *
from Maya_Rigging.Utils import List
from Maya_Rigging.Utils import DummyUtil as dU


def Tentacle(name, side, moduleName, numCon, axis, dis, colorIndex):
    tentaclePlacer = linearDisDummyBoneCreator(name, side, moduleName, numCon, axis, dis, colorIndex)

    # create tentacle annotation
    tentacle = createModuleAnnotation((name+side+moduleName), tentaclePlacer)
    pc.setAttr((tentacle+'.t'), (0, 1, 0))

    # create world pos loc and parent main arm placer ctrl...
    worldPosLoc = buildWorldPosLoc(name)
    if not pc.attributeQuery('tentacle', n=worldPosLoc, ex=True):
        pc.addAttr(worldPosLoc, ln='tentacle', dt='string')

    moduleParts = pc.getAttr(worldPosLoc + '.' + 'tentacle')
    pc.setAttr((worldPosLoc + '.' + 'tentacle'), (str(moduleParts or '')+' '+tentaclePlacer), type='string')

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
    pc.addAttr(tentaclePlacer, ln=(side+'startJoint'), dt='string')
    pc.setAttr((tentaclePlacer + '.' + (side+'startJoint')), tentacleJointsList[0], type='string')
    pc.addAttr(tentaclePlacer, ln=(side+'endJoint'), dt='string')
    pc.setAttr((tentaclePlacer + '.' + (side+'endJoint')), tentacleJointsList[size-1], type='string')
    pc.addAttr(tentaclePlacer, ln=(side+'types'), dt='string')
    pc.setAttr((tentaclePlacer + '.' + (side+'types')), moduleName, type='string')

    pc.select(cl=True)
    dU.add_dummy_twist_joints_attr(tentaclePlacer, tentacleJointsList[0], tentacleJointsList[size - 1], 0)
