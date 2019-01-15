import pymel.core as pc
from ..Utils import CurveUtilLib as cuUL
from ..Utils import CharUtilsLib as chUL


def build_world(name, scale, control_color=''):
    world_a_control = [(name + 'worldA_ctrl')]
    world_b_control = [(name + 'worldB_ctrl')]
    control_grp = []

    if not pc.objExists(world_a_control[0]):
        master_control = pc.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=7, d=3, ut=0, tol=0.001, s=8, ch=0,
                                  n=(name + 'worldA_ctrl'))
        # worldAControl[0] = masterControl
        cuUL.resizeCurves(None, 1, 1, 1, scale)
        color_control(master_control[0], control_color)

    if pc.objExists(world_b_control[0]):
        control_grp.append((name + 'controls_grp'))
        control_grp.append((name + 'skeletons_grp'))
    else:
        pc.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=5.5, d=3, ut=0, tol=0.001, s=8, ch=0,
                  n=(name + 'worldB_ctrl'))
        # worldBControl = pc.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=5.5, d=3, ut=0, tol=0.001, s=8, ch=0,
        #                           n=(name + 'worldB_ctrl'))

        cuUL.resizeCurves(None, 1, 1, 1, scale)
        pc.parent(world_b_control[0], world_a_control[0])
        rig_grp = pc.group(em=True, n=(name + 'rig'))
        chUL.lockAndHide(rig_grp, 'locknHide', 'trans rot scale')

        pc.parent(world_a_control[0], rig_grp)

        control_grp.append(pc.group(em=True, n=(name + 'controls_grp')))
        chUL.lockAndHide(control_grp[0], 'locknHide', 'trans rot scale')
        control_grp.append(pc.group(em=True, n=(name + 'skeletons_grp')))
        pc.setAttr((control_grp[1] + '.overrideEnabled'), 1)
        pc.setAttr((control_grp[1] + '.overrideDisplayType'), 2)
        chUL.lockAndHide(control_grp[1], 'locknHide', 'trans rot scale')
        pc.parent(control_grp[0], control_grp[1], world_b_control[0])
        scale_node = create_scale_grp(name)
        pc.scaleConstraint(world_b_control, scale_node, offset=(1, 1, 1), weight=1)

        color_control(world_b_control[0], control_color)

    return control_grp


def create_non_scale_grp(name):
    non_scale_grp = (name + 'non_scale_grp')
    if not pc.objExists(non_scale_grp):
        non_scale_grp = pc.group(em=True, n=(name + 'non_scale_grp'))
        if pc.objExists(name + 'rig'):
            pc.parent(non_scale_grp, (name + 'rig'))

    return non_scale_grp


def create_scale_grp(name):
    scale_node = (name + 'worldScaleCon_grp')
    non_scale_grp = create_non_scale_grp(name)
    if not pc.objExists(scale_node):
        pc.group(em=True, n=(name + 'worldScaleCon_grp'))
        pc.parent(scale_node, non_scale_grp)
    return scale_node


def color_control(c, control_color):
    if control_color != '':
        try:
            c.overrideEnabled.set(True)
            c.overrideColor.set(control_color)
        except:
            pass
        try:
            c.getShape().overrideEnabled.set(True)
            c.getShape().overrideColor.set(control_color)
        except:
            pass
