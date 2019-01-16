import pymel.core as pc

from Maya_Rigging.Core import BuildWorld as bw
from Maya_Rigging.Utils import CharUtilsLib as chUL
from Maya_UtilLib import Units


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
# (i.e) stretch_network ('joint1' 'R_arm' 'cube1' 'scale' 1 'loc1')


def stretch_network(name, side, start_joint, end_joint, controller, type, mid_lock, mid_controller):
    list = []
    chain_length = 0.0
    default_length = 0.0
    axis = []
    middle_index = ''
    num_joints = ''
    dist = []
    non_scale_grp = (name + 'non_scale_grp')
    scale_node = (name + 'worldScaleCon_grp')

    non_scale_grp = bw.create_scale_grp(name)

    # get complete hierarchy of given joint
    list = chUL.findJointArray(start_joint, end_joint)

    # get full chain length
    chain_length = chUL.getChainLength(start_joint, end_joint)
    # determine the stretch axis of given chain (joint must be oriented)
    axis = chUL.getStretchAxis(list[1], type)

    # get the middle index of given joint chain
    middle_index = (len(list) / 2)
    # hold total number of joints
    num_joints = len(list)

    # TODO: revisit this, dis[0] may not work because no element has been given yet.
    # create distance for start joint to controller
    dist = chUL.createDistance(list[0], controller, True)
    dist[0] = pc.rename((dist[0]), (name + side + start_joint + '_dis'))
    dist[1] = pc.rename((dist[1]), (name + side + start_joint + 'Start_loc'))
    dist[2] = pc.rename((dist[2]), (name + side + start_joint + 'End_loc'))
    default_length = pc.getAttr(dist[3] + '.output')

    pc.pointConstraint(list[0], dist[1], offset=[0, 0, 0], weight=1)
    pc.pointConstraint(controller, dist[2], offset=[0, 0, 0], weight=1)
    pc.setAttr((dist[0] + '.v'), 0)
    pc.setAttr((dist[1] + '.v'), 0)
    pc.setAttr((dist[2] + '.v'), 0)

    chUL.lockAndHide(dist[0], 'lock', 'trans rot scale vis')
    chUL.lockAndHide(dist[1], 'lock', 'trans rot scale vis')
    chUL.lockAndHide(dist[2], 'lock', 'trans rot scale vis')

    dist_grp = pc.group(em=True, n=(name + side + start_joint + 'Distance_grp'))
    pc.parent(dist_grp, non_scale_grp)

    pc.parent(dist[0], dist_grp)
    pc.parent(dist[1], dist_grp)
    pc.parent(dist[2], dist_grp)

    #####
    #  create two multiply divide nodes and two condition nodes and a clamp
    #
    # create a mult/divide node used for determining the ratio of the actual distance to the default length and place it in the ssMDN variable
    ss_mdn = pc.shadingNode('multiplyDivide', n=(name + side + 'sS_md'), asUtility=True, )

    # set it to the divide function
    pc.setAttr((ss_mdn + '.operation'), 2)

    # create a mult/divide node used for determing the default length when the character is scaled
    scalar_mdn = pc.shadingNode('multiplyDivide', n=(name + side + 'scaler_md'), asUtility=True)

    # set its value to multiply
    pc.setAttr((scalar_mdn + '.operation'), 1)

    # create a condition node to determine if the ratio should bend the arm or stretch it
    ss_cnd = pc.shadingNode('condition', n=(name + side + 'sS_cnd'), asUtility=True, )

    # set its operation to greater than
    pc.setAttr((ss_cnd + '.operation'), 2)
    # set its second term to 1
    pc.setAttr((ss_cnd + '.secondTerm'), 1)

    # create a clamp node which will allow the scaling to be restricted by the user through the specified controller
    ss_clmp = pc.shadingNode('clamp', n=(name + side + 'sS_clamp'), asUtility=True)

    # create a condition node to allow for the user turing on and off the stretching ability
    ss_onoff = pc.shadingNode('condition', n=(name + side + 'sS_ONOFF_cnd'), asUtility=True)

    # set its operation to equals
    pc.setAttr((ss_onoff + '.operation'), 0)
    # set its second term to 1
    pc.setAttr((ss_onoff + '.secondTerm'), 1)

    # create an add/subtract node to govern the artificial stretch on the clamp
    clamp_asn = pc.shadingNode('plusMinusAverage', n=(name + side + 'clamp_pma'), asUtility=True)

    # create an add/subtract node to govern the artificial stretch on the clamp
    cond_asn = pc.shadingNode('plusMinusAverage', n=(name + side + 'con_pma'), asUtility=True)

    # add an attribute to the node to set the initial value to one
    pc.addAttr(cond_asn, k=0, ln='offset', at='long', dv=1)

    #####
    #  Add attributes to the controller for the ON/OFF functionality and the stretching value
    #
    pc.addAttr(controller, k=1, ln='STRETCH', at='enum', en='---------:')
    pc.setAttr((controller + '.STRETCH'), keyable=False, channelBox=True)
    pc.addAttr(controller, k=1, ln='autoExtend', at='bool', dv=1)  # add on off attribute
    pc.addAttr(controller, k=1, ln='extendClamp', at='double', min=1, dv=1.25)  # add limiter
    pc.addAttr(controller, k=1, ln='manualExtend', at='double', min=-.99,
               dv=0)  # add the ability to stretch it artificially

    #####
    #  connect the nodes and set the proper values
    #
    # connect the scalar attribute to the input 1X of the scalarMDN
    pc.connectAttr((scale_node + '.scaleX'), (scalar_mdn + '.input1X'), f=True)

    # set the scalarMDN's 2X to the chain length's value
    pc.setAttr((scalar_mdn + '.input2X'), chain_length)

    # connect its output X to the ssMDN's input 2X
    pc.connectAttr((scalar_mdn + '.outputX'), (ss_mdn + '.input2X'), f=True)

    # connect the ddActShape.distance attribute to the input 1X of the ssMDN
    pc.connectAttr((dist[3] + '.output'), (ss_mdn + '.input1X'), f=True)
    # --the result of this will be a ratio of the actual length of the chain to the default length--

    # connect the output X of the ssMDN to the first term of the sS condition node (will allow the IK to collapse instead of shrinking)
    pc.connectAttr((ss_mdn + '.outputX'), (ss_cnd + '.firstTerm'), f=True)

    # add the artificial stretch into the system to allow us to artificially change it
    pc.connectAttr((cond_asn + '.offset'), (cond_asn + '.input1D[0]'),
                   f=True)  # add the offset value of 1 into the add subtract node
    pc.connectAttr((controller + '.manualExtend'), (cond_asn + '.input1D[1]'), f=True)

    pc.connectAttr((cond_asn + '.output1D'), (ss_onoff + '.colorIfTrueG'), f=True)

    # connect the output X of the ssMDN to the input R of the clamp (this will clamp down the sS values
    pc.connectAttr((ss_mdn + '.outputX'), (ss_clmp + '.inputR'), f=True)

    # hook up the clamp add subtract node to the artificial stretch and clamp attributes and the ASN to the clamp itself
    pc.connectAttr((controller + '.extendClamp'), (clamp_asn + '.input1D[0]'), f=True)
    pc.connectAttr((controller + '.manualExtend'), (clamp_asn + '.input1D[1]'), f=True)

    pc.connectAttr((clamp_asn + '.output1D'), (ss_clmp + '.maxR'), f=True)

    # connect the clamps output into the ONOFF condition node's color if true
    pc.connectAttr((ss_clmp + '.outputR'), (ss_onoff + '.colorIfTrueR'), f=True)
    pc.setAttr((ss_onoff + '.colorIfFalseR'), 1)

    # connect the ssONOFF's first term to the ONOFF attr on the controller
    pc.connectAttr((controller + '.autoExtend'), (ss_onoff + '.firstTerm'), f=True)

    # finally connect the ONOFF condition to the sS condition which will control the joints stretching
    pc.connectAttr((ss_onoff + '.outColorR'), (ss_cnd + '.colorIfTrueR'), f=True)
    pc.connectAttr((ss_onoff + '.outColorG'), (ss_cnd + '.secondTerm'), f=True)
    pc.connectAttr((ss_onoff + '.outColorG'), (ss_cnd + '.colorIfFalseR'), f=True)

    #####
    # Create the offsetSystem for the middle joint
    #
    # create attribute
    pc.addAttr(controller, k=1, ln='midPos', at='double', min=-.75, max=.75,
               dv=0)  # create an attribute to slide the middle joint back and fourth

    # create some nodes which we will need for later
    off_inv_mdn = pc.shadingNode('multiplyDivide', n=(name + side + 'offsetPreInv_md'),
                                 asUtility=True)  # used to invert the offset attribute
    pc.setAttr((off_inv_mdn + '.input2X'), -1)  # set the initial attribute to -1 to invert the numbers
    off_pre_mdn = pc.shadingNode('multiplyDivide', n=(name + side + 'offsetPre_md'),
                                 asUtility=True)  # used to adjust the scale value for pre middle joints
    off_post_mdn = pc.shadingNode('multiplyDivide', n=(name + side + 'offsetPost_md'),
                                  asUtility=True)  # used to adjust the scale for post middle joints
    off_pre_asn = pc.shadingNode('plusMinusAverage', n=(name + side + 'offsetPre_pma'),
                                 asUtility=True)  # used to offset the offset controls
    pc.addAttr(off_pre_asn, ln='offset', at='double',
               dv=1)  # add an attribute with a value of 1 to set the default scale value
    off_post_asn = pc.shadingNode('plusMinusAverage', n=(name + side + 'offsetPost_pma'),
                                  asUtility=True)  # used to offset the offset controls
    pc.addAttr(off_post_asn, ln='offset', at='double',
               dv=1)  # add an attribute with a value of 1 to set the default scale value

    # hook up the nodes to each other
    pc.connectAttr((controller + '.midPos'), (off_inv_mdn + '.input1X'), f=True)

    pc.connectAttr((off_pre_asn + '.offset'), (off_pre_asn + '.input1D[0]'), f=True)
    pc.connectAttr((off_post_asn + '.offset'), (off_post_asn + '.input1D[0]'), f=True)
    pc.connectAttr((off_inv_mdn + '.outputX'), (off_pre_asn + '.input1D[1]'), f=True)
    pc.connectAttr((controller + '.midPos'), (off_post_asn + '.input1D[1]'), f=True)

    pc.connectAttr((off_pre_asn + '.output1D'), (off_pre_mdn + '.input1X'), f=True)
    pc.connectAttr((off_post_asn + '.output1D'), (off_post_mdn + '.input1X'), f=True)
    pc.connectAttr((ss_cnd + '.outColorR'), (off_pre_mdn + '.input2X'), f=True)
    pc.connectAttr((ss_cnd + '.outColorR'), (off_post_mdn + '.input2X'), f=True)

    #####
    #  connect the output of the offset MDNs to the joints at the proper place
    #
    # connect the joints from the first up to the middle but not including it

    if type == 'scale':
        if mid_lock == 1:
            pc.addAttr(mid_controller, k=1, ln='midLock', at='double', min=0, max=1, dv=0)

            # duplicate stretch joint in order to get start to mid length
            # string preLength[] = `dupId startJoint prefix temp`
            pre_temp = chUL.dupId(start_joint, 'prefix', 'temp')

            # select middle index joint and delete all child joints
            pc.select(pre_temp[middle_index], r=True)
            pc.pickWalk(d='down')
            temp = pc.ls(sl=True)
            pc.delete(temp[0])

            temp_endjoint = pre_temp[middle_index]
            # get joint length from start to mid
            pre_mid_chain_length = chUL.getChainLength(pre_temp[0], temp_endjoint)
            # delete the temp create joint
            pc.delete(pre_temp[0])

            # duplicate stretch joint in order to get mid to end length
            # string postLength[] = `duplicate -rc list[0]`
            post_temp = chUL.dupId(start_joint, 'prefix', 'temp')

            temp_endjoint = ('temp_' + end_joint)

            # get joint length from mid to end
            post_mid_chain_length = chUL.getChainLength(post_temp[middle_index], temp_endjoint)
            pc.delete(post_temp[0])

            # TODO: revisit this, as it will likely not work preMid[0] will not have anything appended by the time its renamed
            # create distance node from start to mid
            pre_mid = chUL.createDistance(list[0], mid_controller, True)
            pre_mid[0] = pc.rename((pre_mid[0]), (name + side + mid_controller + '_dis'))
            pre_mid[1] = pc.rename((pre_mid[1]), (name + side + mid_controller + 'Start_loc'))
            pre_mid[2] = pc.rename((pre_mid[2]), (name + side + mid_controller + 'End_loc'))

            pc.pointConstraint(list[0], pre_mid[1], offset=[0, 0, 0], weight=1)
            pc.pointConstraint(mid_controller, pre_mid[2], offset=[0, 0, 0], weight=1)
            pc.setAttr((pre_mid[0] + '.v'), 0)
            pc.setAttr((pre_mid[1] + '.v'), 0)
            pc.setAttr((pre_mid[2] + '.v'), 0)

            chUL.lockAndHide(pre_mid[0], 'lock', 'trans rot scale vis')
            chUL.lockAndHide(pre_mid[1], 'lock', 'trans rot scale vis')
            chUL.lockAndHide(pre_mid[2], 'lock', 'trans rot scale vis')

            pc.parent(pre_mid[0], dist_grp)
            pc.parent(pre_mid[1], dist_grp)
            pc.parent(pre_mid[2], dist_grp)

            # create multiply divide node for scaler and operation to divide
            pare_mid_scalar_man = pc.createNode('multiplyDivide', n=(name + side + 'preMidScaler_md'))
            pc.setAttr((pare_mid_scalar_man + '.operation'), 2)

            # create multiply divide node for actual distance and operation to divide
            pre_mid_normalised_mdn = pc.createNode('multiplyDivide', n=(name + side + 'preMidNormalised_md'))
            pc.setAttr((pre_mid_normalised_mdn + '.operation'), 2)

            # create blend node to blend between mid lock on off
            pre_mid_bta = pc.createNode('blendTwoAttr', n=(name + side + 'preMid_bta'))
            pc.connectAttr((mid_controller + '.midLock'), (pre_mid_bta + '.attributesBlender'))

            # do all necessary connection for mid lock setup
            pc.connectAttr((pre_mid[3] + '.output'), (pare_mid_scalar_man + '.input1X'), f=True)
            pc.connectAttr((scale_node + '.scaleX'), (pare_mid_scalar_man + '.input2X'), f=True)

            pc.connectAttr((pare_mid_scalar_man + '.outputX'), (pre_mid_normalised_mdn + '.input1X'), f=True)
            pc.setAttr((pre_mid_normalised_mdn + '.input2X'), pre_mid_chain_length)

            pc.connectAttr((off_pre_mdn + '.outputX'), (pre_mid_bta + '.input[0]'), f=True)
            pc.connectAttr((pre_mid_normalised_mdn + '.outputX'), (pre_mid_bta + '.input[1]'), f=True)

            # create distance node from start to mid
            post_mid = chUL.createDistance(mid_controller, controller, True)
            post_mid[0] = pc.rename((post_mid[0]), (name + side + end_joint + '_dis'))
            post_mid[1] = pc.rename((post_mid[1]), (name + side + end_joint + 'Start_loc'))
            post_mid[2] = pc.rename((post_mid[2]), (name + side + end_joint + 'End_loc'))

            pc.pointConstraint(mid_controller, post_mid[1], offset=[0, 0, 0], weight=1)
            pc.pointConstraint(controller, post_mid[2], offset=[0, 0, 0], weight=1)
            pc.setAttr((post_mid[0] + '.v'), 0)
            pc.setAttr((post_mid[1] + '.v'), 0)
            pc.setAttr((post_mid[2] + '.v'), 0)

            chUL.lockAndHide(post_mid[0], 'lock', 'trans rot scale vis')
            chUL.lockAndHide(post_mid[1], 'lock', 'trans rot scale vis')
            chUL.lockAndHide(post_mid[2], 'lock', 'trans rot scale vis')

            pc.parent(post_mid[0], dist_grp)
            pc.parent(post_mid[1], dist_grp)
            pc.parent(post_mid[2], dist_grp)

            # create multiply divide node for scalar and operation to divide
            post_mid_scalar_man = pc.createNode('multiplyDivide', n=(name + side + 'postMidScaler_md'))
            pc.setAttr((post_mid_scalar_man + '.operation'), 2)

            # create multiply divide node for actual distance and operation to divide
            post_mid_normalised_mdn = pc.createNode('multiplyDivide', n=(name + side + 'postMidNormalised_md'))
            pc.setAttr((post_mid_normalised_mdn + '.operation'), 2)

            # create blend node to blend between mid lock on off
            post_mid_bta = pc.createNode('blendTwoAttr', n=(name + side + 'postMid_bta'))
            pc.connectAttr((mid_controller + '.midLock'), (post_mid_bta + '.attributesBlender'))

            # do all necessary connection for mid lock setup
            pc.connectAttr((post_mid[3] + '.output'), (post_mid_scalar_man + '.input1X'), f=True)
            pc.connectAttr((scale_node + '.scaleX'), (post_mid_scalar_man + '.input2X'), f=True)

            pc.connectAttr((post_mid_scalar_man + '.outputX'), (post_mid_normalised_mdn + '.input1X'), f=True)
            pc.setAttr((post_mid_normalised_mdn + '.input2X'), post_mid_chain_length)

            pc.connectAttr((off_post_mdn + '.outputX'), (post_mid_bta + '.input[0]'), f=True)
            pc.connectAttr((post_mid_normalised_mdn + '.outputX'), (post_mid_bta + '.input[1]'), f=True)

            # connect the joints from start to middle
            for i in range(middle_index):
                pc.connectAttr((pre_mid_bta + '.output'), (list[i] + '.' + axis[0]), f=True)

            # connect the joints from the middle on to the last one
            for i in range(middle_index, num_joints - 1):
                pc.connectAttr((post_mid_bta + '.output'), (list[i] + '.' + axis[0]), f=True)
        else:
            # connect the joints from start to middle
            for i in range(middle_index):
                pc.connectAttr((off_pre_mdn + '.outputX'), (list[i] + '.' + axis[0]), f=True)

            # connect the joints from the middle on to the last one
            for i in range(middle_index, num_joints - 1):
                pc.connectAttr((off_post_mdn + '.outputX'), (list[i] + '.' + axis[0]), f=True)

    elif type == 'translate':
        if mid_lock == 1:
            pc.addAttr(mid_controller, k=1, ln='midLock', at='double', min=0, max=1, dv=0)

            # duplicate stretch joint in order to get start to mid length
            # string preLength[] = `duplicate -rc list[0]`
            pre_temp = chUL.dupId(start_joint, 'prefix', 'temp')

            # select middle index joint and delete all child joints
            pc.select(pre_temp[middle_index], r=True)
            pc.pickWalk(d='down')
            temp = pc.ls(sl=True)
            pc.delete(temp[0])

            temp_endjoint = pre_temp[middle_index]
            # get joint length from start to mid
            pre_mid_chain_length = chUL.getChainLength(pre_temp[0], temp_endjoint)
            # delete the temp create joint
            pc.delete(pre_temp[0])

            # duplicate stretch joint in order to get mid to end length
            # string postLength[] = `duplicate -rc list[0]`
            post_temp = chUL.dupId(start_joint, 'prefix', 'temp')

            temp_endjoint = ('temp_' + end_joint)
            # get joint length from mid to end
            post_mid_chain_length = chUL.getChainLength(post_temp[middle_index], temp_endjoint)
            pc.delete(post_temp[0])

            # create distance node from start to mid
            pre_mid = chUL.createDistance(list[0], mid_controller, True)
            pre_mid[0] = pc.rename((pre_mid[0]), (name + side + mid_controller + '_dis'))
            pre_mid[1] = pc.rename((pre_mid[1]), (name + side + mid_controller + 'Start_loc'))
            pre_mid[2] = pc.rename((pre_mid[2]), (name + side + mid_controller + 'End_loc'))

            pc.pointConstraint(list[0], pre_mid[1], offset=[0, 0, 0], weight=1)
            pc.pointConstraint(mid_controller, pre_mid[2], offset=[0, 0, 0], weight=1)
            pc.setAttr((pre_mid[0] + '.v'), 0)
            pc.setAttr((pre_mid[1] + '.v'), 0)
            pc.setAttr((pre_mid[2] + '.v'), 0)

            chUL.lockAndHide(pre_mid[0], 'lock', 'trans rot scale vis')
            chUL.lockAndHide(pre_mid[1], 'lock', 'trans rot scale vis')
            chUL.lockAndHide(pre_mid[2], 'lock', 'trans rot scale vis')

            pc.parent(pre_mid[0], dist_grp)
            pc.parent(pre_mid[1], dist_grp)
            pc.parent(pre_mid[2], dist_grp)

            # create multiply divide node for scaler and operation to divide
            pare_mid_scalar_man = pc.createNode('multiplyDivide', n=(name + side + 'preMidScaler_md'))
            pc.setAttr((pare_mid_scalar_man + '.operation'), 2)

            # create multiply divide node for actual distance and operation to divide
            pre_mid_normalised_mdn = pc.createNode('multiplyDivide', n=(name + side + 'preMidNormalised_md'))
            pc.setAttr((pre_mid_normalised_mdn + '.operation'), 2)

            # create blend node to blend between mid lock on off
            # string preMid_BTA = `createNode blendTwoAttr -n (name + side + '_preMid_bta')`
            # connectAttr (midController + '.midLock') (preMid_BTA + '.attributesBlender')

            # do all necessary connection for mid lock setup
            pc.connectAttr((pre_mid[3] + '.output'), (pare_mid_scalar_man + '.input1X'), f=True)
            pc.connectAttr((scale_node + '.scaleX'), (pare_mid_scalar_man + '.input2X'), f=True)

            pc.connectAttr((pare_mid_scalar_man + '.outputX'), (pre_mid_normalised_mdn + '.input1X'), f=True)
            pc.setAttr((pre_mid_normalised_mdn + '.input2X'), pre_mid_chain_length)

            # create distance node from start to mid
            post_mid = chUL.createDistance(mid_controller, controller, True)
            post_mid[0] = pc.rename((post_mid[0]), (name + side + end_joint + '_dis'))
            post_mid[1] = pc.rename((post_mid[1]), (name + side + end_joint + 'Start_loc'))
            post_mid[2] = pc.rename((post_mid[2]), (name + side + end_joint + 'End_loc'))

            pc.pointConstraint(mid_controller, post_mid[1], offset=[0, 0, 0], weight=1)
            pc.pointConstraint(controller, post_mid[2], offset=[0, 0, 0], weight=1)
            pc.setAttr((post_mid[0] + '.v'), 0)
            pc.setAttr((post_mid[1] + '.v'), 0)
            pc.setAttr((post_mid[2] + '.v'), 0)

            chUL.lockAndHide(post_mid[0], 'lock', 'trans rot scale vis')
            chUL.lockAndHide(post_mid[1], 'lock', 'trans rot scale vis')
            chUL.lockAndHide(post_mid[2], 'lock', 'trans rot scale vis')

            pc.parent(post_mid[0], dist_grp)
            pc.parent(post_mid[1], dist_grp)
            pc.parent(post_mid[2], dist_grp)

            # create multiply divide node for scalar and operation to divide
            post_mid_scalar_man = pc.createNode('multiplyDivide', n=(name + side + 'postMidScaler_md'))
            pc.setAttr((post_mid_scalar_man + '.operation'), 2)

            # create multiply divide node for actual distance and operation to divide
            post_mid_normalised_mdn = pc.createNode('multiplyDivide', n=(name + side + 'postMidNormalised_md'))
            pc.setAttr((post_mid_normalised_mdn + '.operation'), 2)

            # create blend node to blend between mid lock on off
            # string postMid_BTA = `createNode blendTwoAttr -n (name + side + '_postMid_bta')`
            # connectAttr (midController + '.midLock') (postMid_BTA + '.attributesBlender')

            # do all necessary connection for mid lock setup
            pc.connectAttr((post_mid[3] + '.output'), (post_mid_scalar_man + '.input1X'), f=True)
            pc.connectAttr((scale_node + '.scaleX'), (post_mid_scalar_man + '.input2X'), f=True)

            pc.connectAttr((post_mid_scalar_man + '.outputX'), (post_mid_normalised_mdn + '.input1X'), f=True)
            pc.setAttr((post_mid_normalised_mdn + '.input2X'), post_mid_chain_length)

            # connectAttr -f (offPostMDN + '.outputX') (postMid_BTA + '.input[0]')
            # connectAttr -f (postMidNormalised_MDN + '.outputX') (postMid_BTA + '.input[1]')

            for i in range(1, middle_index + 1):
                # create blend node to blend between mid lock on off
                pre_mid_bta = pc.createNode('blendTwoAttr', n=(name + side + 'preMid_bta'))
                pc.connectAttr((mid_controller + '.midLock'), (pre_mid_bta + '.attributesBlender'))

                # create two multiply divide to absolute the output value
                trans_a = pc.createNode('multiplyDivide', n=(name + side + list[i] + '_transAbs_md'))
                trans_b = pc.createNode('multiplyDivide', n=(name + side + list[i] + '_transAbs_md'))
                # get translate Attr of given joint
                t = pc.getAttr(list[i] + '.' + axis[0])
                pc.setAttr((trans_a + '.input2X'), t)
                pc.setAttr((trans_b + '.input2X'), t)

                # connecting stretch node output to newly created node to normalise the value for translate stretch
                pc.connectAttr((off_pre_mdn + '.outputX'), (trans_a + '.input1X'))
                pc.connectAttr((pre_mid_normalised_mdn + '.outputX'), (trans_b + '.input1X'), f=True)

                # connecting output of divide node to blend midlock attr
                pc.connectAttr((trans_a + '.outputX'), (pre_mid_bta + '.input[0]'), f=True)
                pc.connectAttr((trans_b + '.outputX'), (pre_mid_bta + '.input[1]'), f=True)

                # connecting all joints except midjoint
                pc.connectAttr((pre_mid_bta + '.output'), (list[i] + '.' + axis[0]))

            for i in range(middle_index + 1, num_joints):
                # create blend node to blend between mid lock on off
                post_mid_bta = pc.createNode('blendTwoAttr', n=(name + side + 'postMid_bta'))
                pc.connectAttr((mid_controller + '.midLock'), (post_mid_bta + '.attributesBlender'))

                # create blend node to blend between mid lock on off
                trans_a = pc.createNode('multiplyDivide', n=(name + side + list[i] + '_transAbs_md'))
                trans_b = pc.createNode('multiplyDivide', n=(name + side + list[i] + '_transAbs_md'))
                # get translate Attr of given joint
                t = pc.getAttr(list[i] + '.' + axis[0])
                pc.setAttr((trans_a + '.input2X'), t)
                pc.setAttr((trans_b + '.input2X'), t)

                # connecting stretch node output to newly creted node to normalise the value for translate stretch
                pc.connectAttr((off_post_mdn + '.outputX'), (trans_a + '.input1X'))
                pc.connectAttr((post_mid_normalised_mdn + '.outputX'), (trans_b + '.input1X'), f=True)

                # connecting output of divide node to blend midlock attr
                pc.connectAttr((trans_a + '.outputX'), (post_mid_bta + '.input[0]'), f=True)
                pc.connectAttr((trans_b + '.outputX'), (post_mid_bta + '.input[1]'), f=True)

                # connecting all joints
                pc.connectAttr((post_mid_bta + '.output'), (list[i] + '.' + axis[0]))
        else:
            for i in range(1, middle_index + 1):
                t = pc.getAttr(list[i] + '.' + axis[0])
                trans = pc.createNode('multiplyDivide', n=(list[i] + '_transAbs_md'))
                pc.connectAttr((off_pre_mdn + '.outputX'), (trans + '.input1X'))
                pc.setAttr((trans + '.input2X'), t)
                pc.connectAttr((trans + '.outputX'), (list[i] + '.' + axis[0]))
            for i in range(middle_index + 1, num_joints):
                t = pc.getAttr(list[i] + '.' + axis[0])
                trans = pc.createNode('multiplyDivide', n=(list[i] + '_transAbs_md'))
                pc.connectAttr((off_post_mdn + '.outputX'), (trans + '.input1X'))
                pc.setAttr((trans + '.input2X'), t)
                pc.connectAttr((trans + '.outputX'), (list[i] + '.' + axis[0]))


# print '\n'
# print '======================================================\n'
# print (name + side + '  Stretch Information\n')
# print '------------------------------------------------------\n'
# print ('Actual Joint Chain Length  >>\t' + chainLength + '\n')
# print ('Shortest Distance Length   >>\t' + defaultLength + '\n')
# print '======================================================\n'

# print 'Squash and Stretch Creation Successful! (see script editor for details)'

def build_ik_stretch(name, side, start_joint, end_joint, controller, stretch_type):
    dist = []
    defualt_length = 0.0
    stretch_axis = []

    non_scale_grp = (name + 'non_scale_grp')
    scale_node = (name + 'worldScaleCon_grp')

    non_scale_grp = bw.create_non_scale_grp(name)

    stretch_axis = chUL.getStretchAxis(end_joint, stretch_type)
    dist = chUL.createDistance(start_joint, end_joint, True)
    dist[0] = pc.rename((dist[0]), (name + side + start_joint + '_Ik'))
    dist[1] = pc.rename((dist[1]), (name + side + start_joint + '_Ik'))
    dist[2] = pc.rename((dist[2]), (name + side + start_joint + '_Ik'))
    default_length = pc.getAttr((dist[3] + '.output'))

    pc.pointConstraint(start_joint, dist[1], offset=[0, 0, 0], weight=1)
    pc.pointConstraint(controller, dist[2], offset=[0, 0, 0], weight=1)
    pc.setAttr((dist[0] + '.v'), 0)
    pc.setAttr((dist[1] + '.v'), 0)
    pc.setAttr((dist[2] + '.v'), 0)

    chUL.lockAndHide(dist[0], 'lock', 'trans rot scale vis')
    chUL.lockAndHide(dist[1], 'lock', 'trans rot scale vis')
    chUL.lockAndHide(dist[2], 'lock', 'trans rot scale vis')

    dist_grp = pc.group(em=True, n=(name + side + start_joint + 'IkDistance_grp'))
    pc.parent(dist_grp, non_scale_grp)

    pc.parent(dist[0], dist_grp)
    pc.parent(dist[1], dist_grp)
    pc.parent(dist[2], dist_grp)

    pc.addAttr(controller, k=1, ln='stretch', at='double', min=0, max=1, dv=1)
    ik_handle = pc.ikHandle(name=(name + side + start_joint + '_ikhandle'), startJoint=start_joint,
                            endEffector=end_joint,
                            solver='ikSCsolver')  # TODO: revisit this
    pc.pointConstraint(controller, ik_handle[0], offset=[0, 0, 0], weight=1)
    pc.parent(ik_handle[0], non_scale_grp)
    pc.setAttr((ik_handle[0] + '.visibility'), 0)
    chUL.lockAndHide(ik_handle[0], 'lock', 'vis')

    # create node network fr stretch
    scalar_md = pc.createNode('multiplyDivide', n=(name + side + '_scaler_md'))
    pc.setAttr((scalar_md + '.operation'), 2)
    normalised_md = pc.createNode('multiplyDivide', n=(name + side + '_normalised_md'))
    pc.setAttr((normalised_md + '.operation'), 2)
    stretch_bta = pc.createNode('blendTwoAttr', n=(name + side + '_SsBlend_bta'))
    set_attr = ((stretch_bta + '.input[0]'), 1)
    pc.connectAttr((controller + '.stretch'), (stretch_bta + '.attributesBlender'))

    pc.connectAttr((dist[3] + '.output'), (scalar_md + '.input1X'))
    pc.connectAttr((scale_node + '.scale'), (scalar_md + '.input2'))

    pc.connectAttr((scalar_md + '.outputX'), (normalised_md + '.input1X'))
    pc.setAttr((normalised_md + '.input2X'), default_length)
    pc.connectAttr((normalised_md + '.outputX'), (stretch_bta + '.input[1]'), f=True)

    if stretch_type == 'translate':
        trans_nor_md = pc.createNode('multiplyDivide', n=(name + side + '_transNor_md'))
        temp_val = pc.getAttr(end_joint + '.' + stretch_axis[0])
        pc.setAttr((trans_nor_md + '.input2X'), temp_val)
        pc.connectAttr((normalised_md + '.outputX'), (trans_nor_md + '.input1X'))
        pc.connectAttr((trans_nor_md + '.outputX'), (start_joint + '.' + stretch_axis[0]))

    if stretch_type == 'scale':
        pc.connectAttr((stretch_bta + '.output'), (start_joint + '.' + stretch_axis[0]))
    return ik_handle


# make_joint_volume_setup ('loc1', 'scale', `ls -sl`)
# string controller = 'loc1'
# string stretchType = 'translate'
# string chain[] = `ls -sl`

def make_joint_volume_setup(name, side, controller, stretch_type, chain):
    axis = []
    stretch_axis = []
    twist_axis = []
    child_joint = ''

    stretch_axis = chUL.getStretchAxis(chain[0], stretch_type)
    twist_axis = chUL.getTwistAxis(chain[0])

    # determine twist axis for further info distribution
    if twist_axis[0] == 'rx':
        axis = 'X', 'Y', 'Z'
    elif twist_axis[0] == 'ry':
        axis = 'Y', 'Z', 'X'
    elif twist_axis[0] == 'rz':
        axis = 'Z', 'X', 'Y'

    if not pc.attributeQuery('volume', n=controller, ex=True):
        pc.addAttr(controller, k=1, at='double', min=-1, max=1, dv=1, ln='volume')

    # select all joints of ik chain
    pc.select(chain)
    create_curve_control(chain[0], 'scalePower', 'pow')

    for i in range(len(chain) - 1):
        nor_div = pc.createNode('multiplyDivide', n=(name + side + chain[i] + '_revPowInput_md'))
        pc.setAttr((nor_div + '.operation'), 3)
        pc.setAttr((nor_div + '.input2X'), .5)

        if stretch_type == 'translate':
            trans_nor = pc.createNode('multiplyDivide', n=(name + side + chain[i] + '_transNor_md'))
            pc.setAttr((trans_nor + '.operation'), 2)
            child_joint = chUL.getChildJoint(chain[i])
            temp_val = pc.getAttr(child_joint + '.translate' + axis[0])
            pc.setAttr((trans_nor + '.input2X'), temp_val)
            pc.connectAttr((child_joint + '.translate' + axis[0]), (trans_nor + '.input1X'))
            pc.connectAttr((trans_nor + '.outputX'), (nor_div + '.input1X'))
        else:
            pc.connectAttr((chain[i] + '.scale' + axis[0]), (nor_div + '.input1X'))

        rev_pow1 = pc.createNode('multiplyDivide', n=(name + side + chain[i] + '_normalizes_rev_md'))
        pc.setAttr((rev_pow1 + '.operation'), 2)
        pc.setAttr((rev_pow1 + '.input1X'), 1)
        pc.connectAttr((nor_div + '.outputX'), (rev_pow1 + '.input2X'))

        rev_pow2 = pc.createNode('multiplyDivide', n=(name + side + chain[i] + '_revPowOutput_md'))
        pc.setAttr((rev_pow2 + '.operation'), 3)
        pc.setAttr((rev_pow2 + '.input1Y'), 1)

        pc.connectAttr((rev_pow1 + '.outputX'), (rev_pow2 + '.input1X'))
        pc.connectAttr((chain[i] + '.pow'), (rev_pow2 + '.input2X'))

        vol_bta = pc.createNode('blendTwoAttr', n=(name + side + chain[i] + '_volume_bta'))
        pc.connectAttr((controller + '.volume'), (vol_bta + '.attributesBlender'))
        pc.connectAttr((rev_pow2 + '.outputX'), (vol_bta + '.input[1]'))
        pc.connectAttr((rev_pow2 + '.outputY'), (vol_bta + '.input[0]'))

        pc.connectAttr((vol_bta + '.output'), (chain[i] + '.scale' + axis[1]), f=True)
        pc.connectAttr((vol_bta + '.output'), (chain[i] + '.scale' + axis[2]), f=True)


# stretchy_spline spline '' loc1 scale curve1 1 1 curve1
def stretchy_spline(name, side, controller, stretch_type, crv, world_scale, volume, scale):
    shape = []
    chain = []
    con = []
    ik_handle = ''
    stretch_axis = []

    pc.addAttr(controller, k=1, at='double', min=0, max=1, dv=1, ln='stretching')
    rev = pc.createNode('reverse', n=(name + side + 'stretchAttr_rev'))
    pc.connectAttr((controller + '.stretching'), (rev + '.inputX'))
    info = pc.createNode('curveInfo', name=(name + side + crv + '_info'))
    pc.connectAttr((crv + '.worldSpace[0]'), (info + '.inputCurve'), f=True)
    l = pc.getAttr(info + '.arcLength')

    div = pc.createNode('multiplyDivide', n=(name + side + 'lenDivide_md'))
    pc.setAttr((div + '.operation'), 2)
    pc.connectAttr((info + '.arcLength'), (div + '.input1X'))

    div_a = pc.createNode('multiplyDivide', n=(name + side + 'scaleFactor_md'))
    pc.setAttr((div_a + '.operation'), 2)
    pc.connectAttr((div + '.outputX'), (div_a + '.input1X'))
    pc.setAttr((div_a + '.input2X'), l)
    pc.setAttr((div_a + '.input1Y'), 1)
    pc.setAttr((div_a + '.input2Y'), 1)

    bta = pc.createNode('blendTwoAttr', n=(name + side + 'stretchBlend_bta'))
    pc.connectAttr((rev + '.outputX'), (bta + '.attributesBlender'))
    pc.connectAttr((div_a + '.outputX'), (bta + '.input[0]'))
    pc.connectAttr((div_a + '.outputY'), (bta + '.input[1]'))

    div_b = pc.createNode('multiplyDivide', n=(name + side + 'absMulti_md'))
    pc.setAttr((div_b + '.operation'), 2)
    pc.setAttr((div_b + '.input2X'), 1)
    pc.connectAttr((bta + '.output'), (div_b + '.input1X'))

    # get all information for stretching
    print('crv:', crv)
    shape = pc.listRelatives(crv, fullPath=True, shapes=True)
    print('shape:', shape)
    con = pc.listConnections((shape[0] + '.worldSpace[0]'), type='ikHandle')
    print('con:', con)
    ik_handle = con[0]
    print('ikHandle:', ik_handle)
    chain = pc.ikHandle(ik_handle, q=True, jointList=True)
    temp_count = len(chain)
    child_joint = chUL.getChildJoint(chain[temp_count - 1])
    full_chain = chain
    # insert at index, in list, this item
    full_chain.append(child_joint)
    print('stretchAxis:', chain[1])
    stretch_axis = chUL.getStretchAxis(chain[1], str(stretch_type))
    print('stretchType:', stretch_type)

    print('stretchAxis:', stretch_axis)
    if stretch_axis[0] == 'tx':
        axis = 'X', 'Y', 'Z'
    elif stretch_axis[0] == 'ty':
        axis = 'Y', 'Z', 'X'
    elif stretch_axis[0] == 'tz':
        axis = 'Z', 'X', 'Y'

    if world_scale == 0 and volume == 0:
        # connect scaleAttr for all joints
        if stretch_type == 'scale':
            for c in chain:
                pc.connectAttr((div_b + '.outputX'), (c + '.' + stretch_axis[0]))
        else:
            for c in len(chain):
                trans_nor = pc.createNode('multiplyDivide', n=(name + side + chain[c] + '_transNor_md'))
                child_joint = chUL.getChildJoint(chain[c])
                temp_val = pc.getAttr(child_joint + '.translate' + axis[0])
                pc.setAttr((trans_nor + '.input2X'), temp_val)
                pc.connectAttr((div_b + '.outputX'), (trans_nor + '.input1X'))
                pc.connectAttr((trans_nor + '.outputX'), (full_chain[c + 1] + '.' + stretch_axis[0]))
    else:
        if world_scale == 1 and volume == 0:
            # connectAttr for global scaling
            pc.connectAttr((scale + '.scale'), (div + '.input2'))
            # connect scaleAttr for all joints
            if stretch_type == 'scale':
                for c in chain:
                    pc.connectAttr((div_b + '.outputX'), (c + '.' + stretch_axis[0]))
            else:
                for c in len(chain):
                    trans_nor = pc.createNode('multiplyDivide', n=(name + side + chain[c] + '_transNor_md'))
                    child_joint = chUL.getChildJoint(chain[c])
                    temp_val = pc.getAttr(child_joint + '.translate' + axis[0])
                    pc.setAttr((trans_nor + '.input2X'), temp_val)
                    pc.connectAttr((div_b + '.outputX'), (trans_nor + '.input1X'))
                    pc.connectAttr((trans_nor + '.outputX'), (full_chain[c + 1] + '.' + stretch_axis[0]))
        else:
            # connectAttr for global scaling
            pc.connectAttr((scale + '.scale'), (div + '.input2'))
            if stretch_type == 'scale':
                for c in chain:
                    pc.connectAttr((div_b + '.outputX'), (c + '.' + stretch_axis[0]))
            else:
                for c in range(len(chain) - 1):
                    trans_nor = pc.createNode('multiplyDivide', n=(name + side + chain[c] + '_transNor_md'))
                    child_joint = chUL.getChildJoint(chain[c])
                    temp_val = pc.getAttr(child_joint + '.translate' + axis[0])
                    pc.setAttr((trans_nor + '.input2X'), temp_val)
                    pc.connectAttr((div_b + '.outputX'), (trans_nor + '.input1X'))
                    pc.connectAttr((trans_nor + '.outputX'), (full_chain[c + 1] + '.' + stretch_axis[0]))
            make_joint_volume_setup(name, side, controller, stretch_type, chain)


# based of Jason Schleifer's code
def create_curve_control(control_obj, control_attribute, destination_attribute):
    if not pc.objExists(control_obj):
        pc.error(control_obj + ' does not exist.  Exiting..\n')

    if not pc.attributeQuery(control_attribute, node=control_obj, exists=True):
        pc.addAttr(control_obj, ln=control_attribute, at='double')
        pc.setAttr((control_obj + '.' + control_attribute), k=1)

    objs = pc.ls(sl=True)

    if len(objs) == 0:
        pc.error('Nothing Selected.\n')

    num_controls = len(objs)
    obj_attr = (control_obj + '.' + control_attribute)
    pc.setKeyframe(control_obj, at=control_attribute, t=1, v=0)
    pc.setKeyframe(control_obj, at=control_attribute, t=num_controls, v=0)

    pc.keyTangent(control_obj, wt=1, at=control_attribute)
    pc.keyTangent(control_obj, weightLock=False, at=control_attribute)

    pc.keyTangent(obj_attr, e=True, a=True, t=1, outAngle=50)
    pc.keyTangent(obj_attr, e=True, a=True, t=num_controls, inAngle=-50)

    for x in range(num_controls):
        fc = pc.createNode('frameCache')
        fc = pc.rename(fc, (objs[x] + '_frameCache'))
        pc.connectAttr(obj_attr, (fc + '.stream'))
        pc.setAttr((fc + '.vt'), (x + 1))
        if not pc.attributeQuery(destination_attribute, exists=True, node=objs[x]):
            pc.addAttr(objs[x], ln=destination_attribute, at='double')
            pc.setAttr((objs[x] + '.' + destination_attribute), k=1)
        pc.connectAttr((fc + '.v'), (objs[x] + '.' + destination_attribute), f=True)
