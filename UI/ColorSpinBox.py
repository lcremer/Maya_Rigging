"""
Created a label, Frame, and SpinBox
Used to represent Maya override colors
"""

from PySide import QtGui

# TODO: consider moving someplace better?
colors = [
    '787878',
    '000000',
    '404040',
    '999999',
    '9B0028',
    '000460',
    '0000FF',
    '004619',
    '260043',
    'C800C8',
    '8A4833',
    '3F231F',
    '992600',
    'FF0000',
    '00FF00',
    '004199',
    'FFFFFF',
    'FFFF00',
    '64DCFF',
    '43FFA3',
    'FFB0B0',
    'E4AC79',
    'FFFF63',
    '009954',
    'A16930',
    '9FA130',
    '68A130',
    '30A15D',
    '30A1A1',
    '3067A1',
    '6F30A1'
]


class ColorSpinBox:
    def __init__(self,
                 parent_layout,
                 label_name,
                 default_value=0):
        # Label
        self.parent_layout = parent_layout
        self.label_name = label_name
        self.default_value = default_value
        self.label = QtGui.QLabel(label_name)
        self.parent_layout.addWidget(self.label)
        # Color Frame
        frame = QtGui.QFrame()
        self.frame = frame
        self.frame.setStyleSheet('background-color: #' + colors[default_value])
        self.parent_layout.addWidget(self.frame)
        # SpinBox
        SpinBox = QtGui.QSpinBox()
        self.SpinBox = SpinBox
        self.SpinBox.setValue(default_value)
        self.SpinBox.setMinimum(0)
        self.SpinBox.setMaximum(30)
        self.SpinBox.setFixedWidth(40)
        self.parent_layout.addWidget(self.SpinBox)

        def update_color():
            value = SpinBox.value()
            frame.setStyleSheet('background-color: #' + colors[value])

        self.SpinBox.valueChanged.connect(update_color)

    def index(self):
        return self.SpinBox.value()
