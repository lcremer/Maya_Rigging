import pymel.core as pc

def fingerManualSwitch():
    switch = pc.checkBoxGrp('manualOpChk',q=True,v1=True)
    if switch:        
        pc.radioButtonGrp('curlFacingRdBnGrp',e=True,en=1)
        pc.radioButtonGrp('spreadFacingRdBnGrp',e=True,en=1)
        pc.radioButtonGrp('stretchFacingRdBnGrp',e=True,en=1)
        pc.radioButtonGrp('spinFacingRdBnGrp',e=True,en=1)
    else:
        pc.radioButtonGrp('curlFacingRdBnGrp',e=True,en=0)
        pc.radioButtonGrp('spreadFacingRdBnGrp',e=True,en=0)
        pc.radioButtonGrp('stretchFacingRdBnGrp',e=True,en=0)
        pc.radioButtonGrp('spinFacingRdBnGrp',e=True,en=0)

def updateTextField(textField):
    sel = pc.ls(sl=True)
    if sel != '' and sel[0] != '':
        pc.textFieldButtonGrp(textField,e=True,tx=sel[0])
    else:
        print 'Nothing was selected. Select an object and try again\n' # TODO: change this

def tentOffsetSwitch():
    switch = pc.checkBoxGrp('offsetChk',q=True,v1=True)
    if switch:
        pc.text('tentfill3',e=True,en=1)
        pc.textField('conOffTentTF',e=True,en=1)
        pc.textField('conOffTentTF',e=True,ed=0)
    else:
        pc.text('tentfill3',e=True,en=0)
        pc.textField('conOffTentTF',e=True,en=0)

def handFkSwitch():
    switch = pc.checkBox('fkConChk',q=True,v=True)
    if switch:
        pc.textField('fkConHandTF',e=True,en=1)
        pc.textField('fkConHandTF',e=True,ed=0)
        # pc.text(fingerSideTitle,e=True,en=1)
        pc.radioButtonGrp('fingerSideRdBnGrp',e=True,en=1)
    else:
        pc.textField('fkConHandTF',e=True,en=0)
        # pc.text(fingerSideTitle,e=True,en=0)
        pc.radioButtonGrp('fingerSideRdBnGrp',e=True,en=0)

def fingerUISwitch(name):
    switch = pc.checkBox((name + 'Chk'),q=True,v=True)
    if switch:
        pc.text((name + 'Title'),e=True,en=1)
        pc.textField((name + 'NameTF'),e=True,en=1)
        pc.textFieldButtonGrp((name + 'JointTFBG'),e=True,en=1)
    else:
        pc.text((name + 'Title'),e=True,en=0)
        pc.textField((name + 'NameTF'),e=True,en=0)
        pc.textFieldButtonGrp((name + 'JointTFBG'),e=True,en=0)

def legUItypeSwitch():
    type = pc.optionMenuGrp('legTypeOpGrp',q=True,value=True)
    if type.lower() == 'quadropad':
        pc.textFieldGrp('toeJointTFBG',e=True,en=1)
    else:
        pc.textFieldGrp('toeJointTFBG',e=True,en=0)

def stretchSwitch():
    switch = pc.checkBox('stretchChk',q=True,v=True)
    if switch:
        pc.optionMenu('scaleTypeOpGrp',e=True,en=1)
        pc.checkBox('volChk',e=True,en=1)
        pc.checkBox('midChk',e=True,en=1)
        pc.checkBox('volChk',e=True,v=1)
        pc.checkBox('midChk',e=True,v=1)
    else:
        pc.optionMenu('scaleTypeOpGrp',e=True,en=0)
        pc.checkBox('volChk',e=True,en=0)
        pc.checkBox('midChk',e=True,en=0)
        pc.checkBox('volChk',e=True,v=0)
        pc.checkBox('midChk',e=True,v=0)

def selectSpaceSwitchName():
    index = pc.textScrollList('spaceSwitchParentTSL',q=True,selectIndexedItem=True)
    pc.textScrollList('spaceSwitchNameTSL',e=True,da=True)
    pc.textScrollList('spaceSwitchNameTSL',e=True,selectIndexedItem=index[0])
    nameTF = pc.textScrollList('spaceSwitchNameTSL',q=True,si=True)
    pc.textField('newSpaceNameTF',e=True,tx=nameTF[0])

def changeSpaceName():
    newName = pc.textField('newSpaceNameTF',q=True,tx=True)
    selSpace = pc.textScrollList('spaceSwitchNameTSL',q=True,sii=True)
    pc.textScrollList('spaceSwitchNameTSL',e=True,rii=selSpace[0])
    pc.textScrollList('spaceSwitchNameTSL',e=True,ap=(selSpace[0],newName))
    pc.textScrollList('spaceSwitchNameTSL',e=True,sii=selSpace[0])

def addParentSpace():
    space = pc.ls(sl=True)
    if space[0]=="": pc.error('Selection is empty...')

    for each in space:
        pc.textScrollList('spaceSwitchParentTSL',e=True,a=each)
        pc.textScrollList('spaceSwitchNameTSL',e=True,a=each)

def deleteParentSpace():
    selSpace = pc.textScrollList('spaceSwitchParentTSL',q=True,sii=True)
    pc.textScrollList(spaceSwitchParentTSL,e=True,rii=selSpace[0])
    pc.textScrollList(spaceSwitchNameTSL,e=True,rii=selSpace[0])

def deleteAllParentSpace():
    response = pc.confirmDialog(t='Are you sure?',message='Do you want to remove all items',button=['Yes','No'],defaultButton='Yes')
    if respone == 'Yes':
        pc.textScrollList('spaceSwitchParentTSL',e=True,ra=True)
        pc.textScrollList('spaceSwitchNameTSL',e=True,ra=True)
        pc.textField('newSpaceNameTF',e=True,tx='')

def spaceNodeParentUpdate():
    node = pc.textFieldButtonGrp('parentConTFBG',q=True,tx=True)
    pc.textFieldButtonGrp('parentGrpTFBG',e=True,tx='')
    parent = getParent(node) # TODO: implement and source getParent
    if parent != '':
        pc.textFieldButtonGrp('parentGrpTFBG',e=True,tx=parent)
    else:
        pc.error('No parent found. Load parent node manually') # TODO: redo this

def AutoRigUI():
    
    if pc.window('autoRigWindow', exists=True):
        pc.deleteUI('autoRigWindow')

    # Main Window    
    autoRigWindow = pc.window('autoRigWindow', t='AutoRig', wh=(389,485), mxb=False, mnb=True, resizeToFitChildren=True, sizeable=True, menuBar=True)    

    # Option Menu
    pc.menu(label='File')
    # pc.menuItem(label='Install shelf button') # c='installShelfBtn()' autoRigging kinConnect
    pc.menuItem(divider=True)
    pc.menuItem(label='Close',c=pc.Callback(autoRigWindow))
    
    pc.menu(label='Edit')    
    autoMirrorOptionMi = pc.menuItem('autoMirrorOptionMi', label='Auto Mirror',checkBox=False)
    pc.menuItem(divider=True)
    pc.menuItem(label='Toggle Selectable',c=pc.Callback(toggleBaseSkeletonSelect))
    pc.menuItem(label='Select Skin Joint',c=pc.Callback(selectSkinJoints))
    pc.menuItem(divider=True)

    pc.menu(label='Tools')
    pc.menuItem(label='Curve Utilities',c=pc.Callback(CurveUtilUI))
    pc.menuItem(divider=True)
    pc.menuItem(label='IK Stretch UI', c=pc.Callback(stretchNetworkUI))
    pc.menuItem(label='Spline stretch UI', c=pc.Callback(splineStretchUI))

    # Main Column    
    mainColumn = pc.columnLayout('mainColumn', adj=True, p=autoRigWindow)

    # Name Prefix    
    prefixFrame = pc.frameLayout('prefixFrame',l='Prefix',collapsable=True,collapse=True,borderStyle='etchedIn',p=mainColumn)
       
    nameRCL = pc.rowColumnLayout('nameRCL',nc=4, cw=[(1,50),(2,85),(3,40),(4,85)], cs=[(1,5),(2,5),(3,40),(4,5)], p=prefixFrame)        
    nameTitle = pc.text('nameTitle',l='Name:',align='left')
    nameTF = pc.textField('nameTF')

    pc.text(label='Side:',al='left')    
    sidePrefix = pc.optionMenu('sidePrefix')
    pc.menuItem(label='l/r')
    pc.menuItem(label='lt/rt')
    pc.menuItem(label='left/right')
    pc.menuItem(label='none')
    
    sideTitle = pc.text('sideTitle',l='Scale :', align='left')    
    scaleFloatF = pc.floatField('scaleFloatF',pre=2)
    # TODO: see why these are being reused    
    fill1 = pc.text('fill1',l='')    
    fill2 = pc.text('fill2',l='')

    # Advance Options    
    advOptionFrame = pc.frameLayout('advOptionFrame',l='Advance Options',collapsable=False,collapse=False,borderStyle='etchedIn',p=mainColumn)    
    stretchRCL = pc.rowColumnLayout('stretchRCL',nc=3,cw=[(1,120),(2,80),(3,80)],cs=[(1,0),(2,10),(3,10)],p=advOptionFrame)    
    stretchTitle = pc.text('stretchTitle',l='Stretch',al='left',fn='boldLabelFont')
    fill1 = pc.text(l='')
    fill2 = pc.text(l='')
    
    stretchChk = pc.checkBox('stretchChk',l='Stretch',v=1,cc=pc.Callback(stretchSwitch))    
    fill3 = pc.text('fill3',l='')    
    fill4 = pc.text('fill4',l='')
    
    scaleTypeOpGrp = pc.optionMenu('scaleTypeOpGrp',l='Method :')
    pc.menuItem(l='Scale')
    pc.menuItem(l='Translate')    
    volChk = pc.checkBox('volChk',label='Volume',v=True,cc='')    
    midChk = pc.checkBox('midChk',label='Mid Lock',v=True,cc='')
    
    ikFkTitle = pc.text('ikFkTitle',l=' IK FK',al='left',fn='boldLabelFont')    
    BWTitle = pc.text('BWTitle',l='Build World',al='left',fn='boldLabelFont')    
    fill5 = pc.text('fill5',l='')    
    rotTypeOpGrp = pc.optionMenu('rotTypeOpGrp',l='Method :')
    pc.menuItem(l='constrain')
    pc.menuItem(l='utilNode')
    
    buildChk = pc.checkBox('buildChk',l='Build',v=True,cc='',en=False)
    
    mainPartTab = pc.tabLayout('mainPartTab',w=385,innerMarginWidth=5,sc=lambda *args:pc.frameLayout(advHandFrame,e=True,cl=1),p=mainColumn)

    # Spine Entry    
    spineFrame = pc.frameLayout('spineFrame', collapsable=False,collapse=False,borderStyle='etchedIn',p=mainPartTab) # TODO: populate this some where else
    
    spineForm = pc.formLayout('spineForm',p=spineFrame)    
    spineJointISG = pc.intSliderGrp('spineJointISG',w=100,l='Joints:',f=True,min=0,max=25,cw3=(85,30,50),adjustableColumn3=3)    
    rootJointTFBG = pc.textFieldButtonGrp('rootJointTFBG',l='Root:',text='',buttonLabel=' select ',ed=False, bc=pc.Callback(updateTextField,'rootJointTFBG'), cw3=(85,235,67))    
    chestJointTFBG = pc.textFieldButtonGrp('chestJointTFBG',l='Chest:',text='',buttonLabel=' select ',ed=False, bc=pc.Callback(updateTextField, 'chestJointTFBG'), cw3=(85,235,67))    
    hipsJointTFBG = pc.textFieldButtonGrp('hipsJointTFBG',l='Hip:',text='',buttonLabel=' select ',ed=False, bc=pc.Callback(updateTextField, 'hipsJointTFBG'), cw3=(85,235,67))    
    spineSep1 = pc.separator('spineSep1',height=5,style='out')    
    spineTypeOpGrp = pc.optionMenuGrp('spineTypeOpGrp',l='Type:',cw2=(85,50))
    pc.menuItem(l='Stretchy IK FK')
    pc.menuItem(l='Reverse Spine TODO:Implement') # TODO: Implement
    
    spineTypeBtn = pc.button('spineTypeBtn',l='Create Spine', c=pc.Callback(getFromUI,'spine'))
        
    spineSep2 = pc.separator('spineSep2',height=5,style='out')
        
    pc.formLayout(spineForm,e=True,attachForm=[(spineJointISG, 'top', 0),(spineJointISG, 'left', 0)],attachPosition=[(spineJointISG,'right',0,87)])
    
    pc.formLayout(spineForm,e=True,attachControl=[(rootJointTFBG,'top',0,spineJointISG)],attachForm=[(rootJointTFBG, 'left', 0)])
    
    pc.formLayout(spineForm,e=True,attachControl=[(chestJointTFBG,'top',0,rootJointTFBG)],attachForm=[(chestJointTFBG,'left',0)])

    pc.formLayout(spineForm,e=True,attachControl=[(hipsJointTFBG,'top',0,chestJointTFBG)],attachForm=[(hipsJointTFBG,'left',0)])

    pc.formLayout(spineForm,e=True,attachControl=[(spineSep1,'top',0,hipsJointTFBG)],attachForm=[(spineSep1,'left',0)],attachPosition=[(spineSep1,'right',0,100)])

    pc.formLayout(spineForm,e=True,attachControl=[(spineTypeOpGrp,'top',0,spineSep1)],attachForm=[(spineTypeOpGrp,'left',0)])

    pc.formLayout(spineForm,e=True,attachControl=[(spineTypeBtn,'top',0,spineSep1),(spineTypeBtn,'left',0,spineTypeOpGrp)],attachPosition=[(spineTypeBtn,'right',0,100)])

    pc.formLayout(spineForm,e=True,attachControl=[(spineSep2,'top',0,spineTypeBtn)],attachForm=[(spineSep2,'left',0)],attachPosition=[(spineTypeBtn,'right',0,100)])

    # Arm Entry    
    armFrame = pc.frameLayout('armFrame',collapsable=False,collapse=False,borderStyle='etchedIn',p=mainPartTab)    
    
    armForm = pc.formLayout('armForm',p=armFrame)    
    shoulderJointTFBG = pc.textFieldButtonGrp('shoulderJointTFBG',l='Shoulder:',text='',buttonLabel=' select ',ed=False,bc=pc.Callback(updateTextField,'shoulderJointTFBG'),cw3=(85,235,67))    
    wristJointTFBG = pc.textFieldButtonGrp('wristJointTFBG',l='Wrist:',text='',buttonLabel=' select ',ed=False,bc=pc.Callback(updateTextField,'wristJointTFBG'),cw3=(85,235,67))    
    armSep1 = pc.separator('armSep1',height=5, style='out')    
    armTypeOpGrp = pc.optionMenuGrp('armTypeOpGrp',l='Type:',cw2=(85,50))
    pc.menuItem(l='Basic IK/FK')
    pc.menuItem(l='Advance FK TODO:Implement') # TODO: Implement Advance FK    
    armTypeBtn = pc.button('armTypeBtn',l='Create Arm',c=pc.Callback(getFromUI,'arm'))    
    armSep2 = pc.separator('armSep2',height=5,style='out')    
    armSideRdBnGrp = pc.radioButtonGrp('armSideRdBnGrp',l='Side:',nrb=2,la2=['L','R'],cw3=(85,40,40),sl=1)    
    armSep3 = pc.separator('armSep3',height=5,style='out')

    pc.formLayout(armForm,e=True,af=[(shoulderJointTFBG,'top',0)]) 
    pc.formLayout(armForm,e=True,af=[(shoulderJointTFBG,'left',0)])

    pc.formLayout(armForm,e=True,ac=[(wristJointTFBG,'top',0,shoulderJointTFBG)]) 
    pc.formLayout(armForm,e=True,af=[(wristJointTFBG,'left',0)])

    pc.formLayout(armForm,e=True,ac=[(armSep1,'top',0,wristJointTFBG)])
    pc.formLayout(armForm,e=True,af=[(armSep1,'left',0)])
    pc.formLayout(armForm,e=True,ap=[(armSep1,'right',0,100)])

    pc.formLayout(armForm,e=True,ac=[(armTypeOpGrp,'top',0,armSep1)])
    pc.formLayout(armForm,e=True,af=[(armTypeOpGrp,'left',0)])

    pc.formLayout(armForm,e=True,ac=[(armTypeBtn,'top',0,armSep1)])
    pc.formLayout(armForm,e=True,ac=[(armTypeBtn,'left',0,armTypeOpGrp)])
    pc.formLayout(armForm,e=True,ap=[(armTypeBtn,'right',0,100)])
    
    pc.formLayout(armForm,e=True,ac=[(armSep2,'top',0,armTypeBtn)])
    pc.formLayout(armForm,e=True,af=[(armSep2,'left',0)])
    pc.formLayout(armForm,e=True,ap=[(armSep2,'right',0,100)])
    
    pc.formLayout(armForm,e=True,ac=[(armSideRdBnGrp,'top',0,armSep2)])
    pc.formLayout(armForm,e=True,af=[(armSideRdBnGrp,'left',0)])
    
    pc.formLayout(armForm,e=True,ac=[(armSep3,'top',0,armSideRdBnGrp)])
    pc.formLayout(armForm,e=True,af=[(armSep3,'left',0)])
    pc.formLayout(armForm,e=True,ap=[(armSep3,'right',0,100)])
    
    # legs/feet entry    
    legFrame = pc.frameLayout('legFrame',l='Legs/Feet',collapsable=False,collapse=False,borderStyle='etchedIn',p=mainPartTab)
        
    legForm = pc.formLayout('legForm',p=legFrame)    
    hipJointTFBG = pc.textFieldButtonGrp('hipJointTFBG',l='Hip:',text='',buttonLabel=' select ',ed=False, bc=pc.Callback(updateTextField,'hipJointTFBG'), cw3=(85,235,67))    
    ankleJointTFBG = pc.textFieldButtonGrp('ankleJointTFBG',l='Ankle:',text='',buttonLabel=' select ',ed=False, bc=pc.Callback(updateTextField,'ankleJointTFBG'), cw3=(85,235,67))    
    ballJointTFBG = pc.textFieldButtonGrp('ballJointTFBG',l='Ball:',text='',buttonLabel=' select ',ed=False, bc=pc.Callback(updateTextField,'ballJointTFBG'), cw3=(85,235,67))    
    toeJointTFBG = pc.textFieldButtonGrp('toeJointTFBG',l='Toe:',text='',buttonLabel=' select ',ed=False, bc=pc.Callback(updateTextField, 'toeJointTFBG'), cw3=(85,235,67))    
    legSep1 = pc.separator('legSep1',height=5,style='out')    
    legTypeOpGrp = pc.optionMenuGrp('legTypeOpGrp',l='Type:',cw2=(85,40), cc=pc.Callback(legUItypeSwitch))
    pc.menuItem(l='Biped:')
    pc.menuItem(l='Quadroped:')    
    legTypeBtn = pc.button('legTypeBtn',l='Create Leg',c=pc.Callback(getFromUI,'leg'))    
    legSep2 = pc.separator('legSep2',height=5,style='out')    
    legSideRdBnGrp = pc.radioButtonGrp('legSideRdBnGrp',l='Side:',nrb=2,la2=['L','R'], cw3=(85,40,40), sl=True)    
    legSep3 = pc.separator('legSep3',height=5,style='out')

    pc.formLayout(legForm,e=True,af=[(hipJointTFBG,'top',0),(hipJointTFBG,'left',0)])
    pc.formLayout(legForm,e=True,ac=[(ankleJointTFBG,'top',0,hipJointTFBG)],af=[(ankleJointTFBG,'left',0)])
    pc.formLayout(legForm,e=True,ac=[(ballJointTFBG,'top',0,ankleJointTFBG)],af=[(ankleJointTFBG,'left',0)])
    pc.formLayout(legForm,e=True,ac=[(toeJointTFBG,'top',0,ballJointTFBG)],af=[(toeJointTFBG,'left',0)])
    pc.formLayout(legForm,e=True,ac=[(legSep1,'top',0,toeJointTFBG)],af=[(legSep1,'left',0)],ap=[(legSep1,"right",0,100)])
    pc.formLayout(legForm,e=True,ac=[(legTypeOpGrp,'top',0,legSep1)],af=[(legTypeOpGrp,'left',0)])
    pc.formLayout(legForm,e=True,ac=[(legTypeBtn,'top',0,legSep1),(legTypeBtn,'left',0,legTypeOpGrp)],ap=[(legTypeBtn,"right",0,100)])
    pc.formLayout(legForm,e=True,ac=[(legSep2,'top',0,legTypeBtn)],af=[(legSep2,'left',0)],ap=[(legSep2,"right",0,100)])
    pc.formLayout(legForm,e=True,ac=[(legSideRdBnGrp,'top',0,legSep2)],af=[(legSideRdBnGrp,'left',0)])
    pc.formLayout(legForm,e=True,ac=[(legSep3,'top',0,legSideRdBnGrp)],af=[(legSep3,'left',0)],ap=[(legSep3,"right",0,100)])

    # head entry    
    headFrame = pc.frameLayout('headFrame',l='',collapsable=False,collapse=False,borderStyle='etchedIn',p=mainPartTab)    
    headForm = pc.formLayout('headForm',p=headFrame)    
    neckJointISG = pc.intSliderGrp('neckJointISG',w=100,l='Joints:',f=1,v=3,min=0,max=25,cw3=(85,30,50),adjustableColumn3=3)        
    headJointTFBG = pc.textFieldButtonGrp('headJointTFBG',l='Head:',text='',buttonLabel=' select ',ed=0, bc=pc.Callback(updateTextField, 'headJointTFBG'), cw3=(85,235,67))    
    neckJointTFBG = pc.textFieldButtonGrp('neckJointTFBG',l='Neck:',text='',buttonLabel=' select ',ed=0, bc=pc.Callback(updateTextField, 'neckJointTFBG'), cw3=(85,235,67))    
    headSep1 = pc.separator('headSep1',height=5,style='out')   
    headTypeOpGrp = pc.optionMenuGrp('headTypeOpGrp',l='Type:',cw2=(85,50))
    pc.menuItem(l='Basic Head')    
    headTypeBtn = pc.button('headTypeBtn',l='Create Head',c=pc.Callback(getFromUI,'head'))    
    eyeStartSep = pc.separator('eyeStartSep',height=5,style='out')    
    eyeSepTitle = pc.text('eyeSepTitle',l='Eyes',fn='plainLabelFont',align='center')    
    eyeEndSep = pc.separator('eyeEndSep',height=5,style='out')    
    eyeLJointTFBG = pc.textFieldButtonGrp('eyeLJointTFBG',label='L Eye:',text='',buttonLabel=' Select ',ed=False, bc=pc.Callback(updateTextField, 'eyeLJointTFBG'), cw3=(85,235,67))    
    eyeRJointTFBG = pc.textFieldButtonGrp('eyeRJointTFBG',label='R Eye:',text='',buttonLabel=' Select ',ed=False, bc=pc.Callback(updateTextField, 'eyeRJointTFBG'), cw3=(85,235,67))    
    headSep2 = pc.separator('headSep2',height=5,style='out')    
    eyeTypeOpGrp = pc.optionMenuGrp('eyeTypeOpGrp',l='Type:',cw2=(85,50))
    pc.menuItem(l='Basic Eyes')    
    eyeTypeBtn = pc.button('eyeTypeBtn',l='Create Eyes',c=pc.Callback(getFromUI,'eyes'))    
    headSep3 = pc.separator('headSep3',height=5,style='out')

    pc.formLayout(headForm,e=True,af=[(neckJointISG,'top',0),(neckJointISG,'left',0)],ap=[(neckJointISG,'right',0,87)])
    pc.formLayout(headForm,e=True,ac=[(headJointTFBG,'top',0,neckJointISG)],af=[(headJointTFBG,'left',0)])
    pc.formLayout(headForm,e=True,ac=[(neckJointTFBG,'top',0,headJointTFBG)],af=[(neckJointTFBG,'left',0)])
    pc.formLayout(headForm,e=True,ac=[(headSep1,'top',0,neckJointTFBG)],af=[(headSep1,'left',0)],ap=[(headSep1,'right',0,100)])
    pc.formLayout(headForm,e=True,ac=[(headTypeOpGrp,'top',0,headSep1)],af=[(headTypeOpGrp,'left',0)])
    pc.formLayout(headForm,e=True,ac=[(headTypeBtn,'top',0,headSep1),(headTypeBtn,'left',0,headTypeOpGrp)],ap=[(headTypeBtn,'right',0,100)])
    pc.formLayout(headForm,e=True,ac=[(eyeStartSep,'top',5,headTypeBtn)],af=[(eyeStartSep,'left',0)],ap=[(eyeStartSep,'right',0,45)])
    pc.formLayout(headForm,e=True,ac=[(eyeSepTitle,'top',0,headTypeBtn),(eyeSepTitle,'left',0,eyeStartSep)],ap=[(eyeSepTitle,'right',0,55)])
    pc.formLayout(headForm,e=True,ac=[(eyeEndSep,'top',5,headTypeBtn),(eyeEndSep,'left',0,eyeSepTitle)],ap=[(eyeEndSep,'right',0,100)])
    pc.formLayout(headForm,e=True,ac=[(eyeLJointTFBG,'top',0,eyeSepTitle)],af=[(eyeLJointTFBG,'left',0)])
    pc.formLayout(headForm,e=True,ac=[(eyeRJointTFBG,'top',0,eyeLJointTFBG)],af=[(eyeRJointTFBG,'left',0)])
    pc.formLayout(headForm,e=True,ac=[(headSep2,'top',0,eyeRJointTFBG)],af=[(headSep2,'left',0)],ap=[(headSep2,'right',0,100)])
    pc.formLayout(headForm,e=True,ac=[(eyeTypeOpGrp,'top',0,headSep2)],af=[(eyeTypeOpGrp,'left',0)])
    pc.formLayout(headForm,e=True,ac=[(eyeTypeBtn,'top',0,headSep2),(eyeTypeBtn,'left',0,eyeTypeOpGrp)],ap=[(eyeTypeBtn,'right',0,100)])
    pc.formLayout(headForm,e=True,ac=[(headSep3,'top',0,eyeTypeBtn)],af=[(headSep3,'left',0)],ap=[(headSep3,'right',0,100)])

    # Hand Entry    
    handFrame = pc.frameLayout('handFrame',l='',collapsable=False,collapse=False,borderStyle='etchedIn',p=mainPartTab)    
    handMainColumn = pc.columnLayout('handMainColumn',adj=True,p=handFrame)    
    handCompForm = pc.formLayout('handCompForm',p=handMainColumn)
        
    controlHandTFBG = pc.textFieldButtonGrp('controlHandTFBG',label='Control:',text='',buttonLabel=' Select ',ed=False, bc=pc.Callback(updateTextField,'controlHandTFBG'), cw3=(85,235,67))    
    fkConChk = pc.checkBoxGrp('fkConChk',l='FK Control:',v1=1,cw2=(85,50), cc=pc.Callback(tentOffsetSwitch))    
    fkConHandTF = pc.textField('fkConHandTF',e=False,tx='Square')    
    controlHandSep1 = pc.separator('controlHandSep1',height=5,style='out')
    
    finger1Chk = pc.checkBox('finger1Chk',l='',v=1, cc=pc.Callback(fingerUISwitch, 'finger1'))    
    finger1Title = pc.text('finger1Title',l='Thumb:',align='right')    
    finger1NameTF = pc.textField('finger1NameTF',tx='Thumb')    
    finger1JointTFBG = pc.textFieldButtonGrp('finger1JointTFBG',tx='',buttonLabel=' Select ',ed=False,cw2=(154,67), bc=pc.Callback(updateTextField, 'finger1JointTFBG'))
    
    finger2Chk = pc.checkBox('finger2Chk',l='',v=1,cc=pc.Callback(fingerUISwitch,'finger2'))    
    finger2Title = pc.text('finger2Title',l='Index:',align='right')    
    finger2NameTF = pc.textField('finger2NameTF',tx='Index')    
    finger2JointTFBG = pc.textFieldButtonGrp('finger2JointTFBG',tx='',buttonLabel=' Select ',ed=False,cw2=(154,67), bc=pc.Callback(updateTextField, 'finger2JointTFBG'))
    
    finger3Chk = pc.checkBox('finger3Chk',l='',v=1,cc=pc.Callback(fingerUISwitch,'finger3'))    
    finger3Title = pc.text('finger3Title',l='Middle:',align='right')    
    finger3NameTF = pc.textField('finger3NameTF',tx='Middle')    
    finger3JointTFBG = pc.textFieldButtonGrp('finger3JointTFBG',tx='',buttonLabel=' Select ',ed=False,cw2=(154,67), bc=pc.Callback(updateTextField, 'finger3JointTFBG'))
    
    finger4Chk = pc.checkBox('finger4Chk',l='',v=1, cc=pc.Callback(fingerUISwitch, 'finger4'))    
    finger4Title = pc.text('finger4Title',l='Ring:',align='right')    
    finger4NameTF = pc.textField('finger4NameTF',tx='Ring')    
    finger4JointTFBG = pc.textFieldButtonGrp('finger4JointTFBG',tx='',buttonLabel=' Select ',ed=False,cw2=(154,67), bc=pc.Callback(updateTextField, 'finger4JointTFBG'))
    
    finger5Chk = pc.checkBox('finger5Chk',l='',v=1, cc=pc.Callback(fingerUISwitch, 'finger5'))    
    finger5Title = pc.text('finger5Title',l='Pinky:',align='right')    
    finger5NameTF = pc.textField('finger5NameTF',tx='Pinky')    
    finger5JointTFBG = pc.textFieldButtonGrp('finger5JointTFBG',tx='',buttonLabel=' Select ',ed=False,cw2=(154,67), bc=pc.Callback(updateTextField,'finger5JointTFBG'))
    
    controlHandSep2 = pc.separator('controlHandSep2',height=5,style='out')    
    createHandBtn = pc.button('createHandBtn',l='Create Hand', c=pc.Callback(getFromUI,'hand'))    
    controlHandSep3 = pc.separator('controlHandSep3',height=5,style='out')

    wireTypes = {'arrow','circleCross','pin1','circleOrient','cross','square','cube1','cube2','circle','sphere','plus','triangle','cone','thinCross','pin2'}

    pc.popupMenu(p=fkConHandTF)
    for m in wireTypes:
        pc.menuItem(l=m,c=pc.Callback(pc.textField, fkConHandTF,e=True,tx=m))

    pc.formLayout(handCompForm,e=True,af=[(controlHandTFBG,'top',0),(controlHandTFBG,'left',0)])
    pc.formLayout(handCompForm,e=True,ac=[(fkConChk,'top',3,controlHandTFBG)],af=[(fkConChk,'left',0)],ap=[(fkConChk,'right',0,25)])
    pc.formLayout(handCompForm,e=True,ac=[(fkConHandTF,'top',0,controlHandTFBG),(fkConHandTF,'left',0,fkConChk)],ap=[(fkConHandTF,'right',0,86)])
    pc.formLayout(handCompForm,e=True,ac=[(controlHandSep1,'top',0,fkConHandTF)],af=[(controlHandSep1,'left',0)],ap=[(controlHandSep1,'right',0,100)])

    pc.formLayout(handCompForm,e=True,ac=[(finger1Chk,'top',7,controlHandSep1)],af=[(finger1Chk,'left',0)],ap=[(finger1Chk,'right',0,5)])
    pc.formLayout(handCompForm,e=True,ac=[(finger1Title,'top',7,controlHandSep1),(finger1Title,'left',0,finger1Chk)],ap=[(finger1Title,'right',0,23)])
    pc.formLayout(handCompForm,e=True,ac=[(finger1NameTF,'top',3,controlHandSep1),(finger1NameTF,'left',0,finger1Title)],ap=[(finger1NameTF,'right',0,45)])
    pc.formLayout(handCompForm,e=True,ac=[(finger1JointTFBG,'top',0,controlHandSep1),(finger1JointTFBG,'left',0,finger1NameTF)],ap=[(finger1JointTFBG,'right',0,100)])

    pc.formLayout(handCompForm,e=True,ac=[(finger2Chk,'top',7,finger1JointTFBG)],af=[(finger2Chk,'left',0)],ap=[(finger2Chk,'right',0,5)])
    pc.formLayout(handCompForm,e=True,ac=[(finger2Title,'top',7,finger1JointTFBG),(finger2Title,'left',0,finger2Chk)],ap=[(finger2Title,'right',0,23)])
    pc.formLayout(handCompForm,e=True,ac=[(finger2NameTF,'top',3,finger1JointTFBG),(finger2NameTF,'left',0,finger2Title)],ap=[(finger2NameTF,'right',0,45)])
    pc.formLayout(handCompForm,e=True,ac=[(finger2JointTFBG,'top',0,finger1JointTFBG),(finger2JointTFBG,'left',0,finger2NameTF)],ap=[(finger2JointTFBG,'right',0,100)])

    pc.formLayout(handCompForm,e=True,ac=[(finger3Chk,'top',7,finger2JointTFBG)],af=[(finger3Chk,'left',0)],ap=[(finger3Chk,'right',0,5)])
    pc.formLayout(handCompForm,e=True,ac=[(finger3Title,'top',7,finger2JointTFBG),(finger3Title,'left',0,finger3Chk)],ap=[(finger3Title,'right',0,23)])
    pc.formLayout(handCompForm,e=True,ac=[(finger3NameTF,'top',3,finger2JointTFBG),(finger3NameTF,'left',0,finger3Title)],ap=[(finger3NameTF,'right',0,45)])
    pc.formLayout(handCompForm,e=True,ac=[(finger3JointTFBG,'top',0,finger2JointTFBG),(finger3JointTFBG,'left',0,finger3NameTF)],ap=[(finger3JointTFBG,'right',0,100)])

    pc.formLayout(handCompForm,e=True,ac=[(finger4Chk,'top',7,finger3JointTFBG)],af=[(finger4Chk,'left',0)],ap=[(finger4Chk,'right',0,5)])
    pc.formLayout(handCompForm,e=True,ac=[(finger4Title,'top',7,finger3JointTFBG),(finger4Title,'left',0,finger4Chk)],ap=[(finger4Title,'right',0,23)])
    pc.formLayout(handCompForm,e=True,ac=[(finger4NameTF,'top',3,finger3JointTFBG),(finger4NameTF,'left',0,finger4Title)],ap=[(finger4NameTF,'right',0,45)])
    pc.formLayout(handCompForm,e=True,ac=[(finger4JointTFBG,'top',0,finger3JointTFBG),(finger4JointTFBG,'left',0,finger4NameTF)],ap=[(finger4JointTFBG,'right',0,100)])

    pc.formLayout(handCompForm,e=True,ac=[(finger5Chk,'top',7,finger4JointTFBG)],af=[(finger5Chk,'left',0)],ap=[(finger5Chk,'right',0,5)])
    pc.formLayout(handCompForm,e=True,ac=[(finger5Title,'top',7,finger4JointTFBG),(finger5Title,'left',0,finger5Chk)],ap=[(finger5Title,'right',0,23)])
    pc.formLayout(handCompForm,e=True,ac=[(finger5NameTF,'top',3,finger4JointTFBG),(finger5NameTF,'left',0,finger5Title)],ap=[(finger5NameTF,'right',0,45)])
    pc.formLayout(handCompForm,e=True,ac=[(finger5JointTFBG,'top',0,finger4JointTFBG),(finger5JointTFBG,'left',0,finger5NameTF)],ap=[(finger5JointTFBG,'right',0,100)])

    pc.formLayout(handCompForm,e=True,ac=[(controlHandSep2,'top',0,finger5JointTFBG)],af=[(controlHandSep2,'left',0)],ap=[(controlHandSep2,'right',0,100)])
    pc.formLayout(handCompForm,e=True,ac=[(createHandBtn,'top',0,controlHandSep2)],af=[(createHandBtn,'left',0)],ap=[(createHandBtn,'right',0,100)])
    pc.formLayout(handCompForm,e=True,ac=[(controlHandSep3,'top',0,createHandBtn)],af=[(controlHandSep3,'left',0)],ap=[(controlHandSep3,'right',0,100)])

    # Advance Hand Options    
    advHandFrame = pc.frameLayout('advHandFrame',l='Advance Options',collapsable=True,collapse=True,borderStyle='etchedIn',p=handMainColumn)
    
    advHandRCL = pc.rowColumnLayout('advHandRCL',nc=True,p=advHandFrame)    
    manualOpChk = pc.checkBoxGrp('manualOpChk',l='Manual:',v1=0,cw2=(85,50), cc=pc.Callback(fingerManualSwitch))    
    curlFacingRdBnGrp = pc.radioButtonGrp('curlFacingRdBnGrp',l='Curl:',nrb=3,la3=('X','Y','Z'), cw4=(85,70,70,70),sl=3)    
    spreadFacingRdBnGrp = pc.radioButtonGrp('spreadFacingRdBnGrp',l='Spread:',nrb=3,la3=('X','Y','Z'), cw4=(85,70,70,70),sl=2)    
    spinFacingRdBnGrp = pc.radioButtonGrp('spinFacingRdBnGrp',l='Spin:',nrb=3,la3=('X','Y','Z'), cw4=(85,70,70,70),sl=1)    
    stretchFacingRdBnGrp = pc.radioButtonGrp('stretchFacingRdBnGrp',l='Stretch:',nrb=3,la3=('X','Y','Z'), cw4=(85,70,70,70),sl=1)    
    nameSep1 = pc.separator('nameSep1',height=5,style='out')    
    namingRdBnGrp = pc.radioButtonGrp('namingRdBnGrp',l='Naming:',nrb=3,la3=('1,2,3..','A.B.C..','Base,Mid,Tip'), cw4=(85,70,70,70),sl=2)    
    nameSep3 = pc.separator('nameSep3',height=5,style='out')    
    skipOpChk = pc.checkBoxGrp('skipOpChk',l='Skip Last:',v1=1,cw2=(85,50))    
    nameSep5 = pc.separator('nameSep5',height=5,style='out')    
    fingerSideRdBnGrp = pc.radioButtonGrp('fingerSideRdBnGrp',l='Side:',nrb=2,la2=('L','R'),cw3=(85,40,40),sl=1)

    # Tentacles    
    tenticleFrame = pc.frameLayout('tenticleFrame',l='',collapsable=False,collapse=False,borderStyle='etchedIn',p=mainPartTab)
    
    tentCompForm = pc.formLayout('tentCompForm',p=tenticleFrame)    
    tenticleJointISG = pc.intSliderGrp('tenticleJointISG',l='Joints:',f=1,v=7,min=0,max=25,cw3=(85,30,50),adjustableColumn3=3)    
    tenticleNameTFG = pc.textFieldGrp('tenticleNameTFG',l='Name:',text='',cw2=(85,235))    
    startTentJointTFBG = pc.textFieldButtonGrp('startTentJointTFBG',l='Start:',text='',buttonLabel=' Select ',ed=0,cw3=(85,235,67), bc=pc.Callback(updateTextField, 'startTentJointTFBG'))
    endTentJointTFBG = pc.textFieldButtonGrp('endTentJointTFBG',l='End:',text='',buttonLabel=' Select ',ed=0,cw3=(85,235,67), bc=pc.Callback(updateTextField, 'endTentJointTFBG'))
    conTentTFG = pc.textFieldGrp('conTentTFG',l='Control:',tx='Square',ed=0,cw2=(85,235))    
    dynamicChk = pc.checkBoxGrp('dynamicChk',l='Dynamic:',v1=1,cw2=(85,50))    
    tentFill3 = pc.text('tentFill3',l='Offset Control',fn='boldLabelFont',align='left')    
    offsetChk = pc.checkBoxGrp('offsetChk',l='Offset:',v1=1,cw2=(85,50), cc=pc.Callback(tentOffsetSwitch))    
    conOffTentTF = pc.textField('conOffTentTF',e=0,tx='plus')    
    tentSep1 = pc.separator('tentSep1',height=5,style='out')    
    createTentBtn = pc.button('createTentBtn',l='Create Tentacle',c=pc.Callback(getFromUI,'tentacle'))    
    tentSep2 = pc.separator('tentSep2',height=5,style='out')

    pc.popupMenu(p=conTentTFG)
    for m in wireTypes:
        pc.menuItem(l=m,c=pc.Callback(pc.textFieldGrp, conTentTFG,e=True,tx=m))

    pc.popupMenu(p=conOffTentTF)
    for m in wireTypes:
        pc.menuItem(l=m,c=pc.Callback(pc.textField,conOffTentTF,e=True,tx=m))

    pc.formLayout(tentCompForm,e=True,af=[(tenticleJointISG,'top',0),(tenticleJointISG,'left',0)],ap=[(tenticleJointISG,'right',0,87)])
    pc.formLayout(tentCompForm,e=True,ac=[(tenticleNameTFG,'top',0,tenticleJointISG)],af=[(tenticleNameTFG,'left',0)])
    pc.formLayout(tentCompForm,e=True,ac=[(startTentJointTFBG,'top',0,tenticleNameTFG)],af=[(startTentJointTFBG,'left',0)])
    pc.formLayout(tentCompForm,e=True,ac=[(endTentJointTFBG,'top',0,startTentJointTFBG)],af=[(endTentJointTFBG,'left',0)])
    pc.formLayout(tentCompForm,e=True,ac=[(conTentTFG,'top',0,endTentJointTFBG)],af=[(conTentTFG,'left',0)])
    pc.formLayout(tentCompForm,e=True,ac=[(dynamicChk,'top',0,conTentTFG)],af=[(dynamicChk,'left',0)],ap=[(dynamicChk,'right',0,45)])
    pc.formLayout(tentCompForm,e=True,ac=[(tentFill3,'top',0,conTentTFG),(tentFill3,'left',0,dynamicChk)],ap=[(tentFill3,'right',0,100)])
    pc.formLayout(tentCompForm,e=True,ac=[(offsetChk,'top',3,dynamicChk)],af=[(offsetChk,'left',0)],ap=[(offsetChk,'right',0,25)])
    pc.formLayout(tentCompForm,e=True,ac=[(conOffTentTF,'top',0,dynamicChk),(conOffTentTF,'left',0,offsetChk)],ap=[(conOffTentTF,'right',0,86)])
    pc.formLayout(tentCompForm,e=True,ac=[(tentSep1,'top',0,conOffTentTF)],af=[(tentSep1,'left',0)],ap=[(tentSep1,'right',0,100)])
    pc.formLayout(tentCompForm,e=True,ac=[(createTentBtn,'top',0,tentSep1)],af=[(createTentBtn,'left',0)],ap=[(createTentBtn,'right',0,100)])
    pc.formLayout(tentCompForm,e=True,ac=[(tentSep2,'top',0,createTentBtn)],af=[(tentSep2,'left',0)],ap=[(tentSep2,'right',0,100)])
    
    parentFrame = pc.frameLayout('parentFrame',l='',collapsable=False,collapse=False,borderStyle='etchedIn',p=mainPartTab)
    
    parentForm = pc.formLayout('parentForm',p=parentFrame)    
    parentConTFBG = pc.textFieldButtonGrp('parentConTFBG',l='Control:', text='',buttonLabel=' Select ',ed=False, cw3=(85,235,67), bc=pc.Callback((updateTextField,'parentConTFBG'),(spaceNodeParentUpdate)))    
    parentGrpTFBG = pc.textFieldButtonGrp('parentGrpTFBG',l='Grp:',buttonLabel=' Select ',ed=False,cw3=(85,235,67), bc=pc.Callback(updateTextField,'parentGrpTFBG'))
    parentSep1 = pc.separator('parentSep1',height=5,style='out')    
    parentTypeRdBnGrp = pc.radioButtonGrp('parentTypeRdBnGrp',l='Type:',nrb=3,la3=('Parent','Rotate','Trans/Rotate'),cw4=(85,70,70,70),sl=1)    
    parentSep2 = pc.separator('parentSep2',height=5,style='out')    
    parentSpaceTitle = pc.text('parentSpaceTitle',l='Space:',fn='boldLabelFont',align='left')    
    spaceNameTitle = pc.text('spaceNameTitle',l='Name:',fn='boldLabelFont',align='left')    
    spaceSwitchParentTSL = pc.textScrollList('spaceSwitchParentTSL',h=70,allowMultiSelection=False, sc=pc.Callback(selectSpaceSwitchName))    
    spaceSwitchNameTSL = pc.textScrollList('spaceSwitchNameTSL',h=70,allowMultiSelection=False,en=0)    
    addSpaceBtn = pc.button('addSpaceBtn',l='Add',c=pc.Callback(addParentSpace))    
    removeSpaceBtn = pc.button('removeSpaceBtn',l='Delete',c=pc.Callback(deleteParentSpace))    
    removeAllSpaceBtn = pc.button('removeAllSpaceBtn',l='Clean',c=pc.Callback(deleteAllParentSpace))    
    newSpaceNameTF = pc.textField('newSpaceNameTF',ec=pc.Callback(changeSpaceName))    
    changeNameBtn = pc.button('changeNameBtn',l='Rename',c=pc.Callback(changeSpaceName))    
    parentSep3 = pc.separator('parentSep3',height=5,style='out')    
    createParentBtn = pc.button('createParentBtn',l='Create Space Switch',c=pc.Callback(getFromUI,'parentSwitch'))    
    parentSep4 = pc.separator('parentSep4',height=5,style='out')

    pc.formLayout(parentForm,e=True,af=[(parentConTFBG,'top',0),(parentConTFBG,'left',0)])
    pc.formLayout(parentForm,e=True,ac=[(parentGrpTFBG,'top',0,parentConTFBG)], af=[(parentGrpTFBG,'left',0)])
    pc.formLayout(parentForm,e=True,ac=[(parentSep1,'top',2,parentGrpTFBG)],af=[(parentSep1,'left',0)],ap=[(parentSep1,'right',0,100)])
    pc.formLayout(parentForm,e=True,ac=[(parentTypeRdBnGrp,'top',0,parentSep1)],af=[(parentTypeRdBnGrp,'left',0)],ap=[(parentTypeRdBnGrp,'right',0,100)])
    pc.formLayout(parentForm,e=True,ac=[(parentSep2,'top',0,parentTypeRdBnGrp)],af=[(parentSep2,'left',0)],ap=[(parentSep2,'right',0,100)])
    pc.formLayout(parentForm,e=True,ac=[(parentSpaceTitle,'top',2,parentSep2)],af=[(parentSpaceTitle,'left',0)],ap=[(parentSpaceTitle,'right',0,50)])
    pc.formLayout(parentForm,e=True,ac=[(spaceNameTitle,'top',2,parentSep2),(spaceNameTitle,'left',5,parentSpaceTitle)],ap=[(spaceNameTitle,'right',0,100)])
    pc.formLayout(parentForm,e=True,ac=[(spaceSwitchParentTSL,'top',2,parentSpaceTitle)],af=[(spaceSwitchParentTSL,'left',0)],ap=[(spaceSwitchNameTSL,'right',0,50)])
    pc.formLayout(parentForm,e=True,ac=[(spaceSwitchNameTSL,'top',2,spaceNameTitle),(spaceSwitchNameTSL,'left',5,spaceSwitchParentTSL)],ap=[(spaceSwitchNameTSL,'right',0,100)])
    pc.formLayout(parentForm,e=True,ac=[(addSpaceBtn,'top',2,spaceSwitchParentTSL)],af=[(addSpaceBtn,'left',0)],ap=[(addSpaceBtn,'right',0,15)])
    pc.formLayout(parentForm,e=True,ac=[(removeSpaceBtn,'top',2,spaceSwitchParentTSL),(removeSpaceBtn,'left',0,addSpaceBtn)],ap=[(removeSpaceBtn,'right',0,30)])
    pc.formLayout(parentForm,e=True,ac=[(removeAllSpaceBtn,'top',2,spaceSwitchParentTSL),(removeAllSpaceBtn,'left',0,removeSpaceBtn)],ap=[(removeAllSpaceBtn,'right',0,50)])
    pc.formLayout(parentForm,e=True,ac=[(newSpaceNameTF,'top',2,spaceSwitchNameTSL),(newSpaceNameTF,'left',5,removeAllSpaceBtn)],ap=[(newSpaceNameTF,'right',0,80)])
    pc.formLayout(parentForm,e=True,ac=[(changeNameBtn,'top',2,spaceSwitchParentTSL),(changeNameBtn,'left',0,newSpaceNameTF)],ap=[(changeNameBtn,'right',0,100)])
    pc.formLayout(parentForm,e=True,ac=[(parentSep3,'top',0,changeNameBtn)],af=[(parentSep3,'left',0)],ap=[(parentSep3,'right',0,100)])
    pc.formLayout(parentForm,e=True,ac=[(createParentBtn,'top',0,parentSep3)],af=[(createParentBtn,'left',0)],ap=[(createParentBtn,'right',0,100)])
    pc.formLayout(parentForm,e=True,ac=[(parentSep4,'top',0,createParentBtn)],af=[(parentSep4,'left',0)],ap=[(parentSep4,'right',0,100)])

    # UI Edits
    pc.checkBoxGrp(manualOpChk,e=True,v1=0)
    pc.optionMenu(sidePrefix,e=True,v='lt/rt')
    
    fingerManualSwitch()
    legUItypeSwitch()
    stretchSwitch()

    autoRigWindow.show()