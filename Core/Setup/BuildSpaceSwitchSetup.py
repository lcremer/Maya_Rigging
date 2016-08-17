import pymel.core as pc
# import re

from ...Utils.CharUtilsLib import lockAndHide

def buildSpaceSwitchSetup(node, parent, parentSpace, spaceName, spaceType):

    name = ''
    for s in spaceName:
        name += (s+':')

    if spaceType==1:
        try:
            pc.addAttr(node, ln='SpaceSwitch', at='enum', en='---------', keyable=True)
            pc.setAttr((node+'.SpaceSwitch'), keyable=False, channelBox=True)
        except:
            pass

        pc.addAttr(node, ln='parent', at='enum', en=name, keyable=True)
        lockAndHide(parent,'unLock','trans rot')
        
        con = pc.parentConstraint(parentSpace, parent, mo=True, w=1)
        lockAndHide(parent, 'lock', 'trans rot')

        for i in range(len(parentSpace)):
            cnd = pc.createNode('condition', n=(node+'SpaceSwitch_'+str(i)+'_cnd'))
            pc.setAttr((cnd + '.secondTerm'), i)
            pc.setAttr((cnd + '.colorIfTrueR'), 1)
            pc.setAttr((cnd + '.colorIfFalseR'), 0)
            pc.connectAttr((node + '.parent'), (cnd + '.firstTerm'))
            pc.connectAttr((cnd + '.outColorR'), (con + '.w' +str(i)))

    elif spaceType==2:
        try:
            pc.addAttr(node, ln='SpaceSwitch', at='enum', en='---------', keyable=True)
            pc.setAttr((node+'.SpaceSwitch'), keyable=False, channelBox=True)
        except:
            pass

        pc.addAttr(node, ln='rotateLock', at='enum', en=name, keyable=True)
        lockAndHide(parent, 'unLock', 'trans rot')
        
        con = pc.parentConstraint(parentSpace, parent, mo=True, st=['x','y','z'], w=1)        
        lockAndHide(parent,'lock','trans rot')

        for i in range(len(parentSpace)):
            cnd = pc.createNode('condition', n=(node+'RotateSwitch_'+str(i)+'_cnd'))
            pc.setAttr((cnd + '.secondTerm'), i)
            pc.setAttr((cnd + '.colorIfTrueR'), 1)
            pc.setAttr((cnd + '.colorIfFalseR'), 0)
            pc.connectAttr((node + '.rotateLock'), (cnd + '.firstTerm'))
            pc.connectAttr((cnd + '.outColorR'), (con + '.w' +str(i)))

    elif spaceType==3:
        try:
            pc.addAttr(node, ln='SpaceSwitch', at='enum', en='---------', keyable=True)
            pc.setAttr((node+'.SpaceSwitch'), keyable=False, channelBox=True)
        except:
            pass

        pc.addAttr(node, ln='transLock', at='enum', en=name, keyable=True)
        pc.addAttr(node, ln='rotateLock', at='enum', en=name, keyable=True)
        
        lockAndHide(parent,'unLock','trans rot')
        rotCon = pc.parentConstraint(parentSpace, parent, mo=True, w=1, st=['x','y','z'])
        posCon = pc.parentConstraint(parentSpace, parent, mo=True, w=1, sr=['x','y','z'])
        lockAndHide(parent,'lock','trans rot')

        for i in range(len(parentSpace)):
            cnd1 = pc.createNode('condition', n=(node+'TransSwitch_'+str(i)+'_cnd'))
            pc.setAttr((cnd1 + '.secondTerm'), i)
            pc.setAttr((cnd1 + '.colorIfTrueR'), 1)
            pc.setAttr((cnd1 + '.colorIfFalseR'), 0)
            pc.connectAttr((node + '.transLock'), (cnd1 + '.firstTerm'))
            cnd2 = pc.createNode('condition', n=(node+'RotateSwitch_'+str(i)+'_cnd'))
            pc.setAttr((cnd2 + '.secondTerm'), i)
            pc.setAttr((cnd2 + '.colorIfTrueR'), 1)
            pc.setAttr((cnd2 + '.colorIfFalseR'), 0)
            pc.connectAttr((node + '.rotateLock'), (cnd2 + '.firstTerm'))
            pc.connectAttr((cnd1 + '.outColorR'), (posCon + '.w' +str(i)))
            pc.connectAttr((cnd2 + '.outColorR'), (rotCon + '.w' +str(i)))