import pymel.core as pc

from Maya_Rigging.Utils import AttrUtil as atu
from Maya_Rigging.Core.Setup import BuildArmSetup as bas
from Maya_Rigging.Core.Setup import BuildBipedLegSetup as bbls
from Maya_Rigging.Core.Setup import BuildQuadLegSetup as bqls
from Maya_Rigging.Core.Setup import BuildSpineSetup as bss
from Maya_Rigging.Core.Setup import BuildEyeSetup as bes
from Maya_Rigging.Core.Setup import BuildHandSetup as bhs
from Maya_Rigging.Core.Setup import BuildNeckHeadSetup as bnhs
from Maya_Rigging.Core.Setup import BuildTentacleSetup as bts

from Maya_Rigging.Utils import CharUtilsLib as chUL
from Maya_Rigging.Utils import List
from Maya_Rigging.Utils.String import *


def create_rig(ikfk='',
               stretch='',
               midLock='',
               volume='',
               colorRight=10,
               colorCenter=15,
               colorLeft=26):
    spineRigPart = ''
    spineRigPartArray = []
    neckHeadRigPart = ''
    neckHeadRigPartArray = []
    tentacleRigPart = ''
    tentacleRigPartArray = []

    # global option declaration...

    if ikfk == '':
        ikFkType = pc.optionMenu('rotTypeGlobalOpGrp', q=True, v=True)
    else:
        ikFkType = ikfk
        # print('ikfk:', ikfk)

    if stretch == '' or stretch == 'none':
        stretchType = pc.optionMenu('scaleTypeGlobalOpGrp', q=True, v=True)
        stretch = pc.checkBox('stretchGlobalChk', q=True, v=True)
    else:
        stretchType = stretch
        stretch = True
        # print('stretchType:', stretchType)

    if midLock == '':
        midLock = pc.checkBox('midGlobalChk', q=True, v=True)
    # else:
    #     print('midLock:', midLock)

    if volume == '':
        volume = pc.checkBox('volGlobalChk', q=True, v=True)
    # else:
    #     print('volume:', volume)

    world = 1.0
    scale = 1.0
    dis = 0.0

    if pc.objExists('masterRigPartsHolder_node'):
        moduleList = ''

        if pc.attributeQuery('spineRigParts', n='masterRigPartsHolder_node', ex=True):
            spineModule = pc.getAttr('masterRigPartsHolder_node.spineRigParts')
            moduleList = moduleList + (spineModule + ' ')

        if pc.attributeQuery('neckHeadRigParts', n='masterRigPartsHolder_node', ex=True):
            neckModule = pc.getAttr('masterRigPartsHolder_node.neckHeadRigParts')
            moduleList = moduleList + (neckModule + ' ')

        if pc.attributeQuery('tentacleRigParts', n='masterRigPartsHolder_node', ex=True):
            tentModule = pc.getAttr('masterRigPartsHolder_node.tentacleRigParts')
            moduleList = moduleList + (tentModule + ' ')

        if pc.attributeQuery('armRigParts', n='masterRigPartsHolder_node', ex=True):
            armModule = pc.getAttr('masterRigPartsHolder_node.armRigParts')
            moduleList = moduleList + (armModule + ' ')

        if pc.attributeQuery('legRigParts', n='masterRigPartsHolder_node', ex=True):
            legModule = pc.getAttr('masterRigPartsHolder_node.legRigParts')
            moduleList = moduleList + (legModule + ' ')

        # TODO: can probably refactor this to remove the need for List to seperate the elements
        moduleInf = List.seperate(moduleList)

        # error checking........
        if pc.attributeQuery('spineRigParts', n='masterRigPartsHolder_node', ex=True):
            spineRigPart = pc.getAttr('masterRigPartsHolder_node.spineRigParts')
            spineRigPartArray = List.seperate(spineRigPart)
            for i in range(len(spineRigPartArray)):
                if not pc.attributeQuery('joints', n=spineRigPartArray[i], ex=True):
                    pc.error('You must specify number of joints on ' + spineRigPartArray[i] + ' for SPINE setup')

        if pc.attributeQuery('neckHeadRigParts', n='masterRigPartsHolder_node', ex=True):
            neckHeadRigPart = pc.getAttr('masterRigPartsHolder_node.neckHeadRigParts')
            neckHeadRigPartArray = List.seperate(neckHeadRigPart)
            for i in range(len(neckHeadRigPartArray)):
                if not pc.attributeQuery('joints', n=neckHeadRigPartArray[i], ex=True):
                    pc.error('You must specify number of joints on ' + neckHeadRigPartArray[i] + ' for NECK setup')

        if pc.attributeQuery('tentacleRigParts', n='masterRigPartsHolder_node', ex=True):
            tentacleRigPart = pc.getAttr('masterRigPartsHolder_node.tentacleRigParts')
            tentacleRigPartArray = List.seperate(tentacleRigPart)
            for i in range(len(tentacleRigPartArray)):
                if not pc.attributeQuery('joints', n=tentacleRigPartArray[i], ex=True):
                    pc.error('You must specify number of joints on ' + tentacleRigPartArray[i] + ' for TENTACLE setup')

        pc.progressWindow(t='Building Anim Rig', progress=0, status='building animation rig from skeleton :', min=0,
                          max=len(moduleInf), isInterruptable=True)
        pc.select(cl=True)
        pc.symmetricModelling(e=True, symmetry=False)
        pc.softSelect(e=True, softSelectEnabled=False)
        pc.setToolTo('nurbsSelect')

        if pc.attributeQuery('spineRigParts', n='masterRigPartsHolder_node', ex=True):
            for i in range(len(spineRigPartArray)):
                name = pc.getAttr(spineRigPartArray[i] + '.name')
                side = pc.getAttr(spineRigPartArray[i] + '.sides')
                controlColor = get_control_color(side, colorRight, colorCenter, colorLeft)
                spineRigCmdPart = pc.getAttr(spineRigPartArray[i] + '.spineRig')
                spineRigCmdArray = List.seperate(spineRigCmdPart)

                dis = chUL.getChainLength(spineRigCmdArray[0], spineRigCmdArray[1])
                scale = dis / 3
                dis = 0

                pc.catch(pc.deleteAttr(spineRigPartArray[i], attribute='name'))
                pc.catch(pc.deleteAttr(spineRigPartArray[i], attribute='sides'))
                pc.catch(pc.deleteAttr(spineRigPartArray[i], attribute='spineRig'))

                numJoints = pc.getAttr(spineRigPartArray[i] + '.joints')

                pc.select(spineRigPartArray[i], r=True)
                atu.removeTwistJointsAttr('joints')
                pc.select(cl=True)

                bss.buildSpineSetup(name,
                                    side,
                                    spineRigCmdArray[0],
                                    spineRigCmdArray[1],
                                    spineRigCmdArray[2],
                                    stretchType,
                                    numJoints,
                                    stretch,
                                    volume,
                                    world,
                                    scale,
                                    controlColor,
                                    # TODO: need to refactor to create world controls without having to pass in color
                                    colorCenter)
                if pc.progressWindow(q=True, isCancelled=True):
                    pc.progressWindow(endProgress=True)
                    pc.undoInfo(state=True)
                    return
                pc.progressWindow(e=True, step=1, status=('building anim rig on : ' + spineRigPartArray[i]))

        if pc.attributeQuery('neckHeadRigParts', n='masterRigPartsHolder_node', ex=True):
            for i in range(len(neckHeadRigPartArray)):
                name = pc.getAttr(neckHeadRigPartArray[i] + '.name')
                side = pc.getAttr(neckHeadRigPartArray[i] + '.sides')
                controlColor = get_control_color(side, colorRight, colorCenter, colorLeft)
                neckHeadRigCmdPart = pc.getAttr(neckHeadRigPartArray[i] + '.neckHeadRig')
                neckHeadRigCmdArray = List.seperate(neckHeadRigCmdPart)

                eyeRigCmdPart = pc.getAttr(neckHeadRigPartArray[i] + '.eyeRig')
                eyeRigCmdArray = List.seperate(eyeRigCmdPart)

                pc.catch(pc.deleteAttr(neckHeadRigPartArray[i], attribute='name'))
                pc.catch(pc.deleteAttr(neckHeadRigPartArray[i], attribute='sides'))
                pc.catch(pc.deleteAttr(neckHeadRigPartArray[i], attribute='neckHeadRig'))
                pc.catch(pc.deleteAttr(neckHeadRigPartArray[i], attribute='eyeRig'))

                numJoints = pc.getAttr(neckHeadRigPartArray[i] + '.joints')
                pc.select(neckHeadRigPartArray[i], r=True)
                atu.removeTwistJointsAttr('joints')
                pc.select(cl=True)

                list = chUL.findJointArray(neckHeadRigCmdArray[0], neckHeadRigCmdArray[1])
                dis = chUL.getChainLength(neckHeadRigCmdArray[0], neckHeadRigCmdArray[1])
                if len(list) > 2:
                    scale = dis / 2
                else:
                    scale = dis
                dis = 0

                bnhs.buildNeckHeadSetup(name,
                                        side,
                                        neckHeadRigCmdArray[0],
                                        neckHeadRigCmdArray[1],
                                        stretchType,
                                        stretch,
                                        numJoints,
                                        volume,
                                        world,
                                        scale,
                                        controlColor)
                bes.buildEyeSetup(name,
                                  side,
                                  eyeRigCmdArray[0],
                                  eyeRigCmdArray[1],
                                  world,
                                  scale,
                                  colorRight,
                                  colorCenter,
                                  colorLeft)
                if pc.progressWindow(q=True, isCancelled=True):
                    pc.progressWindow(endProgress=True)
                    pc.undoInfo(state=True)
                    return
                pc.progressWindow(e=True, step=1, status=('building anim rig on : ' + neckHeadRigPartArray[i]))

        if pc.attributeQuery('tentacleRigParts', n='masterRigPartsHolder_node', ex=True):

            # TODO: update new UI to support dynamic and offset checkbox
            # dynamic = pc.checkBox('dynamicGlobalChk', q=True, v=True)
            # offset = pc.checkBox('offsetGlobalChk', q=True, v=True)

            dynamic = False
            offset = False

            for i in range(len(tentacleRigPartArray)):
                name = pc.getAttr(tentacleRigPartArray[i] + '.name')
                side = pc.getAttr(tentacleRigPartArray[i] + '.sides')
                controlColor = get_control_color(side, colorRight, colorCenter, colorLeft)
                type = pc.getAttr(tentacleRigPartArray[i] + '.types')
                tentacleRigCmdPart = pc.getAttr(tentacleRigPartArray[i] + '.tentacleRig')
                tentacleRigCmdArray = List.seperate(tentacleRigCmdPart)

                pc.catch(pc.deleteAttr(tentacleRigPartArray[i], attribute='name'))
                pc.catch(pc.deleteAttr(tentacleRigPartArray[i], attribute='sides'))
                pc.catch(pc.deleteAttr(tentacleRigPartArray[i], attribute='types'))
                pc.catch(pc.deleteAttr(tentacleRigPartArray[i], attribute='tentacleRig'))

                numJoints = pc.getAttr(tentacleRigPartArray[i] + '.joints')
                pc.select(tentacleRigPartArray[i], r=True)
                atu.removeTwistJointsAttr('joints')
                pc.select(cl=True)

                dis = chUL.getChainLength(tentacleRigCmdArray[0], tentacleRigCmdArray[1])
                scale = dis / 9
                dis = 0

                bts.buildTentacleSetup(name,
                                       tentacleRigCmdArray[0],
                                       tentacleRigCmdArray[1],
                                       'square',
                                       offset,
                                       'plus',
                                       dynamic,
                                       (side + type),
                                       stretchType,
                                       stretch,
                                       numJoints,
                                       volume,
                                       world,
                                       scale,
                                       controlColor)
                if pc.progressWindow(q=True, isCancelled=True):
                    pc.progressWindow(endProgress=True)
                    pc.undoInfo(state=True)
                    return
                pc.progressWindow(e=True, step=1, status=('building anim rig on : ' + tentacleRigPartArray[i]))

        if pc.attributeQuery('armRigParts', n='masterRigPartsHolder_node', ex=True):
            armRigPart = pc.getAttr('masterRigPartsHolder_node.armRigParts')
            armRigPartArray = List.seperate(armRigPart)
            for i in range(len(armRigPartArray)):
                name = pc.getAttr(armRigPartArray[i] + '.name')
                side = pc.getAttr(armRigPartArray[i] + '.sides')
                controlColor = get_control_color(side, colorRight, colorCenter, colorLeft)

                armRigCmdPart = pc.getAttr(armRigPartArray[i] + '.armRig')
                armRigCmdArray = List.seperate(armRigCmdPart)

                fingerName = []
                startJoint = []
                fingers = ''
                numFingers = ''
                fingerRotAxis = []
                fingerCheck = 0

                if pc.attributeQuery('fingers', n=armRigPartArray[i], ex=True):
                    fingerName = ['thumb', 'index', 'mid', 'ring', 'pinky']
                    fingers = pc.getAttr(armRigPartArray[i] + '.fingers')
                    startJoint = List.seperate(fingers)

                    numFingers = len(startJoint)
                    fingerRotAxis = chUL.getFingerAxisFigures(startJoint[0])
                    fingerCheck = 1

                pc.catch(pc.deleteAttr(armRigPartArray[i], attribute='name'))
                pc.catch(pc.deleteAttr(armRigPartArray[i], attribute='sides'))
                pc.catch(pc.deleteAttr(armRigPartArray[i], attribute='armRig'))
                pc.catch(pc.deleteAttr(armRigPartArray[i], attribute='fingers'))

                dis = chUL.getChainLength(armRigCmdArray[0], armRigCmdArray[1])
                scale = dis / 7
                dis = 0

                bas.buildArmSetup(name,
                                  side,
                                  armRigCmdArray[0],
                                  armRigCmdArray[1],
                                  stretchType,
                                  ikFkType,
                                  stretch,
                                  midLock,
                                  volume,
                                  world,
                                  scale,
                                  controlColor)
                if fingerCheck:
                    bhs.buildHandSetup(name,
                                       side,
                                       (name + side + 'armSwitches_ctrl'),
                                       1,
                                       'square',
                                       numFingers,
                                       fingerName,
                                       startJoint,
                                       fingerRotAxis,
                                       2,
                                       1,
                                       'parent',
                                       world,
                                       scale,
                                       controlColor)
                if pc.progressWindow(q=True, isCancelled=True):
                    pc.progressWindow(endProgress=True)
                    pc.undoInfo(state=True)
                    return
                pc.progressWindow(e=True, step=1, status=('building anim rig on : ' + armRigPartArray[i]))

        if pc.attributeQuery('legRigParts', n='masterRigPartsHolder_node', ex=True):
            legRigPart = pc.getAttr('masterRigPartsHolder_node.legRigParts')
            legRigPartArray = List.seperate(legRigPart)
            for i in range(len(legRigPartArray)):
                fingerName = []
                startJoint = []
                quadFinger = []
                newFinger = ''
                fingers = ''
                fingerCmd = ''
                numFingers = 0
                fingerRotAxis = []
                fingerCheck = 0
                tempFinger = ''

                name = pc.getAttr(legRigPartArray[i] + '.name')
                side = pc.getAttr(legRigPartArray[i] + '.sides')
                controlColor = get_control_color(side, colorRight, colorCenter, colorLeft)
                legType = pc.getAttr(legRigPartArray[i] + '.legType')

                if pc.attributeQuery('fingers', n=legRigPartArray[i], ex=True):
                    fingerCmd = pc.getAttr(legRigPartArray[i] + '.fingers')
                    fingerCheck = 1

                legRigCmdPart = pc.getAttr(legRigPartArray[i] + '.legRig')
                legRigCmdArray = List.seperate(legRigCmdPart)

                # NOTE: these were catch quite
                pc.catch(pc.deleteAttr(legRigPartArray[i], attribute='name'))
                pc.catch(pc.deleteAttr(legRigPartArray[i], attribute='sides'))
                pc.catch(pc.deleteAttr(legRigPartArray[i], attribute='legRig'))
                pc.catch(pc.deleteAttr(legRigPartArray[i], attribute='fingers'))
                pc.catch(pc.deleteAttr(legRigPartArray[i], attribute='legType'))

                dis = chUL.getChainLength(legRigCmdArray[0], legRigCmdArray[1])
                scale = dis / 7
                dis = 0

                if legType == 'bipedLeg':
                    bbls.buildBipedLegSetup(name,
                                            side,
                                            legRigCmdArray[0],
                                            legRigCmdArray[1],
                                            legRigCmdArray[2],
                                            stretchType,
                                            ikFkType,
                                            stretch,
                                            midLock,
                                            volume,
                                            world,
                                            scale,
                                            controlColor)
                elif legType == 'quadLeg':
                    bqls.buildQuadLegSetup(name,
                                           side,
                                           legRigCmdArray[0],
                                           legRigCmdArray[1],
                                           legRigCmdArray[2],
                                           legRigCmdArray[3],
                                           stretchType,
                                           ikFkType,
                                           stretch,
                                           midLock,
                                           volume,
                                           world,
                                           scale,
                                           controlColor)

                if fingerCheck:
                    if legType == 'bipedLeg':
                        fingerName = ['thumb', 'index', 'mid', 'ring', 'pinky']
                        fingers = fingerCmd
                        startJoint = List.seperate(fingers)

                        numFingers = len(startJoint)
                        fingerRotAxis = chUL.getFingerAxisFigures(startJoint[0])
                    elif legType == 'quadLeg':
                        fingerName = ['thumb', 'index', 'mid', 'ring', 'pinky']
                        fingers = fingerCmd
                        quadFinger = List.seperate(fingers)
                        for x in range(len(quadFinger)):
                            tempFinger = buildQuadFingerIkSetup(quadFinger[x],
                                                                legRigCmdArray[(len(legRigCmdArray) - 1)])
                            newFinger = newFinger + ' ' + tempFinger

                        startJoint = List.seperate(newFinger)

                        numFingers = len(startJoint)
                        fingerRotAxis = chUL.getFingerAxisFigures(startJoint[0])

                    bhs.buildHandSetup(name,
                                       side,
                                       (name + side + 'legSwitches_ctrl'),
                                       1,
                                       'square',
                                       numFingers,
                                       fingerName,
                                       startJoint,
                                       fingerRotAxis,
                                       2,
                                       1,
                                       'parent',
                                       world,
                                       scale,
                                       controlColor)
                if pc.progressWindow(q=True, isCancelled=True):
                    pc.progressWindow(endProgress=True)
                    pc.undoInfo(state=True)
                    return
                pc.progressWindow(e=True, step=1, status=('building anim rig on : ' + legRigPartArray[i]))

        pc.delete('masterRigPartsHolder_node')
        pc.progressWindow(endProgress=True)
        pc.select(cl=True)
        print('Operation successful: Animation rig created.\n')


def buildQuadFingerIkSetup(joint, parent):
    list = chUL.listHierarchy(joint)
    IK = chUL.dupId(joint, 'suffix', 'ik')
    pc.parent(IK[0], parent)

    for i in range(len(list) - 1):
        strip = objGetPrefix(list[i])
        ikhName = (strip + '_ikh')
        ikHandleA = pc.ikHandle(name=(ikhName), startJoint=list[i], endEffector=list[i + 1], solver='ikSCsolver')
        pc.hide(ikHandleA[0])
        pc.parent(ikHandleA[0], IK[i])
        chUL.lockAndHide(ikHandleA[0], 'lock', 'trans rot vis')
        pc.select(cl=True)

    return IK[0]


def get_control_color(side, colorRight, colorCenter, colorLeft):
    controlColor = colorCenter
    if "l" in str(side).lower():
        controlColor = colorLeft
    if "r" in str(side).lower():
        controlColor = colorRight
    return controlColor
