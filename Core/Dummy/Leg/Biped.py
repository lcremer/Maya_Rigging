from Maya_UtilLib.Controls import build_world_pos_loc
from ....Core.Dummy import Fingers
from ....Core.Dummy.Util import *
from ....Utils import DummyUtil as dU


def build(name, side, num_joints, fingers, num_fingers, num_segment, color_index):
    joint_list = ''
    dummy_bone_grp = ''
    curve = pc.curve(d=1, p=[(2, 15, 0), (2, 8, 1), (2, 1, 0)])

    leg_dummy_bone_pos = get_dummy_bone_limb_pos(curve, num_joints)
    pc.delete(curve)

    leg_segment_names = ['hip', 'knee']
    middle_index = (num_joints / 2)
    all_leg_dummy_joints = []

    for i in range(num_joints - 1):
        temp_dummy_joint = create_dummy_joint(color_index)
        if num_joints == 3:
            if i <= middle_index:
                temp_dummy_joint[0] = pc.rename(temp_dummy_joint[0], (name + side + leg_segment_names[0] + '_loc'))
            if i >= middle_index:
                temp_dummy_joint[0] = pc.rename(temp_dummy_joint[0], (name + side + leg_segment_names[1] + '_loc'))
        else:
            if i <= middle_index:
                temp_dummy_joint[0] = pc.rename(temp_dummy_joint[0],
                                                (name + side + leg_segment_names[0] + str(i + 1) + '_loc'))
            if i >= middle_index:
                temp_dummy_joint[0] = pc.rename(temp_dummy_joint[0],
                                                (name + side + leg_segment_names[1] + (
                                                            str(i + 1) - middle_index) + '_loc'))

        temp_position = leg_dummy_bone_pos[i]
        pc.move((temp_position[0]), (temp_position[1]), (temp_position[2]), temp_dummy_joint[0])
        all_leg_dummy_joints.append(temp_dummy_joint[0])
        if i > 0:
            dummy_bone_grp = create_dummy_bone('leg', side, all_leg_dummy_joints[i - 1], all_leg_dummy_joints[i])

    ankle_dummy_joint = create_dummy_joint(color_index)
    ankle_dummy_joint[0] = pc.rename(ankle_dummy_joint[0], (name + side + 'ankle_loc'))
    ball_dummy_joint = create_dummy_joint(color_index)
    ball_dummy_joint[0] = pc.rename(ball_dummy_joint[0], (name + side + 'ball_loc'))
    toe_dummy_joint = create_dummy_joint(color_index)
    toe_dummy_joint[0] = pc.rename(toe_dummy_joint[0], (side + 'toe_loc'))

    main_leg_placer = cuLib.curveControl('cube1', 'curve')
    main_leg_placer[0] = pc.rename(main_leg_placer[0], name + side + 'legPlacer_loc')
    cuLib.resizeCurves(None, 1, 1, 1, 1.5)
    shape_color_override(main_leg_placer[0], color_index)
    pc.addAttr(main_leg_placer[0], ln='jointPosList', dt='string')
    pc.addAttr(main_leg_placer[0], ln='footPlacer', dt='string')

    # create leg annotation
    leg = create_module_annotation((name + side + 'leg'), main_leg_placer[0])
    pc.setAttr((leg + '.t'), (0, 1, 0))

    main_foot_placer = cuLib.curveControl('cube1', 'curve')
    main_foot_placer[0] = pc.rename(main_foot_placer[0], name + side + 'footPlacer_loc')
    cuLib.resizeCurves(None, 1, 1, 1, 1.5)
    shape_color_override(main_foot_placer[0], color_index)
    pc.addAttr(main_foot_placer[0], ln='jointPosList', dt='string')

    hip_position = leg_dummy_bone_pos[0];
    pc.move((hip_position[0]), (hip_position[1]), (hip_position[2]), main_leg_placer[0])

    ankle_position = leg_dummy_bone_pos[num_joints - 1]
    pc.parent(ankle_dummy_joint[0], main_foot_placer[0])
    pc.setAttr((ankle_dummy_joint[0] + '.t'), (0, 0, 0))
    pc.move((ankle_position[0]), (ankle_position[1]), (ankle_position[2]), main_foot_placer[0])

    # create ankle annotation
    ankle = create_module_annotation((name + side + 'ankle'), main_foot_placer[0])
    pc.setAttr((ankle + '.t'), (1, 0, 0))

    pc.move(2, 0, 2, ball_dummy_joint, )
    pc.move(2, 0, 4, toe_dummy_joint, )

    dummy_bone_grp = create_dummy_bone('leg', side, all_leg_dummy_joints[num_joints - 2], ankle_dummy_joint[0])
    dummy_bone_grp = create_dummy_bone('leg', side, ankle_dummy_joint[0], ball_dummy_joint[0])
    dummy_bone_grp = create_dummy_bone('leg', side, ball_dummy_joint[0], toe_dummy_joint[0])

    pc.parent(ball_dummy_joint, toe_dummy_joint, main_foot_placer[0])
    pc.parent(all_leg_dummy_joints, main_foot_placer[0], main_leg_placer[0])

    for n in all_leg_dummy_joints:
        joint_list = joint_list + (n + ' ')
        pc.setAttr(n + '.tx', lock=True)

    joint_list = joint_list + (ankle_dummy_joint[0] + ' ' + ball_dummy_joint[0] + ' ' + toe_dummy_joint[0])
    pc.setAttr((main_leg_placer[0] + '.jointPosList'), joint_list, type='string')
    pc.setAttr((main_leg_placer[0] + '.footPlacer'), main_foot_placer[0], type='string')
    pc.setAttr((main_foot_placer[0] + '.jointPosList'), ankle_dummy_joint[0], type='string')

    pc.setAttr((dummy_bone_grp + '.inheritsTransform'), 0)
    pc.parent(dummy_bone_grp, main_leg_placer[0], r=True)
    pc.select(cl=True)

    pc.select(all_leg_dummy_joints, ankle_dummy_joint[0], ball_dummy_joint, toe_dummy_joint, r=True)
    # pc.scale((0.7, 0.7, 0.7))
    pc.select(cl=True)

    if fingers:
        # declaring position for fingers
        pc.addAttr(main_leg_placer[0], ln='child', dt='string')
        finger_joint_list = ''
        finger_pos = [(1, 0, 2), (1.7, 0, 2), (2.4, 0, 2), (3.1, 0, 2), (3.8, 0, 2)]
        scale = [0.35, 0.32, 0.30, 0.27, 0.25]
        finger_name = ['bigToe', 'indexToe', 'midToe', 'ringToe', 'pinkyToe']

        for i in range(num_fingers):
            finger = Fingers.build(name, finger_name[i], side, num_segment, 'z', 2, color_index)
            finger_joint_list = finger_joint_list + (finger + ' ')
            pc.addAttr(finger, ln='parent', dt='string')
            pc.setAttr((finger + '.parent'), ball_dummy_joint, type='string')
            position = finger_pos[i]
            pc.move((position[0]), (position[1]), (position[2]), finger)
            pc.scale(finger, (scale[i], scale[i], scale[i]))
            pc.parent(finger, main_foot_placer[0])
            pc.select(cl=True)
            pc.setAttr((finger + '.buildTag'), main_leg_placer[0], type='string')
        pc.setAttr((main_leg_placer[0] + '.child'), finger_joint_list, type='string')

    # lock Attrs
    pc.setAttr((ankle_dummy_joint[0] + '.tx'), lock=True)
    pc.setAttr((ball_dummy_joint[0] + '.tx'), lock=True)
    pc.setAttr((toe_dummy_joint[0] + '.tx'), lock=True)
    pc.setAttr((main_foot_placer[0] + '.tx'), lock=True)
    pc.setAttr((main_foot_placer[0] + '.rz'), lock=True)
    pc.setAttr((main_leg_placer[0] + '.rz'), lock=True)

    # create world pos loc and parent main leg placer ctrl..
    world_pos_loc = build_world_pos_loc(name)
    if not pc.attributeQuery('leg', n=world_pos_loc, ex=True):
        pc.addAttr(world_pos_loc, ln='leg', dt='string')

    module_parts = pc.getAttr(world_pos_loc + '.leg')
    pc.setAttr((world_pos_loc + '.leg'), (str(module_parts or '') + ' ' + main_leg_placer[0]), type='string')

    pc.parent(main_leg_placer[0], world_pos_loc)

    # module tags
    pc.addAttr(main_leg_placer[0], ln='moduleTag', dt='string')
    pc.addAttr(main_leg_placer[0], ln='buildTag', dt='string')

    pc.setAttr((main_leg_placer[0] + '.moduleTag'), 'bipedLeg', type='string')
    pc.setAttr((main_leg_placer[0] + '.buildTag'), world_pos_loc, type='string')

    # rig info Attr
    pc.addAttr(main_leg_placer[0], ln='name', dt='string')
    pc.setAttr((main_leg_placer[0] + '.name'), name, type='string')
    pc.addAttr(main_leg_placer[0], ln='side', dt='string')
    pc.setAttr((main_leg_placer[0] + '.side'), side, type='string')
    pc.addAttr(main_leg_placer[0], ln=(side + 'hipJoint'), dt='string')
    pc.setAttr((main_leg_placer[0] + '.' + (side + 'hipJoint')), all_leg_dummy_joints[0], type='string')
    pc.addAttr(main_leg_placer[0], ln=(side + 'ankleJoint'), dt='string')
    pc.setAttr((main_leg_placer[0] + '.' + (side + 'ankleJoint')), ankle_dummy_joint[0], type='string')
    pc.addAttr(main_leg_placer[0], ln=(side + 'ballJoint'), dt='string')
    pc.setAttr((main_leg_placer[0] + '.' + (side + 'ballJoint')), ball_dummy_joint[0], type='string')
    pc.select(cl=True)

    # add dummy twist joints
    for i in range(0, len(all_leg_dummy_joints)):
        if i > 0:
            dU.add_dummy_twist_joints_attr(main_foot_placer[0], all_leg_dummy_joints[i - 1], all_leg_dummy_joints[i], 2)
    dU.add_dummy_twist_joints_attr(main_foot_placer[0], all_leg_dummy_joints[len(all_leg_dummy_joints) - 1],
                                   ankle_dummy_joint[0],
                                   2)
    dU.add_dummy_twist_joints_attr(main_foot_placer[0], ankle_dummy_joint[0], ball_dummy_joint[0], 0)
