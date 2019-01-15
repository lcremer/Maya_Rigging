import pymel.core as pc
from Maya_UtilLib import Units
from ...Utils import CurveUtilLib as cuLib
from ...Utils import CharUtilsLib as charLib


def create_dummy_bone(name, side, start_dummy_joint, end_dummy_joint):
    # creating parent grp
    bone_crv_grp = (side + name + 'BoneCurves_grp')

    # some error checking
    if not pc.objExists(bone_crv_grp):
        bone_crv_grp = pc.group(em=True, n=(side + name + 'BoneCurves_grp'))

    # getting the name of start and end locators stored in dummy joint loc
    start_dummy_sp = pc.getAttr(start_dummy_joint + '.startPos')
    start_dummy_ep = pc.getAttr(start_dummy_joint + '.endPos')
    end_dummy_sp = pc.getAttr(end_dummy_joint + '.startPos')
    end_dummy_ep = pc.getAttr(end_dummy_joint + '.endPos')

    temp = charLib.createDistance(start_dummy_sp, start_dummy_ep)
    shape = pc.listRelatives(temp[0], s=True)

    start_sphere_rad = Units.distance_to_scene_units(pc.getAttr(shape[0] + '.distance'))
    print("start distance: " + str(start_sphere_rad))
    pc.delete(temp)

    temp = charLib.createDistance(end_dummy_sp, end_dummy_ep)
    shape = pc.listRelatives(temp[0], s=True)

    end_sphere_rad = Units.distance_to_scene_units(pc.getAttr(shape[0] + '.distance'))
    print("end distance: " + str(end_sphere_rad))
    pc.delete(temp)

    # creating dummy bone rig
    pc.select(start_dummy_joint, r=True)
    start_loc1 = cuLib.curveControl('loc', 'curve')
    start_loc1[0] = pc.rename(start_loc1[0], start_dummy_joint + 'Aim_loc#')
    start_loc2 = cuLib.curveControl('loc', 'curve')
    start_loc2[0] = pc.rename(start_loc2[0], start_dummy_joint + 'AimPos_loc#')
    pc.parent(start_loc2[0], start_loc1[0])
    pc.setAttr((start_loc2[0] + '.tx'), start_sphere_rad)
    pc.parent(start_loc1[0], start_dummy_joint)

    pc.select(end_dummy_joint, r=True)
    end_loc1 = cuLib.curveControl('loc', 'curve')
    end_loc1[0] = pc.rename(end_loc1[0], end_dummy_joint + 'Aim_loc#')
    end_loc2 = cuLib.curveControl('loc', 'curve')
    end_loc2[0] = pc.rename(end_loc2[0], end_dummy_joint + 'AimPos_loc#')
    pc.parent(end_loc2[0], end_loc1[0])
    pc.setAttr((end_loc2[0] + '.tx'), (-end_sphere_rad))
    pc.parent(end_loc1[0], end_dummy_joint)

    pc.aimConstraint(end_dummy_joint, start_loc1[0], offset=[0, 0, 0], weight=1, aimVector=[1, 0, 0],
                     upVector=[0, 1, 0],
                     worldUpType='vector', worldUpVector=[0, 1, 0])
    pc.aimConstraint(start_dummy_joint, end_loc1[0], offset=[0, 0, 0], weight=1, aimVector=[-1, 0, 0],
                     upVector=[0, 1, 0],
                     worldUpType='vector', worldUpVector=[0, 1, 0])

    pc.select(cl=True)
    connect = cuLib.curveControl('cone', 'curve')
    connect[0] = pc.rename(connect[0], start_dummy_joint + 'Bone_crv#')
    pc.select((connect[0] + '.cv[0:1]'), (connect[0] + '.cv[3:4]'), (connect[0] + '.cv[6:7]'),
              (connect[0] + '.cv[9:10]'), (connect[0] + '.cv[12:13]'), (connect[0] + '.cv[15:16]'), r=True)
    pos_a_clusters = pc.cluster()
    pc.select(cl=True)
    pc.select((connect[0] + '.cv[2]'), (connect[0] + '.cv[5]'), (connect[0] + '.cv[8]'), (connect[0] + '.cv[11]'),
              (connect[0] + '.cv[14]'), r=True)
    pos_b_clusters = pc.cluster()
    pc.select(cl=True)
    pc.setAttr((connect[0] + '.overrideEnabled'), 1)
    pc.setAttr((connect[0] + '.overrideDisplayType'), 2)

    pc.pointConstraint(start_loc2[0], pos_a_clusters[1], offset=[0, 0, 0], weight=1)
    pc.parent(pos_a_clusters[1], start_loc1[0])

    pc.setAttr((pos_a_clusters[1] + '.r'), (0, 0, 0))
    pc.setAttr((pos_a_clusters[1] + '.s'), (1, 1, 1))

    pc.pointConstraint(end_loc2[0], pos_b_clusters[1], offset=[0, 0, 0], weight=1)
    pc.parent(pos_b_clusters[1], end_loc1[0])
    pc.hide(start_loc1[0], end_loc1[0])

    charLib.lockAndHide(start_loc1[0], 'lock', 'trans rot scale vis')
    charLib.lockAndHide(end_loc1[0], 'lock', 'trans rot scale vis')
    pc.parent(connect[0], bone_crv_grp)
    return bone_crv_grp


def create_dummy_joint(color_index):
    imp_sphere = pc.createNode('implicitSphere')
    pc.setAttr((imp_sphere + '.rd'), 0.5)

    parent = pc.listRelatives(imp_sphere, p=True)

    shape_color_override(parent, color_index)
    cuLib.shapeRename(parent[0])

    start_dis = cuLib.curveControl('loc', 'curve')
    start_dis[0] = pc.rename(start_dis[0], parent[0] + 'Sp_loc#')

    end_dis = cuLib.curveControl('loc', 'curve')
    end_dis[0] = pc.rename(end_dis[0], parent[0] + 'Ep_loc#')

    pc.parent(end_dis[0], start_dis[0])
    pc.setAttr((end_dis[0] + '.tx'), 0.7)
    pc.parent(start_dis[0], parent[0])
    pc.hide(start_dis[0], end_dis[0])

    charLib.lockAndHide(start_dis[0], 'lock', 'trans rot scale vis')
    charLib.lockAndHide(end_dis[0], 'lock', 'trans rot scale vis')

    pc.addAttr(parent[0], ln='startPos', dt='string')
    pc.addAttr(parent[0], ln='endPos', dt='string')

    pc.setAttr((parent[0] + '.startPos'), start_dis[0], type='string')
    pc.setAttr((parent[0] + '.endPos'), end_dis[0], type='string')
    return parent


def shape_color_override(n, color_index):
    # color index
    # 6 = blue
    # 13 = red
    # 14 = green
    # 17 = yellow
    # int color_index = 17;

    sel = []

    if n == '':
        sel = pc.ls(sl=True)
    else:
        sel.append(n)

    for s in sel:
        shape = pc.listRelatives(s, f=True, s=True)
        for x in shape:
            pc.setAttr((x + '.overrideEnabled'), 1)
            pc.setAttr((x + '.overrideColor'), color_index)


def linear_dis_dummy_bone_creator(name, side, module_name, num_con, axis, dis, color_index):
    """Returns a list of dummy bones for given module name and side along given axis"""
    control = []
    bone_list = ''
    dummy_bone_grp = ''
    lock = ''
    split = dis / (num_con - 1)
    pos = 0
    tent_main_pos = cuLib.curveControl('cube1', 'curve')
    tent_main_pos[0] = pc.rename(tent_main_pos[0], name + side + module_name + 'Main_ctrl')
    shape_color_override(tent_main_pos[0], color_index)
    cuLib.resizeCurves(None, 1, 1, 1, 1.5)
    pc.addAttr(tent_main_pos[0], ln='jointPosList', dt='string')
    pc.select(cl=True)

    for i in range(num_con):
        tentacle_dummy_jnt = create_dummy_joint(color_index)
        tentacle_dummy_jnt[0] = pc.rename(tentacle_dummy_jnt[0], (name + side + module_name + str(i + 1) + '_loc'))
        control.append(tentacle_dummy_jnt[0])
        pc.scale(tentacle_dummy_jnt[0], (1, 1, 1))
        if i > 0:
            if axis == 'x':
                pc.move(pos, 0, 0, control[i])
                lock = 'z'
            elif axis == 'y':
                pc.move(0, pos, 0, control[i])
                lock = 'x'
            elif axis == 'z':
                pc.move(0, 0, pos, control[i])
                lock = 'x'
            dummy_bone_grp = create_dummy_bone(module_name, side, control[i - 1], control[i])
        pos = (pos + split)
        pc.parent(tentacle_dummy_jnt, tent_main_pos[0])
        bone_list = bone_list + (tentacle_dummy_jnt[0] + ' ')
        pc.select(cl=True)

    for x in range(num_con):
        pc.setAttr((control[x] + '.t' + lock), lock=True)

    pc.setAttr((dummy_bone_grp + '.inheritsTransform'), 0)
    pc.parent(dummy_bone_grp, tent_main_pos[0], r=True)
    pc.setAttr((tent_main_pos[0] + '.jointPosList'), bone_list, type='string')
    pc.select(cl=True)
    return tent_main_pos[0]


def get_dummy_bone_limb_pos(curve, num_joints):
    """Returns list of Dummy Bone positions"""
    dummy_joint_pos = []

    curve_info = pc.pointOnCurve(curve, constructionHistory=1)
    pc.setAttr((curve_info + '.turnOnPercentage'), 1)

    for i in range(num_joints):
        parameter = i * (1.0 / (num_joints - 1))
        pc.setAttr((curve_info + '.parameter'), parameter)
        temp_joint_pos = pc.getAttr(curve_info + '.position')
        dummy_joint_pos.append(temp_joint_pos)

    pc.delete(curve_info)
    return dummy_joint_pos


def create_module_annotation(name, obj):
    annotation = pc.annotate(obj, tx=name, p=(0, 0, 0))
    pc.setAttr((annotation + '.displayArrow'), 0)
    pc.setAttr((annotation + '.overrideEnabled'), 1)
    pc.setAttr((annotation + '.overrideDisplayType'), 2)

    annotation_shape = pc.listRelatives(annotation, p=True)
    annotation_shape[0] = pc.rename(annotation_shape[0], (name + '_annotate'))
    pc.parent(annotation_shape[0], obj)

    return annotation_shape[0]
