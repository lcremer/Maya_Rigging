import pymel.core as pc

#from BuildSpineSetup import *
#from BuildArmSetup import *
#from BuildBipedLegSetup import *
#from BuildNeckHeadSetup import *
#from BuildEyeSetup import *
#from BuildTentacleSetup import *
#from BuildHandSetup import *
#from BuildSpaceSwitchSetup import *

from ..Setup import *

def getFromUI(call):    
    name = pc.textField('nameTF',q=True,tx=True)
    ikFkType = pc.optionMenu('rotTypeOpGrp',q=True,v=True)
    stretchType = pc.optionMenu('scaleTypeOpGrp',q=True,v=True)
    stretch = pc.checkBox('stretchChk',q=True,v=True)
    midLock = pc.checkBox('midChk',q=True,v=True)
    volume = pc.checkBox('volChk',q=True,v=True)
    world = pc.checkBox('buildChk',q=True,v=True)
    mirror = pc.menuItem('autoMirrorOptionMi',q=True,checkBox=True)
    scale = pc.floatField('scaleFloatF',q=True,v=True)
    pc.select(cl=True)
    pc.symmetricModelling(e=True,symmetry=False)
    pc.softSelect(e=True,softSelectEnabled=False)    
    pc.setToolTo('nurbsSelect')

    if call == 'spine':
        side = ''
        rootJoint = pc.textFieldButtonGrp('rootJointTFBG',q=True,tx=True)
        chestJoint = pc.textFieldButtonGrp('chestJointTFBG',q=True,tx=True)
        hipJoint = pc.textFieldButtonGrp('hipsJointTFBG',q=True,tx=True)
        numJoints = pc.intSliderGrp('spineJointISG',q=True,v=True)
        
        if len(rootJoint) == len(chestJoint) and len(rootJoint) == len(hipJoint):
            pc.error('You must select a unique joint for each options')
        else:
            print('Implement buildSpineSetup')
            buildSpineSetup(name, side, rootJoint, chestJoint, hipJoint, stretchType, numJoints, stretch, volume, world, scale)

    if call == 'arm':
        side = pc.optionMenu('sidePrefix',q=True,v=True)
        shoulderJoint = pc.textFieldButtonGrp('shoulderJointTFBG',q=True,tx=True)
        wristJoint = pc.textFieldButtonGrp('wristJointTFBG',q=True,tx=True)
        sideQ = rigSideSep(side)
        armSide = pc.radioButtonGrp('armSideRdBnGrp',q=True,sl=True)

        if side != 'none':
            if armSide == 1:
                side = sideQ[0]
            else:
                side = sideQ[1]
        else:
            side = ''
        if name != '':
            name = (name + '_')

        if len(shoulderJoint) == len(wristJoint):
            pc.error('You must select a unique joint for each options')
        else:
            print('Implement buildArmSetup')
            buildArmSetup(name, side, shoulderJoint, wristJoint, stretchType, ikFkType, stretch, midLock, volume, world, scale)

    if call == 'leg':
        side = pc.optionMenu('sidePrefix',q=True,v=True)
        hipJoint = pc.textFieldButtonGrp('hipJointTFBG',q=True,tx=True)
        ankleJoint = pc.textFieldButtonGrp('ankleJointTFBG',q=True,tx=True)
        ballJoint = pc.textFieldButtonGrp('ballJointTFBG',q=True,tx=True)
        sideQ = rigSideSep(side)
        armSide = pc.radioButtonGrp('legSideRdBnGrp',q=True,sl=True)

        if side != 'none':
            if armSide == 1:
                side = sideQ[0]
            else:
                side = sideQ[1]
        else:
            side = ''
            
        if name != '':
            name = name + '_'

        if len(hipJoint) == len(ankleJoint) or len(ankleJoint) == len(ballJoint) or len(hipJoint) == len(ballJoint):
            pc.error('You must select a unique joint for each options')
        else:
            print('Implement buildBipedLegSetup')
            buildBipedLegSetup(name, side, hipJoint, ankleJoint, ballJoint, stretchType, ikFkType, stretch, midLock, volume, world, scale)

        if mirror:
            if prefixSepCheck(hipJoint)==1:
                print('Implement buildBipedLegSetup')
                rHipJoint = strSearchReplace(hipJoint, sideQ[0], sideQ[1])
                rAnkleJoint = strSearchReplace(ankleJoint, sideQ[0], sideQ[1])
                rBallJoint = strSearchReplace(ballJoint, sideQ[0], sideQ[1])
                buildBipedLegSetup(name, sideQ[1], rHipJoint, rAnkleJoint, rBallJoint, stretchType, ikFkType, stretch, midLock, volume, world, scale)

    if call == 'head':
        side = ''
        neckJoint = pc.textFieldButtonGrp('neckJointTFBG',q=True,tx=True)
        headJoint = pc.textFieldButtonGrp('headJointTFBG',q=True,tx=True)
        numJoint = pc.intSliderGrp('neckJointISG',q=True,v=True)

        if len(headJoint) == len(neckJoint):
            pc.error('You must select a unique joint for each options')
        else:
            print('Implement buildNeckHeadSetup')
            buildNeckHeadSetup(name,side,neckJoint,headJoint,stretchType,stretch,numJoints,volume,world,scale)

    if call == 'eyes':
        side = ''
        leftEye = pc.textFieldButtonGrp('eyeLJointTFBG',q=True,tx=True)
        rightEye = pc.textFieldButtonGrp('eyeRJointTFBG',q=True,tx=True)
        parent = getParent(leftEye)

        if len(leftEye) == len(rightEye):
            pc.error('You must select a unique joint for each options')
        elif parent == '':
            pc.error('Parent for eyes joint required for complete setup')
        else:
            print('Implement BuildEyeSetup')
            buildEyeSetup(name, side, leftEye, rightEye, world, scale)

    if call == 'tentacle':
        side = ''
        tentStartJoint = pc.textFieldButtonGrp('startTentJointTFBG',q=True,tx=True)
        testEndJoint = pc.textFieldButtonGrp('endTentJointTFBG',q=True,tx=True)
        controlType = pc.textFieldGrp('conTentTFG',q=True,tx=True)
        offControlType = pc.textField('conOffTentTF',q=True,tx=True)
        type = pc.textFieldGrp('tenticleNameTFG',q=True,tx=True)
        offsetControls = pc.checkBoxGrp('offsetChk',q=True,v1=True)
        dynamics = pc.checkBoxGrp('dynamicChk',q=True,v1=True)
        numJoints = pc.intSliderGrp('tenticaleJointISG',q=True,v=True)

        if type == '':
            pc.error('You must define the tentacle name.')

        if len(tentStartJoint) == len(tentEndJoint):
            pc.error('You must select a unique joint for each options')
        else:
            print('Implement buildTentacleSetup')
            buildTentacleSetup(name, tentStartJoint, tentEndJoint, controlType, offsetControls, offControlType, dynamics, type, stretchType, stretch, numJoints, volume, world, scale)

    if call == 'hand':
        
        j = 0
        numFingers = 0

        for i in range(5):
            if pc.checkBox(('finger'+i+'Chk'),q=True,v=True) == 1:
                numFingers = i

        fingerName = []
        startJoint = []
        for i in range(numFingers):
            fingerName.append(pc.textField(('finger'+(i+1)+'NameTF'),q=True,tx=True))
            startJoint.append(pc.textFieldButtonGrp(('finger'+(i+1)+'JointTFBG'),q=True,tx=True))

        installCurl = 1
        installSpread = 1
        installSpin = 1
        installStretch = 1

        side = pc.optionMenu('sidePrefix',q=True,v=True)
        controller = pc.textFieldButtonGrp('controlHandTFBG',q=True,tx=True)
        controlType = pc.textField('fkConHandTF',q=True,tx=True)
        fkControl = pc.checkBoxGrp('fkConChk',q=True,v1=True)
        nameMethod = pc.radioButtonGrp('namingRdBnGrp',q=True,sl=True)
        skipLast = pc.checkBoxGrp('skipOpChk',q=True,v=True)
        manual = pc.checkBoxGrp('manualOpChk',q=True,v1=True)
        world = pc.checkBox('buildChk',q=True,v=True)

        sideQ = rigSideSep(side)
        fingerSide = pc.radioButtonGrp('fingerSideRdBnGrp',q=True,sl=True)

        if side != 'none':
            if fingerSide == 1:
                side = sideQ[0]
            else:
                side = sideQ[1]
        else:
            side = ''

        if name != '':
            name = name + '_'

        fingerRotAxis = []
        if manual == 0:
            fingerRotAxis = getFingerAxisFigures(startJoint[0])
        else:
            fingerRotAxis.append(pc.radioButtonGrp('spinFacingRdBnGrp', q=True,sl=True))
            fingerRotAxis.append(pc.radioButtonGrp('curlFacingRdBnGrp', q=True,sl=True))
            fingerRotAxis.append(pc.radioButtonGrp('spreadFacingRdBnGrp', q=True,sl=True))
            fingerRotAxis.append(pc.radioButtonGrp('stretchFacingRdBnGrp', q=True,sl=True))

        # Error Checking
        if not pc.objExists(controller):
            pc.error('The controller you specified to install the hand controls on does not appear to exist!') # TODO: redo text

        if pc.Attribute.exists('fingerCONTROLS',controller):
            pc.error('You appear to already have installed finger controls on this controller!') # TODO: redo text

        if installCurl == 1:
            if installSpread == 1 and fingerRotAxis[1] == fingerRotAxis[2]: pc.error('You must select a unique axis for for the Spread Axis')                
            if installSpin == 1 and fingerRotAxis[1] == fingerRotAxis[0]: pc.error('You must select a unique axis for for the Spin Axis')                
        if installSpread == 1:
            if installCurl == 1 and fingerRotAxis[2] == fingerRotAxis[1]: pc.error('You must select a unique axis for for the Spin Axis')                
            if installSpin == 1 and fingerRotAxis[2] == fingerRotAxis[0]: pc.error('You must select a unique axis for for the Spin Axis')                
        if installSpin == 1:
            if installCurl == 1 and fingerRotAxis[0] == fingerRotAxis[1]: pc.error('You must select a unique axis for for the Spin Axis')
            if installSpread == 1 and fingerRotAxis[0] == fingerRotAxis[2]: pc.error('You must select a unique axis for for the Spin Axis')

        for i in range(numFingers):
            # TODO: isValidObjectName figure out how to check if name is valid in pymel
            # `isValidObjectName($fingerName[$i])` == 0) error ("FINGER " + ($i+1) + ":   The name you specified for this finger is invalid!") 
            for j in range(numFingers):
                if fingerName[i] != fingerName[j] and i != j: pc.error('FINGER ' + (i+1) + ':   You have already used finger name:    <' + fingerName[i] + '>   on finger (' + (j+1) + ')!')
                if pc.objExists(startJoint[i]): pc.error('FINGER ' + (i+1) + ':     The start joint you specified:  <' + startJoint[i] + '>     does not appear to exist!')
                if startJoint[i] != startJoint[j] and (i != j): pc.error('FINGER ' + (i+1) + ':     You have already used the start joint:  <' + startJoint[j] + '>     on finger (' + (j+1) + ')!')

        pc.addAttr(startJoint[0],ln='damp',at='long',min=2,dv=3,keyable=True) # add damp attr for thumb        
        buildHandSetup(name, side, controller, fkControl, controlType, numFingers, fingerName, startJoint, fingerRotAxis, nameMethod, skipLast, "", world, scale)

        if mirror:
            if prefixSepCheck(startJoint[0]) == 1:
                rStartjoint = []
                tempFinger = ''
                tempNames = ''
                for n in range(numFingers):
                    tempFinger = pc.textFieldButtonGrp(('finger' + (n+1) + 'JointTFBG'),q=True,tx=True)
                    tempNames = tempFinger.replace(sideQ[0],sideQ[1])
                    rStartJoint[n] = tempNames
                rController = controller.replace(sideQ[0],sideQ[1])
                pc.addAttr(rStartJoint[0],ln='damp',at='long',min=2,dv=3,keyable=True)                
                buildHandSetup(name, sideQ[1], rController, fkControl, controlType, numFingers, fingerName, rStartJoint, fingerRotAxis, nameMethod, skipLast, "", world, scale)

    if case == 'parentSwitch':
        node = pc.textFieldButtonGrp('parentConTFBG',q=True,tx=True)
        parent = pc.textFieldButtonGrp('parentGrpTFBG',q=True,tx=True)
        parentSpace = pc.textScrollList('spaceSwitchParentTSL',q=True,ai=True)
        spaceName = pc.textScrollList('spaceSwitchNameTSL',q=True,ai=True)
        spaceType = pc.radioButtonGrp('parentTypeRdBnGrp',q=True,sl=True)

        if len(parentSpace) > 0:
            print('Implement buildSpaceSwitchSetup')
            buildSpaceSwitchSetup(node, parent, parentSpace, spaceName, spaceType)
        else:
            pc.error('No target parent found to add space switch')

    pc.select(cl=True)
    print('Operation successful: Animation rig created for '+call+'.\n')

def prefixSepCheck(node):
    side = pc.optionMenu('sidePrefix',q=True,v=True)
    sideQ = rigSideSep(side)
    split = node.split('_')
    if len(splin) > 1 and len(sideQ) > 1:
        if sideQ[0] == split[0]+'_':
            return 1
        else:
            return 0
    else:
        return 0