import pymel.core as pc
from Maya_Rigging.Core import JointStretchNetworkLib as js
from Maya_Rigging.Core import BuildWorld as bw
from Maya_Rigging.Utils import CharUtilsLib as chUL
from Maya_Rigging.Utils import CurveUtilLib as cuUL

def buildSpineSetup(name,
                    side,
                    rootJoint,
                    chestJoint,
                    hipJoint,
                    stretchType,
                    numJoints,
                    stretch,
                    volume,
                    world,
                    scale,
                    controlColor,
                    colorCenter):

    stretchAxis = []
    curveJoints = []
    ikHandle = []
    list = []
    orientAxis = ''
    facingAxis = ''
    curve = ''
    scaleCmd = ''
    cleanGrp = []
    nonScaleGrp = (name+'non_scale_grp')
    scaleNode = (name+'worldScaleCon_grp')

    partGrp = pc.group(em=True, n=(name + side + 'spineParts_grp'))
    chUL.lockAndHide(partGrp, 'locknHide', 'trans rot scale')

    if world:
        cleanGrp = bw.build_world(name, scale, colorCenter)
        pc.parent(partGrp, cleanGrp[0])
    else:
        scaleNode = bw.create_scale_grp(name)

    # considering that root jnt will be the main parent joint so parent in the skeleton grp..
    # parent rootJoint cleanGrp[1]

    list = chUL.findJointArray(rootJoint, chestJoint)
    curve = chUL.jointCurve(rootJoint, chestJoint)
    pc.rebuildCurve(curve, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=2, d=3, tol=0.001)
    curve = pc.rename(curve, (name + side + 'spine_crv'))
    pc.setAttr((curve + '.visibility'), 0)
    chUL.lockAndHide(curve,'lock','trans rot scale vis')
    
    stretchAxis = chUL.getStretchAxis(chestJoint, 'translate')

    if stretchAxis[0] == 'tx': 
        orientAxis = 'xyz' 
        facingAxis = 'X' 
        scaleCmd = pc.Callback(cuUL.resizeCurves, None, 0,1,1,2.5)
    elif stretchAxis[0] == 'ty': 
        orientAxis = 'yzx' 
        facingAxis = 'Y' 
        scaleCmd = pc.Callback(cuUL.resizeCurves, None, 1,0,1,2.5)
    elif stretchAxis[0] == 'tz': 
        orientAxis = 'zxy' 
        facingAxis = 'Z' 
        scaleCmd = pc.Callback(cuUL.resizeCurves, None, 1,1,0,2.5)
        
    curveJoints = chUL.jointsOnCurve(curve, orientAxis, 'zup', numJoints,(name+side+'spineDef'))    
    ikHandle = pc.ikHandle(name=(chestJoint + '_ikh'), startJoint=curveJoints[0], endEffector=curveJoints[numJoints-1], solver='ikSplineSolver', curve=curve, createCurve=0)
    pc.setAttr((ikHandle[0] + '.visibility'), 0)
    chUL.lockAndHide(ikHandle[0],'lock','trans rot scale vis')
    pc.parent(curveJoints[0], rootJoint)

    pc.parent(ikHandle[0], nonScaleGrp)
    pc.parent(curve, nonScaleGrp)
  
    pc.select(curveJoints[0], r=True)
    startTwistLoc = cuUL.curveControl('locator', 'curve', controlColor)
    startTwistLoc[0] = pc.rename(startTwistLoc[0], name + side + 'startTwist_loc')
    pc.hide(startTwistLoc[0])
    chUL.lockAndHide(startTwistLoc[0], 'locknHide', 'scale vis')
    pc.select(cl=True)
  
    pc.select(curveJoints[numJoints-1], r=True)
    endTwistLoc = cuUL.curveControl('locator', 'curve', controlColor)
    endTwistLoc[0] = pc.rename(endTwistLoc[0], name + side + 'endTwist_loc')
    pc.hide(endTwistLoc[0])
    chUL.lockAndHide(endTwistLoc[0], 'locknHide', 'scale vis')
    pc.select(cl=True)

    pc.setAttr((ikHandle[0] + '.dTwistControlEnable'), 1)
    pc.setAttr((ikHandle[0] + '.dWorldUpType'), 4)

    pc.connectAttr((startTwistLoc[0] + '.worldMatrix[0]'), (ikHandle[0] + '.dWorldUpMatrix'), f=True)
    pc.connectAttr((endTwistLoc[0] + '.worldMatrix[0]'), (ikHandle[0] + '.dWorldUpMatrixEnd'), f=True)

    # now create controls for spine
    # hip control
    pc.select(hipJoint, r=True)
    hipControl = cuUL.curveControl('cube1', 'joint', controlColor)
    scaleCmd()
    hipControl[0] = pc.rename(hipControl[0], name + side + 'hip_ctrl')
    hipGrp = chUL.quickZeroOut(hipControl[0])
    pc.parentConstraint(hipControl[0], hipJoint, mo=True, w=1)
    chUL.lockAndHide(hipControl[0], 'locknHide', 'scale vis')
    pc.select(cl=True)
   
    # chest control
    pc.select(chestJoint, r=True)
    chestControl = cuUL.curveControl('cube1', 'joint', controlColor)
    scaleCmd()
    chestControl[0] = pc.rename(chestControl[0], name + side + 'chest_ctrl')
    chestGrp = chUL.quickZeroOut(chestControl[0])
    pc.parentConstraint(chestControl[0], chestJoint, mo=True, w=1)
    chUL.lockAndHide(chestControl[0], 'locknHide', 'scale vis')
    pc.select(cl=True)

    # root control
    pc.select(rootJoint, r=True)
    tempControl = cuUL.curveControl('circle', 'joint', controlColor)
    cuUL.resizeCurves(None, 1, 1, 1, 3)
    tempControl[0] = pc.rename(tempControl[0], name + side + 'root_ctrl')
    chUL.lockAndHide(tempControl[0], 'locknHide', 'scale vis')
    pc.select(cl=True)

    size = len(list)
    allControls = []
    for i in range(1,size-1):
        allControls.append(tempControl[0])
        pc.select(list[i], r=True)
        tempControl = cuUL.curveControl('square', 'joint', controlColor)
        cuUL.resizeCurves(None, 1, 1, 1, 2)
        tempControl[0] = pc.rename(tempControl[0], name + side + 'spine' + str(i) + '_ctrl')
        pc.parentConstraint(tempControl, list[i], mo=True, w=1)
        pc.select(cl=True)
        pc.parent(tempControl[0], allControls[i-1])
            
    allControls.append(tempControl[0])#add last created control in the array
    pc.select(allControls, r=True)
    controlGrp = chUL.quickZeroOut('')
    pc.select(allControls, r=True)
    chUL.lockAndHide('', 'locknHide', 'trans scale vis')
    chUL.lockAndHide('', 'unLock', 'trans')

    #parenting of controls
    pc.parent(startTwistLoc[0], hipControl[0])
    pc.parent(endTwistLoc[0], chestControl[0])
    pc.parent(chestGrp, allControls[len(allControls)-1])

    #create clusters for curve
    pc.select((curve + '.cv[0]'), r=True)
    posAClts = pc.cluster()
    pc.select((curve + '.cv[1]'), r=True)
    posBClts = pc.cluster()
    pc.select((curve + '.cv[2]'), r=True)
    posCClts = pc.cluster()
    pc.select((curve + '.cv[3]'), r=True)
    posDClts = pc.cluster()
    pc.select((curve + '.cv[4]'), r=True)
    posEClts = pc.cluster()
    pc.hide(posAClts[1], posBClts[1], posCClts[1], posDClts[1], posEClts[1])
    pc.select(posAClts[1], posBClts[1], posCClts[1], posDClts[1], posEClts[1], r=True)
    chUL.lockAndHide('','lock','vis')
    pc.select(cl=True)

    #mid offset control
    pc.select(posCClts[1], r=True)
    midOffsetControl = cuUL.curveControl('plus', 'joint', controlColor)
    cuUL.resizeCurves(None, 1, 0, 1, 2.5)
    midOffsetControl[0] = pc.rename(midOffsetControl[0], name + side + 'midOffset_ctrl')
    midOffsetGrp = chUL.quickZeroOut(midOffsetControl[0])
    chUL.lockAndHide(midOffsetControl[0], 'locknHide', 'rot scale vis')
    pc.select(cl=True)

    #finalise controls
    pc.parent(posAClts[1], posBClts[1], hipControl[0])
    pc.parent(posDClts[1], posEClts[1], chestControl[0])
    pc.parent(posCClts[1], midOffsetControl[0])
    pc.parentConstraint(hipControl[0], chestControl[0], midOffsetGrp[0], mo=True, w=1)
    pc.parentConstraint(posAClts[1], rootJoint, mo=True, w=1)

    if stretch:
        js.stretchySpline(name, side, allControls[0], stretchType, curve, 1, volume, scaleNode)

    pc.parent(hipGrp[0], allControls[0])
    pc.parent(controlGrp[0], partGrp)
    pc.parent(midOffsetGrp[0], partGrp)

    #lock all anim control zeroOut grps
    chUL.lockAndHide(midOffsetGrp[0], 'lock', 'trans rot scale vis')
    chUL.lockAndHide(hipGrp[0], 'lock', 'trans rot scale vis')
    chUL.lockAndHide(chestGrp[0], 'lock', 'trans rot scale vis')

    for c in controlGrp:
        chUL.lockAndHide(c, 'lock', 'trans rot scale vis')

    #add spine rig info for future update...
    charRigInfo = chUL.getcharRigInfoNode(name)
    pc.addAttr(charRigInfo, ln=(side+'spineRig'), dt='string')
    pc.setAttr((charRigInfo + '.' + (side+'spineRig')), (allControls[0]+' '+chestControl[0]+' '+hipControl[0]), type='string')

    #parent skeleton 
    pc.select(cl=True)
    chUL.parentSkeletonTo(rootJoint, cleanGrp[1])

    # chUL.createSkinJointSet
    set = chUL.createSkinJointSet(name)
    curveJoints.append(chestJoint)    
    chUL.addSkinJointToSet(set, curveJoints)    

    #scale controls to global value
    pc.select(hipControl, chestControl, midOffsetControl, allControls, r=True)
    cuUL.resizeCurves(None, 1, 1, 1, scale)
    pc.select(cl=True)