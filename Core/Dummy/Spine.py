from Maya_UtilLib.Controls import build_world_pos_loc
from Util import *
from ...Utils import List
from ...Utils import DummyUtil as dU


def build(name, side, module_name, num_con, axis, dis, color_index):
    print('building Spine Dummy Skeleton Module')
    lock = ''

    # create spineModule
    spine_placer = linear_dis_dummy_bone_creator(name, side, module_name, num_con, axis, dis, color_index)
    create_module_annotation((name + side + module_name), spine_placer)
    chest = create_module_annotation((name + side + 'chest'), (name + side + module_name + str(num_con) + '_loc'))
    pc.setAttr((chest + '.t'), (0, 0, 0))

    # negate pos value in order to get hips position opposite to the spine joint
    pos = (dis / dis) * -1

    hips_dummy_jnt = create_dummy_joint(color_index)
    hips_dummy_jnt[0] = pc.rename(hips_dummy_jnt[0], (name + side + module_name + 'Hips_loc'))
    pc.addAttr(hips_dummy_jnt[0], ln='jointPosList', dt='string')
    pc.setAttr((hips_dummy_jnt[0] + '.jointPosList'), hips_dummy_jnt[0], type='string')
    hips = create_module_annotation((name + side + 'hips'), hips_dummy_jnt[0])
    pc.setAttr((hips + '.t'), (0, -1, 0))

    pc.parent(hips_dummy_jnt[0], spine_placer)

    joint_pos_list = pc.getAttr(spine_placer + '.jointPosList')
    joint_pos_lists = List.seperate(joint_pos_list)
    dummy_bone_grp = create_dummy_bone(side, module_name, joint_pos_lists[0], hips_dummy_jnt[0])

    pc.addAttr(hips_dummy_jnt[0], ln='parent', dt='string')
    pc.setAttr((hips_dummy_jnt[0] + '.parent'), joint_pos_lists[0], type='string')

    pc.addAttr(spine_placer, ln='child', dt='string')
    pc.setAttr((spine_placer + '.child'), hips_dummy_jnt[0], type='string')

    if axis == 'x' or axis == 'X':
        pc.move(pos, 0, 0, hips_dummy_jnt[0])
        lock = 'z'
    elif axis == 'y' or axis == 'Y':
        pc.move(0, pos, 0, hips_dummy_jnt[0])
        lock = 'x'
    elif axis == 'z' or axis == 'Z':
        pc.move(0, 0, pos, hips_dummy_jnt[0])
        lock = 'x'

    pc.setAttr((hips_dummy_jnt[0] + '.t' + lock), lock=True)

    pc.setAttr((dummy_bone_grp + '.inheritsTransform'), 0)
    try:
        pc.parent(dummy_bone_grp, spine_placer, r=True)
    except:
        pass
    pc.select(cl=True)

    # create world pos loc and parent main arm placer ctrl...
    world_pos_loc = build_world_pos_loc(name)
    if not pc.attributeQuery('spine', n=world_pos_loc, ex=True):
        pc.addAttr(world_pos_loc, ln='spine', dt='string')

    module_parts = pc.getAttr(world_pos_loc + '.' + 'spine')
    pc.setAttr((world_pos_loc + '.' + 'spine'), (str(module_parts or '') + ' ' + spine_placer), type='string')

    pc.parent(spine_placer, world_pos_loc)

    # module tags
    pc.addAttr(spine_placer, ln='moduleTag', dt='string')
    pc.addAttr(spine_placer, ln='buildTag', dt='string')

    pc.setAttr((spine_placer + '.moduleTag'), 'spine', type='string')
    pc.setAttr((spine_placer + '.buildTag'), world_pos_loc, type='string')

    # rig info Attr
    spine_list = pc.getAttr(spine_placer + '.jointPosList')
    spine_joints_list = List.seperate(spine_list)
    size = len(spine_joints_list)

    pc.addAttr(spine_placer, ln='name', dt='string')
    pc.setAttr((spine_placer + '.name'), name, type='string')
    pc.addAttr(spine_placer, ln='side', dt='string')
    pc.setAttr((spine_placer + '.side'), side, type='string')
    pc.addAttr(spine_placer, ln=(side + 'rootJoint'), dt='string')
    pc.setAttr((spine_placer + '.' + (side + 'rootJoint')), spine_joints_list[0], type='string')
    pc.addAttr(spine_placer, ln=(side + 'chestJoint'), dt='string')
    pc.setAttr((spine_placer + '.' + (side + 'chestJoint')), spine_joints_list[size - 1], type='string')
    pc.addAttr(spine_placer, ln=(side + 'hipJoint'), dt='string')
    pc.setAttr((spine_placer + '.' + (side + 'hipJoint')), hips_dummy_jnt[0], type='string')
    pc.select(cl=True)

    dU.add_dummy_twist_joints_attr(spine_placer, joint_pos_lists[0], spine_joints_list[size - 1], 7)
