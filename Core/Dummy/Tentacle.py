from Maya_UtilLib.Controls import build_world_pos_loc
from Util import *
from ...Utils import List
from ...Utils import DummyUtil as dU


def build(name, side, module_name, num_con, axis, dis, color_index):
    tentacle_placer = linear_dis_dummy_bone_creator(name, side, module_name, num_con, axis, dis, color_index)

    # create tentacle annotation
    tentacle = create_module_annotation((name + side + module_name), tentacle_placer)
    pc.setAttr((tentacle + '.t'), (0, 1, 0))

    # create world pos loc and parent main arm placer ctrl...
    world_pos_loc = build_world_pos_loc(name)
    if not pc.attributeQuery('tentacle', n=world_pos_loc, ex=True):
        pc.addAttr(world_pos_loc, ln='tentacle', dt='string')

    module_parts = pc.getAttr(world_pos_loc + '.' + 'tentacle')
    pc.setAttr((world_pos_loc + '.' + 'tentacle'), (str(module_parts or '') + ' ' + tentacle_placer), type='string')

    pc.parent(tentacle_placer, world_pos_loc)

    # module tags
    pc.addAttr(tentacle_placer, ln='moduleTag', dt='string')
    pc.addAttr(tentacle_placer, ln='buildTag', dt='string')

    pc.setAttr((tentacle_placer + '.moduleTag'), 'tentacle', type='string')
    pc.setAttr((tentacle_placer + '.buildTag'), world_pos_loc, type='string')

    # rig info Attr
    tentacle_list = pc.getAttr(tentacle_placer + '.jointPosList')
    tentacle_joints_list = List.seperate(tentacle_list)
    size = len(tentacle_joints_list)

    pc.addAttr(tentacle_placer, ln='name', dt='string')
    pc.setAttr((tentacle_placer + '.name'), name, type='string')
    pc.addAttr(tentacle_placer, ln='side', dt='string')
    pc.setAttr((tentacle_placer + '.side'), side, type='string')
    pc.addAttr(tentacle_placer, ln=(side + 'startJoint'), dt='string')
    pc.setAttr((tentacle_placer + '.' + (side + 'startJoint')), tentacle_joints_list[0], type='string')
    pc.addAttr(tentacle_placer, ln=(side + 'endJoint'), dt='string')
    pc.setAttr((tentacle_placer + '.' + (side + 'endJoint')), tentacle_joints_list[size - 1], type='string')
    pc.addAttr(tentacle_placer, ln=(side + 'types'), dt='string')
    pc.setAttr((tentacle_placer + '.' + (side + 'types')), module_name, type='string')

    pc.select(cl=True)
    dU.add_dummy_twist_joints_attr(tentacle_placer, tentacle_joints_list[0], tentacle_joints_list[size - 1], 0)