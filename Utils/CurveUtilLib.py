import maya.mel
from Maya_UtilLib.Controls import string_to_shape

from Transform import *
from String import *


# TODO: this should all be moved to UtilLib


# TODO: create shapeMethod that returns string name instead of requiring the string be passed in
# TODO: or create a Curve Shape Util class that has methods for each shape
# TODO: also look into if controlColor can be defaulted to none instead of ''
def curveControl(shape, objType, controlColor=''):
    selection = pc.ls(sl=True, tr=True)
    new_controls = []
    sel = len(selection)

    if sel == 0:
        sel = 1

    for i in range(sel):
        control = c = string_to_shape(shape)

        if objType == 'curve':
            if len(selection) > 0:
                Snap(selection[i], control)
            new_controls.append(control)

        if objType == 'joint':
            pc.select(cl=True)
            jnt = pc.joint()
            pc.setAttr(jnt + '.radius', 0.07)
            pc.select(cl=True)
            pc.makeIdentity(jnt, apply=True, t=1, r=1, s=1, n=0)
            shape = pc.listRelatives(control, f=True, s=True)
            pc.parent(shape[0], jnt, r=True, s=True)
            pc.delete(control)
            jnt = pc.rename(jnt, control)
            if len(selection) > 0:
                Snap(selection[i], jnt)
                pc.makeIdentity(jnt, apply=True, t=1, r=1, s=1, n=0)
            new_controls.append(jnt)
            c = jnt

        if controlColor != '':
            try:
                c.overrideEnabled.set(True)
                c.overrideColor.set(controlColor)
            except:
                pass
            try:
                c.getShape().overrideEnabled.set(True)
                c.getShape().overrideColor.set(controlColor)
            except:
                pass

    pc.select(new_controls, r=True)
    return new_controls


def shapeReplace(obj, crvShp):
    sel = []
    shape = []

    if obj == '':
        sel = pc.ls(sl=True)
    else:
        sel.append(obj)

    for j in sel:
        shape = pc.listRelatives(j, f=True, s=True)
        if len(shape) > 0:
            pc.delete(shape)
            shapeParent(j, crvShp)


def shapeRename(obj):
    sel = []
    shape = []

    if obj == '*':
        pc.select(pc.listTransforms(type='nurbsCurve'), r=True)
        sel = pc.ls(sl=True)
    elif obj == '':
        sel = pc.ls(sl=True)
    else:
        sel.append(obj)

    for j in sel:
        shape = pc.listRelatives(j, f=True, s=True)
        if len(shape) < 2:
            pc.rename(shape[0], j + 'Shape')
        else:
            for i in range(len(shape)):
                pc.rename(shape[i], j + 'Shape' + (str(i + 1)))


def resizeCurves(curves, x, y, z, scale):
    scaleDiv = scale / 1.0
    scaleX = 0.0
    scaleY = 0.0
    scaleZ = 0.0

    if x:
        scaleX = scaleDiv
    else:
        scaleX = 1.0
    if y:
        scaleY = scaleDiv
    else:
        scaleY = 1.0
    if z:
        scaleZ = scaleDiv
    else:
        scaleZ = 1.0

    isCrvS = ''
    isCrvC = ''

    if curves == None or len(curves) < 1:
        curves = pc.ls(sl=True)

    for c in curves:
        curveCheck = 0
        shapes = pc.listRelatives(c, ni=True, s=True)
        for sel in shapes:
            isCrvS = pc.nodeType(sel)
            if isCrvS == 'nurbsCurve':
                curveCheck = 1
                break
        isCrvC = pc.nodeType(c)
        if isCrvC == 'nurbsCurve':
            curveCheck = 1
        if curveCheck == 1:
            temp = c
            if '.cv' not in str(c):
                temp = str(c) + '.cv[*]'
            else:
                temp = c
            pc.select(temp, r=True)  #
            pc.scale((scaleX, scaleY, scaleZ), r=True)
            pc.select(cl=True)
    pc.select(curves, r=True)


def editCurveTransform(axis, mode, deg):
    selection = pc.ls(sl=True)

    for sel in selection:
        shape = pc.listRelatives(sel, s=True)
        objType = pc.objectType(shape[0])
        if objType == 'nurbsCurve':
            pc.select(sel + '.cv[*]', r=True)
            if axis == 'X':
                if mode == 'move':
                    pc.move(deg, 0, 0, r=True, os=True)
                    pc.select(sel, r=True)
                if mode == 'rotate':
                    pc.rotate((deg, 0, 0), os=True)
            if axis == 'Y':
                if mode == 'move':
                    pc.move(0, deg, 0, r=True, os=True)
                    pc.select(sel, r=True)
                if mode == 'rotate':
                    pc.rotate((0, deg, 0), os=True)
            if axis == 'Z':
                if mode == 'move':
                    pc.move(0, 0, deg, r=True, os=True)
                    pc.select(sel, r=True)
                if mode == 'rotate':
                    pc.rotate((0, 0, deg), os=True)


def getSelectedCurve():
    ret = ''
    objs = pc.ls(sl=True, type='transform')

    for ob in objs:
        shape = pc.listRelatives(ob, f=True, s=True)
        if pc.nodeType(shape[0]) == 'nurbsCurve' and ret == '':
            ret = ob
        else:
            pc.error('selected Object is not curve')

    return ret


def shapeParent(obj, crvShape, controlColor=''):
    sel = []
    shape = []
    temp = []

    if obj == '':
        sel = pc.ls(sl=True)
    else:
        sel.append(obj)

    for j in sel:
        pc.select(cl=True)
        temp = curveControl(crvShape, 'curve', controlColor)
        Snap(j, temp[0])
        shape = pc.listRelatives(temp[0], f=True, s=True)
        pc.parent(shape[0], j, r=True, s=True)
        pc.delete(temp[0])
        shapeRename(j)
        pc.select(cl=True)


def UDShapeParent():
    sel = pc.ls(sl=True)
    if len(sel) <= 0:
        pc.error('Select shape then transform and try again')

    shape = pc.listRelatives(sel[0], f=True, s=True)
    for s in shape:
        pc.parent(s, sel[1], add=True, s=True)
    pc.delete(sel[0])
    shapeRename(sel[1])


# TODO: create something that saves a custom text file with pos data and curve name
# creates control curve button saved at top shelf
def curveControlMaker():
    gShelfTopLevel = maya.mel.eval('$tmpVar=$gShelfTopLevel')
    buttonName = ''

    curve = getSelectedCurve()
    openClose = pc.getAttr(curve + '.form')
    if openClose != 0:
        pc.closeCurve(curve, ch=1, ps=1, rpo=1, bb=0.5, bki=0, p=0.1)
    degree = pc.getAttr(curve + '.degree')
    span = pc.getAttr(curve + '.spans')
    cvs = degree + span
    pos = []

    i = 0

    for i in range(cvs):
        cvPos = pc.getAttr(curve + ('.cv[' + str(i) + ']'))  # TODO: see how pymel can improve this.
        pos.append(cvPos)

    result = pc.promptDialog(title='Shelf Button Name',
                             message='Enter Name:',
                             button=['OK', 'Cancel'],
                             defaultButton='OK',
                             cancelButton='Cancel',
                             dismissString='Cancel')

    if result == 'OK':
        buttonName = pc.promptDialog(q=True, text=True)
        if pc.tabLayout(gShelfTopLevel, exists=True):
            pc.shelfButton(parent=(gShelfTopLevel + '|' + pc.tabLayout(gShelfTopLevel, q=True, st=True)),
                           command=(pc.Callback(pc.curve, d=degree, p=pos)),
                           iol=buttonName,
                           label=(buttonName + ' curve'),
                           annotation=(buttonName + ' curve'))
            # pc.saveAllShelves( gShelfTopLevel )
        else:
            pc.error('Must have active shelf to create shelf button')


def fixFacingAxis(facingAxis, neg):
    flip = 0
    deg = 90
    if neg == 1:
        deg = -90
    if facingAxis == 'X' and neg == 1:
        editCurveTransform('Y', 'rotate', 180)
    elif facingAxis == 'Y':
        editCurveTransform('Z', 'rotate', deg)
    elif facingAxis == 'Z':
        editCurveTransform('Y', 'rotate', deg)


def locknHide(n, trans, rot, scale, vis):
    sel = []

    if n == '':
        sel = pc.ls(sl=True)
    else:
        sel.append(n)

    for s in sel:
        if trans == 1:
            pc.setAttr(s + '.tx', lock=True, keyable=False)
            pc.setAttr(s + '.ty', lock=True, keyable=False)
            pc.setAttr(s + '.tz', lock=True, keyable=False)
        if rot == 1:
            pc.setAttr(s + '.rx', lock=True, keyable=False)
            pc.setAttr(s + '.ry', lock=True, keyable=False)
            pc.setAttr(s + '.rz', lock=True, keyable=False)
        if scale == 1:
            pc.setAttr(s + '.sx', lock=True, keyable=False)
            pc.setAttr(s + '.sy', lock=True, keyable=False)
            pc.setAttr(s + '.sz', lock=True, keyable=False)
        if vis == 1:
            pc.setAttr(s + '.v', lock=True, keyable=False)
