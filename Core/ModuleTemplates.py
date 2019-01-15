import pymel.core as pc
from ..Core import Dummy as Dummy
from ..Core import ModuleSymmetryLib as ms


def bipedModuleTemplate(name, spine_count, neck_count, finger, num_finger, toe, num_toes):
    # spine
    Dummy.Spine.build(name, '', 'spine', spine_count, 'y', spine_count, 7)
    pc.move(0, 0.07, 0, (name + 'spineHips_loc'))
    pc.move(0, 17.0, 0, (name + "spineMain_ctrl"))
    # neck and head module
    Dummy.HeadAndNeck.build(name, '', 'neck', neck_count, 'y', neck_count, 7)
    pc.move(0, (23.0 + spine_count), 0, (name + "neckMain_ctrl"))
    # arm modules
    Dummy.Arm.build(name, 'lt_', 3, finger, num_finger, 4, 10)
    Dummy.Arm.build(name, 'rt_', 3, finger, num_finger, 4, 15)
    ms.buildArmModuleSymmetry((name + 'lt_armPlacer_loc'), (name + 'rt_armPlacer_loc'))
    pc.move(3.0, (21.0 + spine_count), 0, (name + 'lt_armPlacer_loc'))
    pc.move(1.0, (21.0 + spine_count), 0, (name + 'lt_clav_loc'))
    pc.rotate((name + 'lt_armPlacer_loc'), (0, 0, -45.0))
    pc.scale((name + 'lt_armPlacer_loc'), (0.8, 0.8, 0.8))
    # leg modules
    Dummy.Leg.Biped.build(name, 'lt_', 3, toe, num_toes, 4, 10)
    Dummy.Leg.Biped.build(name, 'rt_', 3, toe, num_toes, 4, 15)
    ms.buildLegModuleSymmetry((name + 'lt_legPlacer_loc'), (name + 'rt_legPlacer_loc'))
    # connecting modules
    ms.connectModuleComponents((name + 'spine' + str(spine_count) + '_loc'), (name + 'neckMain_ctrl'))
    ms.connectModuleComponents((name + 'spine' + str(spine_count) + '_loc'), (name + 'lt_armPlacer_loc'))
    ms.connectModuleComponents((name + 'spine' + str(spine_count) + '_loc'), (name + 'rt_armPlacer_loc'))
    ms.connectModuleComponents((name + 'spineHips_loc'), (name + 'lt_legPlacer_loc'))
    ms.connectModuleComponents((name + 'spineHips_loc'), (name + 'rt_legPlacer_loc'))
    pc.select(cl=True)


def quadModuleTemplate(name, spineCount, neckCount, earCount, tailCount, toe, numToe):
    # spine
    Dummy.Spine.build(name, '', 'spine', spineCount, 'y', spineCount + 3, 7)
    pc.move(0, 0.07, 0, (name + 'spineHips_loc'))
    pc.move(0, 14.0, -3.0, (name + 'spineMain_ctrl'))
    pc.rotate((name + 'spineMain_ctrl'), (90, 0, 0))
    # neck and head module
    Dummy.HeadAndNeck.build(name, '', 'neck', neckCount, 'y', (neckCount + 1), 7)
    pc.move(0, 16.0, (7.0 + spineCount), (name + 'neckMain_ctrl'))
    pc.rotate((name + "neckMain_ctrl"), (45, 0, 0))
    pc.rotate((name + "headMain_ctrl"), (-45, 0, 0))
    pc.select(cl=True)
    # ears
    Dummy.Tentacle.build(name, 'lt_', 'ear', earCount, 'y', earCount, 10)
    Dummy.Tentacle.build(name, 'rt_', 'ear', earCount, 'y', earCount, 15)
    ms.buildBodyModuleSymmetry((name + 'lt_earMain_ctrl'), (name + 'rt_earMain_ctrl'))
    pc.move(2.0, (22.0 + neckCount), (9.0 + spineCount + neckCount), (name + 'lt_earMain_ctrl'))
    pc.rotate((name + 'lt_earMain_ctrl'), (0, 0, -22.5))
    # legs
    Dummy.Leg.Quadruped.build(name, 'ltFrt_', 4, toe, numToe, 4, 10)
    Dummy.Leg.Quadruped.build(name, 'rtFrt_', 4, toe, numToe, 4, 15)
    ms.buildLegModuleSymmetry((name + 'ltFrt_legPlacer_loc'), (name + 'rtFrt_legPlacer_loc'))
    pc.move((name + 'ltFrt_legPlacer_loc'), (2.0, 15.0, (4.0 + spineCount)))
    pc.setAttr((name + 'ltFrt_hip2_loc.ty'), -4.0)
    pc.setAttr((name + "ltFrt_knee1_loc.ty"), -8.0)

    Dummy.Leg.Quadruped.build(name, 'ltBck_', 4, toe, numToe, 4, 10)
    Dummy.Leg.Quadruped.build(name, 'rtBck_', 4, toe, numToe, 4, 15)
    ms.buildLegModuleSymmetry((name + 'ltBck_legPlacer_loc'), (name + 'rtBck_legPlacer_loc'))
    pc.move((name + "ltBck_legPlacer_loc"), (2.0, 15.0, -5.0))
    # tail
    pc.select(cl=True)
    Dummy.Tentacle.build(name, '', 'tail', tailCount, 'z', ((tailCount + 3) * -1), 7);
    pc.move((name + "tailMain_ctrl"), (0.0, 14.0, -7.0))
    pc.rotate((name + 'tailMain_ctrl'), (-45, 0, 0))
    # connecting modules
    ms.connectModuleComponents((name + 'head1_loc'), (name + 'lt_earMain_ctrl'))
    ms.connectModuleComponents((name + 'head1_loc'), (name + 'rt_earMain_ctrl'))
    ms.connectModuleComponents((name + 'spine' + str(spineCount) + '_loc'), (name + 'neckMain_ctrl'))
    ms.connectModuleComponents((name + 'spine' + str(spineCount) + '_loc'), (name + 'ltFrt_legPlacer_loc'))
    ms.connectModuleComponents((name + 'spine' + str(spineCount) + '_loc'), (name + 'rtFrt_legPlacer_loc'))
    ms.connectModuleComponents((name + 'spineHips_loc'), (name + 'ltBck_legPlacer_loc'))
    ms.connectModuleComponents((name + 'spineHips_loc'), (name + 'rtBck_legPlacer_loc'))
    ms.connectModuleComponents((name + 'spineHips_loc'), (name + 'tailMain_ctrl'))
    pc.select(cl=True)
