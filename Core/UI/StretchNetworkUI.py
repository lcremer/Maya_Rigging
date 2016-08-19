import pymel.core as pc

# from Maya_Rigging import *

def stretchNetworkUI():
    if pc.window('ikStretchWin',exists=True):
        pc.deleteUI('ikStretchWin')

    ikStretchWin = pc.window('ikStretchWin',t='autoRig: Ik Stretch',mxb=False,mnb=False,resizeToFitChildren=True,sizeable=False)

    ikStretchMainForm = pc.formLayout('ikStretchMainForm')
    stretchNameTFG = pc.textFieldGrp('stretchNameTFG',l='Name:',tx='',cw2=[60,70])
    stretchSideOMG = pc.textFieldGrp('stretchSideOMG',l='Side:',tx='',cw2=[30,70])
    stretchEndSep = pc.separator('stretchEndSep',height=5,style='out')
    stretchTypeOpGrp = pc.optionMenuGrp('stretchTypeOpGrp',l='Method:',cw2=[60,50])
    pc.menuItem(l='scale')
    pc.menuItem(l='translate')

    stretchStartJointTFBG = 'stretchStartJointTFBG'; 
    stretchStartJointTFBG = pc.textFieldButtonGrp('stretchStartJointTFBG', label='Start Joint:', text='', buttonLabel=' select ', bc=pc.Callback(updateTextField,'stretchStartJointTFBG'), cw3=(60,128,50))
    stretchEndJointTFBG = 'stretchEndJointTFBG';
    stretchEndJointTFBG = pc.textFieldButtonGrp('stretchEndJointTFBG', label='End Joint:', text='', buttonLabel=' select ', bc=pc.Callback(updateTextField,'stretchEndJointTFBG'), cw3=(60,128,50))
    stretchControlTFBG = 'stretchControlTFBG'
    stretchControlTFBG = pc.textFieldButtonGrp('stretchControlTFBG', label='Control:', text='', buttonLabel=' select ', bc=pc.Callback(updateTextField, 'stretchControlTFBG'), cw3=(60,128,50))
    stretchMidLockCBG = 'stretchMidLockCBG'
    stretchMidLockCBG = pc.checkBoxGrp('stretchMidLockCBG', l='Mid Lock:', v1=0, cw2=(60,20), cc=pc.Callback(snMidSwitch))
    stretchPvControlTFBG = 'stretchPvControlTFBG'
    stretchPvControlTFBG = pc.textFieldButtonGrp('stretchPvControlTFBG', label='PV Control:', text='', buttonLabel=' select ', bc=pc.Callback(updateTextField,'stretchPvControlTFBG'), cw3=(60,128,50))
    stretchApplySep1 = pc.separator('stretchApplySep1', height=5, style='out')
    stretchApplyBtn = pc.button('stretchApplyBtn', l='Create', c=pc.Callback(stretchNetworkPreCMD))
    stretchApplySep2 = pc.separator('stretchApplySep2', height=5, style='out')

    pc.formLayout(ikStretchMainForm,e=True,af=[(stretchNameTFG,'top',0),(stretchNameTFG,'left',0)])
    pc.formLayout(ikStretchMainForm,e=True,af=[(stretchSideOMG,'top',0)],ac=[(stretchSideOMG,'left',0,stretchNameTFG)])
    pc.formLayout(ikStretchMainForm,e=True,ac=[(stretchEndSep,'top',0,stretchSideOMG)],af=[(stretchEndSep,'left',0)],ap=[(stretchEndSep,'right',0,100)])
    pc.formLayout(ikStretchMainForm,e=True,ac=[(stretchTypeOpGrp,'top',0,stretchEndSep)],af=[(stretchTypeOpGrp,'left',0)])
    pc.formLayout(ikStretchMainForm,e=True,ac=[(stretchStartJointTFBG,'top',0,stretchTypeOpGrp)],af=[(stretchStartJointTFBG,'left',0)])
    pc.formLayout(ikStretchMainForm,e=True,ac=[(stretchEndJointTFBG,'top',0,stretchStartJointTFBG)],af=[(stretchEndJointTFBG,'left',0)])
    pc.formLayout(ikStretchMainForm,e=True,ac=[(stretchControlTFBG,'top',0,stretchEndJointTFBG)],af=[(stretchControlTFBG,'left',0)])
    pc.formLayout(ikStretchMainForm,e=True,ac=[(stretchMidLockCBG,'top',0,stretchControlTFBG)],af=[(stretchMidLockCBG,'left',0)])
    pc.formLayout(ikStretchMainForm,e=True,ac=[(stretchPvControlTFBG,'top',0,stretchMidLockCBG)],af=[(stretchPvControlTFBG,'left',0)])
    pc.formLayout(ikStretchMainForm,e=True,ac=[(stretchApplySep1,'top',0,stretchPvControlTFBG)],af=[(stretchApplySep1,'left',0)],ap=[(stretchApplySep1,'right',0,100)])
    pc.formLayout(ikStretchMainForm,e=True,ac=[(stretchApplyBtn,'top',0,stretchApplySep1)],af=[(stretchApplyBtn,'left',0)],ap=[(stretchApplyBtn,'right',0,100)])
    pc.formLayout(ikStretchMainForm,e=True,ac=[(stretchApplySep2,'top',0,stretchApplyBtn)],af=[(stretchApplySep2,'left',0)],ap=[(stretchApplySep2,'right',0,100)])

    pc.checkBoxGrp(stretchMidLockCBG,e=True,v1=True)
    pc.showWindow(ikStretchWin)

def snMidSwitch():
    switch = pc.checkBoxGrp(stretchMidLockCBG,q=True,v1=True)
    if switch:
        pc.textFieldButtonGrp(stretchPvControlTFBG,e=True,en=1)
    else:
        pc.textFieldButtonGrp(stretchPvControlTFBG,e=True,en=0)

def stretchNetworkPreCMD():
    name = pc.textFieldGrp('stretchNameTFG',q=True,tx=True)
    side = pc.textFieldGrp('stretchSideOMG',q=True,tx=True)
    type = pc.optionMenuGrp('stretchTypeOpGrp',q=True,v=True)
    startJoint = pc.textFieldButtonGrp('stretchStartJointTFBG',q=True,tx=True)
    endJoint = pc.textFieldButtonGrp('stretchEndJointTFBG',q=True,tx=True)
    controller = pc.textFieldButtonGrp('stretchControlTFBG',q=True,tx=True)
    midLock = pc.checkBoxGrp('stretchMidLockCBG',q=True,v1=True)
    midController = pc.textFieldButtonGrp('stretchPvControlTFBG',q=True,tx=True)
    stretchNetwork(name,side,startJoint,endJoint,controller,type,midLock,midController)