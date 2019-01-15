import sys
from Util import *
from ...Utils import List


def build(name, side, module_name, num_con, axis, dis, colorIndex):
    neckPlacer = ''

    if num_con > 1:
        neckPlacer = linear_dis_dummy_bone_creator(name, side, module_name, num_con, axis, dis, colorIndex)
        jointPosList = pc.getAttr(neckPlacer + '.jointPosList')
        jointPosLists = List.seperate(jointPosList)
        size = len(jointPosList)

    else:
        mainNeckPlacer = cuLib.curveControl('cube1', 'curve')
        mainNeckPlacer[0] = pc.rename(mainNeckPlacer[0], name + side + module_name + 'Main_ctrl')
        shape_color_override(mainNeckPlacer[0], colorIndex)
        cuLib.resizeCurves(None, 1, 1, 1, 1.5)
        pc.addAttr(mainNeckPlacer[0], ln='jointPosList', dt='string')

        neckDummyJoint = create_dummy_joint(colorIndex)
        neckDummyJoint[0] = pc.rename(neckDummyJoint[0], (name + side + 'neck_loc'))
        pc.scale(neckDummyJoint[0], (1, 1, 1))

        pc.parent(neckDummyJoint[0], mainNeckPlacer[0])

        pc.setAttr((mainNeckPlacer[0] + '.jointPosList'), neckDummyJoint[0], type='string')
        neckPlacer = mainNeckPlacer[0]

    # create neck annotation
    neck = create_module_annotation((name + side + module_name), neckPlacer)

    pc.select(cl=True)
