# -*- coding: utf8 -*-
from apps.settings import spatial_settings

__author__ = 'gmdidro'

from spatialPooler.sp_region import Region
from spatialPooler.mappers.sp_very_simple_mapper import VerySimpleMapper
from spatialPooler.mappers.sp_simple_mapper import SimpleMapper
from enum import Enum


# //TODO: переписать, сейчас не верно беруться размеры
# public void testDiff() throws IOException
# {
#     FileInputStream fis_truth=new FileInputStream("in.txt")
#     Scanner sc_truth=new Scanner(fis_truth)
#     FileInputStream fis_predict=new FileInputStream("out_predict.txt")
#     Scanner sc_p=new Scanner(fis_predict)
#     FileOutputStream fos_err=new FileOutputStream("errs.txt")
#     PrintWriter pw_err=new PrintWriter(fos_err)
#
#
#
#     int w=sc_truth.nextInt()
#     int h=sc_truth.nextInt()
#     int step=sc_truth.nextInt()
#
#     sc_truth.nextLine()
#     sc_p.nextLine()
#
#     for(int s=0s<steps++) {
#         int[] errs=new int[h]
#         for (int i = 0 i < h i++) {
#             BitVector true_bv=MathUtils.bitvectorFromString(sc_truth.nextLine())
#             //System.out.println(sc_truth.nextLine())
#             BitVector predict_bv=MathUtils.bitvectorFromString(sc_p.nextLine())
#             //System.out.println(sc_p.nextLine())
#
#             predict_bv.xor(true_bv)
#             errs[i]=(int)MathUtils.sumOfLongs(predict_bv.elements())
#         }
#         pw_err.println(MathUtils.sumOfInts(errs))
#     }
#     pw_err.close()
# }


def find_by_colxy(cols, x, y):
    for c in cols:
        v = c.get_coord()
        if (v[0] == x and v[1] == y): return c

    return None


class Dir(Enum):
    UP = 1
    DOWN = 2


def test_ladder():
    # FileOutputStream fos=new FileOutputStream("out.txt")
    #  PrintWriter pw=new PrintWriter(fos)

    # FileOutputStream fos_in=new FileOutputStream("in.txt")
    # PrintWriter pw_in=new PrintWriter(fos_in)

    w = 15
    h = 15
    begx = 0
    begy = 0
    step_size = 5

    map = [[0 for j in range(h)] for i in range(w)]
    inp = [0 for i in range(h * w)]
    STEPS = 5
    TOTAL_STEPS = 1000
    STEP_SIZE = STEPS

    setting = spatial_settings
    setting.debug = True

    setting.min_overlap = 1
    setting.desired_local_activity = 1
    setting.connected_pct = 1
    # setting.connectedPerm=0.01
    setting.xinput = w
    setting.yinput = h
    setting.potential_radius = 2
    setting.xdimension = 3
    setting.ydimension = 3
    setting.initial_inhibition_radius = 2

    # pw.print(setting.xDimension + " ")
    # pw.print(setting.yDimension + " ")
    # pw.print(TOTAL_STEPS)
    # pw.println()
    #
    # pw_in.print(setting.xDimension + " ")
    # pw_in.print(setting.yDimension + " ")
    # pw_in.print(TOTAL_STEPS)
    # pw_in.println()

    r = Region(setting, VerySimpleMapper())

    x = begx
    y = begy
    for i in range(x, x + step_size):
        for j in range(y, y + step_size):
            map[i][j] = 1

    for step in range(TOTAL_STEPS):
        print("DATA:\n")
        index = 0
        for k in range(w):
            for m in range(h):
                inp[index] = map[k][m]
                # pw_in.print(in[index])
                print(str(inp[index]) + " ", end="", flush=True)
                index += 1
            print()
            # pw_in.println()
        print()
        # pw_in.println()

        for i in range(x, x + step_size):
            for j in range(y, y + step_size):
                if i < len(map) and j < len(map[0]):
                    map[i][j] = 0

        x = x + STEP_SIZE
        y = y + STEP_SIZE
        if x > w:
            x = 0
            y = 0

        for i in range(x, x + step_size):
            for j in range(y, y + step_size):
                if i < len(map) and j < len(map[0]):
                    map[i][j] = 1

        for c in r.get_columns():
            c.set_is_active(False)

        ov = r.update_overlaps(r.get_columns(), inp)
        r.inhibition_phase(r.get_columns(), ov)
        r.learning_phase(r.get_columns(), inp, ov)
        cols = r.get_columns()

        for i in range(setting.xdimension):
            for j in range(setting.ydimension):
                state = 1 if find_by_colxy(cols, i, j).get_is_active() else 0
                print(str(state) + " ", end="", flush=True)
                # pw.print(state)
                # pw.print(" ")
            print()


def test_learning():
    inp = [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    settings = spatial_settings
    settings.debug = True

    settings.min_overlap = 1
    settings.desired_local_activity = 1
    settings.connected_pct = 1
    settings.xinput = len(inp)
    settings.yinput = 1
    settings.potential_radius = 2
    settings.xdimension = 4
    settings.ydimension = 1
    settings.initial_inhibition_radius = 1
    settings.permanence_inc = 0.2
    settings.permanence_dec = 0.2

    r = Region(settings, SimpleMapper())

    r.get_columns()[0].get_potential_synapses().get(4).set_permanence(0.5)
    r.get_columns()[0].get_potential_synapses().get(5).set_permanence(0.5)
    ov = r.update_overlaps(r.get_columns(), inp)
    r.inhibition_phase(r.get_columns(), ov)
    r.learning_phase(r.get_columns(), inp, ov)

    v = r.get_columns()[0].get_potential_synapses().get(4).get_permanence()
    assert v == 0.7
    v = r.get_columns()[0].get_potential_synapses().get(5).get_permanence()
    assert v == 0.3


def test_update_active_duty_cycle():
    inp = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    settings = spatial_settings
    settings.debug = True

    settings.min_overlap = 1
    settings.desired_local_activity = 1
    settings.connected_pct = 1
    settings.xinput = len(inp)
    settings.yinput = 1
    settings.potential_radius = 2
    settings.xdimension = 4
    settings.ydimension = 1
    settings.initial_inhibition_radius = 1

    r = Region(settings, SimpleMapper())

    overlaps = r.update_overlaps(r.get_columns(), inp)
    r.inhibition_phase(r.get_columns(), overlaps)
    r.update_active_duty_cycle(r.get_columns())
    r.inhibition_phase(r.get_columns(), overlaps)
    r.update_active_duty_cycle(r.get_columns())
    r.inhibition_phase(r.get_columns(), overlaps)
    r.update_active_duty_cycle(r.get_columns())
    r.inhibition_phase(r.get_columns(), overlaps)
    r.update_active_duty_cycle(r.get_columns())

    assert len(r.get_active_duty_cycles()) == len(r.get_columns())
    assert r.get_active_duty_cycles()[0] == 4

    inp = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

    r = Region(settings, SimpleMapper())
    overlaps = r.update_overlaps(r.get_columns(), inp)
    r.inhibition_phase(r.get_columns(), overlaps)
    r.update_active_duty_cycle(r.get_columns())
    r.inhibition_phase(r.get_columns(), overlaps)
    r.update_active_duty_cycle(r.get_columns())
    r.inhibition_phase(r.get_columns(), overlaps)
    r.update_active_duty_cycle(r.get_columns())
    r.inhibition_phase(r.get_columns(), overlaps)
    r.update_active_duty_cycle(r.get_columns())

    assert len(r.get_active_duty_cycles()) == len(r.get_columns())
    assert r.get_active_duty_cycles()[0] == 0
    assert r.get_active_duty_cycles()[1] == 3
    assert r.get_active_duty_cycles()[2] == 3
    assert r.get_active_duty_cycles()[3] == 2


def testUpdateSynapses():
    inp = [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    settings = spatial_settings
    settings.debug = True

    settings.min_overlap = 1
    settings.desired_local_activity = 1
    settings.connected_pct = 1
    settings.xinput = len(inp)
    settings.yinput = 1
    settings.potential_radius = 2
    settings.xdimension = 4
    settings.ydimension = 1
    settings.initial_inhibition_radius = 1
    settings.permanence_inc = 0.2
    settings.permanence_dec = 0.2
    r = Region(settings, SimpleMapper())

    r.get_columns()[0].get_potential_synapses().get(4).set_permanence(0.5)
    r.update_synapses(r.get_columns(), inp)
    v = r.get_columns()[0].get_potential_synapses().get(4).get_permanence()
    assert v == 0.7

    r.get_columns()[0].get_potential_synapses().get(5).set_permanence(0.5)
    r.update_synapses(r.get_columns(), inp)
    v = r.get_columns()[0].get_potential_synapses().get(5).get_permanence()
    assert v == 0.3


def test_inhibition_phase():
    inp = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

    settings = spatial_settings
    settings.debug = True

    settings.min_overlap = 1
    settings.desired_local_activity = 1
    settings.connected_pct = 1
    settings.xinput = len(inp)
    settings.yinput = 1
    settings.potential_radius = 2
    settings.xdimension = 4
    settings.ydimension = 1
    settings.initial_inhibition_radius = 1

    r = Region(settings, SimpleMapper())
    overlaps = r.update_overlaps(r.get_columns(), inp)

    cols = r.inhibition_phase(r.get_columns(), overlaps)
    assert len(cols) == 2

    r = Region(settings, SimpleMapper())
    overlaps = r.update_overlaps(r.get_columns(), inp)

    r.inhibition_phase(r.get_columns(), overlaps)
    # ожидаем разные результаты теста из-за рандомного шафла
    cols = r.inhibition_phase(r.get_columns(), overlaps)
    assert len(cols) == 2
    cols = r.inhibition_phase(r.get_columns(), overlaps)
    assert len(cols) == 2
    cols = r.inhibition_phase(r.get_columns(), overlaps)
    assert len(cols) == 2
    cols = r.inhibition_phase(r.get_columns(), overlaps)
    assert len(cols) == 2


def test_overlap_on_ones():
    inp = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    settings = spatial_settings
    settings.debug = True

    settings.min_overlap = 1
    settings.desired_local_activity = 1
    settings.connected_pct = 1
    settings.xinput = len(inp)
    settings.yinput = 1
    settings.potential_radius = 2
    settings.xdimension = 4
    settings.ydimension = 1

    r = Region(settings, SimpleMapper())
    overlaps = r.update_overlaps(r.get_columns(), inp)

    groundtruth = [5, 5, 5, 5]
    for i in range(len(groundtruth)):
        assert overlaps[i] == groundtruth[i]

    settings.potential_radius = 2
    settings.xdimension = 1
    settings.ydimension = 1

    r = Region(settings, SimpleMapper())
    overlaps = r.update_overlaps(r.get_columns(), inp)

    groundtruth = [5]
    for i in range(len(groundtruth)):
        assert overlaps[i] == groundtruth[i]

    settings.potential_radius = 2
    settings.xdimension = 16
    settings.ydimension = 1

    r = Region(settings, SimpleMapper())
    overlaps = r.update_overlaps(r.get_columns(), inp)

    groundtruth = [3, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 3]
    for i in range(len(groundtruth)):
        assert overlaps[i] == groundtruth[i]


def test_overlap_on_not_ones():
    inp = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

    settings = spatial_settings
    settings.debug = True

    settings.min_overlap = 1
    settings.desired_local_activity = 1
    settings.connected_pct = 1
    settings.xinput = len(inp)
    settings.yinput = 1
    settings.potential_radius = 2
    settings.xdimension = 4
    settings.ydimension = 1

    r = Region(settings, SimpleMapper())
    overlaps = r.update_overlaps(r.get_columns(), inp)

    groundtruth = [3, 2, 3, 2]
    for i in range(len(groundtruth)):
        assert overlaps[i] == groundtruth[i]


def test_htm_constructuion():
    setting = spatial_settings
    setting.debug = True

    setting.min_overlap = 1
    setting.desired_local_activity = 1
    setting.connected_pct = 1
    setting.xinput = 5
    setting.yinput = 1
    setting.potential_radius = 2
    setting.xdimension = 4
    setting.ydimension = 1
    setting.initial_inhibition_radius = 2

    r = Region(setting, SimpleMapper())

    assert len(r.get_columns()) == 4
    assert r.get_input_h() == 1
    assert r.get_input_w() == 5
    assert len(r.get_columns()[0].get_neighbors()) == 2
    v = r.get_columns()[r.get_columns()[0].get_neighbors()[0]].get_coord()
    assert v[0] == 1.0 and v[1] == 0.0


def test_out_prediction():
    setting = spatial_settings
    setting.debug = True

    setting.min_overlap = 1
    setting.desired_local_activity = 1
    setting.connected_pct = 1
    setting.xinput = 4
    setting.yinput = 4
    setting.potential_radius = 2
    setting.xdimension = 4
    setting.ydimension = 1
    setting.initial_inhibition_radius = 2

    r = Region(setting, SimpleMapper())
    inp = [[1, 0, 1, 0], [1, 0, 1, 0], [1, 0, 1, 0], [1, 0, 1, 0]]
    r.step_forward(inp)
    res = r.out_prediction([[1, 0, 1, 0]])
    # print(res)
    for i in range(len(res)):
        for j in range(len(res[0])):
            if inp[i][j] ==1:
                assert res[i][j] > 0


def test_debug_false():
    setting = spatial_settings
    setting.debug = False

    setting.min_overlap = 1
    setting.desired_local_activity = 1
    setting.connected_pct = 1
    setting.xinput = 4
    setting.yinput = 4
    setting.potential_radius = 2
    setting.xdimension = 4
    setting.ydimension = 1
    setting.initial_inhibition_radius = 2

    r = Region(setting, SimpleMapper())
    inp = [[1, 0, 1, 0], [1, 0, 1, 0], [1, 0, 1, 0], [1, 0, 1, 0]]
    res = r.step_forward(inp)
    print(res)
    assert len(list(filter(lambda x: x[0] == True, res)))>0

if __name__ == "__main__":
    print("Testing")
    test_debug_false()
    test_out_prediction()
    test_htm_constructuion()
    test_overlap_on_ones()
    test_inhibition_phase()
    testUpdateSynapses()
    test_learning()
    test_overlap_on_not_ones()
    test_ladder()
