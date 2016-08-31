import pymel.core as pc
import BuildModuleJointSkeletonLib as bSkelLib
from ..Utils import List as List
from ..Utils.String import objGetPrefix


def getParentAttrModuleComponants(obj):
    parentGrp = ''
    strip = ''
    parent = ''    
    if pc.attributeQuery('parent', n=obj, ex=True):
        parentGrp = pc.getAttr(obj+'.parent')
        strip = objGetPrefix(parentGrp)
        parent = (strip + '_jnt')		
    return parent


def buildModuleSkeleton():
    sel = pc.ls(sl=True)
    if len(sel) <= 0:
        pc.select('worldPos_loc')
        sel = pc.ls(sl=True)

    if len(sel) > 0:
        result = pc.confirmDialog(title='Build Skeleton',
                                  message='The current operation will convert all different modules into actual Joints and prepare skeleton for animation rig installation.\n\nAre you sure you want continue?',
                                  messageAlign='center',
                                  button=['OK', 'Cancel'],
                                  defaultButton='OK',
                                  cancelButton='Cancel',
                                  dismissString='Cancel')
        if result == 'Cancel':
            pc.error('operation canceled')

        if result == 'OK':
            buildConfirmed(sel)            
    else:
        pc.error('wordPos_loc could not be found')


def buildConfirmed(sel):
    pc.hide(sel[0])
    
    # This is only being used to get the amount of modules for the sake of keeping progress
    moduleInf = List.seperate(getModuleList(sel))
    pc.progressWindow('buildSkeletonProgress', t='building Skeleton', progress=0, status='building skeleton from modules :', min=0, max=len(moduleInf), isInterruptable=True)

    buildSpine(sel)
    buildNeckHead(sel)
    buildLeg(sel)
    buildArm(sel)
    buildTentacle(sel)

    pc.delete(sel[0])
    pc.progressWindow('buildSkeletonProgress',endProgress=True)


def getModuleList(sel):
    moduleList = ''
    if pc.attributeQuery('spine', n=sel[0], ex=True):
        spineModule = pc.getAttr(sel[0]+'.spine')
        moduleList = moduleList = (spineModule+' ')

    if pc.attributeQuery('neckHead', n=sel[0], ex=True):
        neckModule = pc.getAttr(sel[0]+'.neckHead')
        moduleList = moduleList + (neckModule+' ')

    if pc.attributeQuery('arm', n=sel[0], ex=True):
        armModule = pc.getAttr(sel[0]+'.arm')
        moduleList = moduleList + (armModule+' ')

    if pc.attributeQuery('leg', n=sel[0], ex=True):
        legModule = pc.getAttr(sel[0]+'.leg')
        moduleList = moduleList + (legModule+' ')

    if pc.attributeQuery('tentacle', n=sel[0], ex=True):
        tentacleModule = pc.getAttr(sel[0]+'.tentacle')
        moduleList = moduleList + (tentacleModule+' ')
    return moduleList


def buildSpine(sel):
    if pc.attributeQuery('spine', n=sel[0], ex=True):
        spineMainPlacer = pc.getAttr(sel[0]+'.spine')
        spineModuleLists = List.seperate(spineMainPlacer)
        for s in spineModuleLists:
            if s:
                parent = getParentAttrModuleComponants(s)                
                pc.select(s, r=True)
                bSkelLib.buildSpineJointSkeleton(parent)

                if pc.progressWindow('buildSkeletonProgress', q=True, isCancelled=True):
                    pc.progressWindow('buildSkeletonProgress', endProgress=True)
                    pc.undoInfo(state=True)
                    return
                pc.progressWindow('buildSkeletonProgress',e=True, step=1, status=('building module skeleton on : '+s))


def buildNeckHead(sel):
    if pc.attributeQuery('neckHead', n=sel[0], ex=True):
        neckMainPlacer = pc.getAttr(sel[0]+'.neckHead')
        neckModuleLists = List.seperate(neckMainPlacer)
        for n in neckModuleLists:
            if n:
                parent = getParentAttrModuleComponants(n)
                pc.select(n, r=True)
                bSkelLib.buildNeckHeadJointSkeleton(parent)

                if pc.progressWindow('buildSkeletonProgress', q=True, isCancelled=True):
                    pc.progressWindow('buildSkeletonProgress', endProgress=True)
                    pc.undoInfo(state=True)
                    return
                pc.progressWindow('buildSkeletonProgress',e=True, step=1, status=('building module skeleton on : '+n))


def buildLeg(sel):
    if pc.attributeQuery('leg', n=sel[0], ex=True):
        legMainPlacer = pc.getAttr(sel[0]+'.leg')
        legModuleLists = List.seperate(legMainPlacer)
        for l in legModuleLists:
            if l:
                parent = getParentAttrModuleComponants(l)
                pc.select(l, r=True)
                bSkelLib.buildLegJointSkeleton(parent)

                if pc.progressWindow('buildSkeletonProgress', q=True, isCancelled=True): 
                    pc.progressWindow('buildSkeletonProgress', endProgress=True)
                    pc.undoInfo(state=True)
                    return
                pc.progressWindow('buildSkeletonProgress',e=True, step=1, status=('building module skeleton on : '+l))


def buildArm(sel):
    if pc.attributeQuery('arm', n=sel[0], ex=True):
        armMainPlacer = pc.getAttr(sel[0]+'.arm')
        armModuleLists = List.seperate(armMainPlacer)
        for a in armModuleLists:
            if a:
                parent = getParentAttrModuleComponants(a)
                pc.select(a, r=True)
                bSkelLib.buildArmJointSkeleton(parent)
                
                if pc.progressWindow('buildSkeletonProgress',q=True, isCancelled=True):
                    pc.progressWindow('buildSkeletonProgress',endProgress=True)
                    pc.undoInfo(state=True)
                    return
                pc.progressWindow('buildSkeletonProgress',e=True, step=1, status=('building module skeleton on : '+a))


def buildTentacle(sel):
    if pc.attributeQuery('tentacle', n=sel[0], ex=True):
        tentacleMainPlacer = pc.getAttr(sel[0]+'.tentacle')
        tentacleModuleLists = List.seperate(tentacleMainPlacer)

        for t in tentacleModuleLists:
            if t:
                parent = getParentAttrModuleComponants(t)
                pc.select(t, r=True)
                bSkelLib.buildTentacleJointSkeleton(parent)
                                
                if pc.progressWindow('buildSkeletonProgress', q=True, isCancelled=True):
                    pc.progressWindow('buildSkeletonProgress', endProgress=True) 
                    pc.undoInfo(state=True)
                    return
                pc.progressWindow('buildSkeletonProgress', e=True, step=1, status=('building module skeleton on : '+t))
