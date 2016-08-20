import Utils
import Joints
import Rigging
import Controls
import Core
import UI
import Maya_UtilLib
import pymel.core as pm
from functools import partial


def MenuItem():
    pm.menuItem(parent='CustomTools', subMenu=True, tearOff=True, label='Rigging')
    pm.menuItem(label='Auto Rig', command=partial(UI.AutoRig.Open))


def AddMenuItem():
    Maya_UtilLib.Menu.AddModuleMenu(module='Maya_Rigging', menuFunc=MenuItem)
    Maya_UtilLib.Menu.Draw()

AddMenuItem()
