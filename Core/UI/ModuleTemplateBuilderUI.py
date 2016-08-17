import pymel.core as pc

import CreateModuleRigFromUI as cRig
import BuildModulesFromUI as bm
from RiggingSystem.Core import AutoRig as ar
from RiggingSystem.Utils import AttrUtil as atu
from RiggingSystem.Utils import CurveUtil as cu
from RiggingSystem.Utils import CharUtilsLib as chUL
from RiggingSystem.Core import ModuleSymmetryLib as msL
from RiggingSystem.Core import BuildModuleJointSkeleton as bmjs

def ModuleTemplateUI():
    if pc.window('moduleTemplatesWin',exists=True):
        pc.deleteUI('moduleTemplatesWin')

    moduleTemplatesWin = pc.window('moduleTemplatesWin',t='autoRig: Modules Builder',wh=(450,630),mxb=False,mnb=True,resizeToFitChildren=True,sizeable=True,menuBar=True)

    # option menu
    pc.menu(label='File')
    pc.menuItem(divider=True)
    pc.menuItem(label='Close', c=pc.Callback(pc.deleteUI,moduleTemplatesWin))
    
    pc.menu(label='Edit')
    pc.menuItem(label='Toggle Selectable', c=pc.Callback(bm.buildQuadModulePreCMD))
    pc.menuItem(label='Select Skin Joint', c=pc.Callback(chUL.selectSkinJoints))
    pc.menuItem(divider=True)
    
    pc.menu(label='Tools')
    pc.menuItem(label='Auto Rigger', c=pc.Callback(ar.AutoRigUI))
    pc.menuItem(divider=True)
    pc.menuItem(label='Curve Utilities', c=pc.Callback(cu.CurveUtilUI))
        
    moduleTempalesMainColoumn = pc.columnLayout('moduleTempalesMainColoumn', adj=1, p=moduleTemplatesWin)
    moduleRigTab = pc.tabLayout('moduleRigTab', innerMarginWidth=5, innerMarginHeight=5, p=moduleTempalesMainColoumn)

    createSkColumnLayout = pc.columnLayout('createSkColumnLayout', adj=1, p=moduleRigTab)
    modulePartTab = pc.tabLayout('modulePartTab', innerMarginWidth=5, innerMarginHeight=5, p=createSkColumnLayout)

    mainColumnLayout = pc.columnLayout('mainColumnLayout', adj=1, p=modulePartTab)

    # name prefix
    prefixModuleFrame = pc.frameLayout('prefixModuleFrame', l='Prefix: ',collapsable=False,collapse=False,borderStyle='etchedOut',marginHeight=3,marginWidth=3,p=mainColumnLayout)

    prefixColumnLayout = pc.columnLayout('prefixColumnLayout',adj=1, p=prefixModuleFrame)

    nameModuleRCL = pc.rowColumnLayout('nameModuleRCL',nc=4,cw=[(1,50),(2,90),(3,100),(4,100)],p=prefixColumnLayout)
    nameModuleTitle = pc.text('nameModuleTitle',l='Name :', align='left', p=nameModuleRCL)
    nameModuleTF = pc.textField('nameModuleTF', p=nameModuleRCL)

    sideModuleText = pc.text('sideModuleText', label='      Side : ', al='center', p=nameModuleRCL)
    sideModulePrefix = pc.optionMenu('sideModulePrefix', p=nameModuleRCL)  # select side prefix menu
    pc.menuItem(label='l/r')
    pc.menuItem(label='lt/rt')
    pc.menuItem(label='left/right')
    pc.menuItem(label='custom')
    pc.menuItem(label='none')

    colorIndexSep1 = pc.separator('colorIndexSep1',height=7,style='none',p=prefixColumnLayout)
    colorIndexTitle = pc.text('colorIndexTitle', l='Color:', align='left', fn='boldLabelFont', p=prefixColumnLayout)

    colorIndexModuleRCL = pc.rowColumnLayout('colorIndexModuleRCL', nc=3, cw=[(1,137),(2,137),(3,137)], p=prefixColumnLayout)
    rightColorIndexTitle = pc.text('rightColorIndexTitle', l='Right', align='center', p=colorIndexModuleRCL)
    centerColorIndexTitle = pc.text('centerColorIndexTitle', l='Center', align='center', p=colorIndexModuleRCL)
    leftColorIndexTitle = pc.text('leftColorIndexTitle', l='Left', align='center', p=colorIndexModuleRCL )

    rightColorIndexClSG = pc.colorIndexSliderGrp('rightColorIndexClSG', min=1, max=31, value=16, columnWidth=[(1,37),(2,100)], p=colorIndexModuleRCL)
    centerColorIndexClSG = pc.colorIndexSliderGrp('centerColorIndexClSG ', min=1, max=31, value=8, columnWidth=[(1,37),(2,100)], p=colorIndexModuleRCL)
    leftColorIndexClSG = pc.colorIndexSliderGrp('leftColorIndexClSG', min=1, max=31, value=11, columnWidth=[(1,37),(2,100)], p=colorIndexModuleRCL)

    prefixTemplateSep1 = pc.separator('prefixTemplateSep1', height=7, style='none', p=mainColumnLayout)

    mainScrollLayout = pc.scrollLayout('mainScrollLayout', h=285, verticalScrollBarThickness=16, p=mainColumnLayout)
    mainModuleRCL = pc.rowColumnLayout('mainModuleRCL', nc=2, cw=[(1,125),(2,275)], p=mainScrollLayout)

    hgt = 135

    armModuleFrame = pc.frameLayout('armModuleFrame', l=' Arm',collapsable=False,collapse=False,borderStyle='etchedOut',h=hgt,marginHeight=3,marginWidth=3,p=mainModuleRCL)
    # TODO: remove or replace .bmp icons
    armTempModuleBtn = pc.symbolButton('armTempModuleBtn', h=80, i='armModule.bmp', c=pc.Callback(bm.buildArmDummySkeletonModulePreCMD), p=armModuleFrame)

    armOpModuleFrame = pc.frameLayout('armOpModuleFrame', l=' options:',collapsable=False,collapse=False,borderStyle='etchedOut',h=hgt,marginHeight=3,marginWidth=3,p=mainModuleRCL)

    armOpModuleForm = pc.formLayout('armOpModuleForm', p=armOpModuleFrame)

    noArmLimbsJointsTitle = pc.text('noArmLimbsJointsTitle', l='joints:  ', al='right')
    noArmLimbsJointsISG = pc.intField('noArmLimbsJointsISG', minValue=3, maxValue=10, value=3, s=1)

    armFingersTitle = pc.text('armFingersTitle', l='fingers:  ', al='right')
    armFingersChk = pc.checkBox('armFingersChk', l='', v=1, cc=pc.Callback(armFingersModuleSwitch))

    noArmFingersJointsTitle = pc.text('noArmFingersJointsTitle', l='no:  ', al='right')
    noArmFingersJointISG = pc.intField('noArmFingersJointISG', minValue=0, maxValue=5, value=5, s=4)

    noArmFingersSegJointsTitle = pc.text('noArmFingersSegJointsTitle', l='segment:  ', al='right')
    noArmFingersSegJointISG = pc.intField('noArmFingersSegJointISG', minValue=2, maxValue=10, value=4, s=1)

    armSymmetryTitle = pc.text('armSymmetryTitle', l='symmetry:  ', al='right')
    armSymmetryChk = pc.checkBox('armSymmetryChk', l='', v=0)

    armSep1 = pc.separator('armSep1', height=5, style='out')

    armModuleSideTitle = pc.text('armModuleSideTitle', l='Side:  ', align='left')
    armModuleSideRdBnGrp = pc.radioButtonGrp('armModuleSideRdBnGrp', nrb=2,  la2=['L','R'], cw2=[30,30], sl=1) 

    armSF = pc.scrollField('armSF', wordWrap=True, text='creates arm skeleton template setup. ideal use: any arm Humans, Insects..', editable=False)

    pc.formLayout(armOpModuleForm, e=True, af=[(noArmLimbsJointsTitle,'top',5),(noArmLimbsJointsTitle,'left',0)],ap=[(noArmLimbsJointsTitle,'right',0,15)])
    pc.formLayout(armOpModuleForm, e=True, ac=[(noArmLimbsJointsISG,'top',5,noArmLimbsJointsTitle)],af=[(noArmLimbsJointsISG,'left',0)],ap=[(noArmLimbsJointsISG,'right',0,10)])

    pc.formLayout(armOpModuleForm, e=True, af=[(armFingersTitle,'top',5)],ac=[(armFingersTitle,'left',0,noArmLimbsJointsTitle)],ap=[(armFingersTitle,'right',0,35)])
    pc.formLayout(armOpModuleForm, e=True, ac=[(armFingersChk,'top',5,armFingersTitle),(armFingersChk,'left',25,noArmLimbsJointsISG)],ap=[(armFingersChk,'right',0,35)])
    pc.formLayout(armOpModuleForm, e=True, af=[(noArmFingersJointsTitle,'top',5)],ac=[(noArmFingersJointsTitle,'left',0,armFingersTitle)],ap=[(noArmFingersJointsTitle,'right',0,47)])	
    pc.formLayout(armOpModuleForm, e=True, ac=[(noArmFingersJointISG,'top',5,noArmFingersJointsTitle),(noArmFingersJointISG,'left',7,armFingersChk)],ap=[(noArmFingersJointISG,'right',0,45)])

    pc.formLayout(armOpModuleForm, e=True, af=[(noArmFingersSegJointsTitle,'top',5)], ac=[(noArmFingersSegJointsTitle,'left',0,noArmFingersJointsTitle)],ap=[(noArmFingersSegJointsTitle,'right',0,75)])
    pc.formLayout(armOpModuleForm, e=True, ac=[(noArmFingersSegJointISG,'top',5,noArmFingersSegJointsTitle),(noArmFingersSegJointISG,'left',20,noArmFingersJointISG)],ap=[(noArmFingersSegJointISG,'right',0,65)])

    pc.formLayout(armOpModuleForm, e=True, af=[(armSymmetryTitle,'top',5)],ac=[(armSymmetryTitle,'left',0,noArmFingersSegJointsTitle)],ap=[(armSymmetryTitle,'right',0,100)])
    pc.formLayout(armOpModuleForm, e=True, ac=[(armSymmetryChk,'top',5,armFingersTitle),(armSymmetryChk,'left',35,noArmFingersSegJointISG)],ap=[(armSymmetryChk,'right',0,100)])
    pc.formLayout(armOpModuleForm, e=True, ac=[(armSep1,'top',2,noArmLimbsJointsISG )],af=[(armSep1,'left',0)],ap=[(armSep1,'right',0,100)])
              
    pc.formLayout(armOpModuleForm, e=True, ac=[(armModuleSideTitle,'top',15,armSep1)], af=[(armModuleSideTitle,'left',0)], ap=[(armModuleSideTitle,'right',0,25)])
    pc.formLayout(armOpModuleForm, e=True, ac=[(armModuleSideRdBnGrp,'top',5,armModuleSideTitle)], af=[(armModuleSideRdBnGrp,'left',0)], ap=[(armModuleSideRdBnGrp,'right',0,25)])
    pc.formLayout(armOpModuleForm, e=True, ac=[(armSF,'top',0,armSep1),(armSF,'left',0,armModuleSideTitle)], ap=[(armSF,'right',0,100)])

    armTemplateSep1 = pc.separator('armTemplateSep1', height=5, style='none', p=mainModuleRCL)
    armTemplateSep2 = pc.separator('armTemplateSep2', height=5, style='none', p=mainModuleRCL)

    legModuleFrame = pc.frameLayout('legModuleFrame', l=' Leg', collapsable=False, collapse=False, borderStyle='etchedOut', h=hgt, marginHeight=3, marginWidth=3, p=mainModuleRCL)

    # TODO: remove or replace .bmp icons
    legTempModuleBtn = pc.symbolButton('legTempModuleBtn', h=80, i='legModule.bmp', c=pc.Callback(bm.build_leg_dummy_skeleton_module_pre_cmd), p=legModuleFrame)

    legOpModuledFrame = pc.frameLayout('legOpModuledFrame', l=' options:', collapsable=False, collapse=False, borderStyle='etchedOut', h=hgt, marginHeight=3, marginWidth=3, p=mainModuleRCL)

    legOpModuledForm = pc.formLayout('legOpModuledForm', p=legOpModuledFrame)
    noLegLimbsJointsTitle = pc.text('noLegLimbsJointsTitle', l='joints:  ', al='right')
    noLegLimbsJointsISG = pc.intField('noLegLimbsJointsISG', minValue=3, maxValue=10, value=3, s=1)

    legFingersTitle = pc.text('legFingersTitle', l='fingers:  ', al='right')
    legFingersChk = pc.checkBox('legFingersChk', l='', v=1, cc=pc.Callback(legFingersModuleSwitch))
    noLegFingersJointsTitle = pc.text('noLegFingersJointsTitle', l='no:  ', al='right')
    noLegFingersJointISG = pc.intField('noLegFingersJointISG', minValue=0, maxValue=5, value=5, s=1) 

    noLegFingersSegJointsTitle = pc.text('noLegFingersSegJointsTitle', l='segment:  ', al='right')
    noLegFingersSegJointISG = pc.intField('noLegFingersSegJointISG', minValue=2, maxValue=10, value=4, s=1) 

    legSymmetryTitle = pc.text('legSymmetryTitle', l='symmetry:  ', al='right')
    legSymmetryChk = pc.checkBox('legSymmetryChk', l='', v=0) 
    legSep1 = pc.separator('legSep1', height=5, style='out')
    legModuleSideTitle = pc.text('legModuleSideTitle', l='Side:  ', align='left')
    legModuleSideRdBnGrp = pc.radioButtonGrp('legModuleSideRdBnGrp', nrb=2,  la2=['L','R'], cw2=[30,30], sl=1)
    legSF = pc.scrollField('legSF', wordWrap=True, text='creates leg skeleton template setup. ideal use: any leg Biped, Quadroped..', editable=False)

    pc.formLayout(legOpModuledForm, e=True, af=[(noLegLimbsJointsTitle,'top',5),(noLegLimbsJointsTitle,'left',0)],ap=[(noLegLimbsJointsTitle,'right',0,15)])
    pc.formLayout(legOpModuledForm, e=True, ac=[(noLegLimbsJointsISG,'top',5,noLegLimbsJointsTitle)], af=[(noLegLimbsJointsISG,'left',0)], ap=[(noLegLimbsJointsISG,'right',0,10)])

    pc.formLayout(legOpModuledForm, e=True, af=[(legFingersTitle,'top',5)], ac=[(legFingersTitle,'left',0,noLegLimbsJointsTitle)],ap=[(legFingersTitle,'right',0,35)])
    pc.formLayout(legOpModuledForm, e=True, ac=[(legFingersChk,'top',5,legFingersTitle),(legFingersChk,'left',25,noLegLimbsJointsISG)],ap=[(legFingersChk,'right',0,35)])
    pc.formLayout(legOpModuledForm, e=True, af=[(noLegFingersJointsTitle,'top',5)],ac=[(noLegFingersJointsTitle,'left',0,legFingersTitle)],ap=[(noLegFingersJointsTitle,'right',0,47)])
    pc.formLayout(legOpModuledForm, e=True, ac=[(noLegFingersJointISG,'top',5,noLegFingersJointsTitle),(noLegFingersJointISG,'left',7,legFingersChk)], ap=[(noLegFingersJointISG,'right',0,45)])

    pc.formLayout(legOpModuledForm, e=True, af=[(noLegFingersSegJointsTitle,'top',5)], ac=[(noLegFingersSegJointsTitle,'left',0,noLegFingersJointsTitle)], ap=[(noLegFingersSegJointsTitle,'right',0,75)])
    pc.formLayout(legOpModuledForm, e=True, ac=[(noLegFingersSegJointISG,'top',5,noLegFingersSegJointsTitle),(noLegFingersSegJointISG,'left',20,noLegFingersJointISG)], ap=[(noLegFingersSegJointISG,'right',0,65)])

    pc.formLayout(legOpModuledForm, e=True, af=[(legSymmetryTitle,'top',5)], ac=[(legSymmetryTitle,'left',0,noLegFingersSegJointsTitle)],ap=[(legSymmetryTitle,'right',0,100)])
    pc.formLayout(legOpModuledForm, e=True, ac=[(legSymmetryChk,'top',5,legFingersTitle),(legSymmetryChk,'left',35,noLegFingersSegJointISG)],ap=[(legSymmetryChk,'right',0,100)])
    pc.formLayout(legOpModuledForm, e=True, ac=[(legSep1,'top',2,noLegLimbsJointsISG)],af=[(legSep1,'left', 0)],ap=[(legSep1,'right',0,100)])
    pc.formLayout(legOpModuledForm, e=True, ac=[(legModuleSideTitle,'top',15,legSep1)],af=[(legModuleSideTitle,'left',0)],ap=[(legModuleSideTitle,'right',0,25)])
    pc.formLayout(legOpModuledForm, e=True, ac=[(legModuleSideRdBnGrp,'top',5,legModuleSideTitle)], af=[(legModuleSideRdBnGrp,'left',0)], ap=[(legModuleSideRdBnGrp,'right',0,25)])
    pc.formLayout(legOpModuledForm, e=True, ac=[(legSF,'top',0,legSep1),(legSF,'left',0,legModuleSideTitle)],ap=[(legSF,'right',0,100)])

    legTemplateSep1 = pc.separator('legTemplateSep1', height=5, style='none', p=mainModuleRCL)
    legTemplateSep2 = pc.separator('legTemplateSep2', height=5, style='none', p=mainModuleRCL)

    spineModuleFrame = pc.frameLayout('spineModuleFrame', l=' Spine', collapsable=False, collapse=False, borderStyle='etchedOut', h=hgt, marginHeight=3, marginWidth=3, p=mainModuleRCL)
    # TODO: remove or replace .bmp icons
    spineTempModuleBtn = pc.symbolButton('spineTempModuleBtn', i='spineModule.bmp', c=pc.Callback(bm.buildSpineDummySkeletonModulePreCMD), p=spineModuleFrame)

    spineOpModuledFrame = pc.frameLayout('spineOpModuledFrame', l=' options:', collapsable=False, collapse=False, borderStyle='etchedOut', h=hgt, marginHeight=3, marginWidth=3, p=mainModuleRCL)

    spineOpModuledForm = pc.formLayout('spineOpModuledForm', p=spineOpModuledFrame)
    spineTemplateTitle = pc.text('spineTemplateTitle', l='title:  ', al='right')
    spineTemplateTF = pc.textField('spineTemplateTF', tx='spine')
    noSpineConTitle = pc.text('noSpineConTitle', l='controls:  ', al='right')
    noSpineConIF = pc.intField('noSpineConIF', minValue=2, maxValue=10, value=4, s=1) 

    spineTemplateAxisTitle = pc.text('spineTemplateAxisTitle', l='axis:  ', al='right')
    spineAxisOM = pc.optionMenu('spineAxisOM') 
    pc.menuItem(label='x')
    pc.menuItem(label='y')
    pc.menuItem(label='z')
    disSpineConTitle = pc.text('disSpineConTitle', l='length:  ', al='right')
    disSpineConIF = pc.intField('disSpineConIF', minValue=3, maxValue=50, value=4, s=1) 

    spineSymmetryTitle = pc.text('spineSymmetryTitle', l='symmetry:  ', al='right')
    spineSymmetryChk = pc.checkBox('spineSymmetryChk', l='', v=0) 
    spineInfoSep1 = pc.separator('spineInfoSep1', height=5, style='out')
    spineInfoSF = pc.scrollField('spineInfoSF', wordWrap=True, text='creates spine skeleton template setup. ideal use: any spine \nNote: control defines how many control you want in the rig not joints..', editable=False)

    pc.formLayout(spineOpModuledForm, e=True, af=[(spineTemplateTitle,'top',5),(spineTemplateTitle,'left',0)],ap=[(spineTemplateTitle,'right',0,15)])
    pc.formLayout(spineOpModuledForm, e=True, ac=[(spineTemplateTF,'top',5,spineTemplateTitle)], af=[(spineTemplateTF,'left',0)],ap=[(spineTemplateTF,'right',0,20)])
    pc.formLayout(spineOpModuledForm, e=True, af=[(noSpineConTitle,'top',5)],ac=[(noSpineConTitle,'left',0,spineTemplateTitle)], ap=[(noSpineConTitle,'right',0,40)])
    pc.formLayout(spineOpModuledForm, e=True, ac=[(noSpineConIF,'top',5,noSpineConTitle),(noSpineConIF,'left',5,spineTemplateTF)], ap=[(noSpineConIF,'right',0,35)])

    pc.formLayout(spineOpModuledForm, e=True, af=[(spineTemplateAxisTitle,'top',5)], ac=[(spineTemplateAxisTitle,'left',0,noSpineConTitle)],ap=[(spineTemplateAxisTitle,'right',0,55)])
    pc.formLayout(spineOpModuledForm, e=True, ac=[(spineAxisOM,'top',5,spineTemplateAxisTitle),(spineAxisOM,'left',20,noSpineConIF)],ap=[(spineAxisOM,'right',0,60)])
    pc.formLayout(spineOpModuledForm, e=True, af=[(disSpineConTitle,'top',5)],ac=[(disSpineConTitle,'left',0,spineTemplateAxisTitle)],ap=[(disSpineConTitle,'right',0,77)])
    pc.formLayout(spineOpModuledForm, e=True, ac=[(disSpineConIF,'top',5,disSpineConTitle),(disSpineConIF,'left',4,spineAxisOM)], ap=[(disSpineConIF,'right',0,72)])

    pc.formLayout(spineOpModuledForm, e=True, af=[(spineSymmetryTitle,'top',5)], ac=[(spineSymmetryTitle,'left',0,disSpineConTitle)], ap=[(spineSymmetryTitle,'right',0,100)])
    pc.formLayout(spineOpModuledForm, e=True, ac=[(spineSymmetryChk,'top',5,spineSymmetryTitle),(spineSymmetryChk,'left',17,disSpineConIF)], ap=[(spineSymmetryChk,'right',0,100)])
    pc.formLayout(spineOpModuledForm, e=True, ac=[(spineInfoSep1,'top',2,spineTemplateTF)], af=[(spineInfoSep1,'left',0)], ap=[(spineInfoSep1,'right',0,100)])
    pc.formLayout(spineOpModuledForm, e=True, ac=[(spineInfoSF,'top',0,spineInfoSep1)], af=[(spineInfoSF,'left',0)], ap=[(spineInfoSF,'right',0,100)])

    spineTemplateSep1 = pc.separator('spineTemplateSep1', height=5, style='none', p=mainModuleRCL)
    spineTemplateSep2 = pc.separator('spineTemplateSep2', height=5, style='none', p=mainModuleRCL)

    neckModuleFrame = pc.frameLayout('neckModuleFrame', l=' Neck Head', collapsable=False, collapse=False, borderStyle='etchedOut', h=hgt, marginHeight=3, marginWidth=3, p=mainModuleRCL)
    # TODO: remove or replace .bmp icons
    neckTempModuleBtn = pc.symbolButton('neckTempModuleBtn', i='headNeckModule.bmp', c=pc.Callback(bm.build_head_neck_dummy_skeleton_module_pre_cmd), p=neckModuleFrame)

    neckOpModuledFrame = pc.frameLayout('neckOpModuledFrame', l=' options:', collapsable=False, collapse=False, borderStyle='etchedOut', h=hgt, marginHeight=3, marginWidth=3, p=mainModuleRCL)

    neckOpModuledForm = pc.formLayout('neckOpModuledForm', p=neckOpModuledFrame)

    neckTemplateTitle = pc.text('neckTemplateTitle', l='title:  ', al='right')
    neckTemplateTF = pc.textField('neckTemplateTF', tx='neck')
    noNeckConTitle = pc.text('noNeckConTitle', l='controls:  ', al='right')
    noNeckConIF = pc.intField('noNeckConIF', minValue=1, maxValue=10, value=1, s=1) 

    neckTemplateAxisTitle = pc.text('neckTemplateAxisTitle', l='axis:  ', al='right')
    neckAxisOM = pc.optionMenu('neckAxisOM') 
    pc.menuItem(label='x')
    pc.menuItem(label='y')
    pc.menuItem(label='z')
    disNeckConTitle = pc.text('disNeckConTitle', l='length:  ', al='right')
    disNeckConIF = pc.intField('disNeckConIF', minValue=-50, maxValue=50, value=1, s=1) 

    neckSymmetryTitle = pc.text('neckSymmetryTitle', l='symmetry:  ', al='right')
    neckSymmetryChk = pc.checkBox('neckSymmetryChk', l='', v=0)
    neckInfoSep1 = pc.separator('neckInfoSep1', height=5, style='out')
    neckInfoSF = pc.scrollField('neckInfoSF', wordWrap=True, text='creates neck skeleton template setup. ideal use: any neck \nNote: control defines how many control you want in the rig not joints..', editable=False)

    pc.formLayout(neckOpModuledForm, e=True, af=[(neckTemplateTitle,'top',5),(neckTemplateTitle,'left',0)], ap=[(neckTemplateTitle,'right',0,15)])
    pc.formLayout(neckOpModuledForm, e=True, ac=[(neckTemplateTF,'top',5,neckTemplateTitle)], af=[(neckTemplateTF,'left',0)], ap=[(neckTemplateTF,'right',0,20)])
    pc.formLayout(neckOpModuledForm, e=True, af=[(noNeckConTitle,'top',5)], ac=[(noNeckConTitle,'left',0,neckTemplateTitle)], ap=[(noNeckConTitle,'right',0,40)])
    pc.formLayout(neckOpModuledForm, e=True, ac=[(noNeckConIF,'top',5,noNeckConTitle),(noNeckConIF,'left',5,neckTemplateTF)], ap=[(noNeckConIF,'right',0,35)])

    pc.formLayout(neckOpModuledForm, e=True, af=[(neckTemplateAxisTitle,'top',5)], ac=[(neckTemplateAxisTitle,'left',0,noNeckConTitle)], ap=[(neckTemplateAxisTitle,'right',0,55)])
    pc.formLayout(neckOpModuledForm, e=True, ac=[(neckAxisOM,'top',5,neckTemplateAxisTitle),(neckAxisOM,'left',20,noNeckConIF)], ap=[(neckAxisOM,'right',0,60)])
    pc.formLayout(neckOpModuledForm, e=True, af=[(disNeckConTitle,'top',5)], ac=[(disNeckConTitle,'left',0,neckTemplateAxisTitle)], ap=[(disNeckConTitle,'right',0,77)])
    pc.formLayout(neckOpModuledForm, e=True, ac=[(disNeckConIF,'top',5,disNeckConTitle),(disNeckConIF,'left',4,neckAxisOM)], ap=[(disNeckConIF,'right',0,72)])

    pc.formLayout(neckOpModuledForm, e=True, af=[(neckSymmetryTitle,'top',5)], ac=[(neckSymmetryTitle,'left',0,disNeckConTitle)], ap=[(neckSymmetryTitle,'right',0,100)])
    pc.formLayout(neckOpModuledForm, e=True, ac=[(neckSymmetryChk,'top',5,neckSymmetryTitle),(neckSymmetryChk,'left',17,disNeckConIF)],ap=[(neckSymmetryChk,'right',0,100)])
    pc.formLayout(neckOpModuledForm, e=True, ac=[(neckInfoSep1,'top',2,neckTemplateTF)], af=[(neckInfoSep1,'left',0)], ap=[(neckInfoSep1,'right',0,100)])
    pc.formLayout(neckOpModuledForm, e=True, ac=[(neckInfoSF,'top',0,neckInfoSep1)], af=[(neckInfoSF,'left',0)], ap=[(neckInfoSF,'right',0,100)])
    
    neckTemplateSep1 = pc.separator('neckTemplateSep1', height=5, style='none', p=mainModuleRCL)
    neckTemplateSep2 = pc.separator('neckTemplateSep2', height=5, style='none', p=mainModuleRCL)

    tentacleModuleFrame = pc.frameLayout('tentacleModuleFrame', l=' Tentacle', collapsable=False, collapse=False, borderStyle='etchedOut', h=hgt, marginHeight=3, marginWidth=3, p=mainModuleRCL)
    # TODO: remove or replace .bmp icons
    tentacleTempModuleBtn = pc.symbolButton('tentacleTempModuleBtn', i='tentacleModule.bmp', c=pc.Callback(bm.buildTentacleDummySkeletonModulePreCMD), p=tentacleModuleFrame)    

    tentacleOpModuledFrame = pc.frameLayout('tentacleOpModuledFrame', l=' options:', collapsable=False, collapse=False, borderStyle='etchedOut', h=hgt, marginHeight=3, marginWidth=3, p=mainModuleRCL)

    tentacleOpModuledForm = pc.formLayout('tentacleOpModuledForm', p=tentacleOpModuledFrame)

    tentacleTemplateTitle = pc.text('tentacleTemplateTitle', l='title:  ', al='right')
    tentacleTemplateTF = pc.textField('tentacleTemplateTF', tx='tail')
    noTentacleConTitle = pc.text('noTentacleConTitle', l='controls:  ', al='right')
    noTentacleConIF = pc.intField('noTentacleConIF', minValue=2, maxValue=20, value=7, s=1) 

    tentacleTemplateAxisTitle = pc.text('tentacleTemplateAxisTitle', l='axis:  ', al='right')
    tentacleAxisOM = pc.optionMenu('tentacleAxisOM') 
    pc.menuItem(label='x')
    pc.menuItem(label='y')
    pc.menuItem(label='z')
    disTentacleConTitle = pc.text('disTentacleConTitle', l='length:  ', al='right')
    disTentacleConIF = pc.intField('disTentacleConIF', minValue=-50, maxValue=50, value=7, s=1) 

    tentacleSymmetryTitle = pc.text('tentacleSymmetryTitle', l='symmetry:  ', al='right')
    tentacleSymmetryChk = pc.checkBox('tentacleSymmetryChk', l='', v=0) 
    tentacleInfoSep1 = pc.separator('tentacleInfoSep1', height=5, style='out')
    tentacleInfoSF = pc.scrollField('tentacleInfoSF', wordWrap=True, text='creates tentacle skeleton template setup. ideal use: Tail, Ears \nNote control defines how many control you want in the rig not joints..', editable=False)

    pc.formLayout(tentacleOpModuledForm, e=True, af=[(tentacleTemplateTitle,'top',5),(tentacleTemplateTitle,'left',0)],ap=[(tentacleTemplateTitle,'right',0,15)])
    pc.formLayout(tentacleOpModuledForm, e=True, ac=[(tentacleTemplateTF,'top',5,tentacleTemplateTitle)],af=[(tentacleTemplateTF,'left',0)],ap=[(tentacleTemplateTF,'right',0,20)])
    pc.formLayout(tentacleOpModuledForm, e=True, af=[(noTentacleConTitle,'top',5)], ac=[(noTentacleConTitle,'left',0,tentacleTemplateTitle)], ap=[(noTentacleConTitle,'right',0,40)])
    pc.formLayout(tentacleOpModuledForm, e=True, ac=[(noTentacleConIF,'top',5,noTentacleConTitle),(noTentacleConIF,'left',5,tentacleTemplateTF)],ap=[(noTentacleConIF,'right',0,35)])

    pc.formLayout(tentacleOpModuledForm, e=True, af=[(tentacleTemplateAxisTitle,'top',5)], ac=[(tentacleTemplateAxisTitle,'left',0,noTentacleConTitle)], ap=[(tentacleTemplateAxisTitle,'right',0,55)])
    pc.formLayout(tentacleOpModuledForm, e=True, ac=[(tentacleAxisOM,'top',5,tentacleTemplateAxisTitle),(tentacleAxisOM,'left',20,noTentacleConIF)], ap=[(tentacleAxisOM,'right',0,60)])
    pc.formLayout(tentacleOpModuledForm, e=True, af=[(disTentacleConTitle,'top',5)],ac=[(disTentacleConTitle,'left',0,tentacleTemplateAxisTitle)],ap=[(disTentacleConTitle,'right',0,77)])
    pc.formLayout(tentacleOpModuledForm, e=True, ac=[(disTentacleConIF,'top',5,disTentacleConTitle),(disTentacleConIF,'left',4,tentacleAxisOM)],ap=[(disTentacleConIF,'right',0,72)])

    pc.formLayout(tentacleOpModuledForm, e=True, af=[(tentacleSymmetryTitle,'top',5)], ac=[(tentacleSymmetryTitle,'left',0,disTentacleConTitle)], ap=[(tentacleSymmetryTitle,'right',0,100)])
    pc.formLayout(tentacleOpModuledForm, e=True, ac=[(tentacleSymmetryChk,'top',5,tentacleSymmetryTitle),(tentacleSymmetryChk,'left',15,disTentacleConIF)], ap=[(tentacleSymmetryChk,'right',0,100)])
    pc.formLayout(tentacleOpModuledForm, e=True, ac=[(tentacleInfoSep1,'top',2,tentacleTemplateTF)],af=[(tentacleInfoSep1,'left',0)],ap=[(tentacleInfoSep1,'right',0,100)])
    pc.formLayout(tentacleOpModuledForm, e=True, ac=[(tentacleInfoSF,'top',0,tentacleInfoSep1)], af=[(tentacleInfoSF,'left',0)], ap=[(tentacleInfoSF,'right',0,100)])    

    tentTemplateSep1 = pc.separator('tentTemplateSep1', height=5, style='none', p=mainModuleRCL)
    tentTemplateSep2 = pc.separator('tentTemplateSep2', height=5, style='none', p=mainModuleRCL)

    fingerModuleFrame = pc.frameLayout('fingerModuleFrame', l=' Finger', collapsable=False, collapse=False, borderStyle='etchedOut', h=hgt, marginHeight=3, marginWidth=3, p=mainModuleRCL)
    # TODO: remove or replace .bmp icons
    fingerTempModuleBtn = pc.symbolButton('fingerTempModuleBtn', i='fingerModule.bmp', c=pc.Callback(bm.buildFingerDummySkeletonModulePreCMD), p=fingerModuleFrame)
    
    fingerOpModuledFrame = pc.frameLayout('fingerOpModuledFrame', l=' options:', collapsable=False, collapse=False, borderStyle='etchedOut', h=hgt, marginHeight=3, marginWidth=3, p=mainModuleRCL)

    fingerOpModuledForm = pc.formLayout('fingerOpModuledForm', p=fingerOpModuledFrame)

    fingerTemplateTitle = pc.text('fingerTemplateTitle', l='title:  ', al='right')
    fingerTemplateTF = pc.textField('fingerTemplateTF', tx='index')
    noFingerConTitle = pc.text('noFingerConTitle', l='segments:  ', al='right')
    noFingerConIF = pc.intField('noFingerConIF', minValue=2, maxValue=10, value=4, s=1)

    fingerTemplateAxisTitle = pc.text('fingerTemplateAxisTitle', l='axis:  ', al='right')
    fingerAxisOM = pc.optionMenu('fingerAxisOM')
    pc.menuItem(label='x')
    pc.menuItem(label='y')
    pc.menuItem(label='z')
    disFingerConTitle = pc.text('disFingerConTitle', l='length:  ', al='right')
    disFingerConIF = pc.intField('disFingerConIF', minValue=3, maxValue=15, value=4, s=1) 

    fingerSymmetryTitle = pc.text('fingerSymmetryTitle', l='symmetry:  ', al='right')
    fingerSymmetryChk = pc.checkBox('fingerSymmetryChk', l='', v=0) 
    fingerInfoSep1 = pc.separator('fingerInfoSep1', height=5, style='out')
    fingerModuleSideTitle = pc.text('fingerModuleSideTitle', l='Side:  ', align='left')
    fingerModuleSideRdBnGrp = pc.radioButtonGrp('fingerModuleSideRdBnGrp', nrb=2,  la2=['L','R'], cw2=(30,30), sl=1) 
    fingerInfoSF = pc.scrollField('fingerInfoSF', wordWrap=True, text='creates finger skeleton template setup. ideal use: any fingers Human, Animals', editable=False)

    pc.formLayout('fingerOpModuledForm', e=True, af=[(fingerTemplateTitle,'top',5),(fingerTemplateTitle,'left',0)],ap=[(fingerTemplateTitle,'right',0,15)])
    pc.formLayout('fingerOpModuledForm', e=True, ac=[(fingerTemplateTF,'top',5,fingerTemplateTitle)], af=[(fingerTemplateTF,'left',0)], ap=[(fingerTemplateTF,'right',0,17)])
    pc.formLayout('fingerOpModuledForm', e=True, af=[(noFingerConTitle,'top',5)], ac=[(noFingerConTitle,'left',0,fingerTemplateTitle)], ap=[(noFingerConTitle,'right',0,40)])
    pc.formLayout('fingerOpModuledForm', e=True, ac=[(noFingerConIF,'top',5,noFingerConTitle),(noFingerConIF,'left',4,fingerTemplateTF)], ap=[(noFingerConIF,'right',0,30)])

    pc.formLayout('fingerOpModuledForm', e=True, af=[(fingerTemplateAxisTitle,'top',5)], ac=[(fingerTemplateAxisTitle,'left',0,noFingerConTitle)], ap=[(fingerTemplateAxisTitle,'right',0,55)])
    pc.formLayout('fingerOpModuledForm', e=True, ac=[(fingerAxisOM,'top',5,fingerTemplateAxisTitle),(fingerAxisOM,'left',35,noFingerConIF)], ap=[(fingerAxisOM,'right',0,60)])
    pc.formLayout('fingerOpModuledForm', e=True, af=[(disFingerConTitle,'top',5)], ac=[(disFingerConTitle,'left',0,fingerTemplateAxisTitle )], ap=[(disFingerConTitle,'right',0,77)])
    pc.formLayout('fingerOpModuledForm', e=True, ac=[(disFingerConIF,'top',5,disFingerConTitle),(disFingerConIF,'left',5,fingerAxisOM)],ap=[(disFingerConIF,'right',0,72)])

    pc.formLayout('fingerOpModuledForm', e=True, af=[(fingerSymmetryTitle,'top',5)], ac=[(fingerSymmetryTitle,'left',0,disFingerConTitle)],ap=[(fingerSymmetryTitle,'right',0,100)])
    pc.formLayout('fingerOpModuledForm', e=True, ac=[(fingerSymmetryChk,'top',5,fingerSymmetryTitle),(fingerSymmetryChk,'left',15,disFingerConIF)], ap=[(fingerSymmetryChk,'right',0,100)])
    pc.formLayout('fingerOpModuledForm', e=True, ac=[(fingerInfoSep1,'top',2,fingerTemplateTF)], af=[(fingerInfoSep1,'left',0)], ap=[(fingerInfoSep1,'right',0,100)])
    pc.formLayout('fingerOpModuledForm', e=True, ac=[(fingerModuleSideTitle,'top',10,fingerInfoSep1)], af=[(fingerModuleSideTitle,'left',0)], ap=[(fingerModuleSideTitle,'right',0,25)])
    pc.formLayout('fingerOpModuledForm', e=True, ac=[(fingerModuleSideRdBnGrp,'top',10,fingerModuleSideTitle)], af=[(fingerModuleSideRdBnGrp,'left',0)], ap=[(fingerModuleSideRdBnGrp,'right',0,25)])
    pc.formLayout('fingerOpModuledForm', e=True, ac=[(fingerInfoSF,'top',0,fingerInfoSep1),(fingerInfoSF,'left',0,fingerModuleSideTitle)], ap=[(fingerInfoSF,'right',0,100)])    

    headOpModuledFormSep1 = pc.separator('headOpModuledFormSep1', height=7, style='out', p=mainColumnLayout)

    mainModuleRCL = pc.rowColumnLayout('mainModuleRCL', nc=3, cw=[(1,141),(2,141),(3,141)], p=mainColumnLayout)
    connectModulesBtn = pc.button('connectModulesBtn', l='Connect Modules', c=pc.Callback(msL.connectModuleComponentsUI, '', ''))
    addHeirarchyBtn = pc.button('addHeirarchyBtn', l='Add To Heirarchy', c=pc.Callback(msL.addToModuleComponentsHierarchy, '', ''))
    delModulessBtn = pc.button('delModulessBtn', l='Delete',  c=pc.Callback(msL.deleteModules))
    symmetryModuleBtn = pc.button('symmetryModuleBtn', l='Symmetry',  c=pc.Callback(msL.connectModuleSymmetry)) 
    symmModuleBtn = pc.button('symmModuleBtn', l='Break Symmetry',  c=pc.Callback(msL.breakModuleSymConnection,''))
    mirrorModuleBtn = pc.button('mirrorModuleBtn', l='Mirror Seleted', c=pc.Callback(msL.mirrorModuleTemplates,''))
    OpModuledFormSep1 = pc.separator('OpModuledFormSep1', height=7, style='out', p=createSkColumnLayout)
    buildModulesBtn = pc.button('buildModulesBtn', h=50, l='Build Skeleton', p=createSkColumnLayout, c=pc.Callback(bmjs.buildModuleSkeleton))
    OpModuledFormSep2 = pc.separator('OpModuledFormSep2', height=7, style='out', p=createSkColumnLayout)

    templatesFrame = pc.frameLayout('templatesFrame', l='', collapsable=False, collapse=False, borderStyle='etchedIn', marginHeight=3, marginWidth=3, p=modulePartTab)

    tempMainColumnLayout = pc.columnLayout('tempMainColumnLayout', adj=1, p=templatesFrame)

    chooseDirRCL = pc.rowColumnLayout('chooseDirRCL', nc=1, cw=[1,300], p=tempMainColumnLayout)
    chooseDirTitle = pc.text('chooseDirTitle', l='Choose Directory :', fn='boldLabelFont', align='left', p=chooseDirRCL)

    moduleTempdirMainRCL = pc.rowColumnLayout('chooseDirTitle', nc=3, cw=[(1,50),(2,300),(3,30)], p=tempMainColumnLayout)
    moduleTempdirTitle = pc.text('moduleTempdirTitle', l='path :  ', align='right', p=moduleTempdirMainRCL)
    moduleTempdirTF = pc.textField('moduleTempdirTF', editable=1, tx='Choose your skeleton template directory....', p=moduleTempdirMainRCL)
    moduleTempdirBtn = pc.button('moduleTempdirBtn', l="...", c=pc.Callback(chooseModuleTemplatesDir), p=moduleTempdirMainRCL)

    templateTitleRCL = pc.rowColumnLayout('templateTitleRCL', nc=1, cw=[(1,410)], p=tempMainColumnLayout)
    templatesTitleSep1 = pc.separator('templatesTitleSep1', height=10, style='out', p=templateTitleRCL)
    templatesTitle = pc.text('templatesTitle', l='Templates:', fn='boldLabelFont', align='left', p=templateTitleRCL)
    templatesTitleSep2 = pc.separator('templatesTitleSep2', height=10, style='none', p=templateTitleRCL)

    tempMainScrollLayout = pc.scrollLayout('tempMainScrollLayout', h=285, verticalScrollBarThickness=16, p=tempMainColumnLayout)
    tempalteMainRCL = pc.rowColumnLayout('tempalteMainRCL', nc=2, cw=[(1,120),(2,270)], p=tempMainScrollLayout)

    # separator -height 5 -style "none" -p tempalteMainRCL tempMainScrollLayoutSep1;
    # separator -height 5 -style "none" -p tempalteMainRCL tempMainScrollLayoutSep2;

    hgt = 135

    bipedTempFrame = pc.frameLayout('bipedTempFrame', l='Biped', collapsable=False, collapse=False, borderStyle='etchedOut', h=hgt, marginHeight=3, marginWidth=3, p=tempalteMainRCL)

    bipedTemplateBtn=  pc.symbolButton('bipedTemplateBtn', c=pc.Callback(bm.buildBipedModulePreCMD), p=bipedTempFrame)

    bipedTempInfoFrame = pc.frameLayout('bipedTempInfoFrame', l=' options:', collapsable=False, collapse=False, borderStyle='etchedOut', h=hgt, marginHeight=3, marginWidth=3, p=tempalteMainRCL)

    bipedOpModuleForm = pc.formLayout('bipedOpModuleForm', p=bipedTempInfoFrame)

    noBipedSpineJointsTitle = pc.text('noBipedSpineJointsTitle', l='spine:  ', al='right')
    noBipedSpineJointsISG = pc.intField('noBipedSpineJointsISG', minValue=3, maxValue=10, value=4, s=1) 

    noBipedNeckJointsTitle = pc.text('noBipedNeckJointsTitle', l='neck:  ', al='right')
    noBipedNeckJointsISG = pc.intField('noBipedNeckJointsISG', minValue=1, maxValue=10, value=1, s=1)

    bipedFingersTitle = pc.text('bipedFingersTitle', l='fingers:  ', al='right')
    bipedFingersChk = pc.checkBox('bipedFingersChk', l='', v=1, cc=pc.Callback(bipedFingersModuleSwitch))

    noBipedFingersJointsTitle = pc.text('noBipedFingersJointsTitle', l='no:  ', al='right')
    noBipedFingersJointISG = pc.intField('noBipedFingersJointISG', minValue=0, maxValue=5, value=5, s=4) 

    bipedToesTitle = pc.text('bipedToesTitle', l='Toes:  ', al='right')
    bipedToesChk = pc.checkBox('bipedToesChk', l='', v=1, cc=pc.Callback(bipedToesModuleSwitch))
    
    noBipedToesJointsTitle = pc.text('noBipedToesJointsTitle', l='no:  ', al='right')
    noBipedToesJointISG = pc.intField('noBipedToesJointISG', minValue=0, maxValue=5, value=5, s=4)

    bipedInfoSep1 = pc.separator('bipedInfoSep1', height=5, style='out')

    bipedTempInfoSF = pc.scrollField('bipedTempInfoSF', wordWrap=True, text='This is Biped skeleton template created from several modules.\nImportant Note: \ndifferent module still can be added or deleted.\nfor example: \nears, tail etc...', editable=False)

    pc.formLayout(bipedOpModuleForm, e=True, af=[(noBipedSpineJointsTitle,'top',5),(noBipedSpineJointsTitle,'left',0)], ap=[(noBipedSpineJointsTitle,'right',0,15)])
    pc.formLayout(bipedOpModuleForm, e=True, ac=[(noBipedSpineJointsISG,'top',5,noBipedSpineJointsTitle)], af=[(noBipedSpineJointsISG,'left',0)], ap=[(noBipedSpineJointsISG,'right',0,10)])
    pc.formLayout(bipedOpModuleForm, e=True, af=[(noBipedNeckJointsTitle,'top',5)], ac=[(noBipedNeckJointsTitle,'left',0,noBipedSpineJointsTitle)], ap=[(noBipedNeckJointsTitle,'right',0,30)])
    pc.formLayout(bipedOpModuleForm, e=True, ac=[(noBipedNeckJointsISG,'top',5,noBipedNeckJointsTitle),(noBipedNeckJointsISG,'left',20,noBipedSpineJointsISG)], ap=[(noBipedNeckJointsISG,'right',0,30)])
    pc.formLayout(bipedOpModuleForm, e=True, af=[(bipedFingersTitle,'top',5)], ac=[(bipedFingersTitle,'left',0,noBipedNeckJointsTitle)], ap=[(bipedFingersTitle,'right',0,50)])
    pc.formLayout(bipedOpModuleForm, e=True, ac=[(bipedFingersChk,'top',5,bipedFingersTitle),(bipedFingersChk,'left',10,noBipedNeckJointsISG)], ap=[(bipedFingersChk,'right',0,50)])
    pc.formLayout(bipedOpModuleForm, e=True, af=[(noBipedFingersJointsTitle,'top',5)], ac=[(noBipedFingersJointsTitle,'left',0,bipedFingersTitle)], ap=[(noBipedFingersJointsTitle,'right',0,60)])
    pc.formLayout(bipedOpModuleForm, e=True, ac=[(noBipedFingersJointISG,'top',5,noBipedFingersJointsTitle),(noBipedFingersJointISG,'left',0,bipedFingersChk)],ap=[(noBipedFingersJointISG,'right',0,60)])
    pc.formLayout(bipedOpModuleForm, e=True, af=[(bipedToesTitle,'top',5)], ac=[(bipedToesTitle,'left',0,noBipedFingersJointsTitle)], ap=[(bipedToesTitle,'right',0,80)])
    pc.formLayout(bipedOpModuleForm, e=True, ac=[(bipedToesChk,'top',5,bipedToesTitle),(bipedToesChk,'left',20,noBipedFingersJointISG)],ap=[(bipedToesChk,'right',0,80)])
    pc.formLayout(bipedOpModuleForm, e=True, af=[(noBipedToesJointsTitle,'top',5)], ac=[(noBipedToesJointsTitle,'left',0,bipedToesTitle)], ap=[(noBipedToesJointsTitle,'right',0,95)])
    pc.formLayout(bipedOpModuleForm, e=True, ac=[(noBipedToesJointISG,'top',5,noBipedToesJointsTitle),(noBipedToesJointISG,'left',15,bipedToesChk)], ap=[(noBipedToesJointISG,'right',0,95)])
    pc.formLayout(bipedOpModuleForm, e=True, ac=[(bipedInfoSep1,'top',2,noBipedSpineJointsISG)], af=[(bipedInfoSep1,'left',0)], ap=[(bipedInfoSep1,'right',0,100)])
    pc.formLayout(bipedOpModuleForm, e=True, ac=[(bipedTempInfoSF,'top',0,bipedInfoSep1 )], af=[(bipedTempInfoSF,'left',0)], ap=[(bipedTempInfoSF,'right',0,100)])

    bipedTemplateSep1 = pc.separator('bipedTemplateSep1', height=5, style='none', p=tempalteMainRCL)
    bipedTemplateSep2 = pc.separator('bipedTemplateSep2', height=5, style='none', p=tempalteMainRCL)

    QuadTempFrame = pc.frameLayout('QuadTempFrame', l='Quadroped', collapsable=False, collapse=False, borderStyle='etchedOut', h=hgt, marginHeight=3, marginWidth=3, p=tempalteMainRCL)
    QuadTemplateBtn = pc.symbolButton('QuadTemplateBtn', c=pc.Callback(bm.buildQuadModulePreCMD), p=QuadTempFrame)

    QuadTempInfoFrame = pc.frameLayout('QuadTempInfoFrame', l=' Information:', collapsable=False, collapse=False, borderStyle='etchedOut', h=hgt, marginHeight=3, marginWidth=3, p=tempalteMainRCL)

    quadOpModuleForm = pc.formLayout('quadOpModuleForm', p=QuadTempInfoFrame)

    noQuadSpineJointsTitle = pc.text('noQuadSpineJointsTitle', l='spine:  ', al='right')
    noQuadSpineJointsISG = pc.intField('noQuadSpineJointsISG', minValue=3, maxValue=10, value=4, s=1)

    noQuadNeckJointsTitle = pc.text('noQuadNeckJointsTitle', l='neck:  ', al='right') 
    noQuadNeckJointsISG = pc.intField('noQuadNeckJointsISG', minValue=1, maxValue=10, value=2, s=1) 

    noQuadEarsJointsTitle = pc.text('noQuadEarsJointsTitle', l='ears:  ', al='right')
    noQuadEarsJointsISG = pc.intField('noQuadEarsJointsISG', minValue=1, maxValue=10, value=4, s=1) 

    noQuadTailJointsTitle = pc.text('noQuadTailJointsTitle', l='tail:  ', al='right')
    noQuadTailJointsISG = pc.intField('noQuadTailJointsISG', minValue=1, maxValue=10, value=7, s=1) 

    quadToesTitle = pc.text('quadToesTitle', l='Toes:  ', al='right')
    quadToesChk = pc.checkBox('quadToesChk', l='', v=1, cc=pc.Callback(quadToesModuleSwitch))

    noQuadToesJointsTitle = pc.text('noQuadToesJointsTitle', l='no:  ', al='right')
    noQuadToesJointISG = pc.intField('noQuadToesJointISG', minValue=0, maxValue=5, value=5, s=4) 

    quadInfoSep1 = pc.separator('quadInfoSep1', height=5, style='out')

    QuadTempInfoSF = pc.scrollField('QuadTempInfoSF', wordWrap=True, text='This is Quadroped skeleton template created from several modules.\nImportant Note: \ndifferent modules can be added or deleted.\nfor example: \nears, tail etc...', editable=False)

    pc.formLayout(quadOpModuleForm, e=True, af=[(noQuadSpineJointsTitle,'top',5),(noQuadSpineJointsTitle,'left',0)], ap=[(noQuadSpineJointsTitle,'right',0,15)])
    pc.formLayout(quadOpModuleForm, e=True, ac=[(noQuadSpineJointsISG,'top',5,noQuadSpineJointsTitle)], af=[(noQuadSpineJointsISG,'left',0)], ap=[(noQuadSpineJointsISG,'right',0,10)])
    pc.formLayout(quadOpModuleForm, e=True, af=[(noQuadNeckJointsTitle,'top',5)], ac=[(noQuadNeckJointsTitle,'left',0,noQuadSpineJointsTitle)], ap=[(noQuadNeckJointsTitle,'right',0,30)])
    pc.formLayout(quadOpModuleForm, e=True, ac=[(noQuadNeckJointsISG,'top',5,noQuadNeckJointsTitle),(noQuadNeckJointsISG,'left',15,noQuadSpineJointsISG)], ap=[(noQuadNeckJointsISG,'right',0,25)])
    pc.formLayout(quadOpModuleForm, e=True, af=[(noQuadEarsJointsTitle,'top',5)], ac=[(noQuadEarsJointsTitle,'left',10,noQuadNeckJointsTitle)], ap=[(noQuadEarsJointsTitle,'right',0,45)])
    pc.formLayout(quadOpModuleForm, e=True, ac=[(noQuadEarsJointsISG,'top',5,noQuadEarsJointsTitle),(noQuadEarsJointsISG,'left',15,noQuadNeckJointsISG)], ap=[(noQuadEarsJointsISG,'right',0,40)])
    pc.formLayout(quadOpModuleForm, e=True, af=[(noQuadTailJointsTitle,'top',5)], ac=[(noQuadTailJointsTitle,'left',0,noQuadEarsJointsTitle)], ap=[(noQuadTailJointsTitle,'right',0,60)])
    pc.formLayout(quadOpModuleForm, e=True, ac=[(noQuadTailJointsISG,'top',5,noQuadTailJointsTitle),(noQuadTailJointsISG,'left',20,noQuadEarsJointsISG)], ap=[(noQuadTailJointsISG,'right',0,60)])
    pc.formLayout(quadOpModuleForm, e=True, af=[(quadToesTitle,'top',5)], ac=[(quadToesTitle,'left',0,noQuadTailJointsTitle)], ap=[(quadToesTitle,'right',0,80)])
    pc.formLayout(quadOpModuleForm, e=True, ac=[(quadToesChk,'top',5,quadToesTitle),(quadToesChk,'left',20,noQuadTailJointsISG)], ap=[(quadToesChk,'right',0,80)])
    pc.formLayout(quadOpModuleForm, e=True, af=[(noQuadToesJointsTitle,'top',5)], ac=[(noQuadToesJointsTitle,'left',0,quadToesTitle)], ap=[(noQuadToesJointsTitle,'right',0,95)])
    pc.formLayout(quadOpModuleForm, e=True, ac=[(noQuadToesJointISG,'top',5,noQuadToesJointsTitle),(noQuadToesJointISG,'left',15,quadToesChk)], ap=[(noQuadToesJointISG,'right',0,95)])
    pc.formLayout(quadOpModuleForm, e=True, ac=[(quadInfoSep1,'top',2,noQuadSpineJointsISG)], af=[(quadInfoSep1,'left',0)], ap=[(quadInfoSep1,'right',0,100)])
    pc.formLayout(quadOpModuleForm, e=True, ac=[(QuadTempInfoSF,'top',0,quadInfoSep1)], af=[(QuadTempInfoSF,'left',0)], ap=[(QuadTempInfoSF,'right',0,100)])

    bipedTemplateSep3 = pc.separator('bipedTemplateSep3', height=5, style='none', p=tempalteMainRCL)
    bipedTemplateSep4 = pc.separator('bipedTemplateSep4', height=5, style='none', p=tempalteMainRCL)

    eximModuleRCL = pc.rowColumnLayout('eximModuleRCL', nc=2, cw=[(1,204),(2,204)], cs=[2,3], p=tempMainColumnLayout)
    eximTitleSep1 = pc.separator('eximTitleSep1', height=10, style='out', p=eximModuleRCL)
    eximTitleSep2 = pc.separator('eximTitleSep2', height=10, style='out', p=eximModuleRCL)
    exportModulesBtn = pc.button('exportModulesBtn', h=50, l='Export',  c=pc.Callback(exportModuleTemplates), p=eximModuleRCL)
    importModulesBtn = pc.button('importModulesBtn', h=50, l='Import',  c=pc.Callback(importModuleTemplates), p=eximModuleRCL)
    eximTitleSep3 = pc.separator('eximTitleSep3', height=10, style='out', p=eximModuleRCL)
    eximTitleSep4 = pc.separator('eximTitleSep4', height=10, style='out', p=eximModuleRCL)

    modulePartTab = pc.tabLayout('modulePartTab', edit=True, tabLabel=[(mainColumnLayout,"   -   M O D U L E S   -   "),(templatesFrame,"   -   T E M P L A T E S   -   ")])
    
    global createRigColumnLayout; createRigColumnLayout = pc.columnLayout('createRigColumnLayout', adj=1, p=moduleRigTab)

    globalRigOpFrame = pc.frameLayout('globalRigOpFrame', l='Global Options :', collapsable=False, collapse=False, borderStyle='etchedOut', marginHeight=3, marginWidth=1, p=createRigColumnLayout)

    globalRigOpRCL = pc.rowColumnLayout('globalRigOpRCL', nc=4, cw=[(1,70),(2,120),(3,95),(4,95)], cs=[(1,0),(2,0),(3,10),(4,0)], p=globalRigOpFrame)
    stretchGlobalChk = pc.checkBox('stretchGlobalChk', label='Stretch', v=1, cc=pc.Callback(globalStretchSwitch),p='globalRigOpRCL')
    scaleTypeGlobalOpGrp = pc.optionMenu('scaleTypeGlobalOpGrp', l='Method:', p=globalRigOpRCL)
    pc.menuItem(l='scale')
    pc.menuItem(l='translate')
    volGlobalChk = pc.checkBox('volGlobalChk', label='Volume', v=1, p=globalRigOpRCL)
    midGlobalChk = pc.checkBox('midGlobalChk', label='Mid Lock', v=1, p=globalRigOpRCL)

    globalRigXtraOpRCL = pc.rowColumnLayout('globalRigXtraOpRCL', nc=2, cw=[(1,140),(2,300)], p=createRigColumnLayout)

    globalRigXtraOpFrame = pc.frameLayout('globalRigXtraOpFrame', l='IK FK :', collapsable=False, collapse=False, borderStyle='etchedOut', marginHeight=3, marginWidth=1, p=globalRigXtraOpRCL)

    globalRigXtraOpColumn = pc.columnLayout('globalRigXtraOpColumn', adj=1, p=globalRigXtraOpFrame)

    rigIkFkOpRCL = pc.rowColumnLayout('rigIkFkOpRCL', nc=2, cw=[(1,120),(2,20)], p=globalRigXtraOpColumn)

    rotTypeGlobalOpGrp = pc.optionMenu('rotTypeGlobalOpGrp', l='Method :', p=rigIkFkOpRCL)
    pc.menuItem(l='constrain')
    # menuItem -l "utilNode";
    globalfill1 = pc.text('globalfill1', l='', p=rigIkFkOpRCL)

    rigTentacleOpRCL = pc.rowColumnLayout('rigTentacleOpRCL', nc=2, cw=[(1,65),(2,75)], p=globalRigXtraOpColumn)

    buildGlobalTitle = pc.text('buildGlobalTitle', l='Tentacle:', fn='boldLabelFont', p='rigTentacleOpRCL')
    globalfill2 = pc.text('globalfill2', l='', p='rigTentacleOpRCL')

    dynamicGlobalChk = pc.checkBox('dynamicGlobalChk', l='Dynamic', v=1, p='rigTentacleOpRCL')
    offsetGlobalChk = pc.checkBox('offsetGlobalChk', l='Offset Ctrl', v=1, p='rigTentacleOpRCL')
    
    globalRigJointOpFrame = pc.frameLayout('globalRigJointOpFrame',l='Joint Options :', collapsable=False, collapse=False, borderStyle='etchedOut', p=globalRigXtraOpRCL)

    globalRigJointOpRCL = pc.rowColumnLayout('globalRigJointOpRCL', nc=2, cw=[(1,145),(2,145)], p=globalRigJointOpFrame)
    globalRigAddTitle = pc.text('globalRigAddTitle', l='Add', align='center', p=globalRigJointOpRCL)
    globalRigRemoveTitle = pc.text('globalRigRemoveTitle', l='Remove', align='center', p=globalRigJointOpRCL)
    AddTwistJointBtn = pc.button('AddTwistJointBtn', l='Twist Joint', c=pc.Callback(atu.addTwistJointsAttr,'twistJoints'), p=globalRigJointOpRCL)
    RemoveTwistJointBtn = pc.button('RemoveTwistJointBtn', l='Twist Joint', c=pc.Callback(atu.removeTwistJointsAttr,'twistJoints'),p=globalRigJointOpRCL)
    AddSplineJointsBtn = pc.button('AddSplineJointsBtn', l='Spline Joints', c=pc.Callback(atu.addSplineJointsAttrs,'joints'), p=globalRigJointOpRCL)
    RemoveSplineJointsBtn = pc.button('RemoveSplineJointsBtn', l='Spline Joints', c=pc.Callback(atu.removeTwistJointsAttr,'joints'), p=globalRigJointOpRCL)

    createAnimRigForm = pc.formLayout('createAnimRigForm', p=createRigColumnLayout)
    createAnimRigBtn = pc.button('createAnimRigBtn', h=420, l='CREATE ANIMATION RIG',  c=pc.Callback(cRig.createRig), p=createAnimRigForm)

    createAnimRigForm = pc.formLayout('createAnimRigForm', e=True, af=[(createAnimRigBtn,'top',3),(createAnimRigBtn,'left',0)], ap=[(createAnimRigBtn,'right',0,100)])	
    
    moduleRigTab = pc.tabLayout('moduleRigTab', edit=True, tabLabel=[(createSkColumnLayout,'Create Skeleton'),(createRigColumnLayout,'Create Rig')])
    
    # UI Edits
    sideModulePrefix = pc.optionMenu('sideModulePrefix', e=True, v='lt/rt')
    spineAxisOM = pc.optionMenu('spineAxisOM', e=True, v='y')
    neckAxisOM = pc.optionMenu('neckAxisOM', e=True, v='y')
    tentacleAxisOM = pc.optionMenu('tentacleAxisOM', e=True, v='z')

    pc.showWindow(moduleTemplatesWin)

def updateIntFToScrollBar(ScrollBar, intField):

    val = pc.intScrollBar(ScrollBar, q=True, v=True)
    pc.intField(intField, e=True, v=val)

def chooseModuleTemplatesDir():
    pc.fileBrowserDialog(mode=4, fc=pc.Callback(updateModuleTemplatesDirPath), an='Pick Your Skeleton Templates Directory')

def updateModuleTemplatesDirPath(path, mode):
    pc.textField(moduleTempdirTF, e=False, tx=(path+"/"))

def exportModuleTemplates():
    templateDir = pc.textField(moduleTempdirTF, q=True, tx=True)
    objs = pc.ls(sl=True)

    if (len(objs)>0 and len(objs)<2):
        for obj in objs:
            pc.select(obj)
            path = pc.fileDialog(mode=1, title='export ', directoryMask=(templateDir+'/*.ma'))
            if (path!= ''):
                pc.fileBrowserDialog(path, es=True, type='mayaAscii')
                print "successfully exported objects! \n"
            else:
                print "operation calceled";		    	    
    else:
        pc.error('Too many objects selected. Select root Node and try again')

def importModuleTemplates():
    templateDir = pc.textField('moduleTempdirTF', q=True, tx=True)
    path = pc.fileDialog(mode=0, directoryMask=(templateDir+'/*.ma'))
    if path != '':
        pc.file(path, i=True, type='mayaAscii')
        print('successfully imported objects! \n')
    else:
        print('operation calceled')

def armFingersModuleSwitch():
    switch = pc.checkBox('armFingersChk', q=True, v=True)
    if switch:
        pc.text('noArmFingersJointsTitle', e=True, en=1) 
        pc.intField('noArmFingersJointISG', e=True, en=1)
        pc.text('noArmFingersSegJointsTitle', e=True, en=1)
        pc.intField('noArmFingersSegJointISG', e=True, en=1)
    else:
        pc.text('noArmFingersJointsTitle', e=True, en=0)
        pc.intField('noArmFingersJointISG', e=True, en=0)
        pc.text('noArmFingersSegJointsTitle', e=True, en=0)
        pc.intField('noArmFingersSegJointISG', e=True, en=0)

def legFingersModuleSwitch():
    switch = pc.checkBox('legFingersChk', q=True, v=True)
    if switch:
        pc.text('noLegFingersJointsTitle', e=True, en=1)
        pc.intField('noLegFingersJointISG', e=True, en=1)
        pc.text('noLegFingersSegJointsTitle', e=True, en=1)
        pc.intField('noLegFingersSegJointISG', e=True, en=1)
    else:
        pc.text('noLegFingersJointsTitle', e=True, en=0)
        pc.intField('noLegFingersJointISG', e=True, en=0)
        pc.text('noLegFingersSegJointsTitle', e=True, en=0)
        pc.intField('noLegFingersSegJointISG', e=True, en=0)

def bipedFingersModuleSwitch():
    switch = pc.checkBox('bipedFingersChk', q=True, v=True)
    if switch:
        pc.text('noBipedFingersJointsTitle', e=True, en=1)
        pc.intField('noBipedFingersJointISG', e=True, en=1) 
    else:
        pc.text('noBipedFingersJointsTitle', e=True, en=0)
        pc.intField('noBipedFingersJointISG', e=True, en=0) 

def bipedToesModuleSwitch():
    switch = pc.checkBox('bipedToesChk', q=True, v=True)
    if switch:
        pc.text('noBipedToesJointsTitle', e=True, en=1)
        pc.intField('noBipedToesJointISG', e=True, en=1) 
    else:
        pc.text('noBipedToesJointsTitle', e=True, en=0)
        pc.intField('noBipedToesJointISG', e=True, en=0)

def quadToesModuleSwitch():
    switch = pc.checkBox('quadToesChk', q=True, v=True)
    if switch:
        pc.text('noQuadToesJointsTitle', e=True, en=1)
        pc.intField('noQuadToesJointISG', e=True, en=1) 
    else:
        pc.text('noQuadToesJointsTitle', e=True, en=0)
        pc.intField('noQuadToesJointISG', e=True, en=0)

def globalStretchSwitch():
    switch = pc.checkBox('stretchGlobalChk', q=True, v=True) 
    if switch:
        pc.optionMenu('scaleTypeGlobalOpGrp', e=True, en=1)
        pc.checkBox('volGlobalChk', e=True, en=1)
        pc.checkBox('midGlobalChk', e=True, en=1)
        pc.checkBox('volGlobalChk', e=True, v=1)
        pc.checkBox('midGlobalChk', e=True, v=1) 
    else:
        pc.optionMenu('scaleTypeGlobalOpGrp', e=True, en=0)
        pc.checkBox('volGlobalChk', e=True, v=0)
        pc.checkBox('volGlobalChk', e=True, en=0)
        pc.checkBox('midGlobalChk', e=True, v=0)
        pc.checkBox('midGlobalChk', e=True, en=0)