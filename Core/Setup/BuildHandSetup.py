from Maya_Rigging.Core.BuildWorld import build_world
from Maya_Rigging.Utils.CharUtilsLib import *

def buildHandSetup(name,
                   side,
                   controller,
                   fkC,
                   controlType,
                   numFingers,
                   fingerName,
                   baseJoint,
                   fingerAxis,
                   nameMethod,
                   skipLast,
                   consType,
                   world,
                   scale,
                   controlColor):
    i = 0,
    j = 0
    installCurl = 1
    curlAxis = fingerAxis[1]
    installSpread = 1
    spreadAxis = fingerAxis[2]
    installSpin = 1
    spinAxis = fingerAxis[0]
    installStretch = 1
    stretchAxis = fingerAxis[3]         
    # int fkControl    = 1
    # int nameMethod      = 2
    # int skipLast        = 1 #in arguments
    # int numFingers      = 3 #in arguments
    # string fingerName[] = {'thumb','index','mid','ring','pinky'}#in arguments
    # string startJoint[] = {'joint1','joint5','joint9'}  #in arguments

    stepTemp = (numFingers/2) 
    step = (1.00/stepTemp)

    # if installing spreads we need to make some controller attributes to reverse the direction
    if installSpread == 1:
        j = 1
        
        # add attributes to offset the full spread
        for i in range(numFingers):
            # add an attribute on it
            if i < stepTemp: 
                pc.addAttr(controller, k=0, ln=(fingerName[i] + 'SpreadOffset'), at='double', dv=(1 - (i * step)))
            elif (i+.5) == (numFingers/2.00):
                pc.addAttr(controller, k=0, ln=(fingerName[i] + 'SpreadOffset'), at='double', dv=0)
            elif i < (numFingers-1):
                pc.addAttr(controller, k=0, ln=(fingerName[i] + 'SpreadOffset'), at='double', dv=(-1 * j * step))
                j += 1
            else: 
                pc.addAttr(controller, k=0, ln=(fingerName[i] + 'SpreadOffset'), at='double', dv=(-1))

    # end of installSpreads function
         
    # create some attributes on the controller
    pc.addAttr(controller, k=1, ln='fingerCONTROLS', at='enum', en='-------------')
    pc.setAttr((controller + '.fingerCONTROLS'), lock=True)

    # string controlType = 'square'
    fkFingerJoints = []
    startJoint = []
    # create fk control for finger
    if fkC:
        list = listHierarchy(baseJoint[0])
        size = len(list)
        pc.addAttr(controller, ln='fingerFkVis', dv=1, at='bool', keyable=True)
        pc.setAttr((controller + '.fingerFkVis'), keyable=False, channelBox=True)

        for i in range(numFingers):
            fkFingerJoints = fkControl(baseJoint[i], controlType, 0, controlColor)
            startJoint.append(fkFingerJoints[0])
            pc.connectAttr((controller + '.fingerFkVis'), (fkFingerJoints[0] + '.v'))

    ########
    # Run installs
    # 
    if installCurl == 1:
        # add curl separator attribute
        pc.addAttr(controller, k=1, ln='CURLS', at='enum', en='-------------')
        pc.setAttr((controller + '.CURLS'), lock=True)

        # add full hand curl attribute (.fullCurl)
        pc.addAttr(controller, k=1, ln='fullCurl', at='double', dv=0)

        # install the specific finger controls
        installFingers(1, curlAxis, controller, fingerName, startJoint, numFingers, skipLast, nameMethod)

    if installSpread == 1:
        # add curl separator attribute
        pc.addAttr(controller, k=1, ln='SPREADS', at='enum', en='-------------')
        pc.setAttr((controller + '.SPREADS'), lock=True)

        # add full hand curl attribute (.fullCurl)
        pc.addAttr(controller, k=1, ln='fullSpread', at='double', dv=0)

        # install the specific finger controls
        installFingers(2, spreadAxis, controller, fingerName, startJoint, numFingers, skipLast, nameMethod)

    if installSpin == 1:
        # add curl separator attribute
        pc.addAttr(controller, k=1, ln='SPINS', at='enum', en='-------------')
        pc.setAttr((controller + '.SPINS'), lock=True)

        # install the specific finger controls
        installFingers(3, spinAxis, controller, fingerName, startJoint, numFingers, skipLast, nameMethod)
    
    if installStretch == 1:
        # add curl separator attribute
        pc.addAttr(controller, k=1, ln='STRETCH', at='enum', en='-------------')
        pc.setAttr((controller + '.STRETCH'), lock=True)

        # install the specific finger controls
        installFingers(4, stretchAxis, controller, fingerName, startJoint, numFingers, skipLast, nameMethod)

    # zeroOut finger joints and transfer connection to grp .....
    if fkC:
        partGrp = pc.group(em=True)
        partGrp = pc.rename(partGrp, (name + side + 'fingersParts_grp#'))
        lockAndHide(partGrp, 'locknHide', 'trans rot scale')

        if world:
            cleanGrp = build_world(name, scale)
            pc.parent(partGrp, cleanGrp[0])

        for i in range(numFingers):
            zeroGrp = []
            grp = []
            list = listHierarchy(startJoint[i])
            size = len(list)
            # this local scale for control
            resizeCurves(list, 1, 1, 1, 0.5)
            # now apply global scale for control
            resizeCurves(list, 1, 1, 1, scale)

            for j in range(len(list)):
                grp = quickJointZeroOut(list[j])                
                transferConnection(list[j], grp[0], 'rx')
                transferConnection(list[j], grp[0], 'ry')
                transferConnection(list[j], grp[0], 'rz')
                lockAndHide(list[j], 'locknHide', 'trans scale vis')                
                zeroGrp.append(grp[0])

            # for(x=0x<(size-1)x++)connectAttr (zeroGrp[x]+'.scale') (list[x]+'.inverseScale')
            parent = getParent(zeroGrp[0])
            parentGrp = quickZeroOut(zeroGrp[0])
            pc.parent(parentGrp[0], partGrp)
            
            if parent:
                if consType == 'parent':
                    pc.parentConstraint(parent, parentGrp[0], mo=True, w=1)
                else:
                    pc.pointConstraint(parent, parentGrp[0], mo=True, w=1)
                    pc.orientConstraint(parent, parentGrp[0], mo=True, w=1)

            pc.select(zeroGrp, r=True)
            lockAndHide('', 'lock', 'trans rot scale vis')
            lockAndHide(parentGrp[0],'lock','trans rot scale vis')
            pc.select(cl=True)

            if skipLast:
                pc.delete(list[size-1])
        # end loop zeroOut

    # create skin Joint set
    sknJoints = []
    for i in range(numFingers):
        list = listHierarchy(baseJoint[i])        
        sknJoints.extend(list)

    set = createSkinJointSet(name)
    addSkinJointToSet(set, sknJoints)

    pc.select(controller, r=True)

def installFingers(installOpt, installAxis, controller, fingerName, startJoint, numFingers, skipLast, nameMethod):
    size = 0
    curlMDN = []
    fingerJoints = []
    damp = 0

    fingerJoints.append(startJoint[0])

    fingerJoints = listHierarchy(startJoint[0])
    if skipLast:
        size = len(fingerJoints)-1
    else:
        size = len(fingerJoints)

    if installOpt == 1:
        # create attribute for offset each section of finger
        for i in range(size):
            # create the MDN
            curlMDN.append(pc.createNode('multDoubleLinear', n=('fingerCurlAdjust_' + str(i+1) + '_mdl')))
            # hook the full curl to the input1X
            pc.connectAttr((controller + '.fullCurl'), (curlMDN[i] + '.input1'), f=True)
            # create custom attributes to adjust these
            pc.addAttr(controller, k=0, ln=('curlOffset_s' + str(i+1)), at='double', dv=(.9 + (i/10.00)))
            # hook the custom attributes up
            pc.connectAttr((controller + '.curlOffset_s'+ str(i+1)), (curlMDN[i] + '.input2'), f=True)

    for i in range(numFingers):
        fingerJoints = listHierarchy(startJoint[i])

        location = []  # holds the sub finger naming based on naming method
        if nameMethod == 1:
            for j in range(size+1):
                location[(j-1)] = j

        if nameMethod == 2:
            location = ['_A_','_B_','_C_','_D_','_E_','_F_','_G_','_H_','_I_','_J_','_K_','_L_','_M_','_N_','_O_','_P_','_Q_','_R_','_S_','_T_','_U_','_V_','_W_','_X_','_Y_','_Z_']
        if nameMethod == 3:
            location = ['Base', 'Mid', 'Tip']
    
        installCaps = ['', 'CURLS', 'SPREADS', 'SPINS', 'STRETCH']
        installLower = ['', 'Curl', 'Spread', 'Spin', 'Stretch']
        axis = ['', 'X', 'Y', 'Z']
   
        if installOpt == 1:
            Cap = fingerName[i].upper()
            
            pc.addAttr(controller, k=1, ln=('___' + Cap + '___'), at='enum', en='-------------')
            pc.setAttr((controller + '.' + ('___' + Cap + '___')), lock=True)
            
            if pc.attributeQuery('damp', n=startJoint[i], ex=True):
                try:
                    pc.deleteAttr(startJoint[i], attribute='damp')
                except:
                    pass
                pc.addAttr(controller, ln=(fingerName[i] + 'Damp'), min=0, max=1, dv=0.3, at='double', keyable=True)
                pc.setAttr((controller + '.' + fingerName[i] + 'Damp'), keyable=False, channelBox=True)
                damp = 1
            else: 
                damp = 0

            for j in range(size):
                pc.addAttr(controller, ln=(fingerName[i] + location[j] + installLower[installOpt]), at='double', keyable=True)

                # create a variable and ASN to add the rotations/scale for the selected install
                ASN = pc.createNode('addDoubleLinear', n=(fingerJoints[j] + '_r' + axis[installAxis] + '_adl')) # if rotations are installed

                if damp:
                    DampMDN = pc.createNode('multDoubleLinear', n=(startJoint[i] + '_r' + axis[installAxis] + 'Damp_mdl'))
                    pc.connectAttr((curlMDN[j] + '.output'), (DampMDN + '.input1'), f=True)
                    pc.connectAttr((controller + '.' + fingerName[i] + 'Damp'), (DampMDN + '.input2'), f=True)
                    pc.connectAttr((DampMDN + '.output'), (ASN + '.input1'), f=True)
                else:
                    pc.connectAttr((curlMDN[j] + '.output'), (ASN + '.input1'), f=True)

                # hook up the individual control to the ASN
                pc.connectAttr((controller + '.' + fingerName[i] + location[j] + installLower[installOpt]), (ASN + '.input2'), f=True)

                # hook the ASN to the joint
                pc.connectAttr((ASN + '.output'), (fingerJoints[j] + '.rotate' + axis[installAxis]), f=True)

        elif installOpt == 4: # STRETCH
            # create a specific attribute for the finger stretch
            pc.addAttr(controller, k=1, ln=(fingerName[i] + installLower[installOpt]), at='double', min=.01, dv=1)
            for j in range(size):
                # connect the finger spread to the joints for that finger
                pc.connectAttr((controller + '.' + fingerName[i] + installLower[installOpt]), (fingerJoints[j] + '.scale' + axis[installAxis]), f=True)

        elif installOpt == 2: # SPREADS
            # create an attribute for this finger
            pc.addAttr(controller, k=1, ln=(fingerName[i] + installLower[installOpt]), at='double', dv=0)

            # create an ASN
            ASN = pc.createNode('addDoubleLinear', n=(startJoint[i] + '_r' + axis[installAxis] + '_adl'))

            # create an MDN
            MDN = pc.createNode('multDoubleLinear', n=(startJoint[i] + '_r' + axis[installAxis] + '_mdl'))

            # hook up the ASN to the output of the MDN and the finger spread attr
            pc.connectAttr((MDN + '.output'), (ASN + '.input1'), f=True)
            pc.connectAttr((controller + '.' + fingerName[i] + installLower[installOpt]), (ASN + '.input2'), f=True)

            # hook the MDN up to the controller's adjusters and the controller.fullSpread
            pc.connectAttr((controller + '.' + fingerName[i] + 'SpreadOffset'), (MDN + '.input1'), f=True)
            pc.connectAttr((controller + '.fullSpread'), (MDN + '.input2'), f=True)

            # hook up the ASN to the joint
            pc.connectAttr((ASN + '.output'), (startJoint[i] + '.rotate' + axis[installAxis]), f=True)

        elif installOpt == 3: # SPINS
            # create the attribute for this finger
            pc.addAttr(controller, k=1, ln=(fingerName[i] + installLower[installOpt]), at='double', dv=0)

            # connect it to the base joint for the finger
            pc.connectAttr((controller + '.' + fingerName[i] + installLower[installOpt]), (startJoint[i] + '.rotate' + axis[installAxis]), f=True)