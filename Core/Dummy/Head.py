from Util import *
from ...Utils import List
from ...Core import ModuleSymmetryLib as modSymLib


def build(name, side, module_name, colorIndex):
    dummyBoneGrp = ''
    jointPosList = ''
    jointPosLists = []

    headPlacer = linear_dis_dummy_bone_creator(name, side, module_name, 2, 'y', 7, colorIndex)

    # create head annotation
    head = create_module_annotation((name + side + module_name), headPlacer)

    lEyeDummyJnt = create_dummy_joint(colorIndex)
    lEyeDummyJnt[0] = pc.rename(lEyeDummyJnt[0], (name + side + 'l_' + module_name + 'Eye_loc'))
    pc.scale(lEyeDummyJnt[0], (0.7, 0.7, 0.7))
    pc.addAttr(lEyeDummyJnt[0], ln='jointPosList', dt='string')
    pc.setAttr((lEyeDummyJnt[0] + '.jointPosList'), lEyeDummyJnt[0], type='string')

    # create l_eye annotation
    lEye = create_module_annotation((name + 'l_eye'), lEyeDummyJnt[0])
    pc.setAttr((lEye + '.t'), (0, 1, 0))
    pc.rename(lEye, (name + side + module_name + 'LEye_annotate'))

    rEyeDummyJnt = create_dummy_joint(colorIndex)
    rEyeDummyJnt[0] = pc.rename(rEyeDummyJnt[0], (name + side + 'r_' + module_name + 'Eye_loc'))
    pc.scale(rEyeDummyJnt[0], (0.7, 0.7, 0.7))
    pc.addAttr(rEyeDummyJnt[0], ln='jointPosList', dt='string')
    pc.setAttr((rEyeDummyJnt[0] + '.jointPosList'), rEyeDummyJnt[0], type='string')

    # create r_eye annotation
    rEye = create_module_annotation((name + 'r_eye'), rEyeDummyJnt[0])
    pc.setAttr((rEye + '.t'), (0, 1, 0))
    pc.rename(rEye, (name + side + module_name + 'REye_annotate'))

    modSymLib.moduleSymmetryConnector(lEyeDummyJnt[0], rEyeDummyJnt[0])
    pc.move(1, 3, 1.5, lEyeDummyJnt[0])
    pc.parent(lEyeDummyJnt[0], rEyeDummyJnt[0], headPlacer)

    pc.addAttr(headPlacer, ln='child', dt='string')
    pc.setAttr((headPlacer + '.child'), (lEyeDummyJnt[0] + ' ' + rEyeDummyJnt[0]), type='string')
    pc.addAttr(headPlacer, ln='side', dt='string')
    pc.setAttr((headPlacer + '.side'), side, type='string')

    jointPosList = pc.getAttr(headPlacer + '.jointPosList')
    jointPosLists = List.seperate(jointPosList)
    dummyBoneGrp = create_dummy_bone(side, module_name, jointPosLists[0], lEyeDummyJnt[0])
    dummyBoneGrp = create_dummy_bone(side, module_name, jointPosLists[0], rEyeDummyJnt[0])

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
