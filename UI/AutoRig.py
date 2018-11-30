from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya import OpenMayaUI as omui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from Maya_Rigging.Core import ModuleSymmetryLib as msLib
from Maya_Rigging.Core import DummyRigPartModulesLib as drLib
from Maya_Rigging.Core import BuildModuleJointSkeleton as bmjs
from Maya_Rigging.Core.UI import CreateModuleRigFromUI as cmr
from Maya_Rigging.Core import ModuleTemplates as mt

from CollapsibleButton import CollapsibleButton
from ColorSpinBox import ColorSpinBox
from Util import rigSideSep

autoRigMixinWindow = None

def Open(*args):
    DockableWidgetUI()

def DockableWidgetUI(restore=False):
    global autoRigMixinWindow

    restoredControl = None
    if restore == True:
        restoredControl = omui.MQtUtil.getCurrentParent()

    if autoRigMixinWindow is None:
        autoRigMixinWindow = DockableWidget()
        autoRigMixinWindow.setObjectName('autoRigMixinWindow')

    if restore == True:
        mixinPtr = omui.MQtUtil.findControl(autoRigMixinWindow.objectName())
        omui.MQtUtil.addWidgetToMayaLayout(long(mixinPtr), long(restoredControl))
    else:
        autoRigMixinWindow.show(dockable=True, height=600, width=480, uiScript='DockableWidgetUI(restore=True)')

    return autoRigMixinWindow

class DockableWidget(MayaQWidgetDockableMixin, QWidget):
    toolName = 'autoRigWidget'
    """
    Main AutoRig UI class
    """
    def __init__(self, parent=None):
        #self.delete_instance()

        super(DockableWidget, self).__init__(parent=parent)
        #self.mayaMainWindow = getMayaWindow()
        self.setObjectName(self.__class__.toolName)

        self.setWindowFlags(Qt.Window)
        self.setWindowTitle('AutoRig')
        self.setMinimumWidth(400)
        self.setMaximumWidth(400)

        # main vertical layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.inner_layout = QVBoxLayout(self)

        # Create button panels
        self.globalButton()
        self.templatesButton()
        self.modulesButton()
        self.inner_layout.addStretch(1)

        # Setup the main scroll area
        scrollList = QScrollArea()
        scrollList.setFrameShape(QFrame.NoFrame)
        scrollList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrollList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollList.setWidgetResizable(False)

        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(self.inner_layout)
        scrollList.setWidget(self.scroll_widget)

        self.main_layout.addWidget(scrollList)

        # Non scroll panels
        self.modifyButtons()
        self.generateButtons()

        self.show(dockable=True)

    # Button Panels Methods
    # =====================================================================
    def globalButton(self):

        v_list = QVBoxLayout()

        font = QFont()
        font.setPixelSize(12)
        font.setBold(True)

        def h_layout1():

            h_layout = QHBoxLayout()
            v_list.addLayout(h_layout, stretch=0)

            # Name Label
            labelName = QLabel('Name')
            h_layout.addWidget(labelName)
            # add spacer
            spacer = QSpacerItem(15, 10)
            h_layout.addSpacerItem(spacer)

            # name input
            self.rig_name = QLineEdit()
            h_layout.addWidget(self.rig_name)

            # Side Label
            labelSide = QLabel('Side Prefix')
            h_layout.addWidget(labelSide)
            # add spacer
            spacer = QSpacerItem(15, 10)
            h_layout.addSpacerItem(spacer)

            # Combo box
            self.side_prefix = QComboBox()
            self.side_prefix.addItems(['l/r', 'lt/rt', 'left/right', 'custom', 'none'])
            self.side_prefix.setFixedWidth(80)
            h_layout.addWidget(self.side_prefix)

        # Color Labels
        def h_layout2():

            h_layout = QHBoxLayout()
            v_list.addLayout(h_layout, stretch=0)

            self.right_cb = ColorSpinBox(h_layout, 'Right', 10)
            self.center_cb = ColorSpinBox(h_layout, 'Center', 15)
            self.left_cb = ColorSpinBox(h_layout, 'Left', 26)

        def h_layout3():

            h_layout = QHBoxLayout()
            v_list.addLayout(h_layout, stretch=0)

            # Combo box
            self.stretch_combobox = QComboBox()
            # TODO: update code dependency to allow for Scale instead of scale, case difference
            self.stretch_combobox.addItems(['scale', 'translate', 'none'])
            h_layout.addWidget(self.stretch_combobox)
            # Stretch Checkbox
            stretch_label = QLabel('Stretch')
            h_layout.addWidget(stretch_label)

            # Volume CheckBox
            self.volume_checkbox = QCheckBox('Volume')
            h_layout.addWidget(self.volume_checkbox)
            self.volume_checkbox.toggle()

            self.midlock_checkbox = QCheckBox('Mid Lock')
            h_layout.addWidget(self.midlock_checkbox)
            self.midlock_checkbox.toggle()

        h_layout1()
        h_layout2()
        h_layout3()

        collapsible_button = CollapsibleButton(self.inner_layout, v_list, 'Global', 350, font)

        return collapsible_button.widget

    def templatesButton(self):
        h_list = QHBoxLayout()

        font = QFont()
        font.setPixelSize(12)
        font.setBold(True)

        def biped():

            group = QGroupBox('Biped')
            group.setMaximumWidth(200)

            inner_list = QVBoxLayout()
            group.setLayout(inner_list)

            h_layout1 = QHBoxLayout()
            inner_list.addLayout(h_layout1)
            spine = QSpinBox()
            spine.setFixedWidth(35)
            spine.setValue(4)
            h_layout1.addWidget(spine)
            label_spine = QLabel('Spine')
            h_layout1.addWidget(label_spine)

            neck = QSpinBox()
            neck.setFixedWidth(35)
            neck.setValue(1)
            h_layout1.addWidget(neck)
            label_neck = QLabel('Neck')
            h_layout1.addWidget(label_neck)

            h_layout3 = QHBoxLayout()
            inner_list.addLayout(h_layout3)
            fingers = QCheckBox('Fingers')
            fingers.toggle()
            h_layout3.addWidget(fingers)

            f_joints = QSpinBox()
            f_joints.setFixedWidth(35)
            f_joints.setValue(5)
            h_layout3.addWidget(f_joints)
            label_f_joints = QLabel('Joints')
            h_layout3.addWidget(label_f_joints)

            h_layout4 = QHBoxLayout()
            inner_list.addLayout(h_layout4)
            toes = QCheckBox('Toes')
            toes.toggle()
            h_layout4.addWidget(toes)
            t_joints = QSpinBox()
            t_joints.setFixedWidth(35)
            t_joints.setValue(5)
            h_layout4.addWidget(t_joints)
            label_t_joints = QLabel('Joints')
            h_layout4.addWidget(label_t_joints)

            create = QPushButton('Create')
            inner_list.addWidget(create)

            def disable_fingers():
                f_joints.setEnabled(fingers.isChecked())
                label_f_joints.setEnabled(fingers.isChecked())

            fingers.stateChanged.connect(disable_fingers)

            def disable_toes():
                t_joints.setEnabled(toes.isChecked())
                label_t_joints.setEnabled(toes.isChecked())

            toes.stateChanged.connect(disable_toes)

            def build_biped():
                mt.bipedModuleTemplate(self.rig_name.text(),
                                       spine.value(),
                                       neck.value(),
                                       fingers.isChecked(),
                                       f_joints.value(),
                                       toes.isChecked(),
                                       t_joints.value())

            create.clicked.connect(build_biped)

            return group

        def quadroped():

            group = QGroupBox('Quadroped')
            group.setMaximumWidth(200)

            inner_list = QVBoxLayout()
            group.setLayout(inner_list)

            h_layout1 = QHBoxLayout()
            inner_list.addLayout(h_layout1)
            spine = QSpinBox()
            spine.setFixedWidth(35)
            spine.setValue(4)
            h_layout1.addWidget(spine)
            label_spine = QLabel('Spine')
            h_layout1.addWidget(label_spine)

            neck = QSpinBox()
            neck.setFixedWidth(35)
            neck.setValue(2)
            h_layout1.addWidget(neck)
            label_neck = QLabel('Neck')
            h_layout1.addWidget(label_neck)

            h_layout3 = QHBoxLayout()
            inner_list.addLayout(h_layout3)
            ears = QSpinBox()
            ears.setFixedWidth(35)
            ears.setValue(4)
            h_layout3.addWidget(ears)
            label_ears = QLabel('Ears')
            h_layout3.addWidget(label_ears)

            tail = QSpinBox()
            tail.setFixedWidth(35)
            tail.setValue(7)
            h_layout3.addWidget(tail)
            label_tail = QLabel('Tail')
            h_layout3.addWidget(label_tail)

            h_layout4 = QHBoxLayout()
            inner_list.addLayout(h_layout4)
            toes = QCheckBox('Toes')
            toes.toggle()
            h_layout4.addWidget(toes)
            t_joints = QSpinBox()
            t_joints.setFixedWidth(35)
            t_joints.setValue(5)
            h_layout4.addWidget(t_joints)
            label_t_joints = QLabel('Joints')
            h_layout4.addWidget(label_t_joints)

            create = QPushButton('Create')
            inner_list.addWidget(create)

            def disable_toes():
                t_joints.setEnabled(toes.isChecked())
                label_t_joints.setEnabled(toes.isChecked())

            toes.stateChanged.connect(disable_toes)

            def build_quadroped():
                mt.quadModuleTemplate(self.rig_name.text(),
                                      spine.value(),
                                      neck.value(),
                                      ears.value(),
                                      tail.value(),
                                      toes.isChecked(),
                                      t_joints.value())

            create.clicked.connect(build_quadroped)

            return group

        h_list.addWidget(biped())
        h_list.addWidget(quadroped())

        collapsible_button = CollapsibleButton(self.inner_layout, h_list, 'Templates', 350, font)
        return collapsible_button.widget

    def modulesButton(self):

        # create widget layout
        v_list = QVBoxLayout()

        font = QFont()
        font.setPixelSize(12)
        font.setBold(True)

        side_list = ['Left', 'Right', 'Symmetry']
        axis_list = ['X', 'Y', 'Z']

        def arm():

            group = QGroupBox('Arm')
            v_list.addWidget(group)
            inner_list = QVBoxLayout()
            group.setLayout(inner_list)

            # h layout1
            h_layout1 = QHBoxLayout()
            inner_list.addLayout(h_layout1)

            # Joints input
            joints_box = QSpinBox()
            joints_box.setMaximumWidth(35)
            joints_box.setValue(3)
            h_layout1.addWidget(joints_box)

            # Joints Label
            label_joints = QLabel('Joints')
            h_layout1.addWidget(label_joints)

            # Dynamic & Offset Ctr
            dynamic = QCheckBox('Dynamic')
            h_layout1.addWidget(dynamic)
            offset = QCheckBox('Offset')
            h_layout1.addWidget(offset)

            # Combo box
            side_combo = QComboBox()
            side_combo.addItems(side_list)
            side_combo.setCurrentIndex(2)
            h_layout1.addWidget(side_combo)

            # Side Label
            labelSide = QLabel('Side')
            h_layout1.addWidget(labelSide)

            # h layout2
            h_layout2 = QHBoxLayout()
            inner_list.addLayout(h_layout2)

            # Fingers CheckBox
            fingers_box = QCheckBox('Fingers')
            h_layout2.addWidget(fingers_box)

            # Segments Input
            count_box = QSpinBox()
            count_box.setValue(5)
            count_box.setMaximumWidth(35)
            h_layout2.addWidget(count_box)

            # Segments Label
            label_count = QLabel('Count')
            h_layout2.addWidget(label_count)

            # Segments Input
            segments_box = QSpinBox()
            segments_box.setValue(4)
            segments_box.setMaximumWidth(35)
            h_layout2.addWidget(segments_box)

            # Segments Label
            label_segments = QLabel('Segments')
            h_layout2.addWidget(label_segments)

            spacer = QSpacerItem(70, 10)
            h_layout2.addSpacerItem(spacer)

            # h layout3
            h_layout3 = QHBoxLayout()
            inner_list.addLayout(h_layout3)

            createArm = QPushButton('Create')
            h_layout3.addWidget(createArm)

            def disable_fingers():
                count_box.setEnabled(fingers_box.isChecked())
                label_count.setEnabled(fingers_box.isChecked())
                segments_box.setEnabled(fingers_box.isChecked())
                label_segments.setEnabled(fingers_box.isChecked())

            fingers_box.stateChanged.connect(disable_fingers)
            fingers_box.toggle()

            def build_arm():
                name = self.rig_name.text()
                if name != '':
                    name = (name + '_')

                numJoints = joints_box.value()
                fingers = fingers_box.isChecked()
                numFingers = count_box.value()
                numSegment = segments_box.value()

                leftColorIndex = self.left_cb.index()
                rightColorIndex = self.right_cb.index()

                # TODO: handle custom side prefix
                if side_combo.currentIndex() == 2:
                    # left
                    drLib.buildArmDummySkeletonModule(name,
                                                      self.prefix_left(),
                                                      numJoints,
                                                      fingers,
                                                      numFingers,
                                                      numSegment,
                                                      leftColorIndex)
                    # right
                    drLib.buildArmDummySkeletonModule(name,
                                                      self.prefixRight(),
                                                      numJoints,
                                                      fingers,
                                                      numFingers,
                                                      numSegment,
                                                      rightColorIndex)

                    master = (name + self.prefix_left() + 'armPlacer_loc')
                    slave = (name + self.prefixRight() + 'armPlacer_loc')
                    msLib.buildArmModuleSymmetry(master, slave)

                else:
                    if side_combo.currentIndex() == 0:
                        side = self.prefix_left()
                        colorIndex = leftColorIndex
                    else:
                        side = self.prefixRight()
                        colorIndex = leftColorIndex
                    drLib.buildArmDummySkeletonModule(name,
                                                      side,
                                                      numJoints,
                                                      fingers,
                                                      numFingers,
                                                      numSegment,
                                                      colorIndex)
                    if side_combo.currentIndex() == 1:
                        msLib.mirrorModuleTemplates(name + side + 'armPlacer_loc')

            createArm.clicked.connect(build_arm)

        def leg():

            group = QGroupBox('Leg')
            v_list.addWidget(group)
            inner_list = QVBoxLayout()
            group.setLayout(inner_list)

            # h layout1
            h_layout1 = QHBoxLayout()
            inner_list.addLayout(h_layout1, stretch=0)

            # Joints input
            joints_box = QSpinBox()
            joints_box.setValue(3)
            joints_box.setMaximumWidth(35)
            h_layout1.addWidget(joints_box)

            # Joints Label
            label_joints = QLabel('Joints')
            h_layout1.addWidget(label_joints)

            # Dynamic & Offset Ctr
            dynamic = QCheckBox('Dynamic')
            h_layout1.addWidget(dynamic)
            offset = QCheckBox('Offset')
            h_layout1.addWidget(offset)

            # Combo box
            side_combo = QComboBox()
            side_combo.addItems(side_list)
            side_combo.setCurrentIndex(2)
            h_layout1.addWidget(side_combo)

            # Side Label
            label_side = QLabel('Side')
            h_layout1.addWidget(label_side)

            # h layout2
            h_layout2 = QHBoxLayout()
            inner_list.addLayout(h_layout2, stretch=0)

            # Fingers CheckBox
            fingers_box = QCheckBox('Fingers')
            h_layout2.addWidget(fingers_box)

            # Segments Input
            count_box = QSpinBox()
            count_box.setValue(5)
            count_box.setMaximumWidth(35)
            h_layout2.addWidget(count_box)

            # Segments Label
            label_count = QLabel('Count')
            h_layout2.addWidget(label_count)

            # Segments Input
            segments_box = QSpinBox()
            segments_box.setValue(4)
            segments_box.setMaximumWidth(35)
            h_layout2.addWidget(segments_box)

            # Segments Label
            label_segments = QLabel('Segments')
            h_layout2.addWidget(label_segments)

            # Quadroped CheckBox
            quadroped_box = QCheckBox('Quadroped')
            h_layout2.addWidget(quadroped_box)

            # h layout3
            h_layout3 = QHBoxLayout()
            inner_list.addLayout(h_layout3)

            createArm = QPushButton('Create')
            h_layout3.addWidget(createArm)

            def disable_fingers():
                count_box.setEnabled(fingers_box.isChecked())
                label_count.setEnabled(fingers_box.isChecked())
                segments_box.setEnabled(fingers_box.isChecked())
                label_segments.setEnabled(fingers_box.isChecked())

            fingers_box.stateChanged.connect(disable_fingers)
            fingers_box.toggle()

            def quadroped_joints():
                if quadroped_box.isChecked():
                    joints_box.setValue(4)
                else:
                    joints_box.setValue(3)

            quadroped_box.stateChanged.connect(quadroped_joints)

            # TODO: handle quadroped leg
            def build_leg():
                name = self.rig_name.text()
                if name != '':
                    name = (name + '_')

                numJoints = joints_box.value()
                fingers = fingers_box.isChecked()
                numFingers = count_box.value()
                numSegment = segments_box.value()

                leftColorIndex = self.left_cb.index()
                rightColorIndex = self.right_cb.index()

                if quadroped_box.isChecked():
                    # TODO: handle custom side prefix
                    if side_combo.currentIndex() == 2:
                        # left
                        drLib.buildQuadLegDummySkeletonModule(name,
                                                              self.prefix_left(),
                                                              numJoints,
                                                              fingers,
                                                              numFingers,
                                                              numSegment,
                                                              leftColorIndex)
                        # right
                        drLib.buildQuadLegDummySkeletonModule(name,
                                                              self.prefixRight(),
                                                              numJoints,
                                                              fingers,
                                                              numFingers,
                                                              numSegment,
                                                              rightColorIndex)

                        # commented out to resolve issue with incorrectly mirroring of left side
                        # msLib.mirrorModuleTemplates(name + self.prefix_left() + 'legPlacer_loc')

                        master = (name + self.prefix_left() + 'legPlacer_loc')
                        slave = (name + self.prefixRight() + 'legPlacer_loc')
                        msLib.buildLegModuleSymmetry(master, slave)

                    else:
                        if side_combo.currentIndex() == 0:
                            side = self.prefix_left()
                            colorIndex = leftColorIndex
                        else:
                            side = self.prefixRight()
                            colorIndex = rightColorIndex
                        drLib.buildQuadLegDummySkeletonModule(name,
                                                              side,
                                                              numJoints,
                                                              fingers,
                                                              numFingers,
                                                              numSegment,
                                                              colorIndex)
                        if side_combo.currentIndex() == 1:
                            msLib.mirrorModuleTemplates(name + side + 'legPlacer_loc')
                else:
                    # TODO: handle custom side prefix
                    if side_combo.currentIndex() == 2:
                        # left
                        drLib.buildBipedLegDummySkeletonModule(name,
                                                               self.prefix_left(),
                                                               numJoints,
                                                               fingers,
                                                               numFingers,
                                                               numSegment,
                                                               leftColorIndex)
                        # right
                        drLib.buildBipedLegDummySkeletonModule(name,
                                                               self.prefixRight(),
                                                               numJoints,
                                                               fingers,
                                                               numFingers,
                                                               numSegment,
                                                               rightColorIndex)

                        master = (name + self.prefix_left() + 'legPlacer_loc')
                        slave = (name + self.prefixRight() + 'legPlacer_loc')
                        msLib.buildLegModuleSymmetry(master, slave)

                    else:
                        if side_combo.currentIndex() == 0:
                            side = self.prefix_left()
                            colorIndex = leftColorIndex
                        else:
                            side = self.prefixRight()
                            colorIndex = rightColorIndex
                        drLib.buildBipedLegDummySkeletonModule(name,
                                                               side,
                                                               numJoints,
                                                               fingers,
                                                               numFingers,
                                                               numSegment,
                                                               colorIndex)
                        if side_combo.currentIndex() == 1:
                            msLib.mirrorModuleTemplates(name + side + 'legPlacer_loc')

            createArm.clicked.connect(build_leg)

        def spine():

            group = QGroupBox('Spine')
            v_list.addWidget(group)
            inner_list = QVBoxLayout()
            group.setLayout(inner_list)

            # h layout1
            h_layout1 = QHBoxLayout()
            inner_list.addLayout(h_layout1, stretch=0)

            spine_box = QLineEdit()
            spine_box.setText("spine")
            h_layout1.addWidget(spine_box)

            label_spine = QLabel('Title')
            h_layout1.addWidget(label_spine)

            dynamic = QCheckBox('Dynamic')
            h_layout1.addWidget(dynamic)
            offset = QCheckBox('Offset')
            h_layout1.addWidget(offset)
            sym_box = QCheckBox('Symmetry')
            h_layout1.addWidget(sym_box)

            # h layout2
            h_layout2 = QHBoxLayout()
            inner_list.addLayout(h_layout2, stretch=0)

            controls_box = QSpinBox()
            controls_box.setMaximumWidth(35)
            controls_box.setValue(4)
            h_layout2.addWidget(controls_box)

            label_controls = QLabel('Controls')
            h_layout2.addWidget(label_controls)

            length_box = QSpinBox()
            length_box.setMaximumWidth(35)
            length_box.setValue(4)
            h_layout2.addWidget(length_box)

            label_length = QLabel('Length')
            h_layout2.addWidget(label_length)

            # Dynamic & Offset Ctr
            axis_combo = QComboBox()
            axis_combo.addItems(axis_list)
            axis_combo.setCurrentIndex(1)
            h_layout2.addWidget(axis_combo)
            label_axis = QLabel('Axis')
            h_layout2.addWidget(label_axis)
            spacer = QSpacerItem(35, 10)
            h_layout2.addSpacerItem(spacer)

            # h layout3
            h_layout3 = QHBoxLayout()
            inner_list.addLayout(h_layout3)

            createSpine = QPushButton('Create')
            h_layout3.addWidget(createSpine)

            def build_spine():
                name = self.rig_name.text()
                if name != '':
                    name = (name + '_')

                moduleName = spine_box.text()
                numCon = controls_box.value()
                axis = str(axis_combo.currentText()).lower()
                # length
                dis = length_box.value()
                # control colors
                cenColorIndex = self.center_cb.index()
                leftColorIndex = self.left_cb.index()
                rightColorIndex = self.right_cb.index()

                # TODO: handle custom side prefix
                if sym_box.isChecked():
                    # left
                    drLib.buildSpineDummySkeletonModule(name,
                                                        self.prefix_left(),
                                                        moduleName,
                                                        numCon,
                                                        axis,
                                                        dis,
                                                        leftColorIndex)
                    # right
                    drLib.buildSpineDummySkeletonModule(name,
                                                        self.prefixRight(),
                                                        moduleName,
                                                        numCon,
                                                        axis,
                                                        dis,
                                                        rightColorIndex)
                else:
                    drLib.buildSpineDummySkeletonModule(name,
                                                        '',
                                                        moduleName,
                                                        numCon,
                                                        axis,
                                                        dis,
                                                        cenColorIndex)

                # TODO: handle symmetry

            createSpine.clicked.connect(build_spine)

        def head():

            group = QGroupBox('Neck Head')
            v_list.addWidget(group)
            inner_list = QVBoxLayout()
            group.setLayout(inner_list)

            # h layout1
            h_layout1 = QHBoxLayout()
            inner_list.addLayout(h_layout1, stretch=0)

            neck_box = QLineEdit()
            neck_box.setText("neck")
            h_layout1.addWidget(neck_box)

            label_neck = QLabel('Title')
            h_layout1.addWidget(label_neck)

            # Dynamic & Offset Ctr
            dynamic = QCheckBox('Dynamic')
            h_layout1.addWidget(dynamic)
            offset = QCheckBox('Offset')
            h_layout1.addWidget(offset)
            sym_box = QCheckBox('Symmetry')
            h_layout1.addWidget(sym_box)

            # h layout2
            h_layout2 = QHBoxLayout()
            inner_list.addLayout(h_layout2, stretch=0)

            controls_box = QSpinBox()
            controls_box.setMaximumWidth(35)
            controls_box.setValue(1)
            h_layout2.addWidget(controls_box)

            label_controls = QLabel('Controls')
            h_layout2.addWidget(label_controls)

            length_box = QSpinBox()
            length_box.setMaximumWidth(35)
            length_box.setValue(1)
            h_layout2.addWidget(length_box)

            label_length = QLabel('Length')
            h_layout2.addWidget(label_length)

            axis_combo = QComboBox()
            axis_combo.addItems(axis_list)
            axis_combo.setCurrentIndex(1)
            h_layout2.addWidget(axis_combo)

            label_axis = QLabel('Axis')
            h_layout2.addWidget(label_axis)

            spacer = QSpacerItem(35, 10)
            h_layout2.addSpacerItem(spacer)

            # h layout3
            h_layout3 = QHBoxLayout()
            inner_list.addLayout(h_layout3)

            createHead = QPushButton('Create')
            h_layout3.addWidget(createHead)

            def build_head():
                name = self.rig_name.text()
                if name != '':
                    name = (name + '_')

                moduleName = neck_box.text()
                numCon = controls_box.value()
                axis = str(axis_combo.currentText()).lower()
                # length
                dis = length_box.value()
                # control colors
                cenColorIndex = self.center_cb.index()
                leftColorIndex = self.left_cb.index()
                rightColorIndex = self.right_cb.index()

                # TODO: handle custom side prefix
                if sym_box.isChecked():
                    # left
                    drLib.buildHeadNeckDummySkeletonModule(name,
                                                           self.prefix_left(),
                                                           moduleName,
                                                           numCon,
                                                           axis,
                                                           dis,
                                                           leftColorIndex)
                    # right
                    drLib.buildHeadNeckDummySkeletonModule(name,
                                                           self.prefixRight(),
                                                           moduleName,
                                                           numCon,
                                                           axis,
                                                           dis,
                                                           rightColorIndex)
                else:
                    drLib.buildHeadNeckDummySkeletonModule(name,
                                                           '',
                                                           moduleName,
                                                           numCon,
                                                           axis,
                                                           dis,
                                                           cenColorIndex)

            createHead.clicked.connect(build_head)

        def tentacle():

            group = QGroupBox('Tentacle')
            v_list.addWidget(group)
            inner_list = QVBoxLayout()
            group.setLayout(inner_list)

            # h layout1
            h_layout1 = QHBoxLayout()
            inner_list.addLayout(h_layout1, stretch=0)

            tentacle_box = QLineEdit()
            tentacle_box.setText("tail")
            h_layout1.addWidget(tentacle_box)
            label_tentacle = QLabel('Title')
            h_layout1.addWidget(label_tentacle)

            # Dynamic & Offset Ctr
            dynamic = QCheckBox('Dynamic')
            h_layout1.addWidget(dynamic)
            offset = QCheckBox('Offset')
            h_layout1.addWidget(offset)
            sym_box = QCheckBox('Symmetry')
            h_layout1.addWidget(sym_box)

            # h layout2
            h_layout2 = QHBoxLayout()
            inner_list.addLayout(h_layout2, stretch=0)

            controls_box = QSpinBox()
            controls_box.setMaximumWidth(35)
            controls_box.setValue(7)
            h_layout2.addWidget(controls_box)
            label_controls = QLabel('Controls')
            h_layout2.addWidget(label_controls)

            length_box = QSpinBox()
            length_box.setMaximumWidth(35)
            length_box.setValue(7)
            h_layout2.addWidget(length_box)
            label_length = QLabel('Length')
            h_layout2.addWidget(label_length)

            axis_combo = QComboBox()
            axis_combo.addItems(axis_list)
            h_layout2.addWidget(axis_combo)
            label_axis = QLabel('Axis')
            h_layout2.addWidget(label_axis)

            spacer = QSpacerItem(30, 10)
            h_layout2.addSpacerItem(spacer)

            # h layout3
            h_layout3 = QHBoxLayout()
            inner_list.addLayout(h_layout3)

            createTentacle = QPushButton('Create')
            h_layout3.addWidget(createTentacle)

            def build_tentacle():
                name = self.rig_name.text()
                if name != '':
                    name = (name + '_')

                moduleName = tentacle_box.text()
                numCon = controls_box.value()
                axis = str(axis_combo.currentText()).lower()
                # length
                dis = length_box.value()
                # control colors
                cenColorIndex = self.center_cb.index()
                leftColorIndex = self.left_cb.index()
                rightColorIndex = self.right_cb.index()

                # TODO: handle custom side prefix
                if sym_box.isChecked():
                    # left
                    drLib.buildHeadNeckDummySkeletonModule(name,
                                                           self.prefix_left(),
                                                           moduleName,
                                                           numCon,
                                                           axis,
                                                           dis,
                                                           leftColorIndex)
                    # right
                    drLib.buildHeadNeckDummySkeletonModule(name,
                                                           self.prefixRight(),
                                                           moduleName,
                                                           numCon,
                                                           axis,
                                                           dis,
                                                           rightColorIndex)
                else:
                    drLib.buildHeadNeckDummySkeletonModule(name,
                                                        '',
                                                           moduleName,
                                                           numCon,
                                                           axis,
                                                           dis,
                                                           cenColorIndex)

            createTentacle.clicked.connect(build_tentacle)

        def finger():

            group = QGroupBox('Finger')
            v_list.addWidget(group)
            inner_list = QVBoxLayout()
            group.setLayout(inner_list)

            # h layout1
            h_layout1 = QHBoxLayout()
            inner_list.addLayout(h_layout1, stretch=0)

            finger_box = QLineEdit()
            finger_box.setText("index")
            h_layout1.addWidget(finger_box)
            label_finger = QLabel('Title')
            h_layout1.addWidget(label_finger)

            # Dynamic & Offset Ctr
            dynamic = QCheckBox('Dynamic')
            h_layout1.addWidget(dynamic)
            offset = QCheckBox('Offset')
            h_layout1.addWidget(offset)

            # Side
            side_combo = QComboBox()
            side_combo.addItems(side_list)
            side_combo.setMaximumWidth(50)
            h_layout1.addWidget(side_combo)
            label_side = QLabel('Side')
            h_layout1.addWidget(label_side)

            # h layout2
            h_layout2 = QHBoxLayout()
            inner_list.addLayout(h_layout2, stretch=0)

            controls_box = QSpinBox()
            controls_box.setMaximumWidth(35)
            controls_box.setValue(4)
            h_layout2.addWidget(controls_box)
            label_controls = QLabel('Controls')
            h_layout2.addWidget(label_controls)

            length_box = QSpinBox()
            length_box.setMaximumWidth(35)
            length_box.setValue(4)
            h_layout2.addWidget(length_box)
            label_joints = QLabel('Length')
            h_layout2.addWidget(label_joints)

            axis_combo = QComboBox()
            axis_combo.addItems(axis_list)
            h_layout2.addWidget(axis_combo)
            label_axis = QLabel('Axis')
            h_layout2.addWidget(label_axis)

            spacer = QSpacerItem(30, 10)
            h_layout2.addSpacerItem(spacer)

            # h layout3
            h_layout3 = QHBoxLayout()
            inner_list.addLayout(h_layout3)

            createArm = QPushButton('Create')
            h_layout3.addWidget(createArm)

            def build_finger():
                name = self.rig_name.text()
                if name != '':
                    name = (name + '_')

                moduleName = finger_box.text()
                numCon = controls_box.value()
                axis = str(axis_combo.currentText()).lower()
                # length
                dis = length_box.value()
                # control colors
                cenColorIndex = self.center_cb.index()
                leftColorIndex = self.left_cb.index()
                rightColorIndex = self.right_cb.index()

                # TODO: handle custom side prefix
                if side_combo.currentIndex() == 2:
                    # left
                    drLib.fingerSegmentDummyBoneCreator(name,
                                                        self.prefix_left(),
                                                        moduleName,
                                                        numCon,
                                                        axis,
                                                        dis,
                                                        leftColorIndex)
                    # right
                    drLib.fingerSegmentDummyBoneCreator(name,
                                                        self.prefixRight(),
                                                        moduleName,
                                                        numCon,
                                                        axis,
                                                        dis,
                                                        rightColorIndex)
                else:
                    if side_combo.currentIndex() == 0:
                        side = self.prefix_left()
                    else:
                        side = self.prefixRight()
                    drLib.fingerSegmentDummyBoneCreator(name,
                                                        side,
                                                        moduleName,
                                                        numCon,
                                                        axis,
                                                        dis,
                                                        cenColorIndex)

            createArm.clicked.connect(build_finger)

        arm()
        leg()
        spine()
        head()
        tentacle()
        finger()

        collapsible_button = CollapsibleButton(self.inner_layout, v_list, 'Modules', 350, font)

        return collapsible_button.widget

    def modifyButtons(self):

        # v layout
        v_list = QVBoxLayout()

        # h layout1
        h_layout1 = QHBoxLayout()
        # v_list is module vertical list
        v_list.addLayout(h_layout1, stretch=0)

        # TODO: find out how to pass connectModuleComponants without parameters
        def connectModules():
            msLib.connectModuleComponentsUI('', '')

        connect_modules = QPushButton('Connect Modules')
        connect_modules.clicked.connect(connectModules)
        h_layout1.addWidget(connect_modules)

        # TODO: find out how to pass addToModuleComponantsHierarchy without parameters
        def addToHierarchy():
            msLib.addToModuleComponentsHierarchy()

        add_to_hierarchy = QPushButton('Add To Hierarchy')
        add_to_hierarchy.clicked.connect(addToHierarchy)
        h_layout1.addWidget(add_to_hierarchy)

        delete = QPushButton('Delete Module')
        delete.clicked.connect(msLib.deleteModules)
        h_layout1.addWidget(delete)

        h_layout2 = QHBoxLayout()
        v_list.addLayout(h_layout2, stretch=0)

        sym = QPushButton('Symmetry')
        sym.clicked.connect(msLib.connectModuleSymmetry)
        h_layout2.addWidget(sym)

        def breakModuleSymConnection():
            msLib.breakModuleSymConnection()

        break_sym = QPushButton('Break Symmetry')
        break_sym.clicked.connect(breakModuleSymConnection)
        h_layout2.addWidget(break_sym)

        def mirrorModuleTemplates():
            msLib.mirrorModuleTemplates()

        mir_sel = QPushButton('Mirror Selected')
        mir_sel.clicked.connect(mirrorModuleTemplates)
        h_layout2.addWidget(mir_sel)
        self.main_layout.addLayout(v_list)

    def generateButtons(self):
        font = QFont()
        font.setPixelSize(12)
        font.setBold(True)

        h_layout = QHBoxLayout()
        skeleton_button = QPushButton('GENERATE SKELETON')
        skeleton_button.clicked.connect(bmjs.buildModuleSkeleton)

        rig_button = QPushButton('GENERATE RIG')
        rig_button.clicked.connect(self.build_rig)

        skeleton_button.setMinimumHeight(35)
        rig_button.setMinimumHeight(35)

        skeleton_button.setFont(font)
        rig_button.setFont(font)

        h_layout.addWidget(skeleton_button)
        h_layout.addWidget(rig_button)
        self.main_layout.addLayout(h_layout)

    # Non Button Methods
    # =====================================================================
    def build_rig(self):
        # TODO: delete these when finished setting up colors
        # self.right_cb = ColorSpinBox(h_layout, 'Right', 10)
        # self.center_cb = ColorSpinBox(h_layout, 'Center', 15)
        # self.left_cb = ColorSpinBox(h_layout, 'Left', 26)

        cmr.createRig(
            # TODO: properly populate this
            ikfk='constrain',
            stretch=str(self.stretch_combobox.currentText()),
            midLock=self.midlock_checkbox.isChecked(),
            volume=self.volume_checkbox.isChecked(),
            colorRight=self.right_cb.index(),
            colorCenter=self.center_cb.index(),
            colorLeft=self.left_cb.index())

    def prefix_left(self):
        sides = rigSideSep(self.side_prefix.currentText())
        return sides[0]

    def prefixRight(self):
        sides = rigSideSep(self.side_prefix.currentText())
        return sides[1]