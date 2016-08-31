import pymel.core as pc
import CharUtilsLib as chUL
import List


def addTwistJointAttr(type, count=2, sel=''):

    if sel == '':
        sel = pc.ls(sl=True)

    plusMinus = ''
    multDiv = ''
    loc = ''
    locShape = ''
    parent = ''
    tempString = []
    multDivs = []
    multDivsVis = []
    attrs = []
    red = 0.0

    tempString = pc.listRelatives(sel, f=True, c=True)
    childJoint = ''
    # TODO: clean this up to be more efficient and not iterate over every child joint
    # NOTE: only need to know if there is a child joint to continue if there is not
    for t in tempString:
        if pc.objectType(t, i='joint'):
            childJoint = t

    if pc.attributeQuery('twistJoints', n=sel, ex=True):
        pc.error('Twist Joints Attribute already added!\n')
    else:
        pc.addAttr(sel, k=1, ln=type, at='long', min=0, max=10, dv=count)  # type = 'twistJoints'

    parent = pc.group(em=True)
    parent = pc.rename(parent, (sel + "TwistJnt_grp"))
    pc.parentConstraint(sel, parent, weight=1)
    pc.addAttr(sel, ln='twistJointGrp', dt='string')
    pc.setAttr((sel + '.twistJointGrp'), parent, type='string')

    plusMinus = pc.createNode('plusMinusAverage', n=(sel + 'Twist_pma'), )
    pc.connectAttr((sel + '.' + type), (plusMinus + '.input1D[0]'))
    pc.setAttr((plusMinus + '.input1D[1]'), 1)
    multDiv = pc.createNode('multiplyDivide', n=(sel + 'Twist_md'))
    pc.setAttr((multDiv + '.operation'), 2)
    pc.connectAttr((childJoint + '.translate'), (multDiv + '.input1'))
    pc.connectAttr((plusMinus + '.output1D'), (multDiv + '.input2.input2X'))
    pc.connectAttr((plusMinus + ".output1D"), (multDiv + '.input2.input2Y'))
    pc.connectAttr((plusMinus + '.output1D'), (multDiv + '.input2.input2Z'))
    pc.select(cl=True)

    red = pc.getAttr(sel + '.radius')
    red = (red / 2)

    for y in range(1, 11):
        tempString = chUL.curveControl('sphereCross', 'curve')
        chUL.resizeCurves(None, 1, 1, 1, red)
        loc = pc.rename(tempString[0], (sel + '_' + type + str(y) + '_loc'))
        pc.addAttr(loc, k=0, dv=y, min=0, max=10, ln='twistPosition', at='double')
        pc.parent(loc, parent)

        pc.setAttr((loc + '.overrideEnabled'), 1)
        pc.setAttr((loc + '.overrideColor'), 10)

        multDivs.append(pc.createNode('multiplyDivide', n=(sel + '_' + type + str(y) + '_md')))
        pc.connectAttr((multDiv + '.output'), (multDivs[y - 1] + '.input1'))
        pc.connectAttr((loc + '.twistPosition'), (multDivs[y - 1] + '.input2.input2X'))
        pc.setAttr((multDivs[y - 1] + '.input2.input2Y'), y)
        pc.setAttr((multDivs[y - 1] + '.input2.input2Z'), y)
        pc.connectAttr((multDivs[y - 1] + '.output'), (loc + '.translate'))

        multDivsVis.append(pc.createNode('multiplyDivide', n=(sel + '_' + type + str(y) + 'Vis_md')))
        pc.connectAttr((sel + '.' + type), (multDivsVis[y - 1] + '.input1.input1X'))
        pc.setAttr((multDivsVis[y - 1] + '.input2.input2X'), ((1.00 / (2 * y)) + 0.001))
        pc.connectAttr((multDivsVis[y - 1] + '.outputX'), (loc + '.visibility'))
        chUL.lockAndHide(loc, 'locknHide', 'trans rot scale vis')  # TODO: make sure this works
        pc.select(cl=True)


def addTwistJointsAttr(type):

    sel = pc.ls(sl=True)

    plusMinus = ''
    multDiv = '' 
    loc = '' 
    locShape = ''
    parent = ''
    tempString = []
    multDivs = []
    multDivsVis = []
    attrs = []
    red = 0.0
    if len(sel) == 0:
        pc.warning('Select 1 joint\n')
    for s in sel:        
        tempString = pc.listRelatives(s, f=True, c=True)
        childJoint = ''
        # TODO: clean this up to be more efficient and not iterate over every child joint
        # NOTE: only need to know if there is a child joint to continue if there is not
        for t in tempString:            
            if pc.objectType(t, i='joint'):
                childJoint = t
        if pc.objectType(s) != 'joint' or childJoint == '' or len(tempString) == 0:
            continue
        if pc.attributeQuery('twistJoints', n=s, ex=True):
            pc.error('Twist Joints Attribute already added!\n')
        else:            
            pc.addAttr(s, k=1, ln=type, at='long', min=0, max=10, dv=2)

        parent = pc.group(em=True)
        parent = pc.rename(parent, (s+"TwistJnt_grp"))
        pc.parentConstraint(s, parent, weight=1)
        pc.addAttr(s, ln='twistJointGrp', dt='string')
        pc.setAttr((s+'.twistJointGrp'), parent, type='string')
        
        plusMinus= pc.createNode('plusMinusAverage', n=(s+'Twist_pma'),)
        pc.connectAttr((s+'.'+type), (plusMinus+'.input1D[0]'))
        pc.setAttr((plusMinus+'.input1D[1]'),1)
        multDiv = pc.createNode('multiplyDivide', n=(s+'Twist_md'))
        pc.setAttr((multDiv+'.operation'), 2)
        pc.connectAttr((childJoint+'.translate'), (multDiv+'.input1'))
        pc.connectAttr((plusMinus+'.output1D'), (multDiv+'.input2.input2X'))
        pc.connectAttr((plusMinus+".output1D"), (multDiv+'.input2.input2Y'))
        pc.connectAttr((plusMinus+'.output1D'), (multDiv+'.input2.input2Z'))
        pc.select(cl=True)
        
        red = pc.getAttr(s+'.radius')
        red = (red/2)
        
        for y in range(1,11):
            tempString= chUL.curveControl('sphereCross','curve')
            chUL.resizeCurves(None, 1, 1, 1, red)
            loc = pc.rename(tempString[0], (s+'_'+type+str(y)+'_loc'))
            pc.addAttr(loc, k=0, dv=y, min=0, max=10, ln='twistPosition', at='double')
            pc.parent(loc,parent)
            
            pc.setAttr((loc+'.overrideEnabled'),1)
            pc.setAttr((loc+'.overrideColor'),10)
            
            multDivs.append(pc.createNode('multiplyDivide',n=(s+'_'+type+str(y)+'_md')))
            pc.connectAttr((multDiv+'.output'), (multDivs[y-1]+'.input1'))
            pc.connectAttr((loc+'.twistPosition'), (multDivs[y-1]+'.input2.input2X'))
            pc.setAttr((multDivs[y-1]+'.input2.input2Y'), y)
            pc.setAttr((multDivs[y-1]+'.input2.input2Z'), y)
            pc.connectAttr((multDivs[y-1]+'.output'), (loc+'.translate'))
            
            multDivsVis.append(pc.createNode('multiplyDivide',n=(s+'_'+type+str(y)+'Vis_md')))
            pc.connectAttr((s+'.'+type),(multDivsVis[y-1]+'.input1.input1X'))
            pc.setAttr((multDivsVis[y-1]+'.input2.input2X'), ((1.00/(2*y))+0.001))
            pc.connectAttr((multDivsVis[y-1]+'.outputX'), (loc+'.visibility'))
            chUL.lockAndHide(loc,'locknHide','trans rot scale vis') # TODO: make sure this works
            pc.select(cl=True)
    pc.select(sel)


def removeTwistJointsAttr(type):
    sel=pc.ls(sl=True)
    if (len(sel) == 0):
        pc.warning('Select 1 joint\n')

    for s in sel:
        if pc.attributeQuery(type,n=s,ex=True):
            try:
                twistJointGrp = pc.getAttr(s+'.twistJointGrp')
                if twistJointGrp != '':
                    if pc.objExists(twistJointGrp):
                        pc.delete(twistJointGrp)
            except:
                pc.deleteAttr(type,s,attribute=True)
                pc.deleteAttr('twistJointGrp',s,attribute=True)


def addSplineJointAttrs(type, count=7, sel=''):
    if sel == '':
        sel = pc.ls(sl=True)

    plusMinus = ''
    multDiv = ''
    loc = ''
    locShape = ''
    joints = ''
    curve = ''
    parent = ''
    tempString = []
    multDivs = []
    multDivsVis = []
    attrs = []
    jointsList = []
    red = 0.0

    if pc.attributeQuery('spineRig', n=sel, ex=True) or pc.attributeQuery('neckHeadRig', n=sel, ex=True) or pc.attributeQuery('tentacleRig', n=sel, ex=True):
        if pc.attributeQuery('spineRig', n=sel, ex=True):
            joints = pc.getAttr(sel + '.spineRig')
        elif pc.attributeQuery('neckHeadRig', n=sel, ex=True):
            joints = pc.getAttr(sel + '.neckHeadRig')
        elif pc.attributeQuery('tentacleRig', n=sel, ex=True):
            joints = pc.getAttr(sel + '.tentacleRig')
    else:
        pc.error('setup could not be installed')

    if pc.attributeQuery(type, n=sel, ex=True):
        pc.error('Twist Joints Attribute already added!\n')
    else:
        pc.addAttr(sel, k=1, ln='joints', at='long', min=0, max=25, dv=count)

    jointsList = List.seperate(joints)
    curve = chUL.jointCurve(jointsList[0], jointsList[1])
    pc.skinCluster(jointsList[0], jointsList[1], curve, tsb=True, mi=4, dr=count)
    pc.hide(curve)
    chUL.lockAndHide(curve, 'locknHide', 'trans rot scale vis')

    pc.select(cl=True)
    parent = pc.group(em=True)
    parent = pc.rename(parent, (sel + 'TwistJnt_grp'))
    pc.parent(curve, parent)

    pc.addAttr(sel, ln='twistJointGrp', dt='string')
    pc.setAttr((sel + '.twistJointGrp'), parent, type='string')

    multDiv = pc.createNode('multiplyDivide', n=(sel + 'Twist_md'))
    pc.setAttr((multDiv + '.operation'), 2)
    pc.setAttr((multDiv + '.input1X'), 10)
    pc.connectAttr((sel + '.joints'), (multDiv + '.input2X'))

    red = pc.getAttr(sel + '.radius')
    red = (red / 2)

    for y in range(1, 26):
        curveInfo = pc.pointOnCurve(curve, constructionHistory=1)
        pc.setAttr((curveInfo + '.turnOnPercentage'), 1)

        pc.select(cl=True)
        tempString = chUL.curveControl('sphereCross', 'curve')
        loc = pc.rename(tempString[0], (sel + '_' + type + str(y) + '_loc'))
        chUL.resizeCurves(None, 1, 1, 1, red)
        pc.parent(loc, parent)

        pc.setAttr((loc + '.overrideEnabled'), 1)
        pc.setAttr((loc + '.overrideColor'), 10)

        multDivs.append(pc.createNode('multiplyDivide', n=(sel + 'Twist_md')))
        pc.setAttr((multDivs[y - 1] + '.input2X'), (0.1 * y))
        pc.connectAttr((multDiv + '.outputX'), (multDivs[y - 1] + '.input1X'))
        pc.connectAttr((multDivs[y - 1] + '.outputX'), (curveInfo + '.parameter'))

        pc.connectAttr((curveInfo + '.position'), (loc + '.translate'))

        multDivsVis.append(pc.createNode('multiplyDivide', n=(sel + '_' + type + str(y) + 'Vis_md')))
        pc.connectAttr((sel + '.joints'), (multDivsVis[y - 1] + '.input1.input1X'))
        pc.setAttr((multDivsVis[y - 1] + '.input2.input2X'), ((1.00 / (2 * y)) + 0.001))
        pc.connectAttr((multDivsVis[y - 1] + '.outputX'), (loc + '.visibility'))

        chUL.lockAndHide(loc, 'locknHide', 'trans rot scale vis')
        pc.select(cl=True)

    pc.setAttr(sel + '.joints', 2)


def addSplineJointsAttrs(type):
    sel=pc.ls(sl=True)
    plusMinus = ''
    multDiv = ''
    loc = ''
    locShape = ''
    joints = ''
    curve = ''
    parent = ''
    tempString = []
    multDivs = []
    multDivsVis = []
    attrs = []
    jointsList = []
    red = 0.0

    if len(sel) > 0:
        pc.warning('Select 1 joint\n')
    for s in sel:
        if pc.attributeQuery('spineRig', n=s, ex=True) or pc.attributeQuery('neckHeadRig', n=s, ex=True) or pc.attributeQuery('tentacleRig', n=s, ex=True):
            if pc.attributeQuery('spineRig', n=s, ex=True):
                joints = pc.getAttr(s+'.spineRig')
            elif pc.attributeQuery('neckHeadRig', n=s, ex=True):
                joints = pc.getAttr(s+'.neckHeadRig')
            elif pc.attributeQuery('tentacleRig', n=s, ex=True):
                joints = pc.getAttr(s+'.tentacleRig')
        else:
            pc.error('setup could not be installed')
        
        if pc.attributeQuery(type, n=s, ex=True):
            pc.error('Twist Joints Attribute already added!\n')
        else:
            pc.addAttr(s, k=1, ln=type, at='long', min=0, max=25, dv=7)
        
        jointsList = List.seperate(joints)                
        curve = chUL.jointCurve(jointsList[0], jointsList[1])
        pc.skinCluster(jointsList[0], jointsList[1], curve, tsb=True, mi=4, dr=7)
        pc.hide(curve)
        chUL.lockAndHide(curve, 'locknHide', 'trans rot scale vis')
        
        pc.select(cl=True)
        parent = pc.group(em=True)
        parent = pc.rename(parent, (s+'TwistJnt_grp'))
        pc.parent(curve,parent)
        
        pc.addAttr(s, ln='twistJointGrp', dt='string')
        pc.setAttr((s+'.twistJointGrp'), parent, type='string')
        
        multDiv = pc.createNode('multiplyDivide',n=(s+'Twist_md'))
        pc.setAttr((multDiv+'.operation'),2)
        pc.setAttr((multDiv+'.input1X'),10)
        pc.connectAttr((s+'.'+type),(multDiv+'.input2X'))
        
        red = pc.getAttr(s+'.radius')
        red = (red/2)
        
        for y in range(1,26):
            curveInfo = pc.pointOnCurve(curve, constructionHistory=1)
            pc.setAttr((curveInfo + '.turnOnPercentage'),1)
            
            pc.select(cl=True)
            tempString = chUL.curveControl('sphereCross','curve')
            loc = pc.rename(tempString[0], (s+'_'+type+str(y)+'_loc'))
            chUL.resizeCurves(None,1,1,1,red)
            pc.parent(loc,parent)
            
            pc.setAttr((loc+'.overrideEnabled'),1)
            pc.setAttr((loc+'.overrideColor'),10)
            
            multDivs.append(pc.createNode('multiplyDivide',n=(s+'Twist_md')))
            pc.setAttr((multDivs[y-1]+'.input2X'), (0.1*y))
            pc.connectAttr((multDiv+'.outputX'), (multDivs[y-1]+'.input1X'))
            pc.connectAttr((multDivs[y-1]+'.outputX'), (curveInfo+'.parameter'))
            
            pc.connectAttr((curveInfo+'.position'), (loc+'.translate'))
            
            multDivsVis.append(pc.createNode('multiplyDivide',n=(s+'_'+type+str(y)+'Vis_md')))
            pc.connectAttr((s+'.'+type), (multDivsVis[y-1]+'.input1.input1X'))
            pc.setAttr((multDivsVis[y-1]+'.input2.input2X'), ((1.00/(2*y))+0.001))
            pc.connectAttr((multDivsVis[y-1]+'.outputX'), (loc+'.visibility'))
            
            chUL.lockAndHide(loc, 'locknHide', 'trans rot scale vis')
            pc.select(cl=True)
    pc.select(sel)