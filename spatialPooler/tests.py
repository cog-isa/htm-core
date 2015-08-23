# -*- coding: utf8 -*-
__author__ = 'gmdidro'

from spatialPooler.spooler import SpatialPooler
from spatialPooler import sp_settings
from spatialPooler.sp_region import Region
from spatialPooler.mappers.sp_very_simple_mapper import verySimpleMapper
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


def findByColXY(cols, x, y):
    for c in cols:
        v=c.get_coord()
        if(v[0]==x and v[1]==y): return c

    return None


class Dir(Enum):
    UP=1
    DOWN=2

def testLadder():
    # FileOutputStream fos=new FileOutputStream("out.txt")
    #  PrintWriter pw=new PrintWriter(fos)

    # FileOutputStream fos_in=new FileOutputStream("in.txt")
    # PrintWriter pw_in=new PrintWriter(fos_in)

    W=15
    H=15
    begX=0
    begY=0
    stepSize=5

    map = [[0 for j in range(H)] for i in range(W)]
    myArray=[[0 for j in range(H)] for i in range(W)]
    inp=[]
    inp=[0 for i in range(H*W)]
    STEPS=5
    TOTAL_STEPS=1000
    STEP_SIZE=STEPS

    setting=sp_settings.HTMSettings.get_default_settings()
    setting.debug=True

    setting.activationThreshold = 1
    setting.minOverlap = 1
    setting.desiredLocalActivity = 1
    setting.connectedPct=1
    # setting.connectedPerm=0.01
    setting.xInput=W
    setting.yInput=H
    setting.potentialRadius=2
    setting.xDimension=3
    setting.yDimension=3
    setting.initialInhibitionRadius=2

    # pw.print(setting.xDimension + " ")
    # pw.print(setting.yDimension + " ")
    # pw.print(TOTAL_STEPS)
    # pw.println()
    #
    # pw_in.print(setting.xDimension + " ")
    # pw_in.print(setting.yDimension + " ")
    # pw_in.print(TOTAL_STEPS)
    # pw_in.println()

    r=Region(setting,verySimpleMapper())

    sp=SpatialPooler(setting)
    x=begX
    y=begY
    for  i in range(x,x+stepSize):
        for  j in range(y,y+stepSize):
            map[i][j] = 1

    for step in range(TOTAL_STEPS):
        print("DATA:\n")
        index = 0
        for k in range(W):
            for m in range(H):
                inp[index] = map[k][m]
                # pw_in.print(in[index])
                print(str(inp[index])+" ",end="",flush=True)
                index=index+1
            print()
            # pw_in.println()
        print()
        # pw_in.println()

        for  i in range(x,x+stepSize):
            for  j in range(y,y+stepSize):
                if i<len(map) and j<len(map[0]):
                    map[i][j] = 0

        x=x+STEP_SIZE
        y=y+STEP_SIZE
        if(x>W):
            x=0
            y=0

        for  i in range(x,x+stepSize):
            for  j in range(y,y+stepSize):
                if i<len(map) and j<len(map[0]):
                    map[i][j] = 1

        for c in r.get_columns():
            c.set_is_active(False)


        ov=sp.update_overlaps(r.get_columns(), inp)
        sp.inhibition_phase(r.get_columns(), ov)
        sp.learning_phase(r.get_columns(), inp, ov)
        cols=r.get_columns()

        for i in range(setting.xDimension):
            for j in range(setting.yDimension):
                state=1 if findByColXY(cols,i,j).getIsActive() else 0
                print(str(state)+" ",end="",flush=True)
                # pw.print(state)
                # pw.print(" ")
            print()

def testLearning():
    inp=[1,1,1,1,1,0,1,1, 1,1,1,1, 1,1,1,1]

    settings=sp_settings.HTMSettings.get_default_settings()
    settings.debug=True

    settings.activationThreshold = 1
    settings.minOverlap = 1
    settings.desiredLocalActivity = 1
    settings.connectedPct=1
    settings.xInput=len(inp)
    settings.yInput=1
    settings.potentialRadius=2
    settings.xDimension=4
    settings.yDimension=1
    settings.initialInhibitionRadius=1
    settings.permanenceInc=0.2
    settings.permanenceDec=0.2

    r=Region(settings,SimpleMapper())
    sp=SpatialPooler(settings)
    r.get_columns()[0].get_potential_synapses().get(4).set_permanence(0.5)
    r.get_columns()[0].get_potential_synapses().get(5).set_permanence(0.5)
    ov=sp.update_overlaps(r.get_columns(), inp)
    sp.inhibition_phase(r.get_columns(),ov)
    sp.learning_phase(r.get_columns(), inp, ov)

    v=r.get_columns()[0].get_potential_synapses().get(4).get_permanence()
    assert v == 0.7
    v=r.get_columns()[0].get_potential_synapses().get(5).get_permanence()
    assert v == 0.3


def testUpdateActiveDutyCycle():
    inp=[1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1]

    settings=sp_settings.HTMSettings.get_default_settings()
    settings.debug=True

    settings.activationThreshold = 1
    settings.minOverlap = 1
    settings.desiredLocalActivity = 1
    settings.connectedPct=1
    settings.xInput=input.size()
    settings.yInput=1
    settings.potentialRadius=2
    settings.xDimension=4
    settings.yDimension=1
    settings.initialInhibitionRadius=1

    r=Region(settings,SimpleMapper())

    sp=SpatialPooler(settings)
    overlaps=sp.update_overlaps(r.get_columns(),inp)
    sp.inhibition_phase(r.get_columns(), overlaps)
    sp.update_active_duty_cycle(r.get_columns())
    sp.inhibition_phase(r.get_columns(), overlaps)
    sp.update_active_duty_cycle(r.get_columns())
    sp.inhibition_phase(r.get_columns(), overlaps)
    sp.update_active_duty_cycle(r.get_columns())
    sp.inhibition_phase(r.get_columns(), overlaps)
    sp.update_active_duty_cycle(r.get_columns())

    assert len(sp.get_active_duty_cycles()) == len(r.get_columns())
    assert sp.get_active_duty_cycles()[0] == 4


    inp=[1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,0]

    r=Region(settings, SimpleMapper())
    sp=SpatialPooler(settings)
    overlaps=sp.update_overlaps( r.get_columns(),inp)
    sp.inhibition_phase(r.get_columns(), overlaps)
    sp.update_active_duty_cycle(r.get_columns())
    sp.inhibition_phase(r.get_columns(), overlaps)
    sp.update_active_duty_cycle(r.get_columns())
    sp.inhibition_phase(r.get_columns(), overlaps)
    sp.update_active_duty_cycle(r.get_columns())
    sp.inhibition_phase(r.get_columns(), overlaps)
    sp.update_active_duty_cycle(r.get_columns())

    assert len(sp.get_active_duty_cycles()) == len(r.get_columns())
    assert sp.get_active_duty_cycles()[0]==0
    assert sp.get_active_duty_cycles()[1]==3
    assert sp.get_active_duty_cycles()[2]==3
    assert sp.get_active_duty_cycles()[3]==2


def testUpdateSynapses():
    inp=[1,1,1,1,1,0,1,1, 1,1,1,1, 1,1,1,1]

    settings=sp_settings.HTMSettings.get_default_settings()
    settings.debug=True

    settings.activationThreshold = 1
    settings.minOverlap = 1
    settings.desiredLocalActivity = 1
    settings.connectedPct=1
    settings.xInput=len(inp)
    settings.yInput=1
    settings.potentialRadius=2
    settings.xDimension=4
    settings.yDimension=1
    settings.initialInhibitionRadius=1
    settings.permanenceInc=0.2
    settings.permanenceDec=0.2
    r=Region(settings,SimpleMapper())

    sp=SpatialPooler(settings)
    r.get_columns()[0].get_potential_synapses().get(4).set_permanence(0.5)
    sp.update_synapses(r.get_columns(),inp)
    v=r.get_columns()[0].get_potential_synapses().get(4).get_permanence()
    assert v==0.7

    r.get_columns()[0].get_potential_synapses().get(5).set_permanence(0.5)
    sp.update_synapses(r.get_columns(),inp)
    v=r.get_columns()[0].get_potential_synapses().get(5).get_permanence()
    assert v==0.3


def testInhibitionPhase():
    inp=[1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,0]

    settings=sp_settings.HTMSettings.get_default_settings()
    settings.debug=True

    settings.activationThreshold = 1
    settings.minOverlap = 1
    settings.desiredLocalActivity = 1
    settings.connectedPct=1
    settings.xInput=len(inp)
    settings.yInput=1
    settings.potentialRadius=2
    settings.xDimension=4
    settings.yDimension=1
    settings.initialInhibitionRadius=1

    r=Region(settings,SimpleMapper())
    sp=SpatialPooler(settings)
    sp.r.seed(10)
    overlaps=sp.update_overlaps( r.get_columns(),inp)

    cols=sp.inhibition_phase(r.get_columns(), overlaps)
    assert len(cols)==2

    r=Region(settings,SimpleMapper())
    sp=SpatialPooler(settings)
    sp.r.seed(10)
    overlaps=sp.update_overlaps( r.get_columns(),inp)

    cols=sp.inhibition_phase(r.get_columns(), overlaps)
    # ожидаем разные результаты теста из-за рандомного шафла
    cols=sp.inhibition_phase(r.get_columns(), overlaps)
    assert len(cols)==2
    cols=sp.inhibition_phase(r.get_columns(), overlaps)
    assert len(cols)==2
    cols=sp.inhibition_phase(r.get_columns(), overlaps)
    assert len(cols)==2
    cols=sp.inhibition_phase(r.get_columns(), overlaps)
    assert len(cols)==2


def testOverlapOnOnes():
    inp=[1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1]


    settings=sp_settings.HTMSettings.get_default_settings()
    settings.debug=True

    settings.activationThreshold = 1
    settings.minOverlap = 1
    settings.desiredLocalActivity = 1
    settings.connectedPct=1
    settings.xInput=len(inp)
    settings.yInput=1
    settings.potentialRadius=2
    settings.xDimension=4
    settings.yDimension=1

    r=Region(settings,SimpleMapper())
    sp = SpatialPooler(settings)
    overlaps=sp.update_overlaps( r.get_columns(),inp)

    groundtruth=[5,5,5,5]
    for i in range(len(groundtruth)):
        assert overlaps[i]==groundtruth[i]

    settings.potentialRadius=2
    settings.xDimension=1
    settings.yDimension=1

    r=Region(settings,SimpleMapper())
    sp = SpatialPooler(settings)
    overlaps=sp.update_overlaps( r.get_columns(),inp)

    groundtruth=[5]
    for i in range(len(groundtruth)):
        assert overlaps[i]==groundtruth[i]


    settings.potentialRadius=2
    settings.xDimension=16
    settings.yDimension=1

    r=Region(settings,SimpleMapper())
    sp = SpatialPooler(settings)
    overlaps=sp.update_overlaps( r.get_columns(),inp)

    groundtruth=[3,4,5,5, 5,5,5,5, 5,5,5,5, 5,5,4,3]
    for i in range(len(groundtruth)):
        assert overlaps[i]==groundtruth[i]


def testOverlapOnNotOnes():
    inp=[1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,0]

    settings=sp_settings.HTMSettings.get_default_settings()
    settings.debug=True

    settings.activationThreshold = 1
    settings.minOverlap = 1
    settings.desiredLocalActivity = 1
    settings.connectedPct=1
    settings.xInput=len(inp)
    settings.yInput=1
    settings.potentialRadius=2
    settings.xDimension=4
    settings.yDimension=1

    r=Region(settings,SimpleMapper())

    sp=SpatialPooler(settings)
    overlaps=sp.update_overlaps( r.get_columns(),inp)

    groundtruth=[3,2, 3,2]
    for i in range(len(groundtruth)):
        assert overlaps[i]==groundtruth[i]


def testHTMConstructuion():
    setting = sp_settings.HTMSettings.get_default_settings()
    setting.debug = True

    setting.activationThreshold = 1
    setting.minOverlap = 1
    setting.desiredLocalActivity = 1
    setting.connectedPct = 1
    setting.xInput = 5
    setting.yInput = 1
    setting.potentialRadius = 2
    setting.xDimension = 4
    setting.yDimension = 1
    setting.initialInhibitionRadius=2


    r = Region(setting,SimpleMapper())

    assert len(r.get_columns()) == 4
    assert r.get_input_h() == 1
    assert r.get_input_w() == 5
    assert len(r.get_columns()[0].get_neighbors())==2
    v=r.get_columns()[r.get_columns()[0].get_neighbors()[0]].get_coord()
    assert v[0]==1.0 and v[1]==0.0

if __name__ == "__main__":
    print("Testing")
    testHTMConstructuion()
    testOverlapOnOnes()
    testInhibitionPhase()
    testUpdateSynapses()
    testLearning()
    testOverlapOnNotOnes()
    testLadder()