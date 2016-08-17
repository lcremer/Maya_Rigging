import pymel.core as pc

#from ..Core import *
from Transform import *
from String import *
from CharUtilsLib import *
from CurveUtilLib import *

def CurveUtilUI():
    global curveUtilWindow; curveUtilWindow = 'curveUtilWindow'
    if pc.window(curveUtilWindow,exists=True):
        pc.deleteUI(curveUtilWindow)

    pc.window(curveUtilWindow,t='AutoRig: Curve Utils',wh=(250,570),mxb=False,mnb=True,resizeToFitChildren=True,sizeable=True,menuBar=True)
    pc.menu(label='File')
    # pc.menuItem(l='') Install Shelf Button
    pc.menuItem(divider=True)
    pc.menuItem(label='Close',c=pc.Callback(pc.deleteUI, curveUtilWindow))
    # pc.menu label = 'Help' helpMenu
    # pc.menuItem(label=) HelpWindow

    mainCrvUtilColumn = pc.columnLayout('mainCrvUtilColumn',adj=1,p=curveUtilWindow)
    
    crvNamePrefixFrame = pc.frameLayout('crvNamePrefixFrame',l='Prefix',collapsable=False,collapse=False,borderStyle='etchedIn',p=mainCrvUtilColumn)
    crvNamePrefixRCL = pc.rowColumnLayout('crvNamePrefixFrame',nc=2,cw=[(1,175),(2,60)])
    curveConNameTFG = pc.textFieldGrp('curveConNameTFG',label='Name:',tx='',cw2=(40,130),p=crvNamePrefixRCL)
    zeroGrpCB = pc.checkBox('zeroGrpCB',label='Zero Grp',p=crvNamePrefixRCL)

    curveUtilShapeRCL = pc.rowColumnLayout(nc=2,cw=[(1,175),(2,125)],p=mainCrvUtilColumn)
    aWireTypes = ['arrow',
                  'circleCross',
                  'sphereCross',
                  'pyramid',
                  'pin1',
                  'directions',
                  'trans',
                  'foot',
                  'rotArrow',
                  'circleOrient',
                  'cross',
                  'square',
                  'cube1',
                  'cube2',
                  'orient',
                  'circle',
                  'sphere',
                  'plus',
                  'triangle',
                  'arc180',
                  'arc240',
                  'cone',
                  'thinSingleArrow',
                  'thinDoubleArrow',
                  'thinRotArrow90',
                  'thinRotArrow180',
                  'thinCross',
                  'fatArc180',
                  'pin2',
                  'fatDoubleArrow',
                  'fatRotArrow90',
                  'fatRotArrow180',
                  'locator']
    # NOTE: list is not sorted
    wireName = ''
    curveShapeTitle = pc.text(fn='boldLabelFont',l='Curve Shape:',align='left',p=curveUtilShapeRCL)
    operationTitle = pc.text(fn='boldLabelFont',l='Operation:',align='left',p=curveUtilShapeRCL)
    WireTypeTSL = pc.textScrollList('WireTypeTSL',h=90,allowMultiSelection=False,dcc=pc.Callback(createControl),p=curveUtilShapeRCL)
    for wireName in aWireTypes:
        pc.textScrollList(WireTypeTSL,e=True,append=wireName)
    curveOperationRBG = pc.radioButtonGrp('curveOperationRBG',w=125, label='', numberOfRadioButtons=4, vr=True, labelArray4=['Position','Shape Parent','Shape Replace','Parent Constrain'], sl=1, cw2=[1,124], p=curveUtilShapeRCL)
    mainForm = pc.formLayout(p=mainCrvUtilColumn)
    axisSep = pc.separator(height=5,style='out')
    axisTitle = pc.text(fn='boldLabelFont',l='Axis',align='left')
    facingRdBnCol = pc.radioCollection('facingRdBnCol')
    facingXPosRdBn = pc.radioButton('facingXPosRdBn',label='X')
    facingYPosRdBn = pc.radioButton('facingYPosRdBn',label='Y')
    facingZPosRdBn = pc.radioButton('facingZPosRdBn',label='Z')
    pc.radioCollection(facingRdBnCol,e=True,sl=facingXPosRdBn)
    negChBox = pc.checkBox('negChBox',label='neg',align='left')
    locknHideSep = pc.separator(height=5,style='out')
    locknHideTitle = pc.text(fn='boldLabelFont',l='Lock and Hide',align='left')
    locknHideCBG = pc.checkBoxGrp('locknHideCBG',ncb=4,l1='Translate', l2='Rotate', l3='Scale', l4='vis', cw4=(70,65,54,54), va4=(0,0,0,0))
    locknHideEndSep = pc.separator(height=5,style='out')

    typeTitle = pc.text(fn='boldLabelFont',l='Type',align='left')
    typeRdBnCol = pc.radioCollection()
    curveRdBn = pc.radioButton('curveRdBn',label='as Transform')
    jointRdBn = pc.radioButton('jointRdBn',label='as Joint')
    pc.radioCollection(typeRdBnCol,e=True,sl=curveRdBn)
    wirescaleSep = pc.separator(height=5,style='out')
    conScaleTitle = pc.text(fn='boldLabelFont',l='Controller Scale',align='left')    
    conSize = pc.floatField('conSize',v=1.0,precision=1,enterCommand=pc.Callback(updateConSize))
    createSep1 = pc.separator(height=5,style='out')
    snapBtn = pc.button(l='Create',command=pc.Callback(createControl))
    closeBtn = pc.button(l='Close',command=pc.Callback(pc.deleteUI,curveUtilWindow))
    createSep2 = pc.separator(height=5,style='out')

    crvUtilXtraFrame = pc.frameLayout(l='Utilities',collapsable=False,collapse=False,borderStyle='etchedIn',p=mainForm)

    utilitiesRCL = pc.rowColumnLayout(nc=2, cw=[(1,118),(2,125)], p=crvUtilXtraFrame)
    pc.button(l="Rename Sel Shape", command=pc.Callback(shapeRename,''), p=utilitiesRCL)
    pc.button(l='Rename All Shape', command=pc.Callback(shapeRename,'*'), p=utilitiesRCL)
    pc.button(l='Edit Shape', command=pc.Callback(transformUtilUI), p=utilitiesRCL)
    pc.button(l='Curve Maker', command=pc.Callback(curveControlMaker), p=utilitiesRCL)
    pc.button(l='Shape Parent', command=pc.Callback(UDShapeParent), p=utilitiesRCL)	
    pc.button(l='Snap', command=pc.Callback(Snap,'',''), p=utilitiesRCL)

    fmColor = pc.frameLayout(l='Color',collapsable=False,collapse=False,borderStyle='etchedIn',p=mainCrvUtilColumn)
    mainFmColorColumn = pc.columnLayout(p=fmColor)
    pc.gridLayout(numberOfRows=4, numberOfColumns=8, cellWidthHeight=(30,20), p=mainFmColorColumn)
    pc.iconTextButton(bgc=(.627,.627,.627), command=pc.Callback(updateColorSlider,0))
    pc.iconTextButton(bgc=(.467,.467,.467), command=pc.Callback(updateColorSlider,1))
    pc.iconTextButton(bgc=(.000,.000,.000), command=pc.Callback(updateColorSlider,2))
    pc.iconTextButton(bgc=(.247,.247,.247), command=pc.Callback(updateColorSlider,3))
    pc.iconTextButton(bgc=(.498,.498,.498), command=pc.Callback(updateColorSlider,4))
    pc.iconTextButton(bgc=(0.608,0,0.157), command=pc.Callback(updateColorSlider,5))
    pc.iconTextButton(bgc=(0,0.016,0.373), command=pc.Callback(updateColorSlider,6))
    pc.iconTextButton(bgc=(0,0,1), command=pc.Callback(updateColorSlider,7))
    pc.iconTextButton(bgc=(0,0.275,0.094), command=pc.Callback(updateColorSlider,8))
    pc.iconTextButton(bgc=(0.145,0,0.263), command=pc.Callback(updateColorSlider,9))
    pc.iconTextButton(bgc=(0.78,0,0.78), command=pc.Callback(updateColorSlider,10))
    pc.iconTextButton(bgc=(0.537,0.278,0.2), command=pc.Callback(updateColorSlider,11))
    pc.iconTextButton(bgc=(0.243,0.133,0.122), command=pc.Callback(updateColorSlider,12))
    pc.iconTextButton(bgc=(0.6,0.145,0), command=pc.Callback(updateColorSlider,13))
    pc.iconTextButton(bgc=(1,0,0), command=pc.Callback(updateColorSlider,14))
    pc.iconTextButton(bgc=(0,1,0), command=pc.Callback(updateColorSlider,15))
    pc.iconTextButton(bgc=(0,0.255,0.6), command=pc.Callback(updateColorSlider,16))
    pc.iconTextButton(bgc=(1,1,1), command=pc.Callback(updateColorSlider,17))
    pc.iconTextButton(bgc=(1,1,0), command=pc.Callback(updateColorSlider,18))
    pc.iconTextButton(bgc=(0.388,0.863,1), command=pc.Callback(updateColorSlider,19))
    pc.iconTextButton(bgc=(0.263,1,0.635), command=pc.Callback(updateColorSlider,20))
    pc.iconTextButton(bgc=(1,0.686,0.686), command=pc.Callback(updateColorSlider,21))
    pc.iconTextButton(bgc=(0.89,0.675,0.475), command=pc.Callback(updateColorSlider,22))
    pc.iconTextButton(bgc=(1,1,0.384), command=pc.Callback(updateColorSlider,23))
    pc.iconTextButton(bgc=(0,0.6,0.325), command=pc.Callback(updateColorSlider,24))
    pc.iconTextButton(bgc=(0.627,0.412,0.188), command=pc.Callback(updateColorSlider,25))
    pc.iconTextButton(bgc=(0.62,0.627,0.188), command=pc.Callback(updateColorSlider,26))
    pc.iconTextButton(bgc=(0.408,0.627,0.188), command=pc.Callback(updateColorSlider,27))
    pc.iconTextButton(bgc=(0.188,0.627,0.365), command=pc.Callback(updateColorSlider,28))
    pc.iconTextButton(bgc=(0.188,0.627,0.627), command=pc.Callback(updateColorSlider,29))
    pc.iconTextButton(bgc=(0.188,0.404,0.627), command=pc.Callback(updateColorSlider,30))
    pc.iconTextButton(bgc=(0.435,0.188,0.627), command=pc.Callback(updateColorSlider,31))
    conColor = pc.colorIndexSliderGrp('conColor',min=0,max=31,value=0,cw2=(70,163),p=mainFmColorColumn)

    creditSep = pc.separator(height=5,style='out',p=mainCrvUtilColumn)

    pc.formLayout(mainForm,e=True,af=[(axisSep,'top',0),(axisSep,'left',0)],ap=[(axisSep,'right',0,100)])
    pc.formLayout(mainForm,e=True,ac=[(axisTitle,'top',2,axisSep)],af=[(axisTitle,'left',0)],ap=[(axisTitle,'right',0,20)])
    pc.formLayout(mainForm,e=True,ac=[(facingXPosRdBn,'top',0,axisSep),(facingXPosRdBn,'left',0,axisTitle)],ap=[(facingXPosRdBn,'right',0,40)])
    pc.formLayout(mainForm,e=True,ac=[(facingYPosRdBn,'top',0,axisSep),(facingYPosRdBn,'left',0,facingXPosRdBn)],ap=[(facingYPosRdBn,'right',0,60)])
    pc.formLayout(mainForm,e=True,ac=[(facingZPosRdBn,'top',0,axisSep),(facingZPosRdBn,'left',0,facingYPosRdBn)],ap=[(facingZPosRdBn,'right',0,80)])
    pc.formLayout(mainForm,e=True,ac=[(negChBox,'top',1,axisSep),(negChBox,'left',0,facingZPosRdBn)],ap=[(negChBox,'right',0,100)])
    pc.formLayout(mainForm,e=True,ac=[(locknHideSep,'top',0,facingXPosRdBn)],af=[(locknHideSep,'left',0)],ap=[(locknHideSep,'right',0,100)])
    pc.formLayout(mainForm,e=True,ac=[(locknHideTitle,'top',0,locknHideSep)],af=[(locknHideTitle,'left',0)],ap=[(locknHideTitle,'right',0,100)])
    pc.formLayout(mainForm,e=True,ac=[(locknHideCBG,'top',0,locknHideTitle)],af=[(locknHideCBG,'left',0)],ap=[(locknHideCBG,'right',0,100)])
    pc.formLayout(mainForm,e=True,ac=[(locknHideEndSep,'top',0,locknHideCBG)],af=[(locknHideEndSep,'left',0)],ap=[(locknHideEndSep,'right',0,100)])
    pc.formLayout(mainForm,e=True,ac=[(typeTitle,'top',2,locknHideEndSep)],af=[(typeTitle,'left',0)],ap=[(typeTitle,'right',0,20)])
    pc.formLayout(mainForm,e=True,ac=[(curveRdBn,'top',0,locknHideEndSep),(curveRdBn,'left',0,typeTitle)],ap=[(curveRdBn,'right',0,60)])
    pc.formLayout(mainForm,e=True,ac=[(jointRdBn,'top',0,locknHideEndSep),(jointRdBn,'left',0,curveRdBn)],ap=[(jointRdBn,'right',0,100)])
    pc.formLayout(mainForm,e=True,ac=[(wirescaleSep,'top',5,typeTitle)],af=[(wirescaleSep,'left',0)],ap=[(wirescaleSep,'right',0,100)])
    pc.formLayout(mainForm,e=True,ac=[(conScaleTitle,'top',2,wirescaleSep)],af=[(conScaleTitle,'left',0)],ap=[(conScaleTitle,'right',0,50)])
    pc.formLayout(mainForm,e=True,ac=[(conSize,'top',0,wirescaleSep),(conSize,'left',0,conScaleTitle)],ap=[(conSize,'right',0,100)])
    pc.formLayout(mainForm,e=True,ac=[(createSep1,'top',0,conSize)],af=[(createSep1,'left',0)],ap=[(createSep1,'right',0,100)])
    pc.formLayout(mainForm,e=True,ac=[(snapBtn,'top',0,createSep1)],af=[(snapBtn,'left',2)],ap=[(snapBtn,'right',0,50)])
    pc.formLayout(mainForm,e=True,ac=[(closeBtn,'top',0,createSep1),(closeBtn,'left',0,snapBtn)],ap=[(closeBtn,'right',2,100)])
    pc.formLayout(mainForm,e=True,ac=[(createSep2,'top',0,snapBtn)],af=[(createSep2,'left',0)],ap=[(createSep2,'right',0,100)])
    pc.formLayout(mainForm,e=True,ac=[(crvUtilXtraFrame,'top',0,createSep2)],af=[(crvUtilXtraFrame,'left',0)],ap=[(crvUtilXtraFrame,'right',0,100)])

    pc.showWindow(curveUtilWindow) 

def updateConSize():
    sel = pc.ls(sl=True)
    conScale = pc.floatField('conSize',q=True,v=True)
    if len(sel) != 0:
        resizeCurves(None,1,1,1,conScale)

def updateColorSlider(color):
    pc.colorIndexSliderGrp('conColor',e=True,value=color)
    objs = pc.ls(sl=True)
    if len(objs) != 0:
        for o in objs:
            shape = pc.listRelatives(o,f=True,s=True)
            color = pc.colorIndexSliderGrp('conColor',q=True,v=True)
            if color > 0:
                pc.setAttr(shape[0]+'.overrideEnabled',1)
                pc.setAttr(shape[0]+'.overrideColor',color-1)

def facingAxisWrapper():
    facingAxis = ''    
    facingX = pc.radioButton('facingXPosRdBn',q=True,select=True)
    facingY = pc.radioButton('facingYPosRdBn',q=True,select=True)
    facingZ = pc.radioButton('facingZPosRdBn',q=True,select=True)
    facingNeg = pc.checkBox('negChBox',q=True,v=True)

    if facingX == 1: facingAxis = 'X'
    if facingY == 1: facingAxis = 'Y'
    if facingZ == 1: facingAxis = 'Z'
    fixFacingAxis(facingAxis,facingNeg)

def createControl():    
    objs = pc.ls(sl=True,tr=True)
    size = len(objs)
    shape = []
    con = []
    
    name = pc.textFieldGrp('curveConNameTFG',q=True,tx=True)    
    wireShape = pc.textScrollList('WireTypeTSL',q=True,si=True)    
    zeroGrp = pc.checkBox('zeroGrpCB',q=True,v=True)    
    curveState = pc.radioButton('curveRdBn',q=True,select=True)    
    jointState = pc.radioButton('jointRdBn',q=True,select=True)    
    operationState = pc.radioButtonGrp('curveOperationRBG',q=True,select=True)    
    lockAndHideTrans = pc.checkBoxGrp('locknHideCBG',q=True,v1=True)    
    lockAndHideRot = pc.checkBoxGrp('locknHideCBG',q=True,v2=True)
    lockAndHideScale = pc.checkBoxGrp('locknHideCBG',q=True,v3=True)
    lockAndHideVis = pc.checkBoxGrp('locknHideCBG',q=True,v4=True)
    conScale = pc.floatField('conSize',q=True,v=True)

    if operationState == 1:
        if curveState == 1:
            con = curveControl(wireShape[0],'curve')
        else:
            con = curveControl(wireShape[0],'joint')
        for x in range(size):
            if name != '':
                if size > 1:
                    con[x] = pc.rename(con[x],name+str(x+1))
                else:
                    con[0] = pc.rename(con[0],name)
        if size == 0:
            con[0] = pc.rename(con[0],name)

        pc.select(con,r=True)
        if zeroGrp == 1:
            quickZeroOut('')
        resizeCurves(None,1,1,1,conScale)
        locknHide('',lockAndHideTrans,lockAndHideRot,lockAndHideScale,lockAndHideVis)
        facingAxisWrapper()
        for c in con:
            shape = pc.listRelatives(c,f=True,s=True)
            color = pc.colorIndexSliderGrp('conColor',q=True,v=True)
            if color > 0:
                pc.setAttr(shape[0]+'.overrideEnabled',1)
                pc.setAttr(shape[0]+'.oerrideColor',color-1)
        pc.select(con,r=True)

    if operationState == 2:
        if len(objs) <= 0:
            pc.error('Selection is empty. Select transform and try again')
        else:
            shapeParent('',wireShape[0])
            pc.select(objs,r=True)
            resizeCurves(None,1,1,1,conScale)
            locknHide('',lockAndHideTrans,lockAndHideRot,lockAndHideScale,lockAndHideVis)
            facingAxisWrapper()
            color = pc.colorIndexSliderGrp('conColor',q=True,v=True)
            if color > 0:
                for o in objs:
                    shape = pc.listRelatives(o,f=True,s=True)
                    for s in shape:
                        pc.setAttr(s+'.overrideEnabled',1)
                        pc.setAttr(s+'.overrideColor',color-1)

    if operationState == 3:
        if len(objs) <= 0:
            pc.error('Selection is empty. Select transform and try again')
        else:
            shapeReplace('',wireShape[0])
            pc.select(objs,r=True)
            resizeCurves(None,1,1,1,conScale)
            locknHide('',lockAndHideTrans,lockAndHideRot,lockAndHideScale,lockAndHideVis)
            facingAxisWrapper()
            for o in objs:
                shape = pc.listRelatives(o,f=True,s=True)
                color = pc.colorIndexSliderGrp('conColor',q=True,v=True)
                if color > 0:
                    pc.setAttr(shape[0]+'.overrideEnabled',1)
                    pc.setAttr(shape[0]+'.overrideColor',color-1)

    if operationState == 4:
        if curveState == 1:
            con = curveControl(wireShape[0],'curve')
        else:
            con = curveControl(wireShape[0],'joint')
        for x in range(size):
            if name != '':
                if size > 1:
                    con[x] = pc.rename(con[x],name+(x+1))
                elif size == 1:
                    con[0] == pc.rename(con[0],name)
                else: # TODO: wtf not just do this?
                    con[0] == pc.rename(con[0],name)
                pc.parentConstraint(con[x],objs[x],mo=True,weight=True)
        pc.select(con,r=True)
        if zeroGrp == 1:
            quickZeroOut('')
        resizeCurves(None,1,1,1,conScale)
        locknHide('',lockAndHideTrans,lockAndHideRot,lockAndHideScale,lockAndHideVis)
        facingAxisWrapper()
        for c in con:
            shape = pc.listRelatives(c,f=True,s=True)
            color = pc.colorIndexSliderGrp('conColor',q=True,v=True)
            if color > 0:
                pc.setAttr(shape[0]+'.overrideEnabled',1)
                pc.setAttr(shape[0]+'.overrideColor',color-1)
        pc.select(con,r=True)        

def transformUtilUI():
    if pc.window('transformUtilWin',exists=True):
        pc.deleteUI('transformUtilWin')

    transformUtilWin = pc.window('transformUtilWin',
                                 t='Curve transform Win',
                                 wh=[232,250],
                                 resizeToFitChildren=True,
                                 sizeable=False)

    transformUtilMainColumn = pc.columnLayout('transformUtilMainColumn',adj=1)

    moveCurveFrame = pc.frameLayout('moveCurveFrame',
                                    l='MOVE CURVE',
                                    collapsable=True,
                                    collapse=False,
                                    borderStyle='etchedIn',
                                    marginHeight=3,
                                    marginWidth=1,)

    editMoveform = pc.formLayout('editMoveform')

    moveXaxisBtn = pc.button('moveXaxisBtn',l='X Axis',w=70,command=pc.Callback(moveCurveWrapper,'X','move'))
    moveYaxisBtn = pc.button('moveYaxisBtn',l='Y Axis',w=70,command=pc.Callback(moveCurveWrapper,'Y','move'))
    moveZaxisBtn = pc.button('moveZaxisBtn',l='Z Axis',w=70,command=pc.Callback(moveCurveWrapper,'Z','move'))
    moveDegree = [10,5,1,0,-1,-5,-10]    
    moveCurveFSG = pc.floatSliderGrp('moveCurveFSG',f=1,l=' %',v=0,min=-360,max=360,cw3=(20,30,20),pre=0)
    pc.popupMenu(p=moveCurveFSG)
    for m in moveDegree:
        pc.menuItem(l=m,c=pc.Callback(pc.floatSliderGrp,moveCurveFSG,e=True,v=m))

    pc.formLayout(editMoveform,e=True,af=[(moveCurveFSG,'top',0),(moveCurveFSG,'left',0)],ap=[(moveCurveFSG,'right',0,100)])
    pc.formLayout(editMoveform,e=True,ac=[(moveXaxisBtn,'top',5,moveCurveFSG)],af=[(moveXaxisBtn,'left',0)],ap=[(moveXaxisBtn,'right',0,100)])
    pc.formLayout(editMoveform,e=True,ac=[(moveYaxisBtn,'top',5,moveCurveFSG),(moveYaxisBtn,'left',0,moveXaxisBtn)],ap=[(moveYaxisBtn,'right',0,66)])
    pc.formLayout(editMoveform,e=True,ac=[(moveZaxisBtn,'top',5,moveCurveFSG),(moveZaxisBtn,'left',0,moveYaxisBtn)],ap=[(moveZaxisBtn,'right',0,100)])

    pc.setParent('..')
    pc.setParent('..')    

    rotateCurveFrame = pc.frameLayout('rotateCurveFrame',
                                      l='ROTATE CURVE',
                                      collapsable=True,
                                      collapse=False,
                                      borderStyle='etchedIn',
                                      marginHeight=3,
                                      marginWidth=1)

    editRotateform = pc.formLayout('editRotateform')

    rotateXaxisBtn = pc.button('rotateXaxisBtn',l='X Axis',w=70,command=pc.Callback(moveCurveWrapper,'X','rotate'))
    rotateYaxisBtn = pc.button('rotateYaxisBtn',l='Y Axis',w=70,command=pc.Callback(moveCurveWrapper,'Y','rotate'))
    rotateZaxisBtn = pc.button('rotateZaxisBtn',l='Z Axis',w=70,command=pc.Callback(moveCurveWrapper,'Z','rotate'))
    rotateDegree = [360,270,180,90,45,0,-45,-90,-180,-270,-360]
    rotateCurveFSG = pc.floatSliderGrp('rotateCurveFSG',f=1, l='  %', v=90, min=-360, max=360, cw3=(20,30,20), pre=0)
    pc.popupMenu(p=rotateCurveFSG)
    for r in rotateDegree:
        pc.menuItem(l=r,c=pc.Callback(pc.floatSliderGrp,rotateCurveFSG,e=True,v=r))
    rotateValue = pc.floatSliderGrp(rotateCurveFSG,q=True,v=True)

    pc.formLayout(editRotateform,e=True,af=[(rotateCurveFSG,'top',0),(rotateCurveFSG,'left',0)],ap=[(rotateCurveFSG,'right',0,100)])
    pc.formLayout(editRotateform,e=True,ac=[(rotateXaxisBtn,'top',5,rotateCurveFSG)],af=[(rotateXaxisBtn,'left',0)],ap=[(rotateXaxisBtn,'right',0,100)])
    pc.formLayout(editRotateform,e=True,ac=[(rotateYaxisBtn,'top',5,rotateCurveFSG),(rotateYaxisBtn,'left',0,rotateXaxisBtn)],ap=[(rotateYaxisBtn,'right',0,66)])
    pc.formLayout(editRotateform,e=True,ac=[(rotateZaxisBtn,'top',5,rotateCurveFSG),(rotateZaxisBtn,'left',0,rotateYaxisBtn)],ap=[(rotateZaxisBtn,'right',0,100)])

    pc.setParent('..')
    pc.setParent('..')

    scaleCurveFrame = pc.frameLayout('scaleCurveFrame',
                                      l='RESIZE CURVE',
                                      collapsable=True,
                                      collapse=False,
                                      borderStyle='etchedIn',
                                      marginHeight=3,
                                      marginWidth=1)

    editScaleform = pc.formLayout()
    scales = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0]
    resizeFSG = pc.floatSliderGrp('resizeFSG',f=1, l='  %', v=1, min=0.1, max=2.0, cw3=(20,30,20), pre=1)
    pc.popupMenu(p=resizeFSG)
    for s in scales:
        pc.menuItem(l=s,c=pc.Callback(pc.floatSliderGrp,resizeFSG,e=True,v=s))
    global resizeCBG; resizeCBG = pc.checkBoxGrp('resizeCBG',ncb=3, l1='X', l2='Y', l3='Z', cw3=(40,40,40), va3=(1,1,1))
    global resizeBtn; resizeBtn = pc.button(l='Resize Curves',ann='select curves you want to resize, set scale, choose axis (X, Y, Z). WARNING: if selected curve object has multiple shapeNodes you may have to select the actual shapeNodes of that curve to make it scale correctly!!', c=pc.Callback(resizeCurveWrapper))

    pc.formLayout(editScaleform,e=True,af=[(resizeFSG,'top',0),(resizeFSG,'left',0)],ap=[(resizeFSG,'right',0,100)])
    pc.formLayout(editScaleform,e=True,ac=[(resizeCBG,'top',5,resizeFSG)],af=[(resizeCBG,'left',50)],ap=[(resizeCBG,'right',0,100)])
    pc.formLayout(editScaleform,e=True,ac=[(resizeBtn,'top',5,resizeCBG)],af=[(resizeBtn,'left',0)],ap=[(resizeBtn,'right',0,100)])

    pc.setParent('..')
    pc.setParent('..')

    pc.showWindow(transformUtilWin)

def rotateCurveWrapper(axis,mode):
    rotateValue = pc.floatSliderGrp('rotateCurveFSG',q=True,v=True)
    editCurveTransform(axis,mode,rotateValue)

def moveCurveWrapper(axis,mode):
    moveValue = pc.floatSliderGrp('moveCurveFSG',q=True,v=True)
    editCurveTransform(axis,mode,modeValue)

def resizeCurveWrapper():
    scale = pc.floatSliderGrp('resizeFSG',q=True,v=True)
    x = pc.checkBoxGrp(q=True,v1=resizeCBG)
    y = pc.checkBoxGrp(q=True,v2=resizeCBG)
    z = pc.checkBoxGrp(q=True,v3=resizeCBG)
    scale = scale/1.0
    resizeCurves(None,x,y,z,scale)