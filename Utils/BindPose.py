import maya.cmds as mc
import pymel.core as pc
import copy


def unlockChannels():
    channels = ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ", "scaleX", "scaleY", "scaleZ","visibility"]
    sel = mc.ls(sl=True)
    for node in sel:
        for channel in channels:
            if attributeExists(channel,node):
                mc.setAttr(node+"."+channel, k=True, l=False)

def disconnectJointFromControl():
    sel = mc.ls(type=["joint","transform"],sl=True)
    for node in sel:
        if attributeExists("isHookedUp",node):
            mc.setAttr(node+".isHookedUp",l=False)
            mc.setAttr(node+".isHookedUp",False)
            mc.setAttr(node+".isHookedUp",l=True)
            
            mc.select(node)
            unlockChannels()
            mc.select(cl=True)
            pcon = mc.listRelatives(node, c=True, type="pointConstraint")
            
            if len(pcon) > 0:
                mc.delete(pcon)
            
            oricon = mc.listRelatives(node, c=True, type="orientConstraint")
            
            if len(oricon) > 0:
                mc.delete(oricon)

            scaleXInput = mc.listConnections(node+".scaleX",s=True,d=False,scn=True,p=True)
            scaleYInput = mc.listConnections(node+".scaleY",s=True,d=False,scn=True,p=True)
            scaleZInput = mc.listConnections(node+".scaleZ",s=True,d=False,scn=True,p=True)

            if len(scaleXInput)>0:
                mc.disconnectAttr(node+".scaleX",scaleXInput[0])
            if len(scaleYInput)>0:
                mc.disconnectAttr(node+".scaleY",scaleYInput[0])
            if len(scaleZInput)>0:
                mc.disconnectAttr(node+".scaleZ",scaleZInput[0])

def attributeExists(attr,node):
    if not attr or not node: return False
    if not (mc.objExists(node)): return False    
    attrList = mc.listAttr(node,shortNames=True)
    
    # First check to see if the attribute matches the short names    
    for a in attrList:
        if attr == a:
            return True
    
    # Now check against the long names        
    attrList = mc.listAttr(node)    
    for a in attrList:
        if attr == a:
            return True
           
    return False

def filterLockedConnected(joints):
	
	filtered = []
	for joint in joints:
		transformChannels = ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ", "scaleX", "scaleY", "scaleZ", "rotateOrder", "segmentScaleCompensate"]
		listAttrCmd = "listAttr -l "
		for attr in transformChannels:
			listAttrCmd = listAttrCmd + "-st " + attr + " "
				
		locked = mc.listAttr(joint, l=True, st=transformChannels)
		if locked:
			filtered.append(joint)			
					
		locked = None
	
	return filtered


def lockUnlockJointOrientRotateAxis(objects, isLocked):
    attrs = ["jointOrientX", "jointOrientY", "jointOrientZ", "rotateAxisX", "rotateAxisY", "rotateAxisZ"]
    for node in objects:
        for attr in attrs:
            if mc.nodeType(node) == 'joint':
                mc.setAttr((node+"."+attr), l=isLocked)


def findDagPoseNodes(sel, type):
        
    dagPoseNodes = []
    dagPoses = []
    
    #if not sel:
    #    sel = mc.select('*bindPose*')
    
    poseType = "bindPose"
    if type > 0: 
        poseType = "rigPose"    
    
    for object in sel:
        mc.select(object)
        influences = []        
        history = mc.listHistory(object, pdo=True)
        skinClusters = mc.ls(history, type='skinCluster')        
        rigPoseNode = ''
        # try to find the dag pose nodes from the skin clusters
        
        for skin in skinClusters:
            dagPoses = mc.listConnections(skin, s=True, d=False, scn=True, type="dagPose")            
            for pose in dagPoses:                
                r = pose.find(poseType)
                if pose.find(poseType) >= 0:
                    dagPoseNodes.append(pose)

            # comment from maya 2009 script - ...scripts/others/gotoBindPose.mel
			# for legacy scenes (prior to Maya 2008) the skin cluster may not be connected
			# to the bindpose. In this case we'll have to try to find the bind pose a 
			# different way.
			# following is slightly modified from original

            if len(dagPoseNodes) < 1 and type == 0:
                influences = mc.skinCluster(skin, q=True, inf=True)
                bindPose = []
                for x in range(influences):
                    bindPose = mc.dagPose(influences[x], q=True, bp=True)
                    if len(bindPose) > 0:
                        dagPoseNodes.append(bindPose)
                        x = len(influences)
        
        # try to find the rig pose from the shape node (in case of skin deletion during re-work, try not to lose rigPose)
        shape = mc.listRelatives(object, noIntermediate=True, f=True, shapes=True)        
        if shape:            
            shapeOutputs = mc.listConnections(shape[0]+".message", d=1, s=0, scn=1)
            for output in shapeOutputs:                
                if mc.nodeType(output) == "dagPose":                    
                    if output.find(poseType) >= 0:
                        dagPoseNodes.append(output)
                        
    return dagPoseNodes


def goToDagPose(type):
    
	sel = mc.ls(sl=True)
	dagPoseNodes = findDagPoseNodes(sel, type)
	
	for dagPose in dagPoseNodes:
	    # get the joints associated with the pose node
		joints = mc.dagPose(dagPose, q=True, m=True)
		
		# filter out locked joints
		cleaned = filterLockedConnected(joints)

				
		temp = joints
		for c in cleaned:
		    temp = temp.remove(cleaned)
		    
		# filter any joints that are currently hooked up to controllers        
		hookedUp = []
		h = 0
		for lock in temp:
			if attributeExists('controlJoint',lock) and attributeExists('isHookedUp' and lock):
				if mc.getAttr(lock+'.isHookedUp'):
					hookedUp[h] = lock
					h+=1
					mc.select(cl=True)				
		
		locked = hookedUp
		for h in hookedUp:
		    locked = locked.remove(h)

		warning = 'The following bind pose joints are locked/connected: '
		for lockedJnt in locked:
		    warning += lockedJnt+' '

		confirm = ''
		if len(locked) > 0:
		    mc.warning(warning)
		    confirm = mc.confirmDialog(title='Locked/Connected Joints Found', 
		                               message=("Remove from "+dagPose+"?"),
		                               button=['Remove','Unlock','Cancel'], 
		                               defaultButton='Remove', 
		                               cancelButton='Cancel', 
		                               dismissString='Cancel')
		    
		    if confirm == 'Remove':
		        mc.select(locked)
		        mc.dagPose(mc.ls(sl=True), rm=True, n=dagPose)
		    elif confirm == 'Unlock': print 'TODO: Implement Unlock'

		if confirm != 'Cancel':
			mc.select(mc.dagPose(dagPose, q=True, m=True))
			disconnectJointFromControl()
			mc.select(cl=True)
			mc.dagPose(dagPose, restore=True, g=True)
		
	
	mc.select(sel)

def goToBindPose():
    goToDagPose(0)
    
def goToRigPose():
    goToDagPose(1)

def freezeSkinnedJoint():
    temp = mc.ls(sl=True,type='joint')        
    sel = filterLockedConnected(temp)
    
    for node in sel:
        parent = mc.listRelatives(node, p=True)
        if len(parent[0]) > 0:
            parentDummy = mc.createNode('transform')
            mc.delete(mc.PointConstraint(parent[0], parentDummy, offset=(0,0,0), weight=1))
            mc.delete(mc.OrientConstraint(parent[0], parentDummy, offset=(0,0,0), weight=1))
            
            dummy = mc.createNode('transform')
            mc.parent(dummy, parentDummy)
            mc.delete(mc.PointConstraint(node, dummy, offset=(0,0,0), weight=1))
            mc.delete(mc.OrientConstraint(node, dummy, offset=(0,0,0), weight=1))
            
            rotValues = mc.getAttr(dummy+'.rotate')
            jointOriValues = mc.getAttr(node+'.jointOrient')
            mc.delete(parentDummy)
            
            mc.setAttr(node+'.jointOrientX', rotValues[0])
            mc.setAttr(node+'.jointOrientY', rotValues[1])
            mc.setAttr(node+'.jointOrientZ', rotValues[2])
            
            mc.setAttr(node+'.rotate', (0,0,0))
            mc.setAttr(node+'.rotateX', 0)
            mc.setAttr(node+'.rotateY', 0)
            mc.setAttr(node+'.rotateZ', 0)
            
    mc.select(sel)

def unFreezeSkinnedJoint():
    sel = mc.ls(sl=True, l=True, type='joint')
    for joint in sel:
        parent = mc.listRelatives(joint, p=True, f=True)
        children = mc.listRelatives(joint, c=True, f=True)
        if mc.objExists(children[0]):
            mc.select(children)
            mc.parent(w=True)
            temp = mc.ls(l=True, sl=True)
            children = []
            children = temp
            
        orientDummy = mc.createNode('transform')
        if mc.objExists(parent[0]):
            mc.parent(orientDummy, parent[0])
        mc.delete(mc.PointConstraint(joint,orientDummy,offset=(0,0,0),weight=1))
        mc.delete(mc.OrientConstraint(joint,orientDummy,offset=(0,0,0),weight=1))
        
        rot = mc.getAttr(orientDummy+'rotate')
                
        lockUnlockJointOrientRotateAxis([joint], 0)
        mc.setAttr(joint+'.jointOrient', (0,0,0))
        mc.setAttr(joint+'.rotateAxix', (0,0,0))
        
        mc.setAttr(joint+'.roate', rot)
        
        if mc.objExists(children[0]):
            mc.select(children)
            mc.select(joint, add=True)
            mc.parent()
            
        mc.delete(orientDummy)
        children = None
    mc.select(sel)
    
def storeRigPose():
    sel = mc.ls(sl = True)
    
    for object in sel:        
        
        # check for old rig pose nodes    
        rigNodes = findDagPoseNodes([object],1)        
        confirm = ''               

        if rigNodes and mc.objExists(rigNodes[0]):
            if rigNodes[0].find('rigPose') >= 0:
                confirm = mc.confirmDialog(title = 'Rig Pose Already Exists', 
                                 message = 'Are you sure you want to continue?\nCurrent Rig Pose will Be Deleted',
                                 button = ['Yes','No'],
                                 defaultButton = 'Yes',
                                 canclButton = 'No',
                                 dismissString = 'No')
                
        if confirm != 'No':
            # get the bind pose node from the selected mesh
            bindPose = findDagPoseNodes([object],0)
            history = mc.listHistory(object, pdo = True)
            skin = mc.ls(history, type = 'skinCluster')
            shapeNode = mc.listRelatives(object, noIntermediate=True, f=True, shapes=True)
            joints = []
            
            # get the joints associated with the bind pose - default to skinCluster
            if bindPose and mc.objExists(bindPose[0]):
                joints = mc.listConnections((bindPose[0]+'.members'), s=True, d=False, scn=True)
            elif mc.objExists(skin[0]):
                mc.warning('bind pose node not found for '+shapeNode[0]+' using joints from skinCluster\n')
                joints = mc.skinCluster(skin[0], q=True, inf=True)
            
            if len(joints) > 0:
                mc.select(joints)
                freezeSkinnedJoint()
                if not attributeExists('rigPose',skin[0]):
                    mc.addAttr(skin[0], ln='rigPose', dt='string')
                
                #TODO: read up on why locked and connected joints were being filtered out and only being used to create the new rig node pose
                # mc.select(filterLockedConnected(joints))
                mc.select(joints)
                nodeName = bindPose[0].replace('bind','rig')
                rigPose = mc.dagPose(save=True, sl=True, n=(skin[0]+'_'+nodeName))
                
                # connect from shape node
                mc.addAttr(rigPose, ln='skinnedMesh', dt='string')
                mc.setAttr((rigPose+".skinnedMesh"), l=0)
                mc.connectAttr((shapeNode[0]+".message"),(rigPose+".skinnedMesh"), f=True)
                mc.setAttr((rigPose+".skinnedMesh"), l = 1)
                
                # connect from skin cluster
                mc.setAttr((skin[0]+".rigPose"), l = 0)
                mc.connectAttr((rigPose+".message"),(skin[0]+".rigPose"), f=True)
                mc.setAttr((skin[0]+".rigPose"), l=1)
            else:
                mc.warning('no joints could be found that are associated with '+shapeNode[0]+'\n')
    mc.select(sel)
                        