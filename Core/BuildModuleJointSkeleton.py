import pymel.core as pc
import BuildModuleJointSkeletonLib as bSkelLib
from ..Utils import List
from ..Utils.String import objGetPrefix


def get_parent_attr_module_components(obj):
    parent = ''
    if pc.attributeQuery('parent', n=obj, ex=True):
        parent_grp = pc.getAttr(obj + '.parent')
        strip = objGetPrefix(parent_grp)
        parent = (strip + '_jnt')
    return parent


def build_module_skeleton():
    sel = pc.ls(sl=True)
    if len(sel) <= 0:
        pc.select('worldPos_loc')
        sel = pc.ls(sl=True)

    if len(sel) > 0:
        result = pc.confirmDialog(title='Build Skeleton',
                                  message='The current operation will convert all different modules into actual '
                                          'Joints and prepare skeleton for animation rig installation.\n\nAre you '
                                          'sure you want continue?',
                                  messageAlign='center',
                                  button=['OK', 'Cancel'],
                                  defaultButton='OK',
                                  cancelButton='Cancel',
                                  dismissString='Cancel')
        if result == 'Cancel':
            pc.error('operation canceled')

        if result == 'OK':
            build_confirmed(sel)
    else:
        pc.error('wordPos_loc could not be found')


def build_confirmed(sel):
    pc.hide(sel[0])

    # This is only being used to get the amount of modules for the sake of keeping progress
    module_inf = List.seperate(get_module_list(sel))
    pc.progressWindow('buildSkeletonProgress', t='building Skeleton', progress=0,
                      status='building skeleton from modules :', min=0, max=len(module_inf), isInterruptable=True)

    # TODO: find a way to auto iterate through list of build modules, so this doesn't have to be updated as new modules
    #  are added
    build_spine(sel)
    # TODO: look into how modules head vs neck vs both are determined
    build_neck_head(sel)
    build_leg(sel)
    build_arm(sel)
    build_tentacle(sel)

    pc.delete(sel[0])
    pc.progressWindow('buildSkeletonProgress', endProgress=True)


def get_module_list(sel):
    module_list = ''
    if pc.attributeQuery('spine', n=sel[0], ex=True):
        spine_module = pc.getAttr(sel[0] + '.spine')
        module_list = module_list + (spine_module + ' ')

    if pc.attributeQuery('neckHead', n=sel[0], ex=True):
        neck_module = pc.getAttr(sel[0] + '.neckHead')
        module_list = module_list + (neck_module + ' ')

    if pc.attributeQuery('arm', n=sel[0], ex=True):
        arm_module = pc.getAttr(sel[0] + '.arm')
        module_list = module_list + (arm_module + ' ')

    if pc.attributeQuery('leg', n=sel[0], ex=True):
        leg_module = pc.getAttr(sel[0] + '.leg')
        module_list = module_list + (leg_module + ' ')

    if pc.attributeQuery('tentacle', n=sel[0], ex=True):
        tentacle_module = pc.getAttr(sel[0] + '.tentacle')
        module_list = module_list + (tentacle_module + ' ')
    return module_list


def build_spine(sel):
    # checking if the rig has a spine module
    if pc.attributeQuery('spine', n=sel[0], ex=True):
        spine_main_placer = pc.getAttr(sel[0] + '.spine')
        spine_module_lists = List.seperate(spine_main_placer)
        for s in spine_module_lists:
            if s:
                parent = get_parent_attr_module_components(s)
                pc.select(s, r=True)
                bSkelLib.buildSpineJointSkeleton(parent)

                if pc.progressWindow('buildSkeletonProgress', q=True, isCancelled=True):
                    pc.progressWindow('buildSkeletonProgress', endProgress=True)
                    pc.undoInfo(state=True)
                    return
                pc.progressWindow('buildSkeletonProgress', e=True, step=1,
                                  status=('building module skeleton on : ' + s))


def build_neck_head(sel):
    if pc.attributeQuery('neckHead', n=sel[0], ex=True):
        neck_main_placer = pc.getAttr(sel[0] + '.neckHead')
        neck_module_lists = List.seperate(neck_main_placer)
        for n in neck_module_lists:
            if n:
                parent = get_parent_attr_module_components(n)
                pc.select(n, r=True)
                bSkelLib.buildNeckHeadJointSkeleton(parent)

                if pc.progressWindow('buildSkeletonProgress', q=True, isCancelled=True):
                    pc.progressWindow('buildSkeletonProgress', endProgress=True)
                    pc.undoInfo(state=True)
                    return
                pc.progressWindow('buildSkeletonProgress', e=True, step=1,
                                  status=('building module skeleton on : ' + n))


def build_leg(sel):
    if pc.attributeQuery('leg', n=sel[0], ex=True):
        leg_main_placer = pc.getAttr(sel[0] + '.leg')
        leg_module_lists = List.seperate(leg_main_placer)
        for l in leg_module_lists:
            if l:
                parent = get_parent_attr_module_components(l)
                pc.select(l, r=True)
                bSkelLib.buildLegJointSkeleton(parent)

                if pc.progressWindow('buildSkeletonProgress', q=True, isCancelled=True):
                    pc.progressWindow('buildSkeletonProgress', endProgress=True)
                    pc.undoInfo(state=True)
                    return
                pc.progressWindow('buildSkeletonProgress', e=True, step=1,
                                  status=('building module skeleton on : ' + l))


def build_arm(sel):
    if pc.attributeQuery('arm', n=sel[0], ex=True):
        arm_main_placer = pc.getAttr(sel[0] + '.arm')
        arm_module_lists = List.seperate(arm_main_placer)
        for a in arm_module_lists:
            if a:
                parent = get_parent_attr_module_components(a)
                pc.select(a, r=True)
                bSkelLib.buildArmJointSkeleton(parent)

                if pc.progressWindow('buildSkeletonProgress', q=True, isCancelled=True):
                    pc.progressWindow('buildSkeletonProgress', endProgress=True)
                    pc.undoInfo(state=True)
                    return
                pc.progressWindow('buildSkeletonProgress', e=True, step=1,
                                  status=('building module skeleton on : ' + a))


def build_tentacle(sel):
    if pc.attributeQuery('tentacle', n=sel[0], ex=True):
        tentacle_main_placer = pc.getAttr(sel[0] + '.tentacle')
        tentacle_module_lists = List.seperate(tentacle_main_placer)

        for t in tentacle_module_lists:
            if t:
                parent = get_parent_attr_module_components(t)
                pc.select(t, r=True)
                bSkelLib.buildTentacleJointSkeleton(parent)

                if pc.progressWindow('buildSkeletonProgress', q=True, isCancelled=True):
                    pc.progressWindow('buildSkeletonProgress', endProgress=True)
                    pc.undoInfo(state=True)
                    return
                pc.progressWindow('buildSkeletonProgress', e=True, step=1,
                                  status=('building module skeleton on : ' + t))
