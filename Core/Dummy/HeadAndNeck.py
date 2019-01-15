from Maya_UtilLib.Controls import build_world_pos_loc
from Util import *
from ..Dummy import Head as Head
from ..Dummy import Neck as Neck
from ...Core import ModuleSymmetryLib as modSymLib
from ...Utils import List
from ...Utils import DummyUtil as dU


def build(name, side, module_name, num_con, axis, dis, color_index):
    Neck.build(name, side, module_name, num_con, axis, dis, color_index)
    Head.build(name, side, 'head', color_index)

    neck_placer = (name + side + module_name + 'Main_ctrl')
    head_placer = (name + side + 'headMain_ctrl')

    pc.addAttr(neck_placer, ln='child', dt='string')
    pc.setAttr((neck_placer + '.child'), head_placer, type='string')

    head_pos = 0.0

    neck_joint = pc.getAttr(neck_placer + '.jointPosList')
    neck_joint_list = List.seperate(neck_joint)

    head_joint = pc.getAttr(head_placer + '.jointPosList')
    head_joint_list = List.seperate(head_joint)

    eye_joints = pc.getAttr(head_placer + '.child')

    neck_joint = pc.getAttr(neck_placer + '.jointPosList')
    neck_joint_list = List.seperate(neck_joint)

    size = 0

    if num_con > 1:
        size = len(neck_joint_list)
        modSymLib.connectModuleComponents(neck_joint_list[size - 1], head_placer)
        head_pos = (dis / (num_con - 1))
        pc.move(0, (dis + head_pos), 0, head_placer)
    else:
        modSymLib.connectModuleComponents(neck_joint_list[0], head_placer)
        head_pos = (dis / num_con)
        pc.move(0, head_pos, 0, head_placer)

    pc.parent(head_placer, neck_placer)

    # create world pos loc and parent main arm placer ctrl...
    world_pos_loc = build_world_pos_loc(name)
    if not pc.attributeQuery('neckHead', n=world_pos_loc, ex=True):
        pc.addAttr(world_pos_loc, ln='neckHead', dt='string')

    module_parts = pc.getAttr(world_pos_loc + '.neckHead')
    pc.setAttr((world_pos_loc + '.neckHead'), (str(module_parts or '') + ' ' + neck_placer), type='string')

    pc.parent(neck_placer, world_pos_loc)

    # module tags
    pc.addAttr(head_placer, ln='moduleTag', dt='string')
    pc.addAttr(head_placer, ln='buildTag', dt='string')

    pc.setAttr((head_placer + '.moduleTag'), 'head', type='string')
    pc.setAttr((head_placer + '.buildTag'), world_pos_loc, type='string')

    pc.addAttr(neck_placer, ln='moduleTag', dt='string')
    pc.addAttr(neck_placer, ln='buildTag', dt='string')

    pc.setAttr((neck_placer + '.moduleTag'), 'neck', type='string')
    pc.setAttr((neck_placer + '.buildTag'), world_pos_loc, type='string')

    pc.addAttr(neck_placer, ln='name', dt='string')
    pc.setAttr((neck_placer + '.name'), name, type='string')
    pc.addAttr(neck_placer, ln='side', dt='string')
    pc.setAttr((neck_placer + '.side'), side, type='string')
    pc.addAttr(neck_placer, ln=(side + 'neckJoint'), dt='string')
    pc.setAttr((neck_placer + '.' + (side + 'neckJoint')), neck_joint_list[0], type='string')
    pc.addAttr(neck_placer, ln=(side + 'headJoint'), dt='string')
    pc.setAttr((neck_placer + '.' + (side + 'headJoint')), head_joint_list[0], type='string')
    pc.addAttr(neck_placer, ln=(side + 'eyeJoints'), dt='string')
    pc.setAttr((neck_placer + '.' + (side + 'eyeJoints')), eye_joints, type='string')

    print('adding dummy joints')
    dU.add_dummy_twist_joints_attr(neck_placer, neck_joint_list[0], head_joint_list[0], 3)
