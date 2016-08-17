import pymel.core as pc

from ..Utils import CharUtilsLib as charLib
from ..Utils import List as List
from RiggingSystem.Core.Dummy import Util
# from ..Utils.CharUtilsLib import charLib.lockAndHide

# moduleSymmetryConnect l_footPlacer_loc r_footPlacer_loc
def moduleSymmetryConnector(master, slave):
    masterList = ''
    masterJointsList = []
    slaveList = ''
    slaveJointsList = []

    if pc.attributeQuery('jointPosList', n=master, ex=True):
        charLib.lockAndHide(slave,'unLock','trans rot')
        
        masterList = pc.getAttr(master + '.jointPosList')
        masterJointsList = List.seperate(masterList)
        
        slaveList = pc.getAttr(slave + '.jointPosList')
        slaveJointsList = List.seperate(slaveList)

        charLib.connectMirrorTrans(master,slave,0) # NOTE: this is potentially creating duplicate connections
        charLib.connectMirrorRot(master,slave,1)
        charLib.connectMirrorRot(master,slave,2)
        pc.connectAttr((master+'.ty'),(slave+'.ty'))
        pc.connectAttr((master+'.tz'),(slave+'.tz'))
        pc.connectAttr((master+'.rx'),(slave+'.rx'))
        pc.connectAttr((master+'.s'),(slave+'.s'))
        
        if len(masterJointsList) == len(slaveJointsList):
            for i in range(len(masterJointsList)):                
                if(masterJointsList[i]):
                    charLib.lockAndHide(slaveJointsList[i],'unLock', 'trans rot')
                    charLib.connectMirrorTrans(masterJointsList[i], slaveJointsList[i], 0) # NOTE: when its called again here
                    try:
                        pc.connectAttr((masterJointsList[i]+'.ty'),(slaveJointsList[i]+'.ty'),f=True)
                        pc.connectAttr((masterJointsList[i]+'.tz'),(slaveJointsList[i]+'.tz'),f=True)
                        pc.connectAttr((masterJointsList[i]+'.s'),(slaveJointsList[i]+'.s'),f=True)
                    except:
                        pass

# string $master = "l_wristPlacer_loc";
# string $slave = "r_wristPlacer_loc";

# buildFingerModuleSymmetry $master $slave

def buildFingerModuleSymmetry(master, slave):
    moduleSymmetryConnector(master, slave)
    createChildAttrModuleSymmetry(master, slave)
    masterChildList = pc.getAttr(master + '.child')
    masterJointsLists = List.seperate(masterChildList)
    slaveChildList = pc.getAttr(slave + '.child')
    slaveJointsLists = List.seperate(slaveChildList)

    for i in len(masterJointsLists):
        createChildAttrModuleSymmetry(masterJointsLists[i], slaveJointsLists[i])

    thumbMaster = pc.getAttr(master + '.thumb')
    thumbSlave = pc.getAttr(slave + '.thumb')
    moduleSymmetryConnector(thumbMaster,thumbSlave)

def createChildAttrModuleSymmetry(master, slave):
    
    if pc.attributeQuery('child', n=master, ex=True):
        masterChildList = pc.getAttr(master + '.child')
        masterJointsLists = List.seperate(masterChildList)
        slaveChildList = pc.getAttr(slave + '.child')
        slaveJointsLists = List.seperate(slaveChildList)

        for i in range(len(masterJointsLists)):
            if(masterJointsLists[i]):
                moduleSymmetryConnector(masterJointsLists[i], slaveJointsLists[i])
    else:
        pc.error('Given object is not installed for current operation')

def buildArmModuleSymmetry(master, slave):
    moduleSymmetryConnector(master, slave)
    if pc.attributeQuery('child', n=master, ex=True):
        createChildAttrModuleSymmetry(master,slave)

    masterWristlist = pc.getAttr(master + '.wristPlacer')
    slaveWristlist = pc.getAttr(slave + '.wristPlacer')

    moduleSymmetryConnector(masterWristlist, slaveWristlist)

    # add house keeping attributes 
    pc.addAttr(slave, ln='symmetry', dt='string')
    pc.setAttr((slave+'.symmetry'), master, type='string')
    pc.addAttr(master, ln='doSymmetry', dt='string')
    pc.setAttr((master+'.doSymmetry'),slave, type='string')

def buildLegModuleSymmetry(master, slave):
    moduleSymmetryConnector(master, slave)

    if pc.attributeQuery('child', n=master, ex=True):
        createChildAttrModuleSymmetry(master, slave)
        
    masterFootlist = pc.getAttr(master + '.footPlacer')
    slaveFootlist = pc.getAttr(slave + '.footPlacer')
    
    moduleSymmetryConnector(masterFootlist, slaveFootlist)
    # add house keeping attributes 
    pc.addAttr(slave, ln='symmetry', dt='string')
    pc.setAttr((slave+'.symmetry'), master, type='string')
    pc.addAttr(master, ln='doSymmetry', dt='string')
    pc.setAttr((master+'.doSymmetry'), slave, type='string')

def buildBodyModuleSymmetry(master, slave):
    moduleSymmetryConnector(master, slave)

    if pc.attributeQuery('child', n=master, ex=True):
        createChildAttrModuleSymmetry(master, slave)

    # add house keeping attributes 
    pc.addAttr(slave, ln='symmetry', dt='string')
    pc.setAttr((slave+'.symmetry'), master, type='string')
    pc.addAttr(master, ln='doSymmetry', dt='string')
    pc.setAttr((master+'.doSymmetry'),slave, type='string')

# TODO: Clean this crap up
# connect components...
# The idea here is that by add parent attr to the second selection dat way 
# in skeleton creation respetive module will know its parent...
# and create dummyBone for visual representation...
def connectModuleComponents(master, slave):

    sel = []
    dummyBoneGrp = ''

    # get selection
    sel = pc.ls(sl=True)
    if master == '' or slave == '':
        master = sel[1]
        slave = sel[0]

    if pc.attributeQuery('jointPosList',n=slave,ex=True):    
        pc.addAttr(slave, ln='parent', dt='string')
        pc.setAttr((slave+ ".parent"), master, type='string')
        jointPosList = pc.getAttr(slave + '.jointPosList')
        jointPosLists = List.seperate(jointPosList)
        dummyBoneGrp = Util.createDummyBone(slave,'',master,jointPosLists[0])
        pc.setAttr((dummyBoneGrp+".inheritsTransform"),0)
        pc.parent(dummyBoneGrp,slave, r=True)
        print('Operation successful: '+master+' rig module is now connected to '+slave+'.\n')
    else:
        pc.error('Given object is not installed for current operation')

# TODO: consolidate functionality
def connectModuleComponentsUI(master, slave):
    # get selection
    if master == '' or slave == '':
        sel = pc.ls(sl=True)
        master = sel[1]
        slave = sel[0]
    
    if pc.attributeQuery('jointPosList', n=slave, ex=True) and pc.attributeQuery('child', n=slave, ex=True):
        print('slave:')
        print(slave)
        pc.addAttr(slave, ln='parent', dt='string')
        pc.setAttr((slave + ".parent"), master, type='string')
        jointPosList = pc.getAttr(slave + '.jointPosList')
        jointPosLists = List.seperate(jointPosList)
        dummyBoneGrp = Util.createDummyBone(slave, '', master, jointPosLists[0])
        pc.setAttr((dummyBoneGrp+".inheritsTransform"), 0)
        pc.parent(dummyBoneGrp,slave, r=True)
        print('Operation successful: '+master+' rig module is now connected to '+slave+'.\n')
    elif pc.attributeQuery('jointPosList', n=master, ex=True) and pc.attributeQuery('child', n=master, ex=True):
        print('master:')
        print(master)
        pc.addAttr(master, ln='parent', dt='string')
        pc.setAttr((master + ".parent"), slave, type='string')
        jointPosList = pc.getAttr(master + '.jointPosList')
        jointPosLists = List.seperate(jointPosList)
        dummyBoneGrp = Util.createDummyBone(master, '', slave, jointPosLists[0])
        pc.setAttr((dummyBoneGrp+".inheritsTransform"), 0)
        pc.parent(dummyBoneGrp,master, r=True)
        print('Operation successful: '+slave+' rig module is now connected to '+master+'.\n')
    else:
        pc.error('Failed to connect componants')

def addToModuleComponentsHierarchy(master, slave):
    sel = []

    # get selection
    sel = pc.ls(sl=True)
    if master == '' or slave == '':
        master = sel[1]
        slave = sel[0]

    if pc.attributeQuery('moduleTag', n=master, ex=True):
        if not pc.attributeQuery('child', n=master, ex=True):
            pc.addAttr(master, ln='child', dt='string')
        
        moduleParts = pc.getAttr(master + '.child')
        pc.setAttr((master + '.child'), (moduleParts+' '+slave), type='string')
        print('Operation successful: '+master+' rig module is now added to '+slave+' skeleton creation hierarchy.\n')	    
    else:
        pc.error(sel[1]+' is not installed for current operation')

# this proc will search for attr and disconnect objects from that list
def breakDummyBoneSymConnection(object):
    if pc.attributeQuery('jointPosList', n=object, ex=True):
        jointPosList = pc.getAttr(object + '.jointPosList')
        jointPosLists = List.seperate(jointPosList)
        
        for j in jointPosLists:
            distanationX = pc.listConnections((j+'.tx'), s=1, p=1)
            distanationY = pc.listConnections((j+'.ty'), s=1, p=1)
            distanationZ = pc.listConnections((j+'.tz'), s=1, p=1)
            distanationS = pc.listConnections((j+'.s'), s=1, p=1)
            node = pc.listConnections((j+'.tx'), s=1)
            try:
                pc.disconnectAttr(distanationX[0] (j+'.tx'))
                pc.disconnectAttr(distanationY[0] (j+'.ty'))
                pc.disconnectAttr(distanationZ[0] (j+'.tz'))
                pc.disconnectAttr(distanationS[0] (j+'.s'))
            except:
                pass
            pc.delete(node[0])

# this proc will disconnect symmetry for mainplacer control
def breakMainConSymConnection(control):
    distTx = pc.listConnections((control+'.tx'), s=1, p=1)
    distRy = pc.listConnections((control+'.ry'), s=1, p=1)
    distRz = pc.listConnections((control+'.rz'), s=1, p=1)

    nodeTx = pc.listConnections((control+'.tx'), s=1)
    nodeRy = pc.listConnections((control+'.ry'), s=1)
    nodeRz = pc.listConnections((control+'.rz'), s=1)

    pc.disconnectAttr(distTx[0], (control+'.tx'))
    pc.disconnectAttr(distRy[0], (control+'.ry'))
    pc.disconnectAttr(distRz[0], (control+'.rz'))

    distTy = pc.listConnections((control+'.ty'), s=1, p=1)
    distTz = pc.listConnections((control+".tz"), s=1, p=1)
    distRx = pc.listConnections((control+'.rx'), s=1, p=1)
    distS = pc.listConnections((control+'.s'), s=1, p=1)

    try:
        pc.disconnectAttr(distTy[0], (control+'.ty'))
        pc.disconnectAttr(distTz[0], (control+'.tz'))
        pc.disconnectAttr(distRx[0], (control+'.rx'))
        pc.disconnectAttr(distS[0], (control+'.s'))
    except:
        pass

    #CBdeleteConnection($control+".ty");
    #CBdeleteConnection($control+".tz");
    #CBdeleteConnection($control+".rx");
    #CBdeleteConnection($control+".s");

    pc.delete(nodeTx[0])
    pc.delete(nodeRy[0])
    pc.delete(nodeRz[0])

    if pc.attributeQuery('symmetry', n=control, ex=True):
        symm = pc.getAttr(control+'.symmetry')
        try:
            pc.deleteAttr('symmetry',control,attribute=True)
            pc.deleteAttr('doSymmetry',symm,attribute=True)
        except:
            pass
            	    

# now this one is tricky this will break symmetry for main object as well all chid objects also
def breakModuleComponentsSymConnection(con):
    breakMainConSymConnection(con)
    if pc.attributeQuery('jointPosList', n=con, ex=True):
        breakDummyBoneSymConnection(con)

    if pc.attributeQuery('child', n=con, ex=True):
        objectChildList = pc.getAttr(con+ '.child')
        objectJointsLists = List.seperate(objectChildList)
        
        for o in objectJointsLists:
            breakMainConSymConnection(o)
            breakDummyBoneSymConnection(o)

# this main proc for breaking symmetry for any modules
def breakModuleSymConnection(obj):
    
    sel = []
    # check for selection
    if obj== '':
        sel = pc.ls(sl=True)
    else:
        sel[0] = obj

    breakModuleComponentsSymConnection(sel[0])

    if pc.attributeQuary('wristPlacer', n=sel[0], ex=True):
        masterWrist = pc.getAttr(sel[0]+ '.wristPlacer')
        breakMainConSymConnection(masterWrist)

    if pc.attributeQuary('footPlacer', n=sel[0], ex=True):
        masterFoot = pc.getAttr(sel[0]+ '.footPlacer')
        breakMainConSymConnection(masterFoot)

    print('Operation successful: '+obj+' is now non-symmetrical.\n')

def deleteModules():    
    sel = pc.ls(sl=True)
    for s in sel:
        getModuleTag = pc.getAttr(s+'.moduleTag')
        getBuildTag = pc.getAttr(s+'.buildTag')
        print('Deleting dummy rig module: '+s+'.\n')
        
        if(getModuleTag == 'arm'):
            moduleList = pc.getAttr(getBuildTag+'.'+getModuleTag)
            newModuleList = moduleList.replace(' '+s,'') # TODO: this may not work
            pc.setAttr((getBuildTag+'.'+getModuleTag), newModuleList, type='string')
            
            armJointList = pc.getAttr(s+'.jointPosList')
            armJointListArray = List.seperate(armJointList)
            
            pc.delete(armJointListArray[0])
            pc.delete(s)		    
        elif getModuleTag == 'bipedLeg':
            moduleList = pc.getAttr(getBuildTag+'.leg')
            newModuleList = moduleList.replace(' '+s,'')
            pc.setAttr((getBuildTag+'.leg'), newModuleList, type='string')
            pc.delete(s)
        elif getModuleTag == 'quadLeg':
            moduleList = pc.getAttr(getBuildTag+'.leg')
            newModuleList = moduleList.replace(' '+s,'')
            pc.setAttr((getBuildTag+".leg"), newModuleList, type='string')
            pc.delete(s)
        elif getModuleTag == 'finger':
            if getBuildTag != '':
                moduleList = pc.getAttr(getBuildTag+'.child')
                newModuleList = moduleList.replace(s,"")
                pc.setAttr((getBuildTag+'.child'), newModuleList, type='string')
                pc.delete(s)
        else:
            moduleList = pc.getAttr(getBuildTag+'.'+getModuleTag)
            newModuleList = moduleList.replace(' '+s,'')
            pc.setAttr((getBuildTag+'.'+getModuleTag), newModuleList, type='string')
            pc.delete(s)
            print('Operation successful: dummy rig module is deleted for '+s+'.\n')

def connectModuleSymmetry():
    sel = pc.ls(sl=True)

    if(len(sel)>0):
        master = sel[0]
        slave = sel[1]
        
        getMasterTag = pc.getAttr(sel[0]+'.moduleTag')
        getSlaveTag = pc.getAttr(sel[1]+'.moduleTag')

        if getMasterTag == getSlaveTag:
            if getMasterTag == 'arm':
                buildArmModuleSymmetry(master, slave)
            elif(getMasterTag == 'bipedLeg'):
                buildLegModuleSymmetry(master, slave)
            elif(getMasterTag == 'Quadleg'):
                buildLegModuleSymmetry(master, slave)
            else:
                buildBodyModuleSymmetry(master, slave)
            print('Operation successful: '+sel[1]+' is now symmetrical to '+sel[0]+'.\n')
    else:
        pc.error('select master module then slave module for connecting symmetry')

# this proc mirror's given attr of transform
def mirrorModuleTransformAttr(obj, attr):
    val = pc.getAttr(obj+'.'+attr)
    neg = val*-1
    try:
        pc.setAttr((obj+'.'+attr), neg)
    except:
        pass

def mirrorPosAttrComponents(obj):
    masterList = ''
    masterJointsList = []

    try:
        mirrorModuleTransformAttr(obj, 'tx')
        mirrorModuleTransformAttr(obj, 'ry')
        mirrorModuleTransformAttr(obj, 'rz')
    except:
        pass

    if pc.attributeQuery('jointPosList', n=obj, ex=True):
        masterList = pc.getAttr(obj + '.jointPosList')
        masterJointsList = List.seperate(masterList)
        for m in masterJointsList:
            mirrorModuleTransformAttr(m, "tx");

def mirrorChildAttrComponents(obj):
    if pc.attributeQuery('child', n=obj, ex=True):
        masterChildList = pc.getAttr(obj+'.child')
        masterJointsLists = List.seperate(masterChildList)
        
        for m in masterJointsLists:
            mirrorModuleTemplates(m)

def mirrorModuleTemplates(obj):
    sel = []
    # check for selection
    print('obj: ')
    print(obj)
    if obj == '':
        sel = pc.ls(sl=True)
    else:
        sel.append(obj)
    mirrorPosAttrComponents(sel[0])

    if pc.attributeQuery('child', n=sel[0], ex=True):
        mirrorChildAttrComponents(sel[0])

    if pc.attributeQuery('wristPlacer', n=sel[0], ex=True):
        masterWrist = pc.getAttr(sel[0] + '.wristPlacer')
        mirrorPosAttrComponents(masterWrist)

    if pc.attributeQuery('footPlacer', n=sel[0], ex=True):
        masterFoot = pc.getAttr(sel[0] + '.footPlacer')
        mirrorPosAttrComponents(masterFoot)
    print('Operation successful: '+sel[0]+' is now mirrored.\n')