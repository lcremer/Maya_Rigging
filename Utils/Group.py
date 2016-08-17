"""
Group @ Utils
Functios used for grouping
"""
import maya.cmds as mc
import String

def CreateOffsetGrp(object, prefix = ''):

    if not prefix :
        prefix = String.removeSuffix(object)

    offsetGrp = mc.group(n = prefix + 'Offset_grp', em = 1)
    objectParents = mc.listRelatives(object, p = 1)

    if objectParents:
        mc.parent(offsetGrp, objectParents[0])

    # match object transform
    mc.delete(mc.parentConstraint(object, offsetGrp))
    mc.delete(mc.scaleConstraint(object, offsetGrp))

    # parent object under offset group
    mc.parent(object, offsetGrp)
    return offsetGrp
