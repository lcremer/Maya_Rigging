import pymel.core as pc

# from RiggingSystem import *

def splineStretchUI():
    if pc.window('splineStretchWin',exists=True):
        pc.deleteUI('splineStretchWin')

    splineStretchWin = pc.window('splineStretchWin',t='autoRig: Spline Stretch',mxb=False,mnb=False,resizeToFitChildren=True,sizeable=False)

    splineStretchMainForm = pc.formLayout('splineStretchMainForm')
    splineNameTFG = pc.textFieldGrp('splineNameTFG',l='Name:',tx='',cw2=[60,70])
    splineSideTFG = pc.textFieldGrp('splineSideTFG',l='Side:',tx='',cw2=[30,70])
    splineEndSep = pc.separator('splineEndSep',height=5,style='out')
    splineTypeOpGrp = pc.optionMenuGrp('splineTypeOpGrp',l='Method:',cw2=[60,50])
    pc.menuItem(l='scale')
    pc.menuItem(l='translate')

    splineVolCBG = pc.checkBoxGrp('splineVolCBG',l='Volume:', v1=1, cw2=(60,20))
    splineCurveTFBG = 'splineCurveTFBG'
    splineCurveTFBG = pc.textFieldButtonGrp('splineCurveTFBG',label='Curve:', text='', buttonLabel=' select ', bc=pc.Callback(updateTextField,'splineCurveTFBG'), cw3=(60,128,50))
    splineControlTFBG = 'splineControlTFBG'
    splineControlTFBG = pc.textFieldButtonGrp('splineControlTFBG', label='Control:', text='', buttonLabel=' select ', bc=pc.Callback(updateTextField,'splineControlTFBG'), cw3=(60,128,50))
    scaleCBG = pc.checkBoxGrp('scaleCBG',l='Scale:', v1=0, cw2=(60,20), cc=pc.Callback(ssScaleSwitch))
    scaleNodeTFBG = 'scaleNodeTFBG'
    scaleNodeTFBG = pc.textFieldButtonGrp('scaleNodeTFBG', label='Scale Node:', text='', buttonLabel=' select ', bc=pc.Callback(updateTextField, 'scaleNodeTFBG'), cw3=(60,128,50))
    splineSep1 = pc.separator('splineSep1', height=5, style='out')
    splineApplyBtn = pc.button('splineApplyBtn', l='Create', c=pc.Callback(splineStretchPreCMD))
    splineSep2 = pc.separator('splineSep2', height=5, style='out')

    pc.formLayout(splineStretchMainForm,e=True,af=[(splineNameTFG,'top',0),(splineNameTFG,'left',0)])
    pc.formLayout(splineStretchMainForm,e=True,af=[(splineSideTFG,'top',0)],ac=[(splineSideTFG,'left',0,splineNameTFG)])
    pc.formLayout(splineStretchMainForm,e=True,ac=[(splineEndSep,'top',0,splineSideTFG)],af=[(splineEndSep,'left',0)],ap=[(splineEndSep,'right',0,100)])
    pc.formLayout(splineStretchMainForm,e=True,ac=[(splineTypeOpGrp,'top',0,splineEndSep)],af=[(splineTypeOpGrp,'left',0)])
    pc.formLayout(splineStretchMainForm,e=True,ac=[(splineVolCBG,'top',0,splineTypeOpGrp)],af=[(splineVolCBG,'left',0)])
    pc.formLayout(splineStretchMainForm,e=True,ac=[(splineCurveTFBG,'top',0,splineVolCBG)],af=[(splineCurveTFBG,'left',0)])
    pc.formLayout(splineStretchMainForm,e=True,ac=[(splineControlTFBG,'top',0,splineCurveTFBG)],af=[(splineControlTFBG,'left',0)])
    pc.formLayout(splineStretchMainForm,e=True,ac=[(scaleCBG,'top',0,splineControlTFBG)],af=[(scaleCBG,'left',0)])
    pc.formLayout(splineStretchMainForm,e=True,ac=[(scaleNodeTFBG,'top',0,scaleCBG)],af=[(scaleNodeTFBG,'left',0)])
    pc.formLayout(splineStretchMainForm,e=True,ac=[(splineSep1,'top',0,scaleNodeTFBG)],af=[(splineSep1,'left',0)],ap=[(splineSep1,'right',0,100)])
    pc.formLayout(splineStretchMainForm,e=True,ac=[(splineApplyBtn,'top',0,splineSep1)],af=[(splineApplyBtn,'left',0)],ap=[(splineApplyBtn,'right',0,100)])
    pc.formLayout(splineStretchMainForm,e=True,ac=[(splineSep2,'top',0,splineApplyBtn)],af=[(splineSep2,'left',0)],ap=[(splineSep2,'right',0,100)])

    pc.checkBoxGrp(scaleCBG,e=True,v1=True)
    pc.showWindow(splineStretchWin)

def ssScaleSwitch():
    switch = pc.checkBoxGrp(scaleCBG,q=True,v1=True)
    if switch:
        pc.textFieldButtonGrp(scaleNodeTFBG,e=True,en=1)
    else:
        pc.textFieldButtonGrp(scaleNodeTFBG,e=True,en=0)

def splineStretchPreCMD():
    name = pc.textFieldGrp('splineNameTFG',q=True,tx=True)
    side = pc.textFieldGrp('splineSideTFG',q=True,tx=True)
    controller = pc.textFieldButtonGrp('splineControlTFBG',q=True,tx=True)
    stretchType = pc.optionMenuGrp('splineTypeOpGrp',q=True,v=True)
    crv = pc.textFieldButtonGrp('splineCurveTFBG',q=True,tx=True)
    worldScale = pc.textFieldButtonGrp('scaleNodeTFBG',q=True,tx=True)
    volume = pc.checkBoxGrp('splineVolCBG',q=True,v1=True)
    scale = pc.checkBoxGrp('scaleCBG',q=True,v1=True)

    stretchySpline(name, side, controller, stretchType, crv, scale, volume, worldScale)