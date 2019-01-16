import re

import pymel.core as pc
from Maya_Rigging.Core import JointStretchNetworkLib as js
from Maya_Rigging.Core.BuildModuleJointSkeletonLib import orientJoints
from Maya_Rigging.Core import BuildWorld as bw
from Maya_Rigging.Core.Setup.BuildSpaceSwitchSetup import buildSpaceSwitchSetup
from Maya_Rigging.Core.Setup.BuildTwistJointSetup import buildTwistJointSetup
from Maya_Rigging.Utils import CharUtilsLib as chUL
from Maya_Rigging.Utils import CurveUtilLib as cuUL
from Maya_Rigging.Utils import List

def buildQuadLegSetup(name,
                      side,
                      hipJoint,
                      hockJoint,
                      ankleJoint,
                      ballJoint,
                      stretchType,
                      ikFkType,
                      stretch,
                      midLock,
                      volume,
                      world,
                      scale,
                      controlColor):
    FK = []  			#array to hold fk joint chain
    IK = []				#array to hold fk joint chain
    list = []			#array to hold actual joint chain
    temp = ''			#hold name unused joint to delete
    middleIndex = 0		#hold middle index of ik joint chain
    modPos = []			#hold mid postion for pole vectoe control
    hockIkHandle = []
    ankleIkHandle = []	#hold all created ik handle
    ballIkHandle = []
    toeIkHandle = []
    fkContrlList = []	#array to hold fk control joint chain
    fkCon = []			#array to hold newly creted fk control
    ikSpaceGrp = ''
    parentGrp = []		#holds name of parent grp of given object
    allChild = []
    ballJointChild = []
    childTemp = []
    cleanGrp = []

    partGrp = pc.group(em=True, n=(name + side + 'legParts_grp'))
    chUL.lockAndHide(partGrp, 'locknHide', 'trans rot scale')

    if world:
        cleanGrp = bw.build_world(name, scale)
        pc.parent(partGrp, cleanGrp[0])

    # get child joint of ball joint
    endJoint = chUL.getChildJoint(ballJoint)

    # checking fingers if its there then upparent for creating ik fk joints....
    allChild = pc.listRelatives(ankleJoint, c=True)
    for i in range(len(allChild)):
        if allChild[i]!=ballJoint:
            childTemp = pc.parent(allChild[i], w=True)
            ballJointChild.append(childTemp[0])

    # duplicate joint chain twice in order to create ik fk switch
    FK = chUL.dupId(hipJoint,'prefix','fk')
    IK = chUL.dupId(hipJoint,'prefix','ik')   

    # parent back fingers joint if its there
    if len(allChild)>1:
        for i in range(0,len(allChild)-1):
            pc.parent(ballJointChild[i], ankleJoint)

    for x in range(len(FK)):
        if pc.attributeQuery('twistJoints', n=FK[x], ex=True): # delete twistAttr if exists.....
            try:
                pc.deleteAttr(FK[x], attribute='twistJoints')
                pc.deleteAttr(IK[x], attribute='twistJoints')
            except:
                pass

    # hold all joint chain in array
    IK = chUL.findJointArray(('ik_' + hipJoint), ('ik_' + ballJoint))
    FK = chUL.findJointArray(('fk_' + hipJoint), ('fk_' + ballJoint))
    list = chUL.findJointArray(hipJoint, ballJoint)

    pc.select(cl=True)

    # create controls
    ankleCtrl = cuUL.curveControl('cube1', 'joint', controlColor)
    ankleCtrl[0] = pc.rename(ankleCtrl[0], name + side + 'foot_ctrl')
    cuUL.resizeCurves(None, 0, 0, 1, 2)
    flexCtrl = cuUL.curveControl('sphere', 'joint', controlColor)
    flexCtrl[0] = pc.rename(flexCtrl[0], name + side + 'flex_ctrl')
    cuUL.resizeCurves(None, 1, 1, 1, 0.7)
    kneeCtrl = cuUL.curveControl('cone', 'curve', controlColor)
    kneeCtrl[0] = pc.rename(kneeCtrl[0], name + side + 'knee_ctrl')
    switchCtrl = cuUL.curveControl('pin1', 'curve', controlColor)
    switchCtrl[0] = pc.rename(switchCtrl[0], name + side + 'legSwitches_ctrl')
    chUL.fixFacingAxis('Z', 0)

    # snap controls to to respective joints
    anklePos = pc.xform(ankleJoint, q=True, ws=True, rp=True)
    pc.setAttr((ankleCtrl[0] + '.t'), (anklePos[0], anklePos[1], anklePos[2]))
    tempCon = pc.aimConstraint(ballJoint, ankleCtrl[0], offset=[0,0,0], weight=1, aimVector=[0,0,1], upVector=[0,1,0], worldUpType='vector', worldUpVector=[0,1,0], skip=['x','z'])
    pc.delete(tempCon)
    tempLoc = pc.spaceLocator()
    pc.setAttr((tempLoc + '.t'), (anklePos[0],anklePos[1],anklePos[2]))
    tempClt = pc.cluster(ankleCtrl[0])
    pc.parent(tempClt[1], tempLoc)
    pc.pointConstraint(ballJoint, tempLoc, w=1)
    pc.scale(tempLoc,(scale,scale,scale))
    pc.select(ankleCtrl[0], r=True)
    pc.runtime.DeleteHistory()
    pc.delete(tempLoc)

    # snap flexCtrl[0]
    chUL.Snap(ankleJoint, flexCtrl[0])
    pc.makeIdentity(flexCtrl[0], apply=True, t=0, r=1, s=0)
    pc.parent(flexCtrl[0], ankleCtrl[0])
    flexCtrlZero = chUL.quickZeroOut(flexCtrl[0])

    chUL.Snap(ballJoint, switchCtrl[0])
    pc.setAttr((switchCtrl[0]+'.r'), (0,0,0))
    pc.select(cl=True)
    
    pc.parent(ankleCtrl[0], partGrp)
    pc.parent(kneeCtrl[0], partGrp)
    pc.parent(switchCtrl[0], partGrp)

    pc.parentConstraint(ballJoint, switchCtrl[0], mo=True, weight=1)
    chUL.lockAndHide(switchCtrl[0], 'locknHide', 'trans rot scale vis')

    # get middle index of ik joint for pole control placement
    tempIK = chUL.findJointArray(('ik_' + hipJoint), ('ik_' + hockJoint))
    middleIndex = ((len(tempIK))/2)
    modPos = chUL.zoofindPolePosition(hipJoint, IK[middleIndex], hockJoint, 0.7)
    pc.select(kneeCtrl[0], r=True)
    pc.setAttr((kneeCtrl[0]+'.t'),(modPos[0],modPos[1],modPos[2]))
    chUL.fixFacingAxis('Z', 1)
    pc.select(cl=True)
    # create ik fk connections from given arrey
    chUL.fkIkConnect(list,IK, FK, ikFkType, switchCtrl[0])
    pc.select(cl=True)

    # fk controllers and rename them respectively
    fkCon = chUL.fkControl(FK[0], 'circleCross', 1, controlColor)
    fkContrlList = chUL.listHierarchy(fkCon[0])
    for f in fkContrlList:
        f = pc.rename(f, (name + side + f))

    # check stretch condition and create connections
    hockJointPos = pc.xform(hockJoint, q=True, worldSpace=True, rotatePivot=True)
    if stretch == 1:
        js.stretch_network(name, side, ('ik_' + hipJoint), ('ik_' + hockJoint), ankleCtrl[0], stretchType, midLock, kneeCtrl[0])
        chUL.stretchTypeConnect(list, IK, FK, stretchType, switchCtrl[0])        

    # some stretch corrrection purely name specific might not run on different case remember that..
    if stretch == 1:
        # select -r (name + side + 'ik_' + hipJoint + 'End_loc')
        # select -tgl (name + side + 'ik_' + ankleJoint + 'End_loc')
        tempSel = [(name + side + 'ik_' + hipJoint + 'End_loc'),(name + side + 'ik_' + hockJoint + 'End_loc')]
        chUL.lockAndHide(tempSel[0], 'unLock','trans')
        chUL.lockAndHide(tempSel[1],'unLock','trans')

        transConnection = pc.listConnections((tempSel[0] + '.tx'), d=False, s=True, plugs=True, skipConversionNodes=True)
        transNodePath = transConnection[0]        
        match = re.search('[^.]*',str(transNodePath))
        transNode = []
        if match:
            transNode.append(match.group())
        elif transNodePath:
            transNode.append(transNodePath)
        pc.delete(transNode)
        
        transConnection = pc.listConnections((tempSel[1] + '.tx'), d=False, s=True, plugs=True, skipConversionNodes=True)
        transNodePath = transConnection[0]                
        match = re.search('[^.]*',str(transNodePath))
        transNode = []
        if match:
            transNode.append(match.group())            
        elif transNodePath:
            transNode.append(transNodePath)            
        pc.delete(transNode)
        
        ikSpaceGrp = pc.group(em=True, n=(name + side + 'stretchLocCon_grp'))
        pc.setAttr((ikSpaceGrp+'.t'),(hockJointPos[0],hockJointPos[1],hockJointPos[2]))
        pc.select(cl=True)
        
        pointConA = pc.pointConstraint(ikSpaceGrp, tempSel[0], offset=[0,0,0], weight=1)
        pointConA = pc.pointConstraint(ikSpaceGrp, tempSel[1], offset=[0,0,0], weight=1)


    # creating twist joint setup if attribute exists on given joint
    size = (len(list))-1
    twistJoints = []
    sknJoints = []
    ankleRots = pc.listRelatives(ankleJoint, parent=True)
    for l in list:
        if l == ankleRots[0]:
            twistJoints = buildTwistJointSetup(name,
                                               side,
                                               l,
                                               stretchType,
                                               ikFkType,
                                               'child',
                                               ankleJoint,
                                               switchCtrl[0],
                                               stretch,
                                               volume,
                                               scale,
                                               controlColor)
        else:
            twistJoints = buildTwistJointSetup(name,
                                               side,
                                               l,
                                               stretchType,
                                               ikFkType,
                                               'parent',
                                               ankleJoint,
                                               switchCtrl[0],
                                               stretch,
                                               volume,
                                               scale,
                                               controlColor)
        sknJoints.extend(twistJoints)


    # createik handle for ik joint chain
    hockIkHandle = pc.ikHandle(name=(name + side + 'hock_ikhandle'), startJoint=('ik_' + hipJoint), endEffector=('ik_' + hockJoint), solver='ikRPsolver')
    ankleIkHandle = pc.ikHandle(name=(name + side + 'ankle_ikhandle'), startJoint=('ik_' + hockJoint), endEffector=('ik_' + ankleJoint), solver='ikRPsolver')
    ballIkHandle = pc.ikHandle(name=(name + side + 'ball_ikhandle'), startJoint=('ik_' + ankleJoint), endEffector=('ik_' + ballJoint), solver='ikRPsolver')
    toeIkHandle = pc.ikHandle(name=(name + side + 'toe_ikhandle'), startJoint=('ik_' + ballJoint), endEffector=('ik_' + endJoint), solver='ikRPsolver')

    # add attribute to ankle control and create reverse foot setup for leg
    pc.addAttr(ankleCtrl[0], ln='FOOT', at='bool', keyable=True)
    pc.setAttr((ankleCtrl[0] + '.FOOT'), keyable=False, channelBox=True)
    pc.addAttr(ankleCtrl[0], ln='roll', at='double', min=-10, max=10, keyable=True)
    pc.addAttr(ankleCtrl[0], ln='rollAngle', at='double', dv=50, keyable=True)
    pc.setAttr((ankleCtrl[0] + '.rollAngle'), keyable=False, channelBox=True)
    pc.addAttr(ankleCtrl[0], ln='tap', at='double', keyable=True)
    pc.addAttr(ankleCtrl[0], ln='clawRoll', at='double', keyable=True)
    pc.addAttr(ankleCtrl[0], ln='bank', at='double', keyable=True)
    pc.addAttr(ankleCtrl[0], ln='ballTwist', at='double', keyable=True)
    pc.addAttr(ankleCtrl[0], ln='toePivot', at='double', keyable=True)
    pc.addAttr(ankleCtrl[0], ln='toePivotSide', at='double', keyable=True)
    pc.addAttr(ankleCtrl[0], ln='heelPivot', at='double', keyable=True)
    pc.addAttr(ankleCtrl[0], ln='heelPivotSide', at='double', keyable=True)

    rollBallGrp = pc.group(em=True, n=(name + side + 'clawRoll_grp'))
    tapGrp = pc.group(em=True, n=(name + side + 'tap_grp'))
    toePivotGrp = pc.group(em=True, n=(name + side + 'toePivot_grp'))
    ballPivotGrp = pc.group(em=True, n=(name + side + 'ballPivot_grp'))
    heelPivotGrp = pc.group(em=True, n=(name + side + 'heelPivot_grp'))
    inPivotBankGrp = pc.group(em=True, n=(name + side + 'inPivotBank_grp'))
    outPivotBankGrp = pc.group(em=True, n=(name + side + 'outPivotBank_grp'))

    #snapping to right postion
    heelPos = []
    bankInPos = []
    bankOutPos = []

    anklePos = pc.xform(ankleJoint, q=True, ws=True, rp=True)
    ballPos = pc.xform(ballJoint, q=True, ws=True, rp=True)
    endPos = pc.xform(endJoint, q=True, ws=True, rp=True)

    tempPivots = ''

    if not pc.attributeQuery('heelPos', n=ankleJoint, ex=True):
        tempPivots = chUL.makeFootHeelPivots(ankleJoint,ballJoint)
        heel = pc.getAttr(ankleJoint+'.heelPos')
        bankIn = pc.getAttr(ballJoint + '.bankInPos')
        bankOut = pc.getAttr(ballJoint + '.bankOutPos')
        heelPos = pc.xform(heel, q=True, ws=True, rp=True)
        bankInPos = pc.xform(bankIn, q=True, ws=True, rp=True)
        bankOutPos = pc.xform(bankOut, q=True, ws=True, rp=True)
    else:
        heel = pc.getAttr(ankleJoint+'.heelPos')
        bankIn = pc.getAttr(ballJoint + '.bankInPos')
        bankOut = pc.getAttr(ballJoint + '.bankOutPos')
        heelPos = pc.xform(heel, q=True, ws=True, rp=True)
        bankInPos = pc.xform(bankIn, q=True, ws=True, rp=True)
        bankOutPos = pc.xform(bankOut, q=True, ws=True, rp=True)
    try:
        pc.delete(tempPivots)
    except:
        pass

    pc.setAttr((rollBallGrp + '.t'), (ballPos[0],ballPos[1],ballPos[2]))
    pc.setAttr((tapGrp + '.t'), (ballPos[0],ballPos[1],ballPos[2]))
    pc.setAttr((toePivotGrp + '.t'), (endPos[0],endPos[1],endPos[2]))
    pc.setAttr((ballPivotGrp + '.t'), (ballPos[0],ballPos[1],ballPos[2]))
    pc.setAttr((heelPivotGrp + '.t'), (heelPos[0],heelPos[1],heelPos[2]))
    pc.setAttr((inPivotBankGrp + '.t'), (bankInPos[0],bankInPos[1],bankInPos[2]))
    pc.setAttr((outPivotBankGrp + '.t'), (bankOutPos[0],bankOutPos[1],bankOutPos[2]))

    #parent to the respective grp and zeroout the grp if it has any rotation value
    pc.parent(heelPivotGrp, ankleCtrl[0])
    pc.setAttr((heelPivotGrp + '.r'), (0,0,0))
    pc.parent(toePivotGrp,heelPivotGrp)
    pc.setAttr((toePivotGrp + '.r'), (0,0,0))
    pc.parent(ballPivotGrp, toePivotGrp)
    pc.setAttr((ballPivotGrp + '.r'), (0,0,0))
    pc.parent(inPivotBankGrp, ballPivotGrp)
    pc.setAttr((inPivotBankGrp + '.r'), (0,0,0))
    pc.parent(outPivotBankGrp, inPivotBankGrp)
    pc.setAttr((outPivotBankGrp + '.r'), (0,0,0))
    pc.parent(tapGrp,outPivotBankGrp)
    pc.setAttr((tapGrp + '.r'), (0,0,0))
    pc.parent(rollBallGrp, outPivotBankGrp)
    pc.setAttr((rollBallGrp + '.r'), (0,0,0))
    pc.parent(flexCtrlZero[0],rollBallGrp)
    pc.setAttr((flexCtrlZero[0] + '.r'),(0,0,0))

    #connnecting foot attribute
    footRollRange = pc.createNode('setRange', n=(name + side + 'heelRoll_range'))
    pc.setAttr((footRollRange + '.oldMinX'), -10)

    rollBallRMV = pc.createNode('remapValue', n=(name + side + 'clawRoll_rmv'))
    pc.setAttr((rollBallRMV + '.value[1].value_FloatValue'),0)
    pc.setAttr((rollBallRMV + '.value[2].value_Position'),0.5)
    pc.setAttr((rollBallRMV + '.value[2].value_FloatValue'),1)
    pc.setAttr((rollBallRMV + '.value[2].value_Interp'),1)
    pc.setAttr((rollBallRMV + '.inputMax'),10)

    rollToeRMV = pc.createNode('remapValue', n=(name + side + 'toeRoll_rmv'))
    pc.setAttr((rollToeRMV + '.value[2].value_Position'),0.5)
    pc.setAttr((rollToeRMV + '.value[2].value_Interp'),1)
    pc.setAttr((rollToeRMV + '.inputMax'),10)

    hellRollMDL = pc.createNode('multDoubleLinear', n=(name + side + 'hellRoll_mdl'))
    pc.setAttr((hellRollMDL + '.input2'),-1)

    rollBallAdl = pc.createNode('addDoubleLinear', n=(name + side + 'clawRoll_adl'))
    toeRollAdl = pc.createNode('addDoubleLinear', n=(name + side + 'toeRoll_adl'))
    heelRollAdl = pc.createNode('addDoubleLinear', n=(name + side + 'heelRoll_adl'))

    pc.connectAttr((ankleCtrl[0] + '.rollAngle'), (hellRollMDL + '.input1'))
    pc.connectAttr((hellRollMDL + '.output'), (footRollRange + '.minX'))
    pc.connectAttr((ankleCtrl[0] +'.roll'), (footRollRange + '.valueX'))

    pc.connectAttr((ankleCtrl[0] + '.roll'), (rollBallRMV + '.inputValue'))
    pc.connectAttr((ankleCtrl[0] + '.rollAngle'), (rollBallRMV + '.outputMax'))

    pc.connectAttr((ankleCtrl[0] +'.roll'), (rollToeRMV + '.inputValue'))
    pc.connectAttr((ankleCtrl[0] +'.rollAngle'), (rollToeRMV + '.outputMax'))

    pc.connectAttr((footRollRange + '.outValueX'), (heelRollAdl + '.input1'))
    pc.connectAttr((rollBallRMV + '.outValue'), (rollBallAdl + '.input1'))
    pc.connectAttr((rollToeRMV + '.outValue'), (toeRollAdl + '.input1'))

    pc.connectAttr((ankleCtrl[0] + '.clawRoll'), (rollBallAdl + '.input2'))
    pc.connectAttr((ankleCtrl[0] + '.toePivot'), (toeRollAdl + '.input2'))
    pc.connectAttr((ankleCtrl[0] + '.heelPivot'), (heelRollAdl + '.input2'))


    pc.connectAttr((ankleCtrl[0] + '.tap'), (tapGrp + '.rx'))
    pc.connectAttr((rollBallAdl + '.output'), (rollBallGrp + '.rx'))
    pc.connectAttr((ankleCtrl[0] + '.bank'), (inPivotBankGrp + '.rz'))
    pc.transformLimits(inPivotBankGrp, rz=[0,45], erz=[1,0])
    pc.connectAttr((ankleCtrl[0] + '.bank'), (outPivotBankGrp + '.rz'))
    pc.transformLimits(outPivotBankGrp, rz=[-45,0], erz=[0,1])
    pc.connectAttr((ankleCtrl[0] + '.ballTwist'), (ballPivotGrp + '.ry'))
    pc.connectAttr((toeRollAdl + '.output'), (toePivotGrp + '.rx'))
    pc.connectAttr((ankleCtrl[0] + '.toePivotSide'), (toePivotGrp + '.ry'))
    pc.connectAttr((heelRollAdl + '.output'), (heelPivotGrp + '.rx'))
    pc.connectAttr((ankleCtrl[0] + '.heelPivotSide'), (heelPivotGrp + '.ry'))

    #now create flex leg setup..
    legFlexJointsPos = chUL.getQuadFlexLegJointPos(hipJoint, ankleJoint)
    flexJnt = []

    #creating spring joints
    for i in range(4):
        tempPos = legFlexJointsPos[i]	
        flexJnt.append(pc.joint(p=[(tempPos[0]),(tempPos[1]),(tempPos[2])], n=(name+side+'legFlex'+str(i+1)+'_jnt')))


    # orienting joints and parent..
    orientJoints(flexJnt, 'xyz', 'zdown')
    hipParentJoint = chUL.getParent(hipJoint)
    try:
        pc.parent(flexJnt[0], hipParentJoint)
    except:
        pass
    pc.setAttr((flexJnt[0] + '.visibility'),0)
    chUL.lockAndHide(flexJnt[0],'lock','vis')

    # creating leg offset cntrl setup
    pc.select(cl=True)
    legOffsetCtrl = cuUL.curveControl('cube1', 'joint', controlColor)
    legOffsetCtrl[0] = pc.rename(legOffsetCtrl[0], name + side + 'legOffset_ctrl')

    chUL.Snap(hipJoint,legOffsetCtrl[0])
    pc.setAttr((legOffsetCtrl[0]+'.r'),(0,0,0))

    pc.parent(legOffsetCtrl[0],partGrp)
    chUL.lockAndHide(legOffsetCtrl[0],'locknHide','rot scale vis')

    #looking for first fk control unlock trans create point cons with offset control and lock it again 
    fkConParent = chUL.getParent(fkContrlList[0])    
    chUL.lockAndHide(fkConParent[0],'unLock','trans')
    pc.parentConstraint(legOffsetCtrl[0], flexJnt[0], mo=True, skipRotate=['x','y','z'], weight=1)
    pc.parentConstraint(legOffsetCtrl[0], IK[0], mo=True, skipRotate=['x','y','z'], weight=1)
    pc.parentConstraint(legOffsetCtrl[0], fkConParent, mo=True, skipRotate=['x','y','z'], weight=1)
    pc.parentConstraint(legOffsetCtrl[0], hipJoint, mo=True, skipRotate=['x','y','z'],weight=1)
    chUL.lockAndHide(fkConParent[0],'lock','trans')

    #create flex ik handle
    flexIkHandle = pc.ikHandle(name=(name + side + 'flex_ikhandle'), startJoint=flexJnt[0], endEffector=flexJnt[3], solver='ikRPsolver')
    pc.parent(flexIkHandle[0], rollBallGrp)
    pc.setAttr((flexIkHandle[0] + '.visibility'),0)
    chUL.lockAndHide(flexIkHandle[0],'lock','trans rot scale vis')
    pc.poleVectorConstraint (kneeCtrl[0],flexIkHandle[0])
    pc.parentConstraint(flexJnt[3], flexCtrlZero[0], mo=True, skipTranslate=['x','y','z'], weight=1)

    #parent ik handle into foot control and lock the transforms
    pc.parent(hockIkHandle[0], flexCtrl[0])
    if stretch == 1: 
        pc.parent(ikSpaceGrp, flexCtrl[0])
    pc.setAttr((hockIkHandle[0] + '.visibility'), 0)
    chUL.lockAndHide(hockIkHandle[0],'lock','trans rot scale vis')

    pc.parent(ankleIkHandle[0],rollBallGrp)
    pc.setAttr((ankleIkHandle[0] + '.visibility'), 0)
    chUL.lockAndHide(ankleIkHandle[0],'lock','trans rot scale vis')

    pc.parent(toeIkHandle[0],tapGrp)
    pc.setAttr((toeIkHandle[0] + '.visibility'),0)
    chUL.lockAndHide(toeIkHandle[0],'lock','trans rot scale vis')

    pc.parent(ballIkHandle[0], outPivotBankGrp)
    pc.setAttr((ballIkHandle[0] + '.visibility'),0)
    chUL.lockAndHide(ballIkHandle[0],'lock','trans rot scale vis')

    #create pole vector constraint for ikhandle
    pc.poleVectorConstraint(kneeCtrl[0], hockIkHandle[0])

    #create ikfk visibility connections
    pc.addAttr(switchCtrl[0], ln='autoVis', at='bool', keyable=True)
    pc.setAttr((switchCtrl[0] + '.autoVis'),1)
    pc.addAttr(switchCtrl[0], ln='fkVis', at='bool', keyable=True)
    pc.addAttr(switchCtrl[0], ln='ikVis', at='bool', keyable=True)
    pc.setAttr((switchCtrl[0] + '.autoVis'), keyable=False, channelBox=True)

    fkIkCnd = pc.createNode('condition', n=(name + side + 'fkIkVis_cnd'))
    fkIkRev = pc.createNode('reverse', n=(name + side + 'fkIkVis_rev'))
    pc.connectAttr((switchCtrl[0] + '.FK_IK'), (fkIkRev + '.inputX'))
    pc.connectAttr((fkIkRev + '.outputX'), (fkIkCnd + '.colorIfFalseR'))
    pc.connectAttr((switchCtrl[0] + '.FK_IK'), (fkIkCnd + '.colorIfFalseG'))
    pc.connectAttr((switchCtrl[0] + '.autoVis'), (fkIkCnd + '.firstTerm'))
    pc.connectAttr((switchCtrl[0] + '.fkVis'), (fkIkCnd + '.colorIfTrueG'))
    pc.connectAttr((switchCtrl[0] + '.ikVis'), (fkIkCnd + '.colorIfTrueR'))

    pc.connectAttr((fkIkCnd + '.outColorR'), (fkContrlList[0] + '.visibility'))
    pc.connectAttr((fkIkCnd + '.outColorR'), (FK[0] + '.visibility'))
    pc.connectAttr((fkIkCnd + '.outColorG'), (ankleCtrl[0] + '.visibility'))
    pc.connectAttr((fkIkCnd + '.outColorG'), (kneeCtrl[0] + '.visibility'))
    pc.connectAttr((fkIkCnd + '.outColorG'), (IK[0] + '.visibility'))

    #zero out all controllers and cleanup animation controller
    ankleConGrp = chUL.quickZeroOut(ankleCtrl[0])
    kneeConGrp = chUL.quickZeroOut(kneeCtrl[0])
    legOffsetConGrp = chUL.quickZeroOut(legOffsetCtrl[0])
    pc.select(cl=True)

    #create guide curve
    guideCurve = chUL.curveGuide(IK[middleIndex], kneeCtrl[0])
    pc.connectAttr((fkIkCnd + '.outColorG'), (guideCurve + '.visibility'))

    chUL.lockAndHide(ankleCtrl[0], 'locknHide', 'scale vis')
    chUL.lockAndHide(kneeCtrl[0], 'locknHide', 'rot scale vis')

    if stretchType == 'translate':
        for f in fkContrlList:
            chUL.lockAndHide(f, 'locknHide', 'scale vis')

    if stretchType == 'scale':
        for f in fkContrlList:
            chUL.lockAndHide(f, 'locknHide', 'trans vis')

    parentJoint = pc.listRelatives(hipJoint, parent=True)
    parentGrp = pc.listRelatives(fkContrlList[0], parent=True)
    chUL.lockAndHide(parentGrp[0], 'unLock', 'trans rot')
    pc.parent(parentGrp[0], partGrp)

    #add leg rig info for future update...
    charRigInfo = chUL.getcharRigInfoNode(name)
    pc.addAttr(charRigInfo, ln=(side+'legRig'), dt='string')
    pc.setAttr((charRigInfo + '.' + (side+'legRig')), (ankleCtrl[0]+' '+kneeCtrl[0]+' '+switchCtrl[0]+' '+fkContrlList[0]), type='string')

    #create space switch
    if world:
        if pc.attributeQuery('spineRig', n=charRigInfo, ex=True):
            spineRigPart = pc.getAttr(charRigInfo+'.spineRig')
            spineRigArray = List.seperate(spineRigPart)
            buildSpaceSwitchSetup(ankleCtrl[0], ankleConGrp[0],[spineRigArray[2],spineRigArray[0],(name+'worldB_ctrl')], ['hip','root','world'], 1)
            buildSpaceSwitchSetup(kneeCtrl[0], kneeConGrp[0],[ankleCtrl[0],spineRigArray[0],(name+'worldB_ctrl')], ['foot','root','world'], 1)
            pc.setAttr((ankleCtrl[0]+'.parent'), 2)

    #parent skeleton
    pc.select(cl=True)
    chUL.parentSkeletonTo(hipJoint, cleanGrp[1])

    # createskinJointset
    set = chUL.createSkinJointSet(name)
    sknJoints.extend(list);
    sknJoints.extend(sknJoints)
    chUL.addSkinJointToSet(set, sknJoints)

    #scale controls to global value
    pc.select(kneeCtrl,flexCtrl,legOffsetCtrl,switchCtrl,fkContrlList, r=True)
    cuUL.resizeCurves(None, 1, 1, 1, scale)
    pc.select(cl=True)
    
    if parentJoint[0] != '':
        pc.parentConstraint(parentJoint[0], parentGrp[0], mo=True, weight=1)
        pc.parentConstraint(parentJoint[0], legOffsetConGrp[0], mo=True, weight=1)

    #anim control cleanup
    chUL.lockAndHide(parentGrp[0],'lock','trans rot')
    chUL.lockAndHide(ankleConGrp[0],'lock','trans rot scale vis')
    chUL.lockAndHide(kneeConGrp[0],'lock','trans rot scale vis')
    chUL.lockAndHide(legOffsetCtrl[0],'locknHide','rot scale vis')
    chUL.lockAndHide(legOffsetConGrp[0],'lock','trans rot scale vis')
    chUL.lockAndHide(flexCtrl[0], 'locknHide', 'trans scale vis')
    chUL.lockAndHide(flexCtrlZero[0],'lock','trans rot scale vis')
    pc.delete(fkContrlList[len(fkContrlList)-1]) #deleting end fk control see line no.138 for detail