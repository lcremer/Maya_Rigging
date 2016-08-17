import pymel.core as pc
import CharUtilsLib as chUL
import List

def add_dummy_twist_joints_attr(placer, dummy_parent, dummy_child, count):
    attr_type = 'twistJoints'
    multi_divs = []
    multi_divsVis = []

    if pc.attributeQuery('twistJoints', n=dummy_parent, ex=True):
        pc.error('Twist Joints Attribute already added!\n')
    else:
        pc.addAttr(dummy_parent, k=1, ln=attr_type, at='long', min=0, max=10, dv=count)

    child_loc = pc.spaceLocator(n=dummy_child+"Loc")
    pc.parent(child_loc, dummy_parent)
    pc.parentConstraint(dummy_child, child_loc, weight=1)
    pc.hide(child_loc)

    parent = pc.group(em=True)
    parent = pc.rename(parent, (dummy_parent + "TwistJnt_grp"))
    pc.parent(parent, placer)
    pc.parentConstraint(dummy_parent, parent, weight=1)
    pc.addAttr(dummy_parent, ln='twistJointGrp', dt='string')
    pc.setAttr((dummy_parent + '.twistJointGrp'), parent, type='string')

    plusMinus = pc.createNode('plusMinusAverage', n=(dummy_parent + 'Twist_pma'), )
    pc.connectAttr((dummy_parent + '.' + attr_type), (plusMinus + '.input1D[0]'))
    pc.setAttr((plusMinus + '.input1D[1]'), 1)
    multDiv = pc.createNode('multiplyDivide', n=(dummy_parent + 'Twist_md'))
    pc.setAttr((multDiv + '.operation'), 2)
    pc.connectAttr((child_loc + '.translate'), (multDiv + '.input1'))
    pc.connectAttr((plusMinus + '.output1D'), (multDiv + '.input2.input2X'))
    pc.connectAttr((plusMinus + ".output1D"), (multDiv + '.input2.input2Y'))
    pc.connectAttr((plusMinus + '.output1D'), (multDiv + '.input2.input2Z'))
    pc.select(cl=True)

    red = pc.getAttr(dummy_parent + '.radius')
    red = (red / 2)

    for y in range(1, 11):
        tempString = chUL.curveControl('sphereCross', 'curve')
        chUL.resizeCurves(None, 1, 1, 1, red)
        loc = pc.rename(tempString[0], (dummy_parent + '_' + attr_type + str(y) + '_loc'))
        pc.addAttr(loc, k=0, dv=y, min=0, max=10, ln='twistPosition', at='double')
        pc.parent(loc, parent)

        pc.setAttr((loc + '.overrideEnabled'), 1)
        pc.setAttr((loc + '.overrideColor'), 10)

        multi_divs.append(pc.createNode('multiplyDivide', n=(dummy_parent + '_' + attr_type + str(y) + '_md')))
        pc.connectAttr((multDiv + '.output'), (multi_divs[y - 1] + '.input1'))
        pc.connectAttr((loc + '.twistPosition'), (multi_divs[y - 1] + '.input2.input2X'))
        pc.setAttr((multi_divs[y - 1] + '.input2.input2Y'), y)
        pc.setAttr((multi_divs[y - 1] + '.input2.input2Z'), y)
        pc.connectAttr((multi_divs[y - 1] + '.output'), (loc + '.translate'))

        multi_divsVis.append(pc.createNode('multiplyDivide', n=(dummy_parent + '_' + attr_type + str(y) + 'Vis_md')))
        pc.connectAttr((dummy_parent + '.' + attr_type), (multi_divsVis[y - 1] + '.input1.input1X'))
        pc.setAttr((multi_divsVis[y - 1] + '.input2.input2X'), ((1.00 / (2 * y)) + 0.001))
        pc.connectAttr((multi_divsVis[y - 1] + '.outputX'), (loc + '.visibility'))
        chUL.lockAndHide(loc, 'locknHide', 'trans rot scale vis')
        pc.select(cl=True)


def add_dummy_spline_joints_attrs(placer, dummy_parent, dummy_child, count):
    attr_type = 'twistJoints'
    multDivs = []
    multDivsVis = []

    if pc.attributeQuery(attr_type, n=dummy_parent, ex=True):
        pc.error('Twist Joints Attribute already added!\n')
    else:
        pc.addAttr(dummy_parent, k=1, ln=attr_type, at='long', min=0, max=25, dv=count)

    curve = chUL.jointCurve(dummy_parent, dummy_child)
    pc.skinCluster(dummy_parent, dummy_child, curve, tsb=True, mi=4, dr=7)
    pc.hide(curve)
    chUL.lockAndHide(curve, 'locknHide', 'trans rot scale vis')

    pc.select(cl=True)
    parent = pc.group(em=True)
    parent = pc.rename(parent, (dummy_parent + 'TwistJnt_grp'))
    pc.parent(parent, placer)
    pc.parent(curve, parent)

    pc.addAttr(dummy_parent, ln='twistJointGrp', dt='string')
    pc.setAttr((dummy_parent + '.twistJointGrp'), parent, type='string')

    multDiv = pc.createNode('multiplyDivide', n=(dummy_parent + 'Twist_md'))
    pc.setAttr((multDiv + '.operation'), 2)
    pc.setAttr((multDiv + '.input1X'), 10)
    pc.connectAttr((dummy_parent + '.' + attr_type), (multDiv + '.input2X'))

    red = pc.getAttr(dummy_parent + '.radius')
    red = (red / 2)

    for y in range(1, 26):
        curveInfo = pc.pointOnCurve(curve, constructionHistory=1)
        pc.setAttr((curveInfo + '.turnOnPercentage'), 1)

        pc.select(cl=True)
        tempString = chUL.curveControl('sphereCross', 'curve')
        loc = pc.rename(tempString[0], (dummy_parent + '_' + attr_type + str(y) + '_loc'))
        chUL.resizeCurves(None, 1, 1, 1, red)
        pc.parent(loc, parent)

        pc.setAttr((loc + '.overrideEnabled'), 1)
        pc.setAttr((loc + '.overrideColor'), 10)

        multDivs.append(pc.createNode('multiplyDivide', n=(dummy_parent + 'Twist_md')))
        pc.setAttr((multDivs[y - 1] + '.input2X'), (0.1 * y))
        pc.connectAttr((multDiv + '.outputX'), (multDivs[y - 1] + '.input1X'))
        pc.connectAttr((multDivs[y - 1] + '.outputX'), (curveInfo + '.parameter'))

        pc.connectAttr((curveInfo + '.position'), (loc + '.translate'))

        multDivsVis.append(pc.createNode('multiplyDivide', n=(dummy_parent + '_' + attr_type + str(y) + 'Vis_md')))
        pc.connectAttr((dummy_parent + '.' + attr_type), (multDivsVis[y - 1] + '.input1.input1X'))
        pc.setAttr((multDivsVis[y - 1] + '.input2.input2X'), ((1.00 / (2 * y)) + 0.001))
        pc.connectAttr((multDivsVis[y - 1] + '.outputX'), (loc + '.visibility'))

        chUL.lockAndHide(loc, 'locknHide', 'trans rot scale vis')
        pc.select(cl=True)