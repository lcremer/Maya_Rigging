"""
Creates a button when clicked that expands to reveal nested content
"""


from PySide import QtGui


class CollapsibleButton:
    def __init__(self,
                 parent_layout,
                 widget_layout,
                 button_text,
                 button_width,
                 button_font):

        self.parent_layout = parent_layout
        self.child_layout = QtGui.QVBoxLayout()
        self.widget_layout = widget_layout

        self.button = QtGui.QPushButton(button_text)
        self.button_width = button_width
        self.button_font = button_font

        self.child_layout.insertWidget(0, self.button)
        self.child_layout.addStretch(1)
        self.parent_layout.addLayout(self.child_layout)
        self.vertical_list = QtGui.QVBoxLayout()

        widget = QtGui.QWidget()
        self.widget = widget
        self.widget.setFixedWidth(button_width)
        self.widget.setLayout(self.widget_layout)

        self.child_layout.addWidget(self.widget)
        self.button.setFont(self.button_font)

        def set_enabled():
            widget.setVisible(not widget.isVisible())
            if widget.isVisible():
                widget.show()
            else:
                widget.hide()

        self.button.clicked.connect(set_enabled)




