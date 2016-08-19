import pymel.core as pc

from Maya_Rigging.Core import BuildWorld as bw
from Maya_Rigging.Utils import CharUtilsLib as chUL

# from Maya_Rigging import *

#	This proc creates stretch network for given joints.
#	code based on Gregory Smith's gsCreateSS.
#     INPUTS:
#        n        			>> object hierarchy to create stretch  ('joint1')
#        name						>> namine prefix
#        controller  		>> object to add attribute
#        type       		>> translate / scale
#				midLock  			>> switch on / off for midlock proc
#				midController	>> mid pole vector control to add mid lock switch
#(i.e) stretchNetwork ('joint1' 'R_arm' 'cube1' 'scale' 1 'loc1')


def stretchNetwork(name,side, startJoint, endJoint, controller, type, midLock, midController):
    
    list = []
    chainLength = 0.0
    defaultLength = 0.0
    axis = []
    middleIndex = ''
    numJoints = ''
    dist = []
    nonScaleGrp = (name+'non_scale_grp')
    scaleNode = (name+'worldScaleCon_grp')

    nonScaleGrp = bw.createScaleGrp(name)

    # get complete hierarchy of given joint
    list = chUL.findJointArray(startJoint, endJoint)

    # get full chain length
    chainLength = chUL.getChainLength(startJoint, endJoint)
    # setermine the stretch axis of given chain (joint must be oriented)
    axis = chUL.getStretchAxis(list[1], type)

    # get the middle index of given joint chain
    middleIndex = (len(list)/2)
    # hold total number of joints
    numJoints = len(list)

    # TODO: revisit this, dis[0] may not work because no element has been given yet.
    # create distance for start joint to controller
    dist = chUL.createDistance(list[0], controller)
    dist[0] = pc.rename((dist[0]), (name + side + startJoint + '_dis'))
    dist[1] = pc.rename((dist[1]), (name + side + startJoint + 'Start_loc'))
    dist[2] = pc.rename((dist[2]), (name + side + startJoint + 'End_loc'))    
    defaultLength = pc.getAttr(dist[0] + '.distance')

    pc.pointConstraint(list[0], dist[1], offset=[0,0,0], weight=1)
    pc.pointConstraint(controller, dist[2], offset=[0,0,0], weight=1)
    pc.setAttr((dist[0] + '.v'),0)
    pc.setAttr((dist[1] + '.v'), 0)
    pc.setAttr((dist[2] + '.v'), 0)

    chUL.lockAndHide(dist[0], 'lock', 'trans rot scale vis')
    chUL.lockAndHide(dist[1], 'lock', 'trans rot scale vis')
    chUL.lockAndHide(dist[2], 'lock', 'trans rot scale vis')

    distGrp = pc.group(em=True, n=(name + side + startJoint + 'Distance_grp'))
    pc.parent(distGrp, nonScaleGrp)

    pc.parent(dist[0], distGrp)
    pc.parent(dist[1], distGrp)
    pc.parent(dist[2], distGrp)
    
    #####
    #  create two multiply divide nodes and two condition nodes and a clamp
    #
    # create a mult/divide node used for determining the ratio of the actual distance to the default length and place it in the ssMDN variable
    ssMDN = pc.shadingNode('multiplyDivide',n=(name + side + 'sS_md'), asUtility=True,)

    # set it to the divide function
    pc.setAttr((ssMDN + '.operation'), 2)

    # create a mult/divide node used for determing the default length when the character is scaled
    scalerMDN = pc.shadingNode('multiplyDivide',n=(name + side + 'scaler_md'), asUtility=True)

    # set its value to multiply
    pc.setAttr((scalerMDN + '.operation'), 1)

    # create a condition node to determine if the ratio should bend the arm or stretch it
    ssCND = pc.shadingNode('condition',n=(name + side + 'sS_cnd'), asUtility=True,)

    # set its operation to greater than
    pc.setAttr((ssCND + '.operation'),2)
    # set its second term to 1
    pc.setAttr((ssCND + '.secondTerm'),1)

    # create a clamp node which will allow the scaling to be restricted by the user through the specified controller
    ssCLMP = pc.shadingNode('clamp',n=(name + side + 'sS_clamp'), asUtility=True)

    # create a condition node to allow for the user turing on and off the stretching ability
    ssONOFF = pc.shadingNode('condition',n=(name + side + 'sS_ONOFF_cnd'), asUtility=True)

    # set its operation to equals
    pc.setAttr((ssONOFF + '.operation'), 0)
    # set its second term to 1
    pc.setAttr((ssONOFF + '.secondTerm'),1)

    # create an add/subtract node to govern the artifical stretch on the clamp
    clampASN = pc.shadingNode('plusMinusAverage',n=(name + side + 'clamp_pma'), asUtility=True)

    # create an add/subtract node to govern the artifical stretch on the clamp
    condASN = pc.shadingNode('plusMinusAverage',n=(name + side + 'con_pma'), asUtility=True)

    # add an attribute to the node to set the intial value to one
    pc.addAttr(condASN, k=0, ln='offset', at='long', dv=1)

    #####
    #  Add attributes to the controller for the ON/OFF functionality and the streching value
    #
    pc.addAttr(controller, k=1, ln='STRETCH', at='enum', en='---------:')
    pc.setAttr((controller + '.STRETCH'), keyable=False, channelBox=True)
    pc.addAttr(controller, k=1, ln='autoExtend', at='bool', dv=1)               # add on off attribute
    pc.addAttr(controller, k=1, ln='extendClamp', at='double',  min=1, dv=1.25) # add limiter
    pc.addAttr(controller, k=1, ln='manualExtend', at='double', min=-.99, dv=0) # add the ability to stretch it artificially

    #####
    #  connect the nodes and set the proper values
    #
    # connect the scaler attribute to the input 1X of the scalerMDN
    pc.connectAttr((scaleNode + '.scaleX'), (scalerMDN + '.input1X'), f=True) 

    # set the scalerMDN's 2X to the chain length's value
    pc.setAttr((scalerMDN + '.input2X'), chainLength)

    # connect its output X to the ssMDN's input 2X
    pc.connectAttr((scalerMDN + '.outputX'), (ssMDN + '.input2X'), f=True)

    # connect the ddActShape.distance attribute to the input 1X of the ssMDN
    pc.connectAttr((dist[0] + '.distance'), (ssMDN + '.input1X'), f=True) 
    # --the result of this will be a ratio of the acutal length of the chain to the default length--

    # connect the output X of the ssMDN to the first term of the sS condition node (will allow the IK to collapse instead of shrinking)
    pc.connectAttr((ssMDN + '.outputX'), (ssCND + '.firstTerm'), f=True)

    # add the artificial stretch into the system to allow us to artifically change it
    pc.connectAttr((condASN + '.offset'), (condASN + '.input1D[0]'), f=True)   # add the offset value of 1 into the add subtract node
    pc.connectAttr((controller + '.manualExtend'), (condASN + '.input1D[1]'), f=True)

    pc.connectAttr((condASN + '.output1D'), (ssONOFF + '.colorIfTrueG'), f=True) 

    # connect the output X of the ssMDN to the input R of the clamp (this will clamp down the sS values
    pc.connectAttr((ssMDN + '.outputX'), (ssCLMP + '.inputR'),f=True)

    # hook up the clamp add subtract node to the artifical stretch and clamp attributes and the ASN to the clamp itself
    pc.connectAttr((controller + '.extendClamp'), (clampASN + '.input1D[0]'), f=True)
    pc.connectAttr((controller + '.manualExtend'), (clampASN + '.input1D[1]'), f=True)

    pc.connectAttr((clampASN + '.output1D'),(ssCLMP + '.maxR'),f=True)

    # connect the clamps output into the ONOFF condition node's color if true
    pc.connectAttr((ssCLMP + '.outputR'),(ssONOFF + '.colorIfTrueR'),f=True)
    pc.setAttr((ssONOFF + '.colorIfFalseR'), 1)

    # connect the ssONOFF's first term to the ONOFF attr on the controller
    pc.connectAttr((controller + '.autoExtend'),(ssONOFF + '.firstTerm'),f=True)

    # finally connect the ONOFF condition to the sS condition which will control the joints stretching
    pc.connectAttr((ssONOFF + '.outColorR'),(ssCND + '.colorIfTrueR'),f=True)
    pc.connectAttr((ssONOFF + '.outColorG'),(ssCND + '.secondTerm'),f=True)
    pc.connectAttr((ssONOFF + '.outColorG'),(ssCND + '.colorIfFalseR'),f=True)

    #####
    # Create the offsetSystem for the middle joint
    #
    # create attribute
    pc.addAttr(controller, k=1, ln='midPos', at='double', min=-.75, max=.75, dv=0)                   # create an attribute to slide the middle joint back and fourth

    #create some nodes which we will need for later
    offInvMDN = pc.shadingNode('multiplyDivide',n=(name + side + 'offsetPreInv_md'), asUtility=True)        # used to invert the offset attribute
    pc.setAttr((offInvMDN + '.input2X'),-1)                                                                 # set the initial attribute to -1 to invert the numbers
    offPreMDN = pc.shadingNode('multiplyDivide',n=(name + side + 'offsetPre_md'), asUtility=True)           # used to adjust the scale value for pre middle joints
    offPostMDN = pc.shadingNode('multiplyDivide',n=(name + side + 'offsetPost_md'), asUtility=True)         # used to adjust the scale for post middle joints
    offPreASN = pc.shadingNode('plusMinusAverage',n=(name + side + 'offsetPre_pma'), asUtility=True)        # used to offset the offset controls
    pc.addAttr(offPreASN, ln='offset', at='double', dv=1)                                                   # add an attibute with a value of 1 to set the default scale value
    offPostASN = pc.shadingNode('plusMinusAverage',n=(name + side + 'offsetPost_pma'), asUtility=True)      # used to offset the offset controls
    pc.addAttr(offPostASN, ln='offset', at='double', dv=1)                                                  # add an attibute with a value of 1 to set the default scale value

    #hook up the nodes to eachother
    pc.connectAttr((controller + '.midPos'),(offInvMDN + '.input1X'),f=True)

    pc.connectAttr((offPreASN + '.offset'),(offPreASN + '.input1D[0]'),f=True)
    pc.connectAttr((offPostASN + '.offset'),(offPostASN + '.input1D[0]'),f=True)
    pc.connectAttr((offInvMDN + '.outputX'),(offPreASN + '.input1D[1]'),f=True)
    pc.connectAttr((controller + '.midPos'),(offPostASN + '.input1D[1]'),f=True)

    pc.connectAttr((offPreASN + '.output1D'),(offPreMDN + '.input1X'),f=True)
    pc.connectAttr((offPostASN + '.output1D'),(offPostMDN + '.input1X'),f=True)
    pc.connectAttr((ssCND + '.outColorR'),(offPreMDN + '.input2X'),f=True)
    pc.connectAttr((ssCND + '.outColorR'),(offPostMDN + '.input2X'),f=True)

    #####
    #  connect the output of the offset MDNs to the joints at the proper place
    #
    # connect the joints from the first up to the middle but not including it

    if type == 'scale':
        if midLock == 1:
            pc.addAttr(midController, k=1, ln='midLock', at='double', min=0, max=1, dv=0) 

            # duplicate stretch joint in order to get start to mid length
            # string preLength[] = `dupId startJoint prefix temp`
            preTemp = chUL.dupId(startJoint, 'prefix', 'temp')

            # select middle index joint and delete all child joints
            pc.select(preTemp[middleIndex], r=True)
            pc.pickWalk(d='down')
            temp = pc.ls(sl=True)
            pc.delete(temp[0])
            
            tempEndjoint = preTemp[middleIndex]
            # get joint length from start to mid
            preMidChainLength = chUL.getChainLength(preTemp[0],tempEndjoint)
            # delete the temp create joint
            pc.delete(preTemp[0])

            # duplicate stretch joint in order to get mid to end length
            # string postLength[] = `duplicate -rc list[0]`
            postTemp = chUL.dupId(startJoint, 'prefix', 'temp')
            
            tempEndjoint = ('temp_' + endJoint)

            # get joint length from mid to end
            postMidChainLength = chUL.getChainLength(postTemp[middleIndex],tempEndjoint)
            pc.delete(postTemp[0])

            # TODO: revisit this, as it will likely not work preMid[0] will not have anything appended by the time its renamed
            # create distance node from start to mid
            preMid = chUL.createDistance(list[0], midController)
            preMid[0] = pc.rename((preMid[0]), (name + side + midController + '_dis'))
            preMid[1] = pc.rename((preMid[1]), (name + side + midController + 'Start_loc'))
            preMid[2] = pc.rename((preMid[2]), (name + side + midController + 'End_loc'))
            
            pc.pointConstraint(list[0], preMid[1], offset=[0, 0, 0], weight=1)
            pc.pointConstraint(midController, preMid[2], offset=[0, 0, 0], weight=1)
            pc.setAttr((preMid[0] + '.v'), 0)
            pc.setAttr((preMid[1] + '.v'), 0)
            pc.setAttr((preMid[2] + '.v'), 0)
            
            chUL.lockAndHide(preMid[0], 'lock', 'trans rot scale vis')
            chUL.lockAndHide(preMid[1], 'lock', 'trans rot scale vis')
            chUL.lockAndHide(preMid[2], 'lock', 'trans rot scale vis')
            
            pc.parent(preMid[0], distGrp)
            pc.parent(preMid[1], distGrp)
            pc.parent(preMid[2], distGrp)

            # create multiply divide node for scaler and operation to divide
            preMidScaler_MDN = pc.createNode('multiplyDivide', n=(name + side + 'preMidScaler_md'))
            pc.setAttr((preMidScaler_MDN + '.operation'),2)

            # create multiply divide node for actual distance and operation to divide
            preMidNormalised_MDN = pc.createNode('multiplyDivide', n=(name + side + 'preMidNormalised_md'))
            pc.setAttr((preMidNormalised_MDN + '.operation'),2)

            # create blend node to blend between mid lock on off
            preMid_BTA = pc.createNode('blendTwoAttr', n=(name + side + 'preMid_bta'))
            pc.connectAttr((midController + '.midLock'),(preMid_BTA + '.attributesBlender'))

            # do all necessary connection for mid lock setup
            pc.connectAttr((preMid[0] + '.distance'),(preMidScaler_MDN + '.input1X'),f=True)
            pc.connectAttr((scaleNode + '.scaleX'),(preMidScaler_MDN + '.input2X'),f=True)
            
            pc.connectAttr((preMidScaler_MDN + '.outputX'),(preMidNormalised_MDN + '.input1X'), f=True)
            pc.setAttr((preMidNormalised_MDN + '.input2X'),preMidChainLength)
            
            pc.connectAttr((offPreMDN + '.outputX'),(preMid_BTA + '.input[0]'), f=True)
            pc.connectAttr((preMidNormalised_MDN + '.outputX'),(preMid_BTA + '.input[1]'), f=True) 

            # create distance node from start to mid
            postMid = chUL.createDistance(midController,controller)
            postMid[0] = pc.rename((postMid[0]),(name + side + endJoint + '_dis'))
            postMid[1] = pc.rename((postMid[1]),(name + side + endJoint + 'Start_loc'))
            postMid[2] = pc.rename((postMid[2]),(name + side + endJoint + 'End_loc'))
            
            pc.pointConstraint(midController, postMid[1], offset=[0,0,0], weight=1)
            pc.pointConstraint(controller, postMid[2], offset=[0,0,0], weight=1)
            pc.setAttr((postMid[0] + '.v'),0)
            pc.setAttr((postMid[1] + '.v'),0)
            pc.setAttr((postMid[2] + '.v'),0)
            
            chUL.lockAndHide(postMid[0],'lock','trans rot scale vis')
            chUL.lockAndHide(postMid[1],'lock','trans rot scale vis')
            chUL.lockAndHide(postMid[2],'lock','trans rot scale vis')
            
            pc.parent(postMid[0],distGrp)
            pc.parent(postMid[1],distGrp)
            pc.parent(postMid[2],distGrp)

            # create multiply divide node for scaler and operation to divide
            postMidScaler_MDN = pc.createNode('multiplyDivide', n=(name + side + 'postMidScaler_md'))
            pc.setAttr((postMidScaler_MDN + '.operation'),2)

            # create multiply divide node for actual distance and operation to divide
            postMidNormalised_MDN = pc.createNode('multiplyDivide', n=(name + side + 'postMidNormalised_md'))
            pc.setAttr((postMidNormalised_MDN + '.operation'),2)

            # create blend node to blend between mid lock on off
            postMid_BTA = pc.createNode('blendTwoAttr', n=(name + side + 'postMid_bta'))
            pc.connectAttr((midController + '.midLock'),(postMid_BTA + '.attributesBlender'))

            # do all necessary connection for mid lock setup
            pc.connectAttr((postMid[0] + '.distance'),(postMidScaler_MDN + '.input1X'),f=True)
            pc.connectAttr((scaleNode + '.scaleX'),(postMidScaler_MDN + '.input2X'),f=True)
            
            pc.connectAttr((postMidScaler_MDN + '.outputX'),(postMidNormalised_MDN + '.input1X'),f=True)
            pc.setAttr((postMidNormalised_MDN + '.input2X'),postMidChainLength)
            
            pc.connectAttr((offPostMDN + '.outputX'), (postMid_BTA + '.input[0]'), f=True)
            pc.connectAttr((postMidNormalised_MDN + '.outputX'),(postMid_BTA + '.input[1]'), f=True)

            # connect the joints from start to middle
            for i in range(middleIndex):
                pc.connectAttr((preMid_BTA + '.output'),(list[i] + '.' + axis[0]),f=True)

            # connect the joints from the middle on to the last one
            for i in range(middleIndex, numJoints - 1):
                pc.connectAttr((postMid_BTA + '.output'),(list[i] + '.' + axis[0]), f=True)
        else:        
            #connect the joints from start to middle
            for i in range(middleIndex):
                pc.connectAttr((offPreMDN + '.outputX'),(list[i] + '.' + axis[0]), f=True)

            # connect the joints from the middle on to the last one
            for i in range(middleIndex, numJoints - 1):
                pc.connectAttr((offPostMDN + '.outputX'),(list[i] + '.' + axis[0]), f=True) 
        
    elif type == 'translate':
        if midLock == 1:
            pc.addAttr(midController, k=1, ln='midLock', at='double', min=0, max=1, dv=0) 

            # duplicate stretch joint in order to get start to mid length
		    # string preLength[] = `duplicate -rc list[0]`
            preTemp = chUL.dupId(startJoint,'prefix','temp')

            # select middle index joint and delete all child joints
            pc.select(preTemp[middleIndex], r=True)
            pc.pickWalk(d='down')
            temp = pc.ls(sl=True)
            pc.delete(temp[0])
            
            tempEndjoint = preTemp[middleIndex]
            # get joint length from start to mid
            preMidChainLength = chUL.getChainLength(preTemp[0],tempEndjoint)
            # delete the temp create joint
            pc.delete(preTemp[0])

            # duplicate stretch joint in order to get mid to end length
		    # string postLength[] = `duplicate -rc list[0]`
            postTemp = chUL.dupId(startJoint,'prefix','temp')
            
            tempEndjoint = ('temp_' + endJoint)
            # get joint length from mid to end
            postMidChainLength = chUL.getChainLength(postTemp[middleIndex], tempEndjoint)
            pc.delete(postTemp[0])

            # create distance node from start to mid
            preMid = chUL.createDistance(list[0],midController)
            preMid[0] = pc.rename((preMid[0]),(name + side + midController + '_dis'))
            preMid[1] = pc.rename((preMid[1]),(name + side + midController + 'Start_loc'))
            preMid[2] = pc.rename((preMid[2]),(name + side + midController + 'End_loc'))
            
            pc.pointConstraint(list[0],preMid[1], offset=[0,0,0], weight=1)
            pc.pointConstraint(midController, preMid[2], offset=[0,0,0], weight=1)
            pc.setAttr((preMid[0] + '.v'),0)
            pc.setAttr((preMid[1] + '.v'),0)
            pc.setAttr((preMid[2] + '.v'),0)
            
            chUL.lockAndHide(preMid[0],'lock','trans rot scale vis')
            chUL.lockAndHide(preMid[1],'lock','trans rot scale vis')
            chUL.lockAndHide(preMid[2],'lock','trans rot scale vis')
            
            pc.parent(preMid[0],distGrp)
            pc.parent(preMid[1],distGrp)
            pc.parent(preMid[2],distGrp)

		    #create multiply divide node for scaler and operation to divide
            preMidScaler_MDN = pc.createNode('multiplyDivide', n=(name + side + 'preMidScaler_md'))
            pc.setAttr((preMidScaler_MDN + '.operation'),2)

		    #create multiply divide node for actual distance and operation to divide
            preMidNormalised_MDN = pc.createNode('multiplyDivide', n=(name + side + 'preMidNormalised_md'))
            pc.setAttr((preMidNormalised_MDN + '.operation'),2)

		    #create blend node to blend between mid lock on off
		    #string preMid_BTA = `createNode blendTwoAttr -n (name + side + '_preMid_bta')`
		    #connectAttr (midController + '.midLock') (preMid_BTA + '.attributesBlender')

		    #do all necessary connection for mid lock setup
            pc.connectAttr((preMid[0] + '.distance'),(preMidScaler_MDN + '.input1X'),f=True)
            pc.connectAttr((scaleNode + '.scaleX'),(preMidScaler_MDN + '.input2X'),f=True)
            
            pc.connectAttr((preMidScaler_MDN + '.outputX'),(preMidNormalised_MDN + '.input1X'),f=True)
            pc.setAttr((preMidNormalised_MDN + '.input2X'),preMidChainLength)

		    #create distance node from start to mid
            postMid = chUL.createDistance(midController,controller)
            postMid[0] = pc.rename((postMid[0]),(name + side + endJoint + '_dis'))
            postMid[1] = pc.rename((postMid[1]),(name + side + endJoint + 'Start_loc'))
            postMid[2] = pc.rename((postMid[2]),(name + side + endJoint + 'End_loc'))
            
            pc.pointConstraint(midController,postMid[1], offset=[0,0,0], weight=1)
            pc.pointConstraint(controller, postMid[2], offset=[0,0,0], weight=1)
            pc.setAttr((postMid[0] + '.v'),0)
            pc.setAttr((postMid[1] + '.v'),0)
            pc.setAttr((postMid[2] + '.v'),0)
            
            chUL.lockAndHide(postMid[0],'lock','trans rot scale vis')
            chUL.lockAndHide(postMid[1],'lock','trans rot scale vis')
            chUL.lockAndHide(postMid[2],'lock','trans rot scale vis')
            
            pc.parent(postMid[0],distGrp)
            pc.parent(postMid[1],distGrp)
            pc.parent(postMid[2],distGrp)

		    #create multiply divide node for scaler and operation to divide
            postMidScaler_MDN = pc.createNode('multiplyDivide', n=(name + side + 'postMidScaler_md'))
            pc.setAttr((postMidScaler_MDN + '.operation'),2)

		    #create multiply divide node for actual distance and operation to divide
            postMidNormalised_MDN = pc.createNode('multiplyDivide', n=(name + side + 'postMidNormalised_md'))
            pc.setAttr((postMidNormalised_MDN + '.operation'),2)

		    #create blend node to blend between mid lock on off
		    #string postMid_BTA = `createNode blendTwoAttr -n (name + side + '_postMid_bta')`
		    #connectAttr (midController + '.midLock') (postMid_BTA + '.attributesBlender')

		    #do all necessary connection for mid lock setup
            pc.connectAttr((postMid[0] + '.distance'),(postMidScaler_MDN + '.input1X'), f=True)
            pc.connectAttr((scaleNode + '.scaleX'),(postMidScaler_MDN + '.input2X'), f=True)
            
            pc.connectAttr((postMidScaler_MDN + '.outputX'),(postMidNormalised_MDN + '.input1X'), f=True)
            pc.setAttr((postMidNormalised_MDN + '.input2X'),postMidChainLength)

		    #connectAttr -f (offPostMDN + '.outputX') (postMid_BTA + '.input[0]')
		    #connectAttr -f (postMidNormalised_MDN + '.outputX') (postMid_BTA + '.input[1]')

            for i in range(1,middleIndex+1):
                #create blend node to blend between mid lock on off
                preMid_BTA = pc.createNode('blendTwoAttr', n=(name + side + 'preMid_bta'))
                pc.connectAttr((midController + '.midLock'),(preMid_BTA + '.attributesBlender'))

                #create two multiply divide to absolute the output value
                transA = pc.createNode('multiplyDivide', n=(name + side + list[i] + '_transAbs_md'))
                transB = pc.createNode('multiplyDivide', n=(name + side + list[i] + '_transAbs_md'))
                #get translate Attr of given joint
                t = pc.getAttr(list[i] + '.' + axis[0])
                pc.setAttr((transA + '.input2X'),t)
                pc.setAttr((transB + '.input2X'),t)

                # connecting stretch node output to newly creted node to normalise the value for translate stretch
                pc.connectAttr((offPreMDN + '.outputX'),(transA + '.input1X'))
                pc.connectAttr((preMidNormalised_MDN + '.outputX'),(transB + '.input1X'), f=True) 

                # connecting output of divide node to blend midlock attr
                pc.connectAttr((transA + '.outputX'),(preMid_BTA + '.input[0]'), f=True)
                pc.connectAttr((transB + '.outputX'),(preMid_BTA + '.input[1]'), f=True)

                #connecting all joints except midjoint
                pc.connectAttr((preMid_BTA + '.output'),(list[i] + '.' + axis[0]))

            for i in range(middleIndex+1,numJoints):
		        #create blend node to blend between mid lock on off
                postMid_BTA = pc.createNode('blendTwoAttr', n=(name + side + 'postMid_bta'))
                pc.connectAttr((midController + '.midLock'),(postMid_BTA + '.attributesBlender'))

		        #create blend node to blend between mid lock on off
                transA = pc.createNode('multiplyDivide', n=(name + side +list[i] + '_transAbs_md'))
                transB = pc.createNode('multiplyDivide', n=(name + side +list[i] + '_transAbs_md'))
		        #get translate Attr of given joint
                t = pc.getAttr(list[i] + '.' + axis[0])
                pc.setAttr((transA + '.input2X'),t)
                pc.setAttr((transB + '.input2X'),t)

		        # connecting stretch node output to newly creted node to normalise the value for translate stretch
                pc.connectAttr((offPostMDN + '.outputX'),(transA + '.input1X'))
                pc.connectAttr((postMidNormalised_MDN + '.outputX'),(transB + '.input1X'), f=True)

		        # connecting output of divide node to blend midlock attr
                pc.connectAttr((transA + '.outputX'),(postMid_BTA + '.input[0]'), f=True)
                pc.connectAttr((transB + '.outputX'),(postMid_BTA + '.input[1]'), f=True) 

		        #connecting all joints
                pc.connectAttr((postMid_BTA + '.output'),(list[i] + '.' + axis[0]))
        else:
            for i in range(1,middleIndex+1):
                t = pc.getAttr(list[i] + '.' + axis[0])
                trans = pc.createNode('multiplyDivide', n=(list[i] + '_transAbs_md'))
                pc.connectAttr((offPreMDN + '.outputX'),(trans + '.input1X'))
                pc.setAttr((trans + '.input2X'),t)
                pc.connectAttr((trans + '.outputX'),(list[i] + '.' + axis[0]))
            for i in range(middleIndex+1,numJoints):
                t = pc.getAttr(list[i] + '.' + axis[0])
                trans = pc.createNode('multiplyDivide', n=(list[i] + '_transAbs_md'))
                pc.connectAttr((offPostMDN + '.outputX'),(trans + '.input1X'))
                pc.setAttr((trans + '.input2X'),t)
                pc.connectAttr((trans + '.outputX'),(list[i] + '.' + axis[0]))

#print '\n'
#print '======================================================\n'
#print (name + side + '  Stretch Information\n')
#print '------------------------------------------------------\n'
#print ('Actual Joint Chain Length  >>\t' + chainLength + '\n')
#print ('Shortest Distance Length   >>\t' + defaultLength + '\n')
#print '======================================================\n'

#print 'Squash and Stretch Creation Successful! (see script editor for details)'

def buildIkStretch(name, side, startJoint, endJoint, controller, stretchType):
    dist = []
    defualtLength = 0.0
    stretchAxis = []

    nonScaleGrp = (name+'non_scale_grp')
    scaleNode = (name+'worldScaleCon_grp')

    nonScaleGrp = bw.createNonScaleGrp(name)

    stretchAxis = chUL.getStretchAxis(endJoint,stretchType)
    dist = chUL.createDistance(startJoint,endJoint)
    dist[0] = pc.rename((dist[0]), (name + side +startJoint + '_Ik'))
    dist[1] = pc.rename((dist[1]), (name + side +startJoint + '_Ik'))
    dist[2] = pc.rename((dist[2]), (name + side +startJoint + '_Ik'))
    defaultLength = pc.getAttr((dist[0] + '.distance'))

    pc.pointConstraint(startJoint, dist[1], offset=[0,0,0], weight=1)
    pc.pointConstraint(controller, dist[2], offset=[0,0,0], weight=1) 
    pc.setAttr((dist[0] + '.v'),0)
    pc.setAttr((dist[1] + '.v'),0)
    pc.setAttr((dist[2] + '.v'),0)

    chUL.lockAndHide(dist[0],'lock','trans rot scale vis')
    chUL.lockAndHide(dist[1],'lock','trans rot scale vis')
    chUL.lockAndHide(dist[2],'lock','trans rot scale vis')

    distGrp = pc.group(em=True, n=(name + side + startJoint + 'IkDistance_grp'))
    pc.parent(distGrp,nonScaleGrp)

    pc.parent(dist[0],distGrp)
    pc.parent(dist[1],distGrp)
    pc.parent(dist[2],distGrp)

    pc.addAttr(controller, k=1, ln='stretch', at='double', min=0, max=1, dv=1)
    ikHandle = pc.ikHandle(name=(name + side + startJoint + '_ikhandle'), startJoint=startJoint, endEffector=endJoint, solver='ikSCsolver') # TODO: revisit this
    pc.pointConstraint(controller, ikHandle[0], offset=[0,0,0], weight=1)
    pc.parent(ikHandle[0],nonScaleGrp)
    pc.setAttr((ikHandle[0] + '.visibility'),0)
    chUL.lockAndHide(ikHandle[0],'lock','vis')

    # create node network fr stretch
    scalerMD = pc.createNode('multiplyDivide', n=(name + side + '_scaler_md'))
    pc.setAttr((scalerMD + '.operation'),2)
    normalisedMD = pc.createNode('multiplyDivide', n=(name + side + '_normalised_md'))
    pc.setAttr((normalisedMD + '.operation'),2)
    stretchBTA = pc.createNode('blendTwoAttr', n=(name + side + '_SsBlend_bta'))
    setAttr=((stretchBTA + '.input[0]'),1)
    pc.connectAttr((controller + '.stretch'),(stretchBTA + '.attributesBlender'))

    pc.connectAttr((dist[0] + '.distance'),(scalerMD + '.input1X'))
    pc.connectAttr((scaleNode + '.scale'),(scalerMD + '.input2'))

    pc.connectAttr((scalerMD + '.outputX'),(normalisedMD + '.input1X'))
    pc.setAttr((normalisedMD + '.input2X'),defaultLength)
    pc.connectAttr((normalisedMD + '.outputX'),(stretchBTA + '.input[1]'), f=True)

    if stretchType == 'translate':  
        transNorMD = pc.createNode('multiplyDivide', n=(name + side + '_transNor_md'))
        tempVal = pc.getAttr(endJoint + '.' + stretchAxis[0])
        pc.setAttr((transNorMD + '.input2X'),tempVal)
        pc.connectAttr((normalisedMD + '.outputX'),(transNorMD + '.input1X'))
        pc.connectAttr((transNorMD + '.outputX'),(startJoint + '.' + stretchAxis[0]))
  
    if stretchType == 'scale':
        pc.connectAttr((stretchBTA + '.output'),(startJoint + '.' + stretchAxis[0]))
    return ikHandle

#makeJointVolumeSetup ('loc1', 'scale', `ls -sl`)
#string controller = 'loc1'
#string stretchType = 'translate'
#string chain[] = `ls -sl`

def makeJointVolumeSetup(name, side, controller, stretchType, chain):
    axis = []
    stretchAxis = []
    twistAxis = []
    childJoint = ''

    stretchAxis = chUL.getStretchAxis(chain[0], stretchType)
    twistAxis = chUL.getTwistAxis(chain[0])

    # determine twist axis for further info distribution
    if twistAxis[0] == 'rx':
        axis = 'X', 'Y', 'Z'
    elif twistAxis[0] == 'ry':
        axis = 'Y', 'Z', 'X'
    elif twistAxis[0] == 'rz':
        axis = 'Z', 'X', 'Y'

    if not pc.attributeQuery('volume', n=controller, ex=True):
        pc.addAttr(controller, k=1, at='double', min=-1, max=1, dv=1, ln='volume')

    # select all joints of ik chain
    pc.select(chain)    
    createCurveControl(chain[0], 'scalePower', 'pow')

    for i in range(len(chain)-1):
        norDiv = pc.createNode('multiplyDivide', n=(name + side + chain[i] +'_revPowInput_md'))
        pc.setAttr((norDiv + '.operation'), 3)
        pc.setAttr((norDiv + '.input2X'), .5)
        
        if stretchType == 'translate':
            transNor = pc.createNode('multiplyDivide', n=(name + side + chain[i] +'_transNor_md'))
            pc.setAttr((transNor + '.operation'), 2)
            childJoint = chUL.getChildJoint(chain[i])
            tempVal = pc.getAttr(childJoint + '.translate' + axis[0])
            pc.setAttr((transNor + '.input2X'), tempVal)
            pc.connectAttr((childJoint + '.translate' + axis[0]), (transNor + '.input1X'))
            pc.connectAttr((transNor + '.outputX'), (norDiv + '.input1X'))
        else:
            pc.connectAttr((chain[i] + '.scale' + axis[0]), (norDiv + '.input1X'))
            
        revPow1 = pc.createNode('multiplyDivide', n=(name + side + chain[i] +'_normalizes_rev_md'))
        pc.setAttr((revPow1 + '.operation'), 2)
        pc.setAttr((revPow1 + '.input1X'), 1)
        pc.connectAttr((norDiv + '.outputX'), (revPow1 + '.input2X'))
        
        revPow2 = pc.createNode('multiplyDivide', n=(name + side + chain[i] +'_revPowOutput_md'))
        pc.setAttr((revPow2 + '.operation'), 3)
        pc.setAttr((revPow2 + '.input1Y'), 1)
        
        pc.connectAttr((revPow1 + '.outputX'), (revPow2 + '.input1X'))
        pc.connectAttr((chain[i] + '.pow'), (revPow2 + '.input2X'))
        
        vol_bta = pc.createNode('blendTwoAttr', n=(name + side + chain[i] + '_volume_bta'))
        pc.connectAttr((controller + '.volume'), (vol_bta + '.attributesBlender'))
        pc.connectAttr((revPow2 + '.outputX'), (vol_bta + '.input[1]'))
        pc.connectAttr((revPow2 + '.outputY'), (vol_bta + '.input[0]'))
        
        pc.connectAttr((vol_bta + '.output'), (chain[i] + '.scale' + axis[1]), f=True)
        pc.connectAttr((vol_bta + '.output'), (chain[i] + '.scale' + axis[2]), f=True)

# stretchySpline spline '' loc1 scale curve1 1 1 curve1
def stretchySpline(name, side, controller, stretchType, crv, worldScale, volume, scale):

    shape = []
    chain = []
    con = []
    ikHandle = ''
    stretchAxis = []

    pc.addAttr(controller, k=1, at='double', min=0, max=1, dv=1, ln='stretching')
    rev = pc.createNode('reverse', n=(name + side + 'stretchAttr_rev'))
    pc.connectAttr((controller + '.stretching'),(rev + '.inputX'))
    info = pc.createNode('curveInfo', name=(name + side + crv + '_info'))
    pc.connectAttr((crv + '.worldSpace[0]'), (info + '.inputCurve'), f=True)
    l = pc.getAttr(info + '.arcLength')

    div = pc.createNode('multiplyDivide', n=(name + side + 'lenDivide_md'))
    pc.setAttr((div + '.operation'), 2)
    pc.connectAttr((info + '.arcLength'), (div + '.input1X'))

    divA = pc.createNode('multiplyDivide', n=(name + side + 'scaleFactor_md'))
    pc.setAttr((divA + '.operation'), 2)
    pc.connectAttr((div + '.outputX'), (divA + '.input1X'))
    pc.setAttr((divA + '.input2X'), l)
    pc.setAttr((divA + '.input1Y'), 1)
    pc.setAttr((divA + '.input2Y'), 1)

    bta = pc.createNode('blendTwoAttr', n=(name + side + 'stretchBlend_bta'))
    pc.connectAttr((rev + '.outputX'), (bta + '.attributesBlender'))
    pc.connectAttr((divA + '.outputX'), (bta + '.input[0]'))
    pc.connectAttr((divA + '.outputY'), (bta + '.input[1]'))

    divB = pc.createNode('multiplyDivide', n=(name + side + 'absMulti_md'))
    pc.setAttr((divB + '.operation'), 2)
    pc.setAttr((divB + '.input2X'), 1)
    pc.connectAttr((bta + '.output'), (divB + '.input1X'))

    # get all information for stretching
    print('crv:', crv)
    shape = pc.listRelatives(crv, fullPath=True, shapes=True)
    print('shape:', shape)
    con = pc.listConnections((shape[0]+'.worldSpace[0]'), type='ikHandle')
    print('con:', con)
    ikHandle = con[0]
    print('ikHandle:', ikHandle)
    chain = pc.ikHandle(ikHandle, q=True, jointList=True)    
    tempCount = len(chain)
    childJoint = chUL.getChildJoint(chain[tempCount-1])    
    fullchain = chain
    # insert at index, in list, this item
    fullchain.append(childJoint)
    print('stretchAxis:', chain[1])
    stretchAxis = chUL.getStretchAxis(chain[1], str(stretchType))
    print('stretchType:', stretchType)

    print('stretchAxis:', stretchAxis)
    if stretchAxis[0] == 'tx':
        axis = 'X', 'Y', 'Z'
    elif stretchAxis[0] == 'ty':
        axis = 'Y', 'Z', 'X'
    elif stretchAxis[0] == 'tz':
        axis = 'Z', 'X', 'Y'

    if worldScale == 0 and volume == 0:
        # connect scaleAttr for all joints
        if stretchType == 'scale':
            for c in chain:
                pc.connectAttr((divB + '.outputX'), (c + '.' + stretchAxis[0]))
        else:
            for c in len(chain):
                transNor = pc.createNode('multiplyDivide', n=(name + side + chain[c]+'_transNor_md'))
                childJoint = chUL.getChildJoint(chain[c])
                tempVal = pc.getAttr(childJoint + '.translate' + axis[0])
                pc.setAttr((transNor + '.input2X'), tempVal)
                pc.connectAttr((divB + '.outputX'), (transNor + '.input1X'))
                pc.connectAttr((transNor + '.outputX'), (fullchain[c+1] + '.' + stretchAxis[0]))
    else:
        if worldScale == 1 and volume == 0:
            # connectAttr for global scaling
            pc.connectAttr((scale + '.scale'),(div + '.input2'))
            # connect scaleAttr for all joints
            if stretchType == 'scale':
                for c in chain:
                    pc.connectAttr((divB + '.outputX'),(c + '.' + stretchAxis[0]))
            else:
                for c in len(chain):
                    transNor = pc.createNode('multiplyDivide', n=(name + side + chain[c]+'_transNor_md'))
                    childJoint = chUL.getChildJoint(chain[c])
                    tempVal = pc.getAttr(childJoint + '.translate' + axis[0])
                    pc.setAttr((transNor + '.input2X'),tempVal)
                    pc.connectAttr((divB + '.outputX'),(transNor + '.input1X'))
                    pc.connectAttr((transNor + '.outputX'),(fullchain[c+1] + '.' + stretchAxis[0]))
        else:
            # connectAttr for global scalling
            pc.connectAttr((scale + '.scale'),(div + '.input2'))
            if stretchType == 'scale':
                for c in chain:
                    pc.connectAttr((divB + '.outputX'),(c + '.' + stretchAxis[0]))
            else:
                for c in range(len(chain)-1):
                    transNor = pc.createNode('multiplyDivide', n=(name + side + chain[c]+'_transNor_md'))
                    childJoint = chUL.getChildJoint(chain[c])
                    tempVal = pc.getAttr(childJoint + '.translate' + axis[0])
                    pc.setAttr((transNor + '.input2X'),tempVal)
                    pc.connectAttr((divB + '.outputX'),(transNor + '.input1X'))
                    pc.connectAttr((transNor + '.outputX'),(fullchain[c+1] + '.' + stretchAxis[0]))
            makeJointVolumeSetup(name, side, controller, stretchType, chain)


# based of Jason Schleifer's code
def createCurveControl(controlObj, controlAttribute, destinationAttribute):

    if not pc.objExists(controlObj):
        pc.error(controlObj + ' does not exist.  Exiting..\n')

    if not pc.attributeQuery(controlAttribute,node=controlObj, exists=True):
        pc.addAttr(controlObj,ln=controlAttribute, at='double')
        pc.setAttr((controlObj + '.' + controlAttribute),k=1)
    
    objs = pc.ls(sl=True)

    if len(objs) == 0:
        pc.error('Nothing Selected.\n')

    numControls = len(objs)
    objAttr = (controlObj + '.' + controlAttribute)
    pc.setKeyframe(controlObj, at=controlAttribute, t=1, v=0) 
    pc.setKeyframe(controlObj, at=controlAttribute, t=numControls, v=0) 

    pc.keyTangent(controlObj, wt=1, at=controlAttribute)
    pc.keyTangent(controlObj, weightLock=False, at=controlAttribute)

    pc.keyTangent(objAttr, e=True, a=True, t=1, outAngle=50)
    pc.keyTangent(objAttr, e=True, a=True, t=numControls, inAngle=-50)
    
    for x in range(numControls):
        fc = pc.createNode('frameCache')
        fc = pc.rename(fc, (objs[x] + '_frameCache'))
        pc.connectAttr(objAttr, (fc + '.stream'))
        pc.setAttr((fc + '.vt'),(x+1))
        if not pc.attributeQuery(destinationAttribute, exists=True, node=objs[x]):
            pc.addAttr(objs[x],ln=destinationAttribute, at='double')
            pc.setAttr((objs[x] + '.'+destinationAttribute), k=1)
        pc.connectAttr((fc + '.v'),(objs[x] + '.' + destinationAttribute), f=True)