import Maya_Rigging.Utils
import Maya_Rigging.Joints
import Maya_Rigging.Rigging
import Maya_Rigging.Controls
import Maya_Rigging.Core
import Maya_Rigging.UI
import Maya_UtilLib
import pymel.core as pm
from functools import partial


def MenuItem():
    pm.menuItem(parent=Maya_UtilLib.ui_name, subMenu=True, tearOff=True, label='Rigging')
    pm.menuItem(label='Auto Rig', command=partial(Maya_Rigging.UI.AutoRig.Open))


def AddMenuItem():
    Maya_UtilLib.Menu.add_module_menu(module='Maya_Rigging', menu_func=MenuItem)
    Maya_UtilLib.Menu.draw()


AddMenuItem()
