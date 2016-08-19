import pymel.core as pc
from BuildSpaceSwitchSetup import buildSpaceSwitchSetup
from Maya_Rigging.Core.BuildWorld import buildWorld
from ...Utils.CharUtilsLib import curveGuide
from ...Utils.CharUtilsLib import getcharRigInfoNode
from ...Utils.CharUtilsLib import lockAndHide
from ...Utils.CharUtilsLib import quickZeroOut
from ...Utils.CurveUtilLib import curveControl
from ...Utils.CurveUtilLib import fixFacingAxis
from ...Utils.CurveUtilLib import resizeCurves
from ...Utils.Transform import Snap

#eval('source \'buildWorld.mel\'')
#source 'snaps.mel'
#charUtilsLib
#curveUtilitiesLib
#libString

def buildEyeSetup(name,
                  side,
                  leftEye,
                  rightEye,
                  world,
                  scale,
                  colorRight,
                  colorCenter,
                  colorLeft):
    partGrp = pc.group(em=True, n=(name + side + 'eyesParts_grp#'))
    if world:
        cleanGrp = buildWorld(name, scale)
        pc.parent(partGrp, cleanGrp[0])

    #controls creation
    pc.select(leftEye, r=True)
    leftEyeOriControl = curveControl('cone', 'curve', colorLeft)
    leftEyeOriControl[0] = pc.rename(leftEyeOriControl[0], leftEye + '_orient_ctrl')
    pc.setAttr((leftEyeOriControl[0] + '.r'),(0,0,0))
    fixFacingAxis('Z',1)
    resizeCurves(None, 1, 1, 1, 0.9)
    leftEyeOriGrp = quickZeroOut(leftEyeOriControl[0])
    lockAndHide(leftEyeOriControl[0],'locknHide','trans scale vis')
    
    pc.select(rightEye, r=True)
    rightEyeOriControl = curveControl('cone', 'curve', colorRight)
    rightEyeOriControl[0] = pc.rename(rightEyeOriControl[0], rightEye + '_orient_ctrl')
    pc.setAttr((rightEyeOriControl[0] + '.r'),(0,0,0))
    fixFacingAxis('Z',1)
    resizeCurves(None, 1, 1, 1, 0.9)
    rightEyeOriGrp = quickZeroOut(rightEyeOriControl[0])
    lockAndHide(rightEyeOriControl[0],'locknHide','trans scale vis')

    eyeControl = curveControl('cross', 'curve', colorCenter)
    eyeControl[0] = pc.rename(eyeControl[0], name + side + 'eyeMain_ctrl#')
    tempCon = pc.pointConstraint(leftEye, rightEye, eyeControl[0], offset=(0,0,0), weight=1)
    pc.delete(tempCon)
    pc.refresh()
    fixFacingAxis('Z',1)
    resizeCurves(None, 1, 1, 1, 1.1)
    eyeConGrp = quickZeroOut(eyeControl[0])
    lockAndHide(eyeControl[0], 'locknHide', 'rot scale vis')
    
    pc.select(leftEye, r=True)
    leftEyeAimControl = curveControl('circleCross', 'curve', colorLeft)
    leftEyeAimControl[0] = pc.rename(leftEyeAimControl[0], leftEye + '_aim_ctrl')
    pc.setAttr((leftEyeAimControl[0] + '.r'),(0, 0, 0))
    fixFacingAxis('Z',1)
    resizeCurves(None, 1, 1, 1, 0.3)
    leftEyeAimGrp = quickZeroOut(leftEyeAimControl[0])
    lockAndHide(leftEyeAimControl[0], 'locknHide', 'rot scale vis')

    pc.select(rightEye, r=True)
    rightEyeAimControl = curveControl('circleCross', 'curve', colorRight)
    rightEyeAimControl[0] = pc.rename(rightEyeAimControl[0], rightEye + '_aim_ctrl')
    pc.setAttr((rightEyeAimControl[0] + '.r'),(0,0,0))
    fixFacingAxis('Z', 1)
    resizeCurves(None, 1, 1, 1, 0.3)
    rightEyeAimGrp = quickZeroOut(rightEyeAimControl[0])
    lockAndHide(rightEyeAimControl[0], 'locknHide', 'rot scale vis')

    # create space and rig....
    pc.parent(leftEyeAimGrp[0], eyeControl[0])
    pc.parent(rightEyeAimGrp[0], eyeControl[0])
    mainPos = pc.getAttr(eyeConGrp[0] + '.tz')
    pc.setAttr((eyeConGrp[0] + '.tz'), (mainPos + 5))

    # create two locator for up locator
    leftUploc = pc.spaceLocator(n=(leftEye + '_upLoc'))
    rightUploc = pc.spaceLocator(n=(leftEye + '_upLoc'))

    Snap(leftEye, leftUploc)
    Snap(rightEye, rightUploc)
    pc.setAttr((leftUploc + '.r'), (0, 0, 0))
    pc.setAttr((rightUploc + '.r'), (0, 0, 0))
    mainPos = pc.getAttr(leftUploc + '.ty')
    pc.setAttr((leftUploc + '.ty'), (mainPos + 0.5))
    mainPos = pc.getAttr(rightUploc + '.ty')
    pc.setAttr((rightUploc + '.ty'), (mainPos + 0.5))

    pc.hide(leftUploc, rightUploc)
    pc.setAttr((leftUploc + '.v'), lock=True)
    pc.setAttr((rightUploc + '.v'), lock=True)

    pc.aimConstraint(leftEyeAimControl[0], leftEyeOriGrp[0], offset=(0,0,0), weight=1, aimVector=(0,0,1), upVector=(0,1,0), worldUpType='object', worldUpObject=leftUploc)
    pc.aimConstraint(rightEyeAimControl[0], rightEyeOriGrp[0], offset=(0,0,0), weight=1, aimVector=(0,0,1), upVector=(0,1,0), worldUpType='object', worldUpObject=rightUploc)

    pc.parentConstraint(leftEyeOriControl[0], leftEye, mo=True, skipTranslate=['x','y','z'], weight=1)
    pc.parentConstraint(rightEyeOriControl[0], rightEye, mo=True, skipTranslate=['x','y','z'], weight=1)
    curveGuide(leftEyeOriControl[0], leftEyeAimControl[0])
    curveGuide(rightEyeOriControl[0], rightEyeAimControl[0])
    #cleanup

    pc.parent(eyeConGrp[0], partGrp)

    parentJoint = pc.listRelatives(leftEye, parent=True)
    if parentJoint[0] != '':
        oriParentGrp = pc.group(em=True, n=(name + side + 'eyeOri_grp#'))
        Snap(parentJoint[0], oriParentGrp)
        pc.setAttr((oriParentGrp + '.r'), (0,0,0))
        pc.parent(leftEyeOriGrp, oriParentGrp)
        pc.parent(rightEyeOriGrp, oriParentGrp)
        pc.parentConstraint(parentJoint[0], oriParentGrp, mo=True, weight=1)
        pc.parent(leftUploc, parentJoint[0])
        pc.parent(rightUploc, parentJoint[0])
        pc.parent(oriParentGrp, partGrp)
    else:
        pc.parent(leftEyeOriControl[0], partGrp)
        pc.parent(rightEyeOriControl[0], partGrp)

    #create space switch
    charRigInfo = getcharRigInfoNode(name)
    if world:
        if pc.attributeQuery('neckHeadRig', n=charRigInfo, ex=True):
            headRigPart = pc.getAttr(charRigInfo+'.neckHeadRig')
            headRigArray = headRigPart.split(' ')
            buildSpaceSwitchSetup(eyeControl[0], eyeConGrp[0],[headRigArray[0],(name+'worldB_ctrl')], ['head','world'], 1)

    pc.select(eyeControl[0], leftEyeOriControl[0], leftEyeAimControl[0], rightEyeOriControl[0], rightEyeAimControl[0], r=True)
    resizeCurves(None, 1, 1, 1, scale)
    pc.select(cl=True)