"""
Locator @ Utils
Utility functions for creating locators
"""

import pymel.core as pc

def CenterSelection(selections = None):
    """
    Creates a locator at the center of objects, in given list, or selected
    @param selections: list (str), list of objects used for center
    @return: none
    """
    if not selections:
        selections = pc.selected()
            
    bb = pc.exactWorldBoundingBox(selections)
    o = [0.0, 0.0, 0.0]
    o[0] = ((bb[3]+bb[0])/2)
    o[1] = ((bb[4]+bb[1])/2)
    o[2] = ((bb[5]+bb[2])/2)
    
    newLoc = pc.spaceLocator((o[0], o[1], o[2]))
    pc.xform(newLoc[0],cp=True)    

# TODO: rename these
def Snap(master, slave):    
    s = []
    if master == '' or slave == '':
        s = pc.selected()
        master = s[0]
        slave = s[1]
                    
    oCons = pc.orientConstraint(master,slave,w=1.0)
    pCons = pc.parentConstraint(master,slave,w=1.0)
    pc.refresh()

    pc.delete(oCons)
    pc.delete(pCons)

def NdsSnap(master, slave):
    s = pc.selected()
    if master == '' or slave == '':
        master = s[0]
        slave = s[1]

    if master == '' or slave == '':
        return
    
    xt = pc.getAttr(master+".translate")
    xr = pc.getAttr(master+".rotate")
    pc.setAttr(slave+".translateX",(xt[0]))
    pc.setAttr(slave+".translateY",(xt[1]))
    pc.setAttr(slave+".translateZ",(xt[2]))
    pc.setAttr(slave+".rotateX",(xr[0]))
    pc.setAttr(slave+".rotateY",(xr[1]))
    pc.setAttr(slave+".rotateZ",(xr[2]))

def AnimSnap(master, slave):
    s = pc.selected()
    if master == '' or slave == '':
        master = s[0]
        slave = s[1]

    d = pc.duplicate(master,slave,rc=True,rr=True)
    dupeSlave = d[0]

    Snap(master,dupeSlave)
    NdsSnap(dupeSlave,slave)
    pc.delete(dupeSlave)