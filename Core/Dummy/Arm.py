from Maya_UtilLib.Controls import build_world_pos_loc
from Util import *
import Fingers
from ...Utils import DummyUtil as dU
from ...Core import ModuleSymmetryLib as modSymLib


def build(name, side, num_joints, fingers, num_fingers, num_segment, color_index):
    elements_list = ''
    dummy_bone_grp = ''
    clav_dummy_joint = create_dummy_joint(color_index)
    clav_dummy_joint[0] = pc.rename(clav_dummy_joint[0], (name + side + 'clav_loc'))
    pc.move(1, 0, 1, clav_dummy_joint[0])

    curve = pc.curve(d=1, p=[(3, 0, 0), (10, 0, -1), (17, 0, 0)])
    arm_dummy_bone_pos = get_dummy_bone_limb_pos(curve, num_joints)
    pc.delete(curve)

    arm_segment_names = ['shoulder', 'elbow']
    middle_index = (num_joints / 2)
    all_arm_dummy_joints = []

    for i in range(num_joints - 1):
        temp_dummy_joint = create_dummy_joint(color_index)
        if num_joints == 3:
            if i <= middle_index:
                temp_dummy_joint[0] = pc.rename(temp_dummy_joint[0], (name + side + arm_segment_names[0] + '_loc'))
            if i >= middle_index:
                temp_dummy_joint[0] = pc.rename(temp_dummy_joint[0], (name + side + arm_segment_names[1] + '_loc'))
        else:
            if i <= middle_index:
                temp_dummy_joint[0] = pc.rename(temp_dummy_joint[0],
                                              (name + side + arm_segment_names[0] + str(i + 1) + '_loc'))
            if i >= middle_index:
                temp_dummy_joint[0] = pc.rename(temp_dummy_joint[0],
                                              (name + side + arm_segment_names[1] + (
                                                      str(i + 1) - middle_index) + '_loc'))

        temp_position = arm_dummy_bone_pos[i]
        pc.move((temp_position[0]), (temp_position[1]), (temp_position[2]), temp_dummy_joint[0])

        all_arm_dummy_joints.append(temp_dummy_joint[0])

        if i > 0:
            dummy_bone_grp = create_dummy_bone('arm', side, all_arm_dummy_joints[i - 1], all_arm_dummy_joints[i])

    main_arm_placer = cuLib.curveControl('cube1', 'curve')
    main_arm_placer[0] = pc.rename(main_arm_placer[0], name + side + 'armPlacer_loc')
    cuLib.resizeCurves(None, 1, 1, 1, 1.5)
    shape_color_override(main_arm_placer[0], color_index)
    pc.addAttr(main_arm_placer[0], ln='jointPosList', dt='string')

    # create arm annotation
    arm = create_module_annotation((name + side + 'arm'), main_arm_placer[0])
    pc.setAttr((arm + '.t'), (0, 1, 0))

    # shoulderPosition
    shoulder_position = arm_dummy_bone_pos[0]
    pc.move((shoulder_position[0]), (shoulder_position[1]), (shoulder_position[2]), main_arm_placer[0])
    wrist_dummy_joint = create_dummy_joint(color_index)
    wrist_dummy_joint[0] = pc.rename(wrist_dummy_joint[0], (name + side + 'wrist_loc'))
    wrist_end_dummy_joint = create_dummy_joint(color_index)
    wrist_end_dummy_joint[0] = pc.rename(wrist_end_dummy_joint[0], (name + side + 'wristEnd_loc'))

    main_wrist_placer = cuLib.curveControl('cube1', 'curve')
    main_wrist_placer[0] = pc.rename(main_wrist_placer[0], name + side + 'wristPlacer_loc')
    cuLib.resizeCurves(None, 1, 1, 1, 1.5)
    shape_color_override(main_wrist_placer[0], color_index)
    pc.addAttr(main_wrist_placer[0], ln='jointPosList', dt='string')
    pc.setAttr((main_wrist_placer[0] + '.jointPosList'), wrist_dummy_joint[0], type='string')

    # create wrist annotation
    wrist = create_module_annotation((name + side + 'wrist'), main_wrist_placer[0])
    pc.setAttr((wrist + '.t'), (0, 1, 0))

    pc.addAttr(main_arm_placer[0], ln='wristPlacer', dt='string')
    pc.setAttr((main_arm_placer[0] + '.wristPlacer'), main_wrist_placer[0], type='string')

    pc.move(0.7, 0, 0, wrist_end_dummy_joint)
    dummy_bone_grp = create_dummy_bone('arm', side, clav_dummy_joint[0], all_arm_dummy_joints[0])
    dummy_bone_grp = create_dummy_bone('arm', side, all_arm_dummy_joints[num_joints - 2], wrist_dummy_joint[0])
    dummy_bone_grp = create_dummy_bone('arm', side, wrist_dummy_joint[0], wrist_end_dummy_joint[0])

    pc.parent(wrist_dummy_joint, wrist_end_dummy_joint, main_wrist_placer[0])

    # wristPosition
    wrist_position = arm_dummy_bone_pos[num_joints - 1]
    pc.move((wrist_position[0]), (wrist_position[1]), (wrist_position[2]), main_wrist_placer[0])

    elements_list = elements_list + (clav_dummy_joint[0] + ' ')
    for n in range(len(all_arm_dummy_joints)):
        elements_list = elements_list + (all_arm_dummy_joints[n] + ' ')
        pc.setAttr((all_arm_dummy_joints[n] + '.ty'), lock=True)

    elements_list = elements_list + (wrist_dummy_joint[0] + ' ' + wrist_end_dummy_joint[0])
    pc.setAttr((main_arm_placer[0] + '.jointPosList'), elements_list, type='string')

    pc.parent(all_arm_dummy_joints, main_arm_placer[0])
    pc.parent(main_wrist_placer[0], main_arm_placer[0])
    pc.setAttr((wrist_dummy_joint[0] + '.ty'), lock=True)
    pc.setAttr((wrist_end_dummy_joint[0] + '.ty'), lock=True)
    pc.setAttr((wrist_end_dummy_joint[0] + '.tz'), lock=True)
    pc.setAttr((main_wrist_placer[0] + '.ty'), lock=True)

    pc.select(clav_dummy_joint[0], all_arm_dummy_joints, wrist_dummy_joint[0], wrist_end_dummy_joint[0], r=True)
    # pc.scale((0.7,0.7,0.7))
    pc.select(cl=True)

    if fingers:
        # declaring position for fingers
        finger_list = ''

        finger_pos = [(17.7, -0.35, 1), (18.3, 0.15, 0.9), (18.2, 0.3, 0.1), (18.15, 0.15, -0.5), (18.1, 0, -1)]
        finger_rot = [(85, -35, -30), (0, -3, 0), (0, 0, 0), (0, 5, 0), (0, 10.25, 0)]
        scale = [0.35, 0.35, 0.4, 0.35, 0.3]
        finger_names = ['thumb', 'index', 'middle', 'ring', 'pinky']

        pc.select(cl=True)
        for j in range(num_fingers):
            if j == 0:  # idea here is that thumb joints will have one less segment compare to other fingers
                finger = Fingers.build(name, finger_names[j], side, num_segment, 'x', 3, color_index)
            else:
                finger = Fingers.build(name, finger_names[j], side, (num_segment + 1), 'x', 3, color_index)

            finger_list = finger_list + (finger + ' ')

            position = finger_pos[j]
            pc.move(position[0], position[1], position[2], finger)

            rotation = finger_rot[j]
            pc.rotate(finger, rotation[0], rotation[1],
                      rotation[2])  # NOTE: for some reason pymel rotate does not follow the pattern that move does

            modSymLib.connectModuleComponents(wrist_dummy_joint[0], finger)

            pc.scale(finger, (scale[j], scale[j], scale[j]))

            pc.parent(finger, main_wrist_placer[0])

            pc.setAttr((finger + '.buildTag'), main_arm_placer[0], type='string')

            pc.select(cl=True)

        pc.addAttr(main_arm_placer[0], ln='child', dt='string')
        pc.setAttr((main_arm_placer[0] + '.child'), finger_list, type='string')

    pc.setAttr((dummy_bone_grp + '.inheritsTransform'), 0)
    pc.parent(dummy_bone_grp, main_arm_placer[0], r=True)

    # create world pos loc and parent main arm placer ctrl...
    world_pos_loc = build_world_pos_loc(name)

    if not pc.attributeQuery('arm', n=world_pos_loc, ex=True):
        pc.addAttr(world_pos_loc, ln='arm', dt='string')

    module_parts = pc.getAttr(world_pos_loc + '.' + 'arm')
    pc.setAttr((world_pos_loc + '.' + 'arm'), (str(module_parts or '') + ' ' + main_arm_placer[0]), type='string')

    pc.parent(clav_dummy_joint[0], main_arm_placer[0], world_pos_loc)

    # module tags
    pc.addAttr(main_arm_placer[0], ln='moduleTag', dt='string')
    pc.addAttr(main_arm_placer[0], ln='buildTag', dt='string')

    pc.setAttr((main_arm_placer[0] + '.moduleTag'), 'arm', type='string')
    pc.setAttr((main_arm_placer[0] + '.buildTag'), world_pos_loc, type='string')

    # rig info Attr
    pc.addAttr(main_arm_placer[0], ln='name', dt='string')
    pc.setAttr((main_arm_placer[0] + '.name'), name, type='string')
    pc.addAttr(main_arm_placer[0], ln='side', dt='string')
    pc.setAttr((main_arm_placer[0] + '.side'), side, type='string')
    pc.addAttr(main_arm_placer[0], ln=(side + 'shoulderJoint'), dt='string')
    pc.setAttr((main_arm_placer[0] + '.' + (side + 'shoulderJoint')), all_arm_dummy_joints[0], type='string')
    pc.addAttr(main_arm_placer[0], ln=(side + 'wristJoint'), dt='string')
    pc.setAttr((main_arm_placer[0] + '.' + (side + 'wristJoint')), wrist_dummy_joint[0], type='string')
    pc.select(cl=True)

    # add dummy twist joints
    for i in range(0, len(all_arm_dummy_joints)):
        if i > 0:
            dU.add_dummy_twist_joints_attr(main_arm_placer[0], all_arm_dummy_joints[i - 1], all_arm_dummy_joints[i], 2)
    dU.add_dummy_twist_joints_attr(main_arm_placer[0], all_arm_dummy_joints[len(all_arm_dummy_joints) - 1],
                                   wrist_dummy_joint[0], 2)
