import pymel.core as pc

from ...Utils.CharUtilsLib import rigSideSep
from ..ModuleSymmetryLib import buildBodyModuleSymmetry
from ..ModuleSymmetryLib import buildLegModuleSymmetry
from ..ModuleSymmetryLib import buildArmModuleSymmetry
from ...Core import ModuleTemplates as mt
from ...Core import ModuleSymmetryLib as msLib
from ...Core import Dummy as Dummy


def buildArmDummySkeletonModulePreCMD():
    name = pc.textField('nameModuleTF', q=True, tx=True)
    side = pc.optionMenu('sideModulePrefix', q=True, v=True)
    numJoints = pc.intField('noArmLimbsJointsISG', q=True, v=True)
    fingers = pc.checkBox('armFingersChk', q=True, v=True)
    numFingers = pc.intField('noArmFingersJointISG', q=True, v=True)
    numSegment = pc.intField('noArmFingersSegJointISG', q=True, v=True)
    leftColorIndex = pc.colorIndexSliderGrp('leftColorIndexClSG', q=True, v=True)
    rightColorIndex = pc.colorIndexSliderGrp('rightColorIndexClSG', q=True, v=True)
    symm = pc.checkBox('armSymmetryChk', q=True, v=True)

    colorIndex = 0
    sideQ = []
    sideDef = pc.radioButtonGrp('armModuleSideRdBnGrp', q=True, sl=True)
    customSide = ''

    if side == 'none':
        pc.error('You must select side to create this module....')

    if side == 'custom':
        result = pc.promptDialog(title='Custom Side Seprated By /', 
                                 message='Enter Name:', 
                                 text='_/_', 
                                 button=['OK','Cancel'],
                                 defaultButton='OK', 
                                 cancelButton='Cancel', 
                                 dismissString='Cancel')
        if result == 'Cancel':
            pc.error('operation canceled')
        
        if result == 'OK':
            customSide = pc.promptDialog(query=True, text=True)
            sideQ = rigSideSep(customSide)
            if sideDef == 1:
                side = sideQ[0]
                colorIndex = leftColorIndex
            else:
                side = sideQ[1]
                colorIndex = rightColorIndex

    elif side != 'none':
        sideQ = rigSideSep(side)
        if sideDef == 1:
            side = sideQ[0]
            colorIndex = leftColorIndex
        else:
            side = sideQ[1]
            colorIndex = rightColorIndex
    else:
        side = ''
    if name != '':
        name = (name + '_')

    Dummy.Arm(name, side, numJoints, fingers, numFingers, numSegment, (colorIndex-1))

    if sideDef==2 and symm==0:
        msLib.mirrorModuleTemplates (name+side+'armPlacer_loc')

    if symm:
        symmSide = ''
        if sideDef == 1:
            symmSide = sideQ[1]
            colorIndex = rightColorIndex
        else:
            symmSide = sideQ[0]
            colorIndex = leftColorIndex

        Dummy.Arm(name, symmSide, numJoints, fingers, numFingers, numSegment, (colorIndex-1))

        if sideDef == 1:
            master = (name+side+'armPlacer_loc')
            slave = (name+symmSide+'armPlacer_loc')
            buildArmModuleSymmetry(master,slave)
        else:
            master = (name+symmSide+'armPlacer_loc')
            slave = (name+side+'armPlacer_loc')
            buildArmModuleSymmetry(master,slave)

def build_leg_dummy_skeleton_module_pre_cmd():
    name = pc.textField('nameModuleTF', q=True, tx=True)
    side = pc.optionMenu('sideModulePrefix', q=True, v=True)
    numJoints = pc.intField('noLegLimbsJointsISG', q=True, v=True)
    fingers = pc.checkBox('legFingersChk', q=True, v=True)
    numFingers = pc.intField('noLegFingersJointISG', q=True, v=True)
    numSegment = pc.intField('noLegFingersSegJointISG', q=True, v=True)
    leftColorIndex = pc.colorIndexSliderGrp('leftColorIndexClSG', q=True, v=True)
    rightColorIndex = pc.colorIndexSliderGrp('rightColorIndexClSG', q=True, v=True)
    symm = pc.checkBox('legSymmetryChk', q=True, v=True)

    colorIndex = 0
    sideQ = []
    sideDef = pc.radioButtonGrp('legModuleSideRdBnGrp', q=True, sl=True)
    customSide = ''

    if side == 'none':
        pc.error('You must select side to create this module....')

    if side == 'custom':
        result = pc.promptDialog(title='Custom Side Seprated By /',message='Enter Name:',text='_/_',button=['OK','Cancel'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
        if result == 'Cancel':
            pc.error('operation canceled')
        if result == 'OK':
            customSide = pc.promptDialog(query=True, text=True)
            sideQ = rigSideSep(customSide)
            if sideDef == 1:
                side = sideQ[0]
                colorIndex = leftColorIndex
            else:
                side = sideQ[1]
                colorIndex = rightColorIndex
    elif side != 'none':
        sideQ = rigSideSep(side)
        if sideDef == 1:
            side = sideQ[0]
            colorIndex = leftColorIndex
        else:
            side = sideQ[1]
            colorIndex = rightColorIndex
    else:
        side = ''

    if name != '':
        name = (name + '_')

    result = pc.confirmDialog(title='Build Module',message='Define leg Module type?',messageAlign='center',button=['Biped','Quadroped'],defaultButton='Biped')

    if result == 'Quadroped' and numJoints<4:
        pc.error('you must define minimum 4 joints for Quadroped leg module...')

    if result == 'Biped':
        Dummy.Leg.Biped(name, side, numJoints, fingers, numFingers, numSegment, (colorIndex - 1))
    if result == 'Quadroped':
        Dummy.Leg.Quadruped(name, side, numJoints, fingers, numFingers, numSegment, (colorIndex - 1))

    if sideDef==2 and symm==0:
        msLib.mirrorModuleTemplates(name+side+'legPlacer_loc')

    if symm:
        symmSide = ''
        if sideDef == 1:
            symmSide = sideQ[1]
            colorIndex = rightColorIndex
        else:
            symmSide = sideQ[0]
            colorIndex = leftColorIndex

        if result == 'Biped':
            Dummy.Leg.Biped(name, symmSide, numJoints, fingers, numFingers, numSegment, (colorIndex - 1))
        # TODO: correct spelling for this, should be Quadruped
        if result == 'Quadroped':
            Dummy.Leg.Quadruped(name, symmSide, numJoints, fingers, numFingers, numSegment, (colorIndex - 1))

        if sideDef == 1:
            master = (name+side+'legPlacer_loc')
            slave = (name+symmSide+'legPlacer_loc')
            buildLegModuleSymmetry(master, slave)
        else:
            master = (name+symmSide+'legPlacer_loc')
            slave = (name+side+'legPlacer_loc')
            buildLegModuleSymmetry(master, slave)

def buildSpineDummySkeletonModulePreCMD():
    name = pc.textField('nameModuleTF', q=True, tx=True)
    side = pc.optionMenu('sideModulePrefix', q=True, v=True)
    moduleName = pc.textField('spineTemplateTF', q=True, tx=True)
    numCon = pc.intField('noSpineConIF', q=True, v=True)
    axis = pc.optionMenu('spineAxisOM', q=True, v=True)
    dis = pc.intField('disSpineConIF', q=True, v=True)
    cenColorIndex = pc.colorIndexSliderGrp('centerColorIndexClSG', q=True, v=True)
    leftColorIndex = pc.colorIndexSliderGrp('leftColorIndexClSG', q=True, v=True)
    rightColorIndex = pc.colorIndexSliderGrp('rightColorIndexClSG', q=True, v=True)

    colorIndex = 0
    symm = pc.checkBox('spineSymmetryChk', q=True, v=True)

    sideQ = rigSideSep(side)
    sideDef = 1

    if symm:
        if side == 'none':
            pc.error('You must select side in Symmtery mode....')
        if side == 'custom':
            result = pc.promptDialog(title='Custom Side Seprated By /',message='Enter Name:',text='_/_',button=['OK','Cancel'],defaultButton='OK',cancelButton='Cancel',dismissStrin='Cancel')
            if result == 'Cancel':
                pc.error('operation canceled')
                
            if result == 'OK':
                customSide = pc.promptDialog(query=True, text=True)
                sideQ = rigSideSep(customSide)
                if sideDef == 1:
                    side = sideQ[0]
                    colorIndex = leftColorIndex
                else:
                    side = sideQ[1]
                    colorIndex = rightColorIndex
        else:
            if sideDef == 1:
                side = sideQ[0]
            else:
                side = sideQ[1]
            colorIndex = leftColorIndex 
    else:
        side = ''
        colorIndex = cenColorIndex
    if name != '':
        name = (name + '_')

    Dummy.Spine(name, side, moduleName, numCon, axis, dis, (colorIndex-1))
    if symm:
        Dummy.Spine(name, sideQ[1], moduleName, numCon, axis, dis, (rightColorIndex-1))
        master = (name+side+moduleName+'Main_ctrl') 
        slave = (name+sideQ[1]+moduleName+'Main_ctrl')
        buildBodyModuleSymmetry(master,slave)

def build_head_neck_dummy_skeleton_module_pre_cmd():
    name = pc.textField('nameModuleTF', q=True, tx=True)
    side = pc.optionMenu('sideModulePrefix', q=True, v=True)
    moduleName = pc.textField('neckTemplateTF', q=True, tx=True)
    numCon = pc.intField('noNeckConIF', q=True, v=True)
    axis = pc.optionMenu('neckAxisOM', q=True, v=True)
    dis = pc.intField('disNeckConIF', q=True, v=True)
    cenColorIndex = pc.colorIndexSliderGrp('centerColorIndexClSG', q=True, v=True)
    leftColorIndex = pc.colorIndexSliderGrp('leftColorIndexClSG', q=True, v=True)
    rightColorIndex = pc.colorIndexSliderGrp('rightColorIndexClSG', q=True, v=True)

    colorIndex = 0

    symm = pc.checkBox('neckSymmetryChk', q=True, v=True)

    sideQ = rigSideSep(side)
    sideDef = 1
    
    if symm:
        if side == 'none':
            pc.error('You must select side in Symmtery mode....')
        if side == 'custom':
            result = pc.promptDialog(title='Custom Side Seprated By /',message='Enter Name:',text='_/_',button=['OK','Cancel'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
            if result == 'Cancel':
                pc.error('operation canceled')

            if result == 'OK':
                customSide = pc.promptDialog(query=True, text=True)
                sideQ = rigSideSep(customSide)
                if sideDef == 1:
                    side = sideQ[0]
                    colorIndex = leftColorIndex
                else:
                    side = sideQ[1]
                    colorIndex = rightColorIndex
        else:
            if sideDef == 1:
                side = sideQ[0]
            else:
                side = sideQ[1]
            colorIndex = leftColorIndex	
    else:        
        side = ''        
        colorIndex = cenColorIndex
        if name != '':
            name = (name + '_')

    Dummy.HeadNeck(name, side, moduleName, numCon, axis, dis, (colorIndex-1))
    if symm:
        Dummy.HeadNeck(name, sideQ[1], moduleName, numCon, axis, dis, (rightColorIndex-1))
        master = (name+side+moduleName+'Main_ctrl') 
        slave = (name+sideQ[1]+moduleName+'Main_ctrl')
        buildBodyModuleSymmetry(master,slave)

def buildTentacleDummySkeletonModulePreCMD():
    name = pc.textField('nameModuleTF', q=True, tx=True)
    side = pc.optionMenu('sideModulePrefix', q=True, v=True)
    moduleName = pc.textField('tentacleTemplateTF', q=True, tx=True)
    numCon = pc.intField('noTentacleConIF', q=True, v=True)
    axis = pc.optionMenu('tentacleAxisOM', q=True, v=True)
    dis = pc.intField('disTentacleConIF', q=True, v=True)
    cenColorIndex = pc.colorIndexSliderGrp('centerColorIndexClSG', q=True, v=True)
    leftColorIndex = pc.colorIndexSliderGrp('leftColorIndexClSG', q=True, v=True)
    rightColorIndex = pc.colorIndexSliderGrp('rightColorIndexClSG', q=True, v=True)

    colorIndex = 0

    symm = pc.checkBox('tentacleSymmetryChk', q=True, v=True)

    sideQ = rigSideSep(side)
    sideDef = 1

    if symm:
        if side == 'none':
            pc.error('You must select side in Symmtery mode....')
        if side == 'custom':
            result = pc.promptDialog(title='Custom Side Seprated By /',message='Enter Name:',text='_/_',button=['OK','Cancel'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
            if result == 'Cancel':
                pc.error('operation canceled')

            if result == 'OK':
                customSide = pc.promptDialog(query=True, text=True)
                sideQ = rigSideSep(customSide)
                if sideDef == 1:
                    side = sideQ[0]
                    colorIndex = leftColorIndex
                else:
                    side = sideQ[1]
                    colorIndex = rightColorIndex
        else:
            if sideDef == 1:
                side = sideQ[0]
            else:
                side = sideQ[1]
            colorIndex = leftColorIndex
    else:
        side = ''
        colorIndex = cenColorIndex
        if name != '':
            name = (name + '_')

    Dummy.Tentacle(name, side, moduleName, numCon, axis, dis, (colorIndex-1))
    if symm:
        Dummy.Tentacle(name, sideQ[1], moduleName, numCon, axis, dis, (rightColorIndex-1))
        master = (name+side+moduleName+'Main_ctrl') 
        slave = (name+sideQ[1]+moduleName+'Main_ctrl')
        buildBodyModuleSymmetry(master,slave)

def buildFingerDummySkeletonModulePreCMD():
    name = pc.textField('nameModuleTF', q=True, tx=True)
    side = pc.optionMenu('sideModulePrefix', q=True, v=True)
    fingerName = pc.textField('fingerTemplateTF', q=True, tx=True)
    numCon = pc.intField('noFingerConIF', q=True, v=True)
    axis = pc.optionMenu('fingerAxisOM', q=True, v=True)
    dis = pc.intField('disFingerConIF', q=True, v=True)
    cenColorIndex = pc.colorIndexSliderGrp('centerColorIndexClSG', q=True, v=True)
    leftColorIndex = pc.colorIndexSliderGrp('leftColorIndexClSG', q=True, v=True)
    rightColorIndex = pc.colorIndexSliderGrp('rightColorIndexClSG', q=True, v=True)

    colorIndex = 0

    symm = pc.checkBox('fingerSymmetryChk', q=True, v=True)

    sideQ = rigSideSep(side)
    sideDef = 1

    if symm:
        if side == 'none':
            pc.error('You must select side in Symmtery mode....')
        if side == 'custom':
            result = pc.promptDialog(title='Custom Side Seprated By /',message='Enter Name:',text='_/_',button=['OK','Cancel'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
            if result == 'Cancel':
                pc.error('operation canceled')
            
            if result == 'OK':
                customSide = pc.promptDialog(query=True, text=True)
                sideQ = rigSideSep(customSide)
                if sideDef == 1:
                    side = sideQ[0]
                    colorIndex = leftColorIndex
                else:
                    side = sideQ[1]
                    colorIndex = rightColorIndex
        else:
            if sideDef == 1:
                side = sideQ[0]
            else:
                side = sideQ[1]
            colorIndex = leftColorIndex 
    else:
        side = ''
        colorIndex = cenColorIndex
        if name != '':
            name = (name + '_')

    Dummy.Fingers(name, fingerName, side, numCon, axis, dis, (colorIndex-1))
    if symm:
        Dummy.Fingers(name, fingerName, sideQ[1], numCon, axis, dis, (rightColorIndex-1))
        master = (name+side+fingerName+'Main_ctrl')
        slave = (name+sideQ[1]+fingerName+'Main_ctrl')
        buildBodyModuleSymmetry(master,slave)

def buildBipedModulePreCMD():
    name = pc.textField('nameModuleTF', q=True, tx=True)
    spineCount = pc.intField('noBipedSpineJointsISG', q=True, v=True)
    neckCount = pc.intField('noBipedNeckJointsISG', q=True, v=True)
    finger = pc.checkBox('bipedFingersChk', q=True, v=True)
    numFinger = pc.intField('noBipedFingersJointISG', q=True, v=True)
    toe = pc.checkBox('bipedToesChk', q=True, v=True)
    numToe = pc.intField('noBipedToesJointISG', q=True, v=True)
    
    mt.bipedModuleTemplate(name, spineCount, neckCount, finger, numFinger, toe, numToe)

def buildQuadModulePreCMD():
    name = pc.textField('nameModuleTF', q=True, tx=True)
    spineCount = pc.intField('noQuadSpineJointsISG', q=True, v=True)
    neckCount = pc.intField('noQuadNeckJointsISG', q=True, v=True)
    earCount = pc.intField('noQuadEarsJointsISG', q=True, v=True)
    tailCount = pc.intField('noQuadTailJointsISG', q=True, v=True)
    toe = pc.checkBox('bipedToesChk', q=True, v=True)
    numToe = pc.intField('noBipedToesJointISG', q=True, v=True)
    
    mt.quadModuleTemplate(name, spineCount, neckCount, earCount, tailCount,  toe, numToe)