import pymel.core as pc
import re
import copy
import math
import List as List

from String import *
from Transform import *
from CurveUtilLib import * # TODO: clean this up


def dupId(n, prePost, id):
    newDup = []
    sel = []
    shortName = []
    dagPath = ''
    fullChain = []
    size = 0

    # check for selection
    if n == '':
        sel = pc.ls(sl=True)
    else:
        sel.append(n)

    fullChain = listHierarchy(sel[0])    
    newDup = pc.duplicate(sel,rc=True)
    newDup = listHierarchy(newDup)    
    size = len(newDup)

    for c in range(size):
        dagPath = fullChain[c]        
        match = re.search(r'[^|]*$',str(dagPath))
        if match:
            shortName.append(match.group())                        
        elif dagPath:
            shortName.append(dagPath)

    for i in range(size):
        if prePost == 'prefix':
            newDup[i] = pc.rename(newDup[i],(id+'_'+shortName[i]))            
        if prePost == 'suffix':
            newDup[i] = pc.rename(newDup[i],(shortName[i]+'_'+id))            

    return newDup

# TODO: move to List
# using this method to prevent changes to original list/array given
def reverseArray(array):
    c = copy.copy(array)    
    c.reverse()
    reversedArray = c    
    return reversedArray


def fkIkConnect(jnt, IK, FK, type, controller):
    if not pc.attributeQuery('FK_IK', n=controller, ex=True):
        pc.addAttr(controller,ln='FK_IK',at='double',min=0,max=1,dv=1,keyable=True)

    if len(jnt) == len(IK) and len(jnt) == len(FK):
        if(type == 'util'):
            for i in len(jnt):
                rotColorBlend = pc.createNode('blendColors',n=jnt[i]+'_rot_cb')
                pc.connectAttr(IK[i]+'.rotateX',rotColorBlend+'.color1R',f=True)
                pc.connectAttr(IK[i]+'.rotateY',rotColorBlend+'.color1G',f=True)
                pc.connectAttr(IK[i]+'.rotateZ',rotColorBlend+'.color1B',f=True)
                pc.connectAttr(FK[i]+'.rotateX',rotColorBlend+'.color2R',f=True)
                pc.connectAttr(FK[i]+'.rotateY',rotColorBlend+'.color2G',f=True)
                pc.connectAttr(FK[i]+'.rotateZ',rotColorBlend+'.color2B',f=True)

                pc.connectAttr((rotColorBlend + '.outputR'),(jnt[i] + '.rotateX'),f=True)
                pc.connectAttr((rotColorBlend + '.outputG'),(jnt[i] + '.rotateY'),f=True)
                pc.connectAttr((rotColorBlend + '.outputB'),(jnt[i] + '.rotateZ'),f=True)
                pc.connectAttr((controller + '.FK_IK'),(rotColorBlend[i] + '.blender'),f=True)

        if(type == 'constrain'):
            rev = pc.createNode('reverse',n=controller+'_IK_FK_rev')
            pc.connectAttr(controller+'.FK_IK',rev+'.ix',f=True)
            for i in range(len(jnt)):
                ikFkCon = pc.parentConstraint(FK[i],IK[i],jnt[i],skipTranslate=['x','y','z'],weight=1)
                pc.connectAttr(rev+'.ox',ikFkCon+'.w0',f=True)
                pc.connectAttr(controller+'.FK_IK',ikFkCon+'.w1',f=True)

    else:
        print('array of ik-fk does not match')


def stretchTypeConnect(jnt, IK, FK, type, controller):
    if not pc.attributeQuery('FK_IK', n=controller, ex=True):
        pc.addAttr(controller,ln='FK_IK',at=double,min=0,max=1,dv=1,keyable=True)

    if len(jnt) == len(IK) and len(jnt) == len(FK):
        if type == 'translate':
            for i in range(len(jnt)):
                transColorBlend = pc.createNode('blendColors',n=jnt[i]+'_trans_cb')
                pc.connectAttr((IK[i] + '.translateX'),(transColorBlend + '.color1R'),f=True)
                pc.connectAttr((IK[i] + '.translateY'),(transColorBlend + '.color1G'),f=True)
                pc.connectAttr((IK[i] + '.translateZ'),(transColorBlend + '.color1B'),f=True)
                pc.connectAttr((FK[i] + '.translateX'),(transColorBlend + '.color2R'),f=True)
                pc.connectAttr((FK[i] + '.translateY'),(transColorBlend + '.color2G'),f=True)
                pc.connectAttr((FK[i] + '.translateZ'),(transColorBlend + '.color2B'),f=True)

                pc.connectAttr((transColorBlend + '.outputR'),(jnt[i] + '.translateX'),f=True)
                pc.connectAttr((transColorBlend + '.outputG'),(jnt[i] + '.translateY'),f=True)
                pc.connectAttr((transColorBlend + '.outputB'),(jnt[i] + '.translateZ'),f=True)
                pc.connectAttr((controller + '.FK_IK'),(transColorBlend + '.blender'),f=True)

        if type == 'scale':
            for i in range(len(jnt)):
                scaleColorBlend = pc.createNode('blendColors',n=jnt[i]+'_scale_cb')
                pc.connectAttr((IK[i] + '.scaleX'),(scaleColorBlend + '.color1R'),f=True)
                pc.connectAttr((IK[i] + '.scaleY'),(scaleColorBlend + '.color1G'),f=True)
                pc.connectAttr((IK[i] + '.scaleZ'),(scaleColorBlend + '.color1B'),f=True)
                pc.connectAttr((FK[i] + '.scaleX'),(scaleColorBlend + '.color2R'),f=True)
                pc.connectAttr((FK[i] + '.scaleY'),(scaleColorBlend + '.color2G'),f=True)
                pc.connectAttr((FK[i] + '.scaleZ'),(scaleColorBlend + '.color2B'),f=True)

                pc.connectAttr((scaleColorBlend + '.outputR'),(jnt[i] + '.scaleX'),f=True)
                pc.connectAttr((scaleColorBlend + '.outputG'),(jnt[i] + '.scaleY'),f=True)
                pc.connectAttr((scaleColorBlend + '.outputB'),(jnt[i] + '.scaleZ'),f=True)
                pc.connectAttr((controller + '.FK_IK'),(scaleColorBlend + '.blender'),f=True)


# create all needed fk ik connections for given joint
#     INPUTS:
#        jnt 			>> object to create fk ik connection ("joint1")
#        IK				>> ik joint hierarchy
#        FK				>> fk joint hierarchy
#        type           >> type of connection ("translate / scale")
#        controller     >> object to create fk ik control attribute
#
# (i.e) stretchTypeConnect("joint1", "IK_joint1", "FK_joint1", "utilNods", "fkIk_anim")
def listHierarchy(n):
    sel = []
    child = []
    fullchains = []
    if n == '':
        sel = pc.ls(sl=True)
    else:
        sel.append(n)

    for i in range(len(sel)):
        child = pc.listRelatives(sel, allDescendents=True,path=True,type='joint')
        fullchains.extend(child)
        fullchains.extend(sel)
        fullchains = reverseArray(fullchains)

    return fullchains


# this proc will return hierarchy for selected joint
def zoofindPolePosition(startJoint, midJoint, endJoint, dist):
    temp = []
    joint2 = endJoint
    joint1 = ''
    joint0 = ''

    if pc.objExists(midJoint): joint1 = midJoint
    else:
        parents = pc.listRelatives(joint2,p=True)
        if len(parents): joint1 = parents[0]
    if pc.objExists(startJoint): joint0 = startJoint
    else:
        parents = pc.listRelatives(joint1,p=True)
        if len(parents): joint0 = parents[0]

    if not pc.objExists(joint0): return
    if not pc.objExists(joint1): return
    if not pc.objExists(joint2): return
    pos0 = pc.xform(joint0,q=True,ws=True,rp=True)
    pos1 = pc.xform(joint1,q=True,ws=True,rp=True)
    pos2 = pc.xform(joint2,q=True,ws=True,rp=True)
    midway = ((pos2[0]+pos0[0])/2, (pos2[1]+pos0[1])/2, (pos2[2]+pos0[2])/2)
    dotA = (pos2[0]-pos0[0], pos2[1]-pos0[1], pos2[2]-pos0[2])
    dotB = (pos1[0]-pos0[0], pos1[1]-pos0[1], pos1[2]-pos0[2])
    lengthFactor = pc.util.sqrt(dotA[0]*dotA[0] + dotA[1]*dotA[1] + dotA[2]*dotA[2])
    projAB = zooVectorProj(dotA,dotB)
    multiplier = 1.0
    int = []
    sub = []

    sub = (pos0[0]+projAB[0], pos0[1]+projAB[1], pos0[2]+projAB[2])
    sub = (pos1[0]-sub[0], pos1[1]-sub[1], pos1[2]-sub[2])
    dist *= lengthFactor
    mag = pc.util.sqrt(sub[0]*sub[0] + sub[1]*sub[1] + sub[2]*sub[2])

    if mag < 0.00001: return pos1
    else: multiplier = dist/mag
    int.append(midway[0] + sub[0]*multiplier)
    int.append(midway[1] + sub[1]*multiplier)
    int.append(midway[2] + sub[2]*multiplier)

    return int


# proc from zooToolBox
def zooVectorProj(vecA, vecB):
    a = vecA
    b = vecB
    magA = zooVectorMag(a)    
    dot = pc.util.dot(a,b)
    magA = pc.util.pow(magA,2)
    magA = dot/magA

    return [vecA[0]*magA, vecA[1]*magA, vecA[2]*magA]


# returns the vector found by projecting vecB onto vecA
def zooVectorMag(vec):
    mag = pc.util.pow(vec[0], 2) + pc.util.pow(vec[1],2) + pc.util.pow(vec[2], 2)
    return pc.util.sqrt(mag)


# This proc will create Fk controls for selecte joint
#
#    INPUTS:
#        n          >> object to create fk ik connection ("joint1")
#        ctrlType   >> type of curve control
#
#		REQUIRES:     curveControl.mel, snap.mel
#		(i.e) fkControl("joint1", "circleOrient")
def fkControl(n, ctrlType, zeroOut, controlColor=''):
    sel = []
    FKCon = []
    FKAnim = []
    grp = []
    if n == '':
        sel = pc.ls(sl=True)
    else:
        sel.append(n)

    FKCon = listHierarchy(sel[0])
    FKAnim = dupId(FKCon[0], 'suffix', 'ctrl')
    for i in range(len(FKCon)):
        shapeParent(FKAnim[i], ctrlType, controlColor)
        try:
            pc.setAttr(FKAnim[i]+'.radius', 0)
        except:
            pass
        ikFkCon = pc.parentConstraint(FKAnim[i], FKCon[i], weight=1.0)
        pc.connectAttr((FKAnim[i]+".scale"), (FKCon[i]+".scale"))
        if zeroOut:
            grp = quickZeroOut(FKAnim[i])
            lockAndHide(grp[0], 'lock', 'trans rot scale vis')
        pc.select(cl=True)
    if zeroOut:
        for x in range(len(FKCon) - 1):
            pc.connectAttr(FKAnim[x]+'.scale', FKAnim[x+1]+'.inverseScale')
    return FKAnim


# TODO: check that functions can be passed this way
# to get different type of selection from selected objects
def selectionType(type, cmd):
    select = pc.ls(sl=True)
    pc.select(cl=True)
    evenIndex = 0
    oddIndex = 1

    if type == 'even':
        for i in range(len(select)/2):
            pc.select(select[evenIndex],toggle=True)
            even = (evenIndex + 2)
            evenIndex = even
            cmd()
            print('/n'+evenIndex)
    if type == 'odd':
        for i in range(len(select)/2):
            pc.select(select[oddIndex],toggle=True)
            odd = (oddIndex + 2)
            oddIndex = odd
            cmd()
            print('/n'+oddIndex)


# This little proc return child of selected joint
def getChildJoint(n):
    sel = []
    temp = []
    if n == '':
        sel = pc.ls(sl=True)
    else:
        sel.append(n)

    if pc.nodeType(sel[0]) == 'joint':
        temp.extend(pc.listRelatives(sel[0],children=True,path=True,typ='joint'))
        if len(temp) < 1:
            pc.error('\nNo child found on specified joint\n')
    else:
        pc.error('Selected object is not a Joint')    
    return temp[0]


# This little proc help you lock n unlock tranfrom attributes
# INPUTS
#			n 				= specified object or selected objects
#			mode			= lock / unlock / locknHide
#			channels        = specify channels "trans rot scale"
def lockAndHide(n, mode, channels):
    flags = []
    sel = []
    if n == '':
        sel = pc.ls(sl=True)
    else:
        sel.append(n)

    flags = List.seperate(channels) #.split(' ')

    for f in flags:
        if mode == 'lock':
            if f == 'trans':
                pc.setAttr(n+'.tx',lock=True)
                pc.setAttr(n+'.ty',lock=True)
                pc.setAttr(n+'.tz',lock=True)
            elif f == 'rot':
                pc.setAttr(n+'.rx',lock=True)
                pc.setAttr(n+'.ry',lock=True)
                pc.setAttr(n+'.rz',lock=True)
            elif f == 'scale':
                pc.setAttr(n+'.sx',lock=True)
                pc.setAttr(n+'.sy',lock=True)
                pc.setAttr(n+'.sz',lock=True)
            elif f == 'vis':
                pc.setAttr(n+'.v',lock=True)
        elif mode == 'locknHide':
            if f == 'trans':
                pc.setAttr(n+'.tx',lock=True,keyable=False)
                pc.setAttr(n+'.ty',lock=True,keyable=False)
                pc.setAttr(n+'.tz',lock=True,keyable=False)
            elif f == 'rot':
                pc.setAttr(n+'.rx',lock=True,keyable=False)
                pc.setAttr(n+'.ry',lock=True,keyable=False)
                pc.setAttr(n+'.rz',lock=True,keyable=False)
            elif f == 'scale':
                pc.setAttr(n+'.sx',lock=True,keyable=False)
                pc.setAttr(n+'.sy',lock=True,keyable=False)
                pc.setAttr(n+'.sz',lock=True,keyable=False)
            elif f == 'vis':
                pc.setAttr(n+'.v',lock=True,keyable=False)
        elif mode == 'unLock':
            if f == 'trans':
                pc.setAttr(n+'.tx',lock=False,keyable=True)
                pc.setAttr(n+'.ty',lock=False,keyable=True)
                pc.setAttr(n+'.tz',lock=False,keyable=True)
            elif f == 'rot':
                pc.setAttr(n+'.rx',lock=False,keyable=True)
                pc.setAttr(n+'.ry',lock=False,keyable=True)
                pc.setAttr(n+'.rz',lock=False,keyable=True)
            elif f == 'scale':
                pc.setAttr(n+'.sx',lock=False,keyable=True)
                pc.setAttr(n+'.sy',lock=False,keyable=True)
                pc.setAttr(n+'.sz',lock=False,keyable=True)
            elif f == 'vis':
                pc.setAttr(n+'.v',lock=False,keyable=True)


# This proc creates distance connection for specified joint
def createDistance(start_joint, end_joint):
    """creates distanceDimension node with its locators matching the position of start_joint and end_joint"""
    result = []
    
    # get worldSpace value in order to get exact position of selected joint
    start_pos = pc.xform(start_joint, q=True, worldSpace=True, rotatePivot=True)
    end_pos = pc.xform(end_joint, q=True, worldSpace=True, rotatePivot=True)

    # create dummy locators
    tmp_loc1 = pc.spaceLocator(n=start_joint + '_start_loc')
    tmp_loc2 = pc.spaceLocator(n=start_joint + '_end_loc')

    # snap locators to respective joints    
    pc.move(start_pos[0], start_pos[1], start_pos[2], tmp_loc1, a=True,ws=True)
    pc.move(end_pos[0], end_pos[1], end_pos[2], tmp_loc2, a=True, ws=True)

    dimension_node = pc.createNode('distanceDimShape')
    pc.connectAttr(tmp_loc1 + '.worldPosition[0]', dimension_node + '.startPoint')
    pc.connectAttr(tmp_loc2 + '.worldPosition[0]', dimension_node + ".endPoint")

    # rename distance dimension node
    dimension_parent = pc.listRelatives(dimension_node, parent=True)
    new_name = pc.rename(dimension_parent, (start_joint + '_distance'))

    result.append(new_name)		#distance node
    result.append(tmp_loc1)	    #start locator
    result.append(tmp_loc2)	    #end locator

    return result


# This little function return length joint chain
def getChainLength(startJoint, endJoint):
    temp = []
    dis = 0.0
    shape = []
    child = ''

    list = findJointArray(startJoint, endJoint)    
    if len(list) <= 1:
        print ('\n No additional Joints selected \n')
    else:        
        for i in range(len(list)-1):
            child = getChildJoint(list[i])
            temp = createDistance(list[i], child)
            shape = pc.listRelatives(temp[0], s=True)            
            dis = dis + pc.getAttr(shape[0]+".distance")
            pc.delete(temp)
    return dis


def getStretchAxis(obj, type):
    stretchAxis = []
    child = ''
    axis = pc.getAttr(obj+'.t')

    if type == 'scale':
        if math.fabs(axis[0]) > math.fabs(axis[1]) and math.fabs(axis[0]) > math.fabs(axis[2]):
            stretchAxis = ['sx', 'sy', 'sz']
        elif math.fabs(axis[1]) > math.fabs(axis[0]) and math.fabs(axis[1]) > math.fabs(axis[2]):
            stretchAxis = ['sy', 'sz', 'sx']
        elif math.fabs(axis[2]) > math.fabs(axis[1]) and math.fabs(axis[2]) > math.fabs(axis[0]):
            stretchAxis = ['sz', 'sx', 'sy']
        else:
            stretchAxis = ['sx', 'sy', 'sz']
    if type == 'translate':
        if math.fabs(axis[0]) > math.fabs(axis[1]) and math.fabs(axis[0]) > math.fabs(axis[2]):
            stretchAxis = ['tx', 'ty', 'tz']
        elif math.fabs(axis[1]) > math.fabs(axis[0]) and math.fabs(axis[1]) > math.fabs(axis[2]):
            stretchAxis = ['ty', 'tz', 'tx']
        elif math.fabs(axis[2]) > math.fabs(axis[1]) and math.fabs(axis[2]) > math.fabs(axis[0]):
            stretchAxis = ['tz', 'tx', 'ty']
        else:
            stretchAxis = ['tx', 'ty', 'tz']

    return stretchAxis


def findJointArray(startJoint, endJoint):

    i = 1
    redFlag = 0
    fullChain = []
    fullChain.append(endJoint) # first joint in the array will be the last joint

    while redFlag == 0: # loop through the joints until the current joint is the last joint        
        temp = pc.listRelatives(fullChain[i-1], p=True, type='joint')
        if temp[0]:
            fullChain.append(temp[0])
        else:
            fullChain.append(temp)
        if fullChain[i] == startJoint:
            redFlag = 1
        elif fullChain[i] == '':
            pc.error(startJoint + ' ' + endJoint + ' are not in same hierarchy')
        i = i + 1
       
    result = reverseArray(fullChain)    
    return result


def parentSkeletonTo(node, parent):
    i = 1
    redFlag = 0
    fullChain = []
    fullChain.append(node)
    while redFlag == 0:
        if fullChain[i-1]!='':
            imdParent = pc.listRelatives(fullChain[i-1],p=True,pa=True)                  
            if imdParent:    
                fullChain.append(imdParent[0])
            else:# TODO: find a cleaner way to do this
                fullChain.append('')
        if fullChain[i] == parent:
            redFlag = 1
        if fullChain[i] == '':
            pc.parent(fullChain[i-1],parent)
            redFlag = 1
        i = i + 1
    pc.select(cl=True)


def getTwistAxis(obj):
    twistAxis = []
    child = ''
    axis = []
    child = getChildJoint(obj)
    axis = pc.getAttr(child+'.t')

    if (math.fabs(axis[0])> math.fabs(axis[1])) and (math.fabs(axis[0])>math.fabs(axis[2])):
        twistAxis = ['rx','rz','ry']
    elif (math.fabs(axis[1])> math.fabs(axis[0])) and (math.fabs(axis[1])>math.fabs(axis[2])):
        twistAxis = ['ry','rz','rx']
    elif (math.fabs(axis[2])> math.fabs(axis[1])) and (math.fabs(axis[2])>math.fabs(axis[0])):
        twistAxis = ['rz','rx','ry']
    else:
        twistAxis = ['rx','rz','ry']

    return twistAxis


def curveGuide(startPos, endPos):
    nonScaleGrp = 'non_scale_grp'
    partGrp = 'curveGuide_grp'
    posA = pc.xform(startPos,q=True,worldSpace=True,rotatePivot=True)
    posB = pc.xform(endPos,q=True,worldSpace=True,rotatePivot=True)
    curve = pc.curve(d=1,p=[(posA[0],posA[1],posA[2]),(posB[0],posB[1],posB[2])],k=[0,1])
    pc.rename(curve,endPos+'Guide_crv')
    pc.setAttr(curve+'.template',1)

    pc.select(curve+'.cv[0]',r=True)
    posAClts = pc.cluster()
    pc.select(curve+'.cv[1]',r=True)
    posBClts = pc.cluster()
    pc.hide(posAClts,posBClts)
    pc.setAttr(posAClts[1] + '.v',lock=True)
    pc.setAttr(posBClts[1] + '.v',lock=True)
    pc.parent(posAClts[1],startPos)
    pc.parent(posBClts[1],endPos)

    if not pc.objExists(nonScaleGrp):
        nonScaleGrp = pc.group(em=True,n='non_scale_grp')
    if not pc.objExists(partGrp):
        partGrp = pc.group(em=True,n='curveGuide_grp')
        pc.parent(partGrp,nonScaleGrp)
    pc.parent(curve,partGrp)
    return curve


def jointCurve(startJoint, endJoint):
    noJoint = findJointArray(startJoint, endJoint)
    cvPos = []
    for j in noJoint:        
        cvPos.append(pc.xform(j,q=True,worldSpace=True,rotatePivot=True))

    curve = pc.curve(d=3,ep=cvPos)
    pc.rebuildCurve(curve, ch=0, rpo=1, rt=0, end=1, kr=2, kcp=0, kep=1, kt=0, s=0, d=3, tol=0.01)
    return curve


def jointsOnCurve(curve, orientAxis, upAxis, numJoints, name):
    pc.select(cl=True)    
    curveInfo = pc.pointOnCurve(curve, ch=True)
    pc.setAttr(curveInfo+'.turnOnPercentage', 1)

    i = 0
    joints = []
    for i in range(numJoints+1):
        parameter = i * (1.0/numJoints)
        pc.setAttr(curveInfo+'.parameter', parameter)
        position = pc.getAttr(curveInfo+'.position')        
        joints.append(pc.joint(n=(name + str(i+1) + '_jnt'), p=position))
    pc.delete(curveInfo)
    pc.joint(joints, e=True, oj=orientAxis, secondaryAxisOrient=upAxis, ch=True, zso=True)
    return joints


def getParent(object):    
    parent = pc.listRelatives(object,parent=True)
    return parent;    


def transferConnection(master, slave, attr):
    transConnection = pc.listConnections(master+'.'+attr, d=False, s=True, plugs=True, skipConversionNodes=False)
    if transConnection:        
        pc.connectAttr(transConnection[0],slave+'.'+attr)
        pc.disconnectAttr(transConnection[0],master+'.'+attr)


def connectMirrorTrans(obj1, obj2, axis):
    aAxisStr = ['x','y','z']
    axisStr = '.t'+aAxisStr[axis]    

    revNode = pc.createNode('plusMinusAverage',n=obj2+'MirrorTrans_pma')
    pc.setAttr(revNode+'.operation',2)
    pc.setAttr(revNode+'.input1D[0]',0)
    pc.connectAttr((obj1+axisStr), (revNode+".input1D[1]"),f=True)
    pc.connectAttr((revNode+".output1D"), (obj2+axisStr),f=True)


def connectMirrorRot(obj1, obj2, axis):
    aAxisStr = ['x', 'y', 'z']
    axisStr = ".r"+aAxisStr[axis]

    revNode = pc.createNode('plusMinusAverage', n=(obj2+'MirrorRot_pma'))
    pc.setAttr(revNode+'.operation',2)
    pc.setAttr(revNode+'.input1D[0]',0)
    pc.connectAttr((obj1+axisStr),(revNode+'.input1D[1]'),f=True)
    pc.connectAttr((revNode+'.output1D'),(obj2+axisStr),f=True)


def makeFootHeelPivots(ankleJoint, ballJoint):
    pc.select(cl=True)

    tempLoc = curveControl('grp','curve')
    tempLoc[0] = pc.rename(tempLoc[0],ballJoint+'Pos_loc')

    heelJnt = curveControl('loc','curve')
    heelJnt[0] = pc.rename(heelJnt[0],ankleJoint+'Heel_loc')

    bankInJnt = curveControl('loc','curve')
    bankInJnt[0] = pc.rename(bankInJnt[0],ballJoint+'InPos_loc')

    bankOutJnt = curveControl('loc','curve')
    bankInJnt[0] = pc.rename(bankInJnt[0],ankleJoint+'OutPos_loc')

    endJoint = getChildJoint(ballJoint)

    pc.parent(heelJnt,bankInJnt,bankOutJnt,tempLoc[0])

    ankleJntXform = pc.xform(ankleJoint,q=True,ws=True,t=True)
    ballJntXform = pc.xform(ballJoint,q=True,ws=True,t=True)

    pc.setAttr(tempLoc[0]+'.t',ballJntXform[0],ballJntXform[1],ballJntXform[2])
    tempCon = pc.aimConstraint(endJoint, tempLoc[0], o=[0,0,0], w=1, aimVector=[0,0,1], upVector=[0,1,0], worldUpType='vector', worldUpVector=[0,1,0])
    pc.delete(tempCon)

    pc.setAttr(heelJnt[0]+'.tz',(ankleJntXform[2] - ballJntXform[2])*1.4)
    pc.setAttr(bankInJnt[0]+'.tx',(ankleJntXform[2] - ballJntXform[2])*0.7)
    pc.setAttr(bankOutJnt[0]+'.tx',(ankleJntXform[2] - ballJntXform[2])*-0.7)

    pc.addAttr(ankleJoint, ln='heelPos', dt='string')
    pc.setAttr(ankleJoint+'.heelPos',heelJnt[0],type='string')

    pc.addAttr(ballJoint,ln='bankInPos',dt='string')
    pc.setAttr(ballJoint+'.bankInPos',bankInJnt[0],type='string')

    pc.addAttr(ballJoint,ln='bankOutPos',dt='string')
    pc.setAttr(ballJoint+'.bankOutPos',bankOutJnt[0],type='string')
    pc.select(cl=True)
    return tempLoc[0]


def getQuadFlexLegJointPos(startJoint, endJoint):
    temp = createDistance(startJoint,endJoint)
    shape = pc.listRelatives(temp[0],s=True)
    dis = pc.getAttr(shape[0]+'.distance')
    pc.delete(temp)

    startLoc = curveControl('loc','curve')
    endLoc = curveControl('loc','curve')
    midALoc = curveControl('loc','curve')
    midBLoc = curveControl('loc','curve')

    Snap(startJoint,startLoc[0])
    Snap(endJoint,endLoc[0])

    animCon = pc.aimConstraint(endJoint, startLoc[0], offset=[0,0,0], weight=1, aimVector=[0,-1,0], upVector=[0,0,1], worldUpType='vector', worldUpVector=[0,1,0])
    pc.delete(animCon)

    midDis = (dis/3)

    pc.parent(endLoc[0], midALoc[0], midBLoc[0], startLoc[0])
    pc.setAttr(midALoc[0]+'.r',(0,0,0))
    pc.setAttr(midALoc[0]+'.tx',0)
    pc.setAttr(midALoc[0]+'.ty',midDis*-1)
    pc.setAttr(midALoc[0]+'.tz',midDis)

    pc.setAttr(midBLoc[0]+'.r',(0,0,0))
    pc.setAttr(midBLoc[0]+'.tx',0)
    pc.setAttr(midBLoc[0]+'.ty',midDis*-2)
    pc.setAttr(midBLoc[0]+'.tz',midDis*-1)

    tempPos1 = pc.xform(startLoc[0],q=True,worldSpace=True,rotatePivot=True)
    tempPos2 = pc.xform(midALoc[0],q=True,worldSpace=True,rotatePivot=True)
    tempPos3 = pc.xform(midBLoc[0],q=True,worldSpace=True,rotatePivot=True)
    tempPos4 = pc.xform(endLoc[0],q=True,worldSpace=True,rotatePivot=True)

    jointPos = []
    jointPos.append(tempPos1)
    jointPos.append(tempPos2)
    jointPos.append(tempPos3)
    jointPos.append(tempPos4)

    pc.delete(endLoc[0], midALoc[0], midBLoc[0], startLoc[0])

    return jointPos


def quickZeroOut(n):
    s = []
    zeros = []
    strip = ''

    if n == '':
        s = pc.ls(sl=True,tr=True)
    else:
        s.append(n)

    for node in s:
        l = len(str(node))
        sN = node
        cap = node[0:1].upper()        
        if l > 1:
            end = node[1:l]
            sN = cap + end
            strip = objGetPrefix(sN) 
            size = len(strip)
            if size > 1:
                sN = strip
        else:
            sN = cap

        name = ('frz'+sN+'_grp')
        num = 1
        while pc.objExists(name): # find unique name
            num = num + 1
            name = ('frz'+sN+num+'_grp')
        grp = pc.group(em=True,w=True,n=name)
        parents = pc.listRelatives(node,parent=True)
        if len(parents) > 0:
            pc.parent(grp,parents[0])

        dupe = pc.duplicate(node,rr=True,rc=True)
        dupe[0] = pc.rename(dupe[0],('frz'+sN+'_grp'))

        NdsSnap(dupe[0],grp)

        pc.delete(dupe)

        parentedNode = pc.parent(node,grp)
        zeros.append(grp)

    pc.select(s,r=True)
    return zeros


def quickJointZeroOut(n):
    s = []
    zeros = []
    strip = ''
    grp = ''

    if n == '':
        s = pc.ls(sl=True)
    else:
        s.append(n)

    for node in s:
        l = len(str(node))
        sN = node
        cap = node[0:1].upper()
        if l > 1:
            end = node[1:l]
            sN = cap + end
            strip = objGetPrefix(sN)
            size = len(strip)
            if size > 1:
                sN = strip
        else:
            sN = cap

        name = ('frz'+sN+'_grp')
        num = 1
        while pc.objExists(name): # find unique name
            num = num + 1
            name = ('frz'+sN+num+'_grp')
        pc.select(cl=True)
        grp = pc.joint(n=name)
        pc.setAttr(grp+'.radius',0)
        Snap(node,grp)
        pc.makeIdentity(grp,apply=True,t=0,r=1,s=0)
        parents = pc.listRelatives(node, parent=True)        

        if len(parents) > 0:
            pc.parent(grp,parents[0])
        
        parentedNode = pc.parent(node,grp)
        zeros.append(grp)

    # pc.select(s,r=True)
    return zeros


def getcharRigInfoNode(name):
    nonScaleGrp = name + 'non_scale_grp'
    if not pc.objExists(nonScaleGrp):
        pc.warning('The rig group' + nonScaleGrp + 'does not exist.')
        return
    charInfo = pc.listRelatives(nonScaleGrp,ad=True,type='geometryVarGroup')
    if(len(charInfo)==1):
        return charInfo[0]
    else:
        charInfoNode = pc.createNode('geometryVarGroup',n=name+'charRigInfo',p=nonScaleGrp)
        rigAuther = pc.util.getEnv('USER')   
        print("rigAuther: ")
        print(rigAuther)
        # TODO: change this to grab from rig textbox
        setupVersion = '1.0'
        date = pc.about(cd=True)

        pc.addAttr(charInfoNode,ln='setupWithVersion',dt='string')
        pc.addAttr(charInfoNode,ln='rigAuthor',dt='string')
        pc.addAttr(charInfoNode,ln='date',dt='string')
        pc.setAttr(charInfoNode+'.rigAuthor',rigAuther,l=True,type='string')
        pc.setAttr(charInfoNode+'.setupWithVersion',setupVersion,l=True,type='string')
        pc.setAttr(charInfoNode+'.date',date,l=True,type='string')
        return charInfoNode


# rig side seperator, seperates side drop down selected option
def rigSideSep(obj):
    ret = []
    if obj == '':
        return ret
    
    parts = obj.split('/')
    
    if len(parts) <= 1:
        ret.append(obj)
    else:
        ret.append(parts[len(parts)-2]+'_')
        ret.append(parts[len(parts)-1]+'_')
    return ret


def getFingerAxisFigures(obj):
    # x=1 y=2 z=3
    # 1 element = spin
    # 2 element = curl
    # 3 element = spread
    # 4 element = stretch

    fingerAxis = []
    rotAxis = getTwistAxis(obj)
    if rotAxis[0] == 'rx':
        fingerAxis = [1,3,2,1]
    elif rotAxis[0] == 'ry':
        fingerAxis = [2,3,1,1]
    elif rotAxis[0] == 'rz':
        fingerAxis = [3,1,2,1]

    return fingerAxis


def toggleBaseSkeletonSelect():
    baseSkeleton = 'skeletons_grp'
    if pc.objExists(baseSkeleton):
        state = pc.getAttr(baseSkeleton+'.ove')
        pc.setAttr(baseSkeleton+'.ove',1-state)


def createSkinJointSet(prefix):
    
    if not pc.objExists(prefix+'SkinJoints_set'):        
        pc.sets(n=prefix+'SkinJoints_set')
    return (prefix+'SkinJoints_set')


def addSkinJointToSet(set, jointList):
    if pc.objExists(set):
        for j in jointList:            
            pc.sets(set,fe=j)


def selectSkinJoints():
    if pc.objExists('*SkinJoints_set'):
        members = pc.sets('*SkinJoints_set',q=True)
        pc.select(members, r=True)
    else:
        pc.error('SkinJoints_set does not exist')