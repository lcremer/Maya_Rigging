import pymel.core as pc
from ..Utils.String import objGetPrefix
from ..Utils.CurveUtilLib import curveControl
from ..Utils.String import strSearchReplace
from ..Utils import AttrUtil as aU
from ..Utils import List as List
import BuildModuleJointSkeleton as bModSkel


def buildTentacleSkeleton():
    jointsList = []
    jointNameList = []
    strip = ''
    grp = ''
    sel = pc.ls(sl=True)
    if pc.attributeQuery('jointPosList', n=sel[0], ex=True):
        l = pc.getAttr(sel[0] + '.jointPosList')
        jointsList = List.seperate(l)
        for i in len(jointsList):
            strip = objGetPrefix(jointsList[i])            
            jointNameList[i] = (strip + '_jnt')

        createJointHierarchy(jointsList,jointNameList,grp)
        pc.delete(sel[0])
    else:
        pc.error('selected object is not installed for current operation')


def createJointHierarchy(targetPos, names, grp):
    # will create joint chain based on location of objects in targetPos,
    # rename them the names in aNames, and place the result in the existing group grp
    # returns new pathNames
    joints = []
    if len(targetPos) == len(names):
        xForm = []
        jnt = ''
        for i in range(len(targetPos)):
            if targetPos[i]:
                pc.select(cl=True)
                xForm = pc.xform(targetPos[i], q=True, ws=True, rp=True)
                jnt = pc.joint(p=(xForm[0],xForm[1],xForm[2]), n=names[i])
                if i == 0:
                    if grp != '' and pc.objExists(grp):                        
                        jnt = pc.parent(jnt, grp)
                    elif pc.listRelatives(jnt, p=True) != '':
                        jnt = pc.parent(jnt, w=True)
                else:
                    jnt = pc.parent(jnt, joints[i-1])
                joints.append(jnt[0])
                pc.select(cl=True)
    pc.select(cl=True)
    return joints


def buildTwistJoints(sel=''):
    if sel == '':
        sel = pc.ls(sl=True)
    twistJoints = {}
    if pc.attributeQuery('jointPosList', n=sel[0], ex=True):
        l = pc.getAttr(sel[0] + '.jointPosList')
        jointsList = List.seperate(l)
        for j in jointsList:
            strip = objGetPrefix(j)
            if pc.attributeQuery('twistJoints', n=j, ex=True):
                twistJointCount = pc.getAttr(j + '.twistJoints')
                twistJoints.update({(strip+'_jnt'): twistJointCount})
    else:
        pc.error('selected object is not installed for current operation')
    for t in twistJoints:
        aU.addTwistJointAttr('twistJoints', twistJoints[t], t)


def buildSplineJoints(sel=''):
    if sel == '':
        sel = pc.ls(sl=True)
    twistJoints = {}
    if pc.attributeQuery('jointPosList', n=sel[0], ex=True):
        l = pc.getAttr(sel[0] + '.jointPosList')
        jointsList = List.seperate(l)
        for j in jointsList:
            strip = objGetPrefix(j)
            if pc.attributeQuery('twistJoints', n=j, ex=True):
                twistJointCount = pc.getAttr(j + '.twistJoints')
                twistJoints.update({(strip + '_jnt'): twistJointCount})
    else:
        pc.error('selected object is not installed for current operation')
    for t in twistJoints:
        aU.addSplineJointAttrs('twistJoints', twistJoints[t], t)


def buildJointSkeleton(grp):
    jointsList = []
    jointNameList = []
    strip = ''
    jointHierarchy = []
    sel = pc.ls(sl=True)
    if pc.attributeQuery('jointPosList', n=sel[0], ex=True):
        l = pc.getAttr(sel[0] + '.jointPosList')
        jointsList = List.seperate(l)
        for j in jointsList:
            strip = objGetPrefix(j)
            jointNameList.append(strip + '_jnt')
        jointHierarchy = createJointHierarchy(jointsList, jointNameList, grp)
    else:
        pc.error('selected object is not installed for current operation')
    return jointHierarchy


def makeRotAlignJointSetup(joint, rotValue):
    pc.select(joint, r=True)
    tempLoc = curveControl('loc','curve')
    pc.setAttr((tempLoc[0]+'.r'), (0,0,0))    
    con = pc.parentConstraint(tempLoc[0], joint, mo=True, skipTranslate=['x', 'y', 'z'], weight=1)
    pc.setAttr((tempLoc[0]+'.r'), ((rotValue.x), (rotValue.y), (rotValue.z)))
    pc.delete(con,tempLoc[0])
    pc.makeIdentity(joint, apply=True, t=0, r=1, s=0)


# orientJoints `ls -sl` xyz zup
def orientJoints(joints, orientAxis, sao):
    # orients joints.  orient is value of joint -orientJoint ('xyz') and sao is value of joint -sao ('zdown')	
    jnt =  ''
    relatives = []
    for jnt in joints:
        # checking for child joint so if there is no child joint zero out joint orient..
        relatives = pc.listRelatives(jnt, c=True, type='joint')
        if len(relatives) > 0:
            pc.xform(jnt, ro=(0,0,0))
            pc.joint(jnt, e=True, orientJoint=orientAxis, sao=sao, zso=True)
        else:
            pc.setAttr((jnt+'.jointOrient'),(0,0,0))


def stripSuffixToJnt(obj, attr):
    list = pc.getAttr(obj+'.'+attr)
    strip = objGetPrefix(list)
    newList = (strip + '_jnt')
    return newList


def createMasterRigPartsHolder():
    masterRigPartsHolder = 'masterRigPartsHolder_node'

    if not pc.objExists(masterRigPartsHolder):
        masterRigPartsHolder = pc.createNode('unknown')
        masterRigPartsHolder = pc.rename(masterRigPartsHolder,'masterRigPartsHolder_node')

    return masterRigPartsHolder


def buildLegJointSkeleton(parent):
    hipJointHierarchy = [] 
    fingerJointHierarchy = []
    fingerRot = []
    tempFinger = [0, 0, 0]

    sel = pc.ls(sl=True)
    s = sel

    if not pc.attributeQuery('symmetry', n=sel[0], ex=True):

        footPlacer = pc.getAttr(sel[0]+'.footPlacer')
        ankleloc = pc.getAttr(footPlacer+'.jointPosList')
        strip = objGetPrefix(ankleloc)
        ankleJoint = (strip + '_jnt')

        hipRot = pc.getAttr(sel[0]+'.r')
        pc.setAttr((sel[0]+'.rx'), 0)
        pc.setAttr((sel[0]+'.ry'), 0)

        ankleRot = pc.getAttr(footPlacer+'.r')
        pc.setAttr((footPlacer+'.rx'), 0)
        pc.setAttr((footPlacer+'.ry'), 0)

        hipJointHierarchy = buildJointSkeleton(parent)

        # orienting leg joints
        orientJoints(hipJointHierarchy, 'xyz', 'zdown')

        if pc.attributeQuery('child', n=sel[0], ex=True):
            fingerList = pc.getAttr(sel[0] + '.child')
            fingerJointsLists = List.seperate(fingerList)
            for f in fingerJointsLists:
                if f:
                    pc.select(f, r=True)
                    tempFinger = pc.getAttr(f+'.r')
                    pc.setAttr((f+'.r'), (0, 0, 0))
                    parentGrps = pc.getAttr(f+'.parent')
                    strip = objGetPrefix(parentGrps)
                    parent = (strip + '_jnt')
                    fingerJointHierarchy = buildJointSkeleton(parent)
                    # orienting leg  finger joints
                    orientJoints(fingerJointHierarchy, 'xyz', 'zdown')
                    makeRotAlignJointSetup (fingerJointHierarchy[0], tempFinger)

        makeRotAlignJointSetup(ankleJoint, ankleRot)
        makeRotAlignJointSetup(hipJointHierarchy[0], hipRot)

        # collecting info to create leg rig CMD
        name = pc.getAttr(sel[0]+'.name')
        side = pc.getAttr(sel[0]+'.side')
        module = pc.getAttr(sel[0]+'.moduleTag')
        hipJoint = stripSuffixToJnt(sel[0], (side+'hipJoint'))
        ankleJoint = stripSuffixToJnt(sel[0], (side+'ankleJoint'))
        ballJoint = stripSuffixToJnt(sel[0], (side+'ballJoint'))

        pc.addAttr(hipJointHierarchy[0], ln='name', dt='string')
        pc.setAttr((hipJointHierarchy[0] + '.name'), name, type='string')
        pc.addAttr(hipJointHierarchy[0], ln='sides', dt='string')
        pc.setAttr((hipJointHierarchy[0] + '.sides'), side, type='string')
        pc.addAttr(hipJointHierarchy[0], ln='legType', dt='string')
        pc.setAttr((hipJointHierarchy[0] + '.legType'), module, type='string')
        pc.addAttr(hipJointHierarchy[0], ln='legRig', dt='string')

        if pc.getAttr(sel[0]+'.moduleTag') == 'quadLeg':
            hockJoint = stripSuffixToJnt(sel[0], (side+'hockJoint'))
            pc.setAttr((hipJointHierarchy[0] + '.legRig'), (hipJoint+' '+hockJoint+' '+ankleJoint+' '+ballJoint), type='string')
        else:
            pc.setAttr((hipJointHierarchy[0] + '.legRig'), (hipJoint+' '+ankleJoint+' '+ballJoint), type='string')

        if pc.attributeQuery('child', n=sel[0], ex=True):
            finger = ''
            fingerList = []
            strip = ''
            newList = ''
            child = pc.getAttr(sel[0]+'.child')
            childList = List.seperate(child)
            for i in range(len(childList)):
                if(childList[i]):
                    fingerList = pc.getAttr(childList[i]+'.jointPosList')
                    fingerList = List.seperate(fingerList)
                    strip = objGetPrefix(fingerList[0])
                    newList = (strip + '_jnt')
                    finger += (' '+newList)
                
            pc.addAttr(hipJointHierarchy[0], ln='fingers', dt='string')
            pc.setAttr((hipJointHierarchy[0] + '.fingers'), finger, type='string')

        node = createMasterRigPartsHolder()
        if not pc.attributeQuery('legRigParts', n=node, ex=True):
            pc.addAttr(node, ln='legRigParts', dt='string')

        rigParts = pc.getAttr(node + '.legRigParts')
        pc.setAttr((node + '.legRigParts'), (str(rigParts or '')+' '+hipJointHierarchy[0]), type='string')

        if pc.attributeQuery('doSymmetry', n=sel[0], ex=True):
            doSymm = pc.getAttr(sel[0]+'.doSymmetry')
            symmSide = pc.getAttr(doSymm+'.side')
            mirrorSide = pc.getAttr(sel[0]+'.side')
            mirrorJoints = pc.mirrorJoint(hipJointHierarchy[0], mirrorYZ=True, mirrorBehavior=True, searchReplace=[mirrorSide,symmSide])
            rigAttr = pc.getAttr(mirrorJoints[0]+'.legRig')
            rigAttr = rigAttr.replace(mirrorSide, symmSide)
            pc.setAttr((mirrorJoints[0] + '.legRig'), rigAttr, type='string')
            pc.setAttr((mirrorJoints[0] + '.sides'), symmSide, type='string')

            if pc.attributeQuery('child', n=sel[0], ex=True):
                fingerRigAttr = pc.getAttr(mirrorJoints[0]+'.fingers')
                fingerRigAttr = fingerRigAttr.replace(mirrorSide, symmSide)
                pc.setAttr((mirrorJoints[0] + '.fingers'), fingerRigAttr, type='string')

            rigParts = pc.getAttr(node + '.legRigParts')
            pc.setAttr((node + '.legRigParts'), (str(rigParts or '')+' '+mirrorJoints[0]), type='string')

    buildTwistJoints(s)
    pc.delete(sel[0])


# buildArmJointSkeleton ''
def buildArmJointSkeleton(parent):
    armJointList = ''
    armJointListArray = []
    shoulderJointHierarchy = [] 
    fingerJointHierarchy = []
    fingerRot = []
    tempFinger = [0,0,0]
    twistJoints = 0

    sel = pc.ls(sl=True)
    s = sel

    armJointList = pc.getAttr(sel[0] + '.jointPosList')
    armJointListArray = List.seperate(armJointList)

    if not pc.attributeQuery('symmetry', n=sel[0], ex=True):
        wristPlacer = pc.getAttr(sel[0]+'.wristPlacer')
        wristloc = pc.getAttr(wristPlacer+'.jointPosList')
        strip = objGetPrefix(wristloc)
        wristJoint = (strip + '_jnt')

        shoulderRot = pc.getAttr(sel[0]+'.r')
        pc.setAttr((sel[0]+'.r'), (0,0,0))

        wristRot = pc.getAttr(wristPlacer+'.r')
        pc.setAttr((wristPlacer+'.r'), (0,0,0))

        shoulderJointHierarchy = buildJointSkeleton(parent)
        # orienting arm joints
        orientJoints(shoulderJointHierarchy, 'xyz', 'ydown')

        if pc.attributeQuery('child', n=sel[0], ex=True):
            fingerList = pc.getAttr(sel[0] + '.child')
            fingerJointsLists = List.seperate(fingerList)
            for f in fingerJointsLists:
                if(f):
                    pc.select(f, r=True)
                    tempFinger = pc.getAttr(f+'.r')
                    pc.setAttr((f+'.r'), (0,0,0))
                    parentGrp = pc.getAttr(f+'.parent')
                    strip = objGetPrefix(parentGrp)
                    parent = (strip + '_jnt')
                    fingerJointHierarchy = buildJointSkeleton(parent)
                    # orienting finger joints
                    orientJoints(fingerJointHierarchy, 'xyz', 'ydown')
                    # making joint rotion align to module controllers
                    makeRotAlignJointSetup(fingerJointHierarchy[0], tempFinger)

        makeRotAlignJointSetup(wristJoint, wristRot)
        makeRotAlignJointSetup(shoulderJointHierarchy[1], shoulderRot)

        # collecting info to create arm rig CMD
        name = pc.getAttr(sel[0]+'.name')
        side = pc.getAttr(sel[0]+'.side')
        shoulderJoint = stripSuffixToJnt(sel[0],(side+'shoulderJoint'))
        wristJoint = stripSuffixToJnt(sel[0],(side+'wristJoint'))

        pc.addAttr(shoulderJointHierarchy[0], ln='name', dt='string')
        pc.setAttr((shoulderJointHierarchy[0] + '.name'), name, type='string')
        pc.addAttr(shoulderJointHierarchy[0], ln='sides', dt='string')
        pc.setAttr((shoulderJointHierarchy[0] + '.sides'), side, type='string')

        pc.addAttr(shoulderJointHierarchy[0], ln='armRig', dt='string')
        pc.setAttr((shoulderJointHierarchy[0] + '.armRig'), (shoulderJoint+' '+wristJoint), type='string')

        if pc.attributeQuery('child', n=sel[0], ex=True):
            finger = ''
            fingerList = []
            strip = ''
            newList = ''
            child = pc.getAttr(sel[0]+'.child')
            childList = List.seperate(child)

            for c in childList:
                if(c):
                    fingerList = pc.getAttr(c+'.jointPosList')
                    fingerList = List.seperate(fingerList)
                    strip = objGetPrefix(fingerList[0])
                    newList = (strip + '_jnt')
                    finger = finger + (' '+newList)
                
            pc.addAttr(shoulderJointHierarchy[0], ln='fingers', dt='string')
            pc.setAttr((shoulderJointHierarchy[0] + '.fingers'), finger, type='string')

        node = createMasterRigPartsHolder()
        if not pc.attributeQuery('armRigParts', n=node, ex=True):
            pc.addAttr(node, ln='armRigParts', dt='string')

        rigParts = pc.getAttr(node + '.armRigParts')
        pc.setAttr((node + '.armRigParts'), (str(rigParts or '')+' '+shoulderJointHierarchy[0]), type='string')

        if pc.attributeQuery('doSymmetry', n=sel[0], ex=True):
            doSymm = pc.getAttr(sel[0]+'.doSymmetry')
            symmSide = pc.getAttr(doSymm+'.side')
            mirrorSide = pc.getAttr(sel[0]+'.side')
            mirrorJoints = pc.mirrorJoint(shoulderJointHierarchy[0], mirrorYZ=True, mirrorBehavior=True, searchReplace=[mirrorSide,symmSide])
            rigAttr = pc.getAttr(mirrorJoints[0]+'.armRig')
            rigAttr = rigAttr.replace(mirrorSide, symmSide)
            pc.setAttr((mirrorJoints[0] + '.armRig'), rigAttr, type='string')
            pc.setAttr((mirrorJoints[0] + '.sides'), symmSide, type='string')
            
            if pc.attributeQuery('child', n=sel[0], ex=True):
                fingerRigAttr = pc.getAttr(mirrorJoints[0]+'.fingers')                
                fingerRigAttr = fingerRigAttr.replace(mirrorSide, symmSide)
                pc.setAttr((mirrorJoints[0] + '.fingers'), fingerRigAttr, type='string')
                
            rigParts = pc.getAttr(node + '.armRigParts')
            pc.setAttr((node + '.armRigParts'), (str(rigParts or '')+' '+mirrorJoints[0]), type='string')

    buildTwistJoints(s)
    pc.delete(armJointListArray[0])
    pc.delete(sel[0])


def createChildAttrJointHierarchy(joint):
    # this proc find child attr on main placer ctrl and create joint heirarchy..
 
    jointHierarchy = []
    if pc.attributeQuery('child', n=joint, ex=True):
        fingerList = pc.getAttr(joint + '.child')
        fingerJointsLists = List.seperate(fingerList)

        for f in fingerJointsLists:
            pc.select(f, r=True)
            parentGrp = pc.getAttr(f+'.parent')
            strip = objGetPrefix(parentGrp)
            parent = (strip + '_jnt')
            jointHierarchy = buildJointSkeleton(parent)
    else:
        pc.error('Given object is not installed for current operation')
    return jointHierarchy


def buildSpineJointSkeleton(parent):
    sel = pc.ls(sl=True)
    s = sel
    spineJoints = []
    hipJoint = []
    rigParts = ''
    node = ''

    if len(sel)>0:
        if not pc.attributeQuery('symmetry', n=sel[0], ex=True):
            spineRot = pc.getAttr(sel[0]+'.r')            
            pc.setAttr((sel[0]+'.r'), (0, 0, 0))

            # creating spine joints
            spineJoints = buildJointSkeleton(parent)
            
            # creating hip joint
            hipJoint = createChildAttrJointHierarchy (sel[0])

            # orienting spine joints
            orientJoints(spineJoints, 'xyz', 'zup')
            orientJoints(hipJoint, 'xyz', 'zup')
            
            makeRotAlignJointSetup(spineJoints[0], spineRot)

            # collecting info to create spine rig CMD
            name = pc.getAttr(sel[0]+'.name')
            side = pc.getAttr(sel[0]+'.side')
            rootJoint = stripSuffixToJnt(sel[0], (side+'rootJoint'))
            chestJoint = stripSuffixToJnt(sel[0], (side+'chestJoint'))
            hipJoint = stripSuffixToJnt(sel[0], (side+'hipJoint'))
            
            pc.addAttr(spineJoints[0], ln='name', dt='string')
            pc.setAttr((spineJoints[0] + '.name'), name, type='string')
            pc.addAttr(spineJoints[0], ln='sides', dt='string')
            pc.setAttr((spineJoints[0] + '.sides'), side, type='string')
            pc.addAttr(spineJoints[0], ln='spineRig', dt='string')
            pc.setAttr((spineJoints[0] + '.spineRig'), (rootJoint+' '+chestJoint+' '+hipJoint), type='string')
            
            node = createMasterRigPartsHolder()
            if not pc.attributeQuery('spineRigParts',n=node,ex=True):
                pc.addAttr(node, ln='spineRigParts', dt='string')
                
            rigParts = pc.getAttr(node + '.spineRigParts')            
            pc.setAttr((node + '.spineRigParts'), (str(rigParts or '')+' '+spineJoints[0]), type='string')
        if pc.attributeQuery('doSymmetry',n=sel[0],ex=True):
            doSymm = pc.getAttr(sel[0]+'.doSymmetry')
            symmSide = pc.getAttr(doSymm+'.side')
            mirrorSide = pc.getAttr(sel[0]+'.side')
            mirrorJoints = pc.mirrorJoint(spineJoints[0], mirrorYZ=True, mirrorBehavior=True, searchReplace=[mirrorSide,symmSide])
            rigAttr = pc.getAttr(mirrorJoints[0]+'.spineRig')
            rigAttr = rigAttr.replace(mirrorSide, symmSide)
            pc.setAttr((mirrorJoints[0] + '.spineRig'), rigAttr, type='string')
            pc.setAttr((mirrorJoints[0] + '.sides'), symmSide, type='string')
            
            rigParts = pc.getAttr(node + '.spineRigParts')
            pc.setAttr((node + '.spineRigParts'), (str(rigParts or '')+' '+mirrorJoints[0]), type='string')
        buildSplineJoints(s)
        pc.delete(sel[0])
    else:
        pc.error('No object is selected, plz try again...')


def buildNeckHeadJointSkeleton(parent):

    sel = pc.ls(sl=True)
    s = sel
    neckJoints = []
    headJoints = []
    eyeJoints = []
    child = ''
    headParent = ''
    rigParts = ''
    node = ''
    twistJoints = 0
    if len(sel) > 0:
        if not pc.attributeQuery('symmetry', n=sel[0], ex=True):
            child = pc.getAttr(sel[0]+'.child')
            
            neckRot = pc.getAttr(sel[0]+'.r')
            pc.setAttr((sel[0]+'.r'),(0,0,0))
            
            headRot = pc.getAttr(child+'.r')
            pc.setAttr((child+'.r'), (0,0,0))

            # creating neck joints
            neckJoints = buildJointSkeleton(parent)
            
            headParent = bModSkel.getParentAttrModuleComponants(child)

            # creating head joints
            pc.select(child, r=True)
            headJoints = buildJointSkeleton(headParent)
            # creating eye joints
            eyeJoints = createChildAttrJointHierarchy(child)

            # orienting neck joints
            orientJoints(neckJoints, 'xyz', 'zup')

            # orienting head joints
            orientJoints(headJoints, 'xyz', 'zup')
            orientJoints(eyeJoints, 'xyz', 'zup')
            
            makeRotAlignJointSetup(headJoints[0], headRot)
            makeRotAlignJointSetup (neckJoints[0], neckRot)

            # collecting info to create spine rig CMD
            name = pc.getAttr(sel[0]+'.name')
            side = pc.getAttr(sel[0]+'.side')
            neckJoint = stripSuffixToJnt(sel[0],(side+'neckJoint'))
            headJoint = stripSuffixToJnt(sel[0],(side+'headJoint'))
            eyeJoint = pc.getAttr(sel[0]+'.'+side+'eyeJoints')
            eyeJoint = eyeJoint.replace('_loc', '_jnt')
            
            pc.addAttr(neckJoints[0], ln='name', dt='string')
            pc.setAttr((neckJoints[0] + '.name'), name, type='string')
            pc.addAttr(neckJoints[0], ln='sides', dt='string')
            pc.setAttr((neckJoints[0] + '.sides'), side, type='string')
            pc.addAttr(neckJoints[0], ln='neckHeadRig', dt='string')
            pc.setAttr((neckJoints[0] + '.neckHeadRig'), (neckJoint+' '+headJoint), type='string')
            pc.addAttr(neckJoints[0], ln='eyeRig', dt='string')
            pc.setAttr((neckJoints[0] + '.eyeRig'), eyeJoint, type='string')

            node = createMasterRigPartsHolder()
            if not pc.attributeQuery('neckHeadRigParts', n=node, ex=True):
                pc.addAttr(node, ln='neckHeadRigParts', dt='string')
            if not pc.attributeQuery('eyeRigParts', n=node, ex=True):
                pc.addAttr(node, ln='eyeRigParts', dt='string')

            rigParts = pc.getAttr(node + '.neckHeadRigParts')
            pc.setAttr((node + '.neckHeadRigParts'), (str(rigParts or '')+' '+neckJoints[0]), type='string')
            rigParts = pc.getAttr(node + '.eyeRigParts')
            pc.setAttr((node + '.eyeRigParts'), (str(rigParts or '')+' '+neckJoints[0]), type='string')

        if pc.attributeQuery('doSymmetry', n=sel[0], ex=True):
            doSymm = pc.getAttr(sel[0]+'.doSymmetry')
            symmSide = pc.getAttr(doSymm+'.side')
            mirrorSide = pc.getAttr(sel[0]+'.side')
            mirrorJoints = pc.mirrorJoint(neckJoints[0], mirrorYZ=True, mirrorBehavior=True, searchReplace=[mirrorSide,symmSide])
            
            rigAttr = pc.getAttr(mirrorJoints[0]+'.neckHeadRig')
            rigAttr = rigAttr.split(mirrorSide, symmSide)
            pc.setAttr((mirrorJoints[0] + '.neckHeadRig'), rigAttr, type='string')
            pc.setAttr((mirrorJoints[0] + '.sides'), symmSide, type='string')
            
            rigParts = pc.getAttr(node + '.neckHeadRigParts')
            pc.setAttr((node + '.neckHeadRigParts'), (str(rigParts or '')+' '+mirrorJoints[0]), type='string')
            
            rigAttr = pc.getAttr(mirrorJoints[0]+'.eyeRig')
            rigAttr = rigAttr.split(mirrorSide, symmSide)
            pc.setAttr((mirrorJoints[0] + '.eyeRig'), str(rigAttr or ''), type='string')

            rigParts = pc.getAttr(node + '.eyeRigParts')
            pc.setAttr((node + '.eyeRigParts'), (str(rigParts or '')+' '+mirrorJoints[0]), type='string')
        buildSplineJoints(s)
        pc.delete(sel[0])
    else:
        pc.error('No object is selected, plz try again...')


def buildTentacleJointSkeleton(parent):
    sel = pc.ls(sl=True)
    tentacleJoints = []
    rigParts = ''
    node = ''

    if len(sel) > 0:
        if not pc.attributeQuery('symmetry', n=sel[0], ex=True):
            tentRot = pc.getAttr(sel[0]+'.r')
            pc.setAttr((sel[0]+'.r'), (0, 0, 0))

            # creating tentacle joints
            tentacleJoints = buildJointSkeleton(parent)

            # orienting neck joints
            orientJoints(tentacleJoints, 'xyz', 'ydown')
            
            makeRotAlignJointSetup(tentacleJoints[0], tentRot)

            # collecting info to create spine rig CMD
            name = pc.getAttr(sel[0]+'.name')
            side = pc.getAttr(sel[0]+'.side')
            moduleName = pc.getAttr(sel[0]+'.'+side+'types')
            startJoint = stripSuffixToJnt(sel[0], (side+'startJoint'))
            endJoint = stripSuffixToJnt(sel[0], (side+'endJoint'))

            pc.addAttr(tentacleJoints[0], ln='name', dt='string')
            pc.setAttr((tentacleJoints[0] + '.name'), name, type='string')
            pc.addAttr(tentacleJoints[0], ln='sides', dt='string')
            pc.setAttr((tentacleJoints[0] + '.sides'), side, type='string')
            pc.addAttr(tentacleJoints[0], ln='types', dt='string')
            pc.setAttr((tentacleJoints[0] + '.types'), moduleName, type='string')
            pc.addAttr(tentacleJoints[0], ln='tentacleRig', dt='string')
            pc.setAttr((tentacleJoints[0] + '.tentacleRig'), (startJoint+' '+endJoint), type='string')
            
            node = createMasterRigPartsHolder()
            if not pc.attributeQuery('tentacleRigParts', n=node, ex=True):
                pc.addAttr(node, ln='tentacleRigParts', dt='string')
                
            rigParts = pc.getAttr(node + '.tentacleRigParts')
            pc.setAttr((node + '.tentacleRigParts'), (str(rigParts or '')+' '+tentacleJoints[0]), type='string')

        if pc.attributeQuery('doSymmetry', n=sel[0], ex=True):
            doSymm = pc.getAttr(sel[0]+'.doSymmetry')
            symmSide = pc.getAttr(doSymm+'.side')
            mirrorSide = pc.getAttr(sel[0]+'.side')
            mirrorJoints = pc.mirrorJoint(tentacleJoints[0], mirrorYZ=True, mirrorBehavior=True, searchReplace=[mirrorSide, symmSide])
            rigAttr = pc.getAttr(mirrorJoints[0]+'.tentacleRig')
            rigAttr = strSearchReplace(rigAttr, mirrorSide, symmSide)
            pc.setAttr((mirrorJoints[0] + '.tentacleRig'), rigAttr, type='string')
            pc.setAttr((mirrorJoints[0] + '.sides'), symmSide, type='string')
            
            rigParts = pc.getAttr(node + '.tentacleRigParts')
            pc.setAttr((node + '.tentacleRigParts'), (str(rigParts or '')+' '+mirrorJoints[0]), type='string')
    else:
        pc.error('No object is selected, try again...')

    buildSplineJoints(sel)
