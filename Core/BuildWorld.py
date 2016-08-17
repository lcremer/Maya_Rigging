import pymel.core as pc

from RiggingSystem.Utils import CurveUtilLib as cuUL
from RiggingSystem.Utils import CharUtilsLib as chUL

def buildWorld(name, scale, controlColor = ''):
    worldAControl = [(name + 'worldA_ctrl')]
    worldBControl = [(name + 'worldB_ctrl')]
    controlGrp = []    

    if not pc.objExists(worldAControl[0]):
        masterControl = pc.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=7, d=3, ut=0, tol=0.001, s=8, ch=0, n=(name + 'worldA_ctrl'))
        worldAControl[0] = masterControl
        cuUL.resizeCurves(None, 1, 1, 1, scale)
        color_control(masterControl[0], controlColor)

    if pc.objExists(worldBControl[0]):
        controlGrp.append((name + 'controls_grp'))
        controlGrp.append((name + 'skeletons_grp'))
    else:
        worldBControl = pc.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=5.5, d=3, ut=0, tol=0.001, s=8, ch=0, n=(name + 'worldB_ctrl'))

        cuUL.resizeCurves(None, 1, 1, 1, scale)
        pc.parent(worldBControl[0], worldAControl[0])
        rigGrp = pc.group(em=True, n=(name + 'rig'))
        chUL.lockAndHide(rigGrp, 'locknHide', 'trans rot scale')
        
        pc.parent(worldAControl[0], rigGrp)
        
        controlGrp.append(pc.group(em=True, n=(name + 'controls_grp')))
        chUL.lockAndHide(controlGrp[0],'locknHide','trans rot scale')
        controlGrp.append(pc.group(em=True, n=(name + 'skeletons_grp')))
        pc.setAttr((controlGrp[1]+'.overrideEnabled'),1)
        pc.setAttr((controlGrp[1]+'.overrideDisplayType'),2)
        chUL.lockAndHide(controlGrp[1],'locknHide','trans rot scale')
        pc.parent(controlGrp[0],controlGrp[1],worldBControl[0])
        scaleNode = createScaleGrp(name)
        pc.scaleConstraint(worldBControl, scaleNode, offset=(1,1,1), weight=1)

        color_control(worldBControl[0], controlColor)
    
    return controlGrp

def createNonScaleGrp(name):
    nonScaleGrp = (name+'non_scale_grp')
    if not pc.objExists(nonScaleGrp):
        nonScaleGrp = pc.group(em=True, n=(name+'non_scale_grp'))
        if pc.objExists(name+'rig'):
            pc.parent(nonScaleGrp, (name+'rig'))

    return nonScaleGrp

def createScaleGrp(name):
    scaleNode = (name+'worldScaleCon_grp')
    nonScaleGrp = createNonScaleGrp(name)
    if not pc.objExists(scaleNode):
        pc.group(em=True, n=(name+'worldScaleCon_grp'))
        pc.parent(scaleNode, nonScaleGrp)
    return scaleNode


def color_control(c, controlColor):
    if controlColor != '':
        try:
            c.overrideEnabled.set(True)
            c.overrideColor.set(controlColor)
        except:
            pass
        try:
            c.getShape().overrideEnabled.set(True)
            c.getShape().overrideColor.set(controlColor)
        except:
            pass