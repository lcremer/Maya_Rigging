"""
Pivot @ Utils
Functions used for manipulating Pivots
"""

import maya.cmds as mc

# TODO: It should be expanded to allow choosing between setting the base of the pivot with different Axis
# either at the origin or within the bounds of the object
def CenterPivotAtBase(selections = None, all = False):
    """
    Tool was made to solve the common issue of Model assets not having pivot setup for use in game editor
    @param selections: list of objects that pivot should be placed at the center of their base
    @param all: if all is True, selections is ignored and all mesh objects are selected and moved to origin with pivot at origin
    """

    if all:
        # get polymesh object list
        # go through each element get center
        # set pivot to center with y offset to bottom
        #   Later add UI to select base axis
        # export each object seperatly as FBX into current dir

        # getting all transforms
        transforms = cmds.ls(tr = True)
        # filtering for polymeshes
        meshes = cmds.filterExpand(transforms, sm = 12);

        # centering pivot at base for all polymeshes
        #   Getting bounding box from object
        # {0 = xmin, 1 = ymin, 2 zmin, 3 = xmax, 4 = ymax, 5 = zmax}
        # Center
        # pos = [(bBox[3]+bBox[0])/2, (bBox[4]+bBox[3])/2, (bBox[5]+bBox[2])/2]

        # Note if it is prefered to set the base pivot to the y origin
        # set pos[1] to 0
        for index in range(len(meshes)):
            bBox = mc.exactWorldBoundingBox(meshes[index])
            pos = [(bBox[3]+bBox[0])/2, bBox[1], (bBox[5]+bBox[2])/2]
            #pos = [0, bBox[1], 0]
            mc.select(meshes[index])
            mc.xform(piv = (pos[0], pos[1], pos[2]), ws = True)

        return

    # TODO: implement this
    if not selections:
        selections = mc.ls(tr = 1)

        return
