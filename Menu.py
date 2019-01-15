from functools import partial

import Maya_Rigging.UI
import Maya_UtilLib
from Maya_UtilLib.Labels import ui_name
from pymel import core as pm


def menu_item():
    pm.menuItem(parent=ui_name, subMenu=True, tearOff=True, label='Rigging')
    pm.menuItem(label='Auto Rig', command=partial(Maya_Rigging.UI.AutoRig.open))


def add_menu_item():
    Maya_UtilLib.Menu.add_module_menu(module='Maya_Rigging', menu_func=menu_item)
    Maya_UtilLib.Menu.draw()
