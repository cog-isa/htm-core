# -*- coding: utf8 -*-
import HTMSettings
from utils import kthScore

__author__ = 'AVPetrov'
import random
from region import Region

class SpatialPooler:
    def __init__(self, settings):
        self.settings = settings
        self.r = random.Random()
        self.r.seed = 10
        self.activeDutyCycles = [0 for i in range(self.settings.xDimension*self.settings.yDimension)]
        self.overlapDutyCycles = [0 for i in range(self.settings.xDimension*self.settings.yDimension)]
    # this.settings=settings;
    # activeDutyCycles=new int[settings.xDimension*settings.yDimension];
    # overlapDutyCycles=new int[settings.xDimension*settings.yDimension];

    def getActiveDutyCycles(self):
        return self.activeDutyCycles


    # Вычисление значения перекрытия каждой колонки с заданным входным вектором.
    #
    #  @param input - входной сигнал
    # @param cols - колонки
    # @return значения переключения для каждой колонки
    def updateOverlaps(self,cols, input):
        overlaps=[0 for i in range(len(cols))]
        i=0
        for c in cols:
            for s in c.getConnectedSynapses():
                overlaps[i]=overlaps[i] + (1 if input[s.getIndexConnectTo()==1] else 0)
            i=i+1
        return overlaps

    # Вычисление колонок, остающихся победителями после применения взаимного подавления.
    def inhibitionPhase(self, cols, overlaps):
        activeColumns=[]

        indexies = [i for i in range(len(cols))]
        self.r.shuffle(indexies)
        for indx in indexies:
            column=cols[indx]
            if len(column.getNeighbors()) > 0:
                # выборка перекрытий колонок, соседних с данной
                neighborOverlaps = [overlaps[i] for i in column.getNeighbors()]
                # определить порог перекрытия
                minLocalOverlap = kthScore(neighborOverlaps, self.settings.desiredLocalActivity)
                # если колонка имеет перекрытие большее, чем у соседей, то она становиться активной

                if overlaps[column.getIndex()] > 0 and overlaps[column.getIndex()] >= minLocalOverlap:
                    # для случая одинаковых оверлапов у выбраныных соседей
                    n=0
                    for i in column.getNeighbors():
                        n=n+(1 if self.findByColIndex(cols,0).getIsActive() else 0)
                    if n<=(self.settings.desiredLocalActivity-1): #-1 - считая саму колонку
                        column.setIsActive(True)
                        activeColumns.append(column)
                else:
                    column.setIsActive(False)
        return activeColumns


    def findByColIndex(self,cols, index):
        for c in cols:
            if(c.getIndex()==index):
                return c
        return None

    # Если синапс был активен (через него шел сигнал от входного вектора), его значение преманентности увеличивается,
    # а иначе - уменьшается.
    # @param inp - входной сигнал
    def updateSynapses(self,cols,inp):
        for col in cols:
            for synapse in col.getPotentialSynapses().values():
                if inp[synapse.getIndexConnectTo()]:
                    synapse.increasePermanence()
                else:
                    synapse.decreasePermanence()

    def updateActiveDutyCycle(self,cols):
        for i in range(len(cols)):
            self.activeDutyCycles[i] = self.activeDutyCycles[i] + (1 if cols[i].getIsActive()  else 0)


    def updateOverlapDutyCycle(self,col,overlaps):
        self.overlapDutyCycles[col.getIndex()] = self.overlapDutyCycles[col.getIndex()] + (1 if overlaps[col.getIndex()] > self.settings.minOverlap else 0)


    # Если activeDutyCycle больше minValue, то значение ускорения равно 1. Ускорение начинает линейно увеличиваться
    # как только activeDutyCycle колонки падает ниже minDutyCycle.
    #
    # @param minValue - минимальнео число активных циклов
    def updateBoostFactor(self,col, minValue):
        value = 1

        if (self.activeDutyCycles[col.getIndex()] < minValue):
                value = 1 + (minValue - self.activeDutyCycles[col.getIndex()]) * (self.settings.maxBoost - 1)
        col.setBoostFactor(value)

    # Обновление значений перманентности, фактора ускорения и радиуса подавления колонок.
    # Механизм ускорения работает в том случае, если колонка не побеждает достаточно долго (activeDutyCycle).
    # Если колонка плохо перекрывается с входным сигналом достоачно долго (overlapDutyCycle), то увеличиваются
    # перманентности.

    def learningPhase(self,cols, inp,overlaps):

        # 1. изменить значения перманентности всех синапсов проксимальных сегментов *активных* колонок
        self.updateSynapses(cols,inp)

        for column in cols:
            # определить максимальное число срабатываний колонки среди соседей колонки и её самой колонку
            maxActiveDuty = 0
            for index in column.getNeighbors():
                maxActiveDuty = maxActiveDuty  if maxActiveDuty > self.activeDutyCycles[index] else self.activeDutyCycles[index]

            # определить минимальное число срабатываний (% от maxActiveDuty)
            minDutyCycle = self.settings.minDutyCycleFraction * maxActiveDuty

            self.updateBoostFactor(column,minDutyCycle)

            self.updateOverlapDutyCycle(column,overlaps)
            # если колонка редко срабатывает стимулировать её
            if self.overlapDutyCycles[column.getIndex()] < minDutyCycle:
                column.stimulate()

            # TODO: в оригинальной реализиации радиус менялся и соседи тоже...
            # column.updateNeighbors(averageReceptiveFieldSize())

        # теперь обновим activeDutyCycle всех колонок.
        self.updateActiveDutyCycle(cols)

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

from mappers.VerySimpleMapper import verySimpleMapper
from mappers.SimpleMapper import simpleMapper


def _tests():
   # testHTMConstructuion();
   #      //overlap test
   #      testOverlapOnOnes();
   #      testOverlapOnNotOnes();
   #
   #      //inhibition test
   #      testInhibitionPhase();
   #
   #      testUpdateSynapses();
   #      testUpdateActiveDutyCycle();
   #
   #      //testLearning();
   #      //testLadder();
    return


    # //TODO: переписать, сейчас не верно беруться размеры
    # public void testDiff() throws IOException
    # {
    #     FileInputStream fis_truth=new FileInputStream("in.txt");
    #     Scanner sc_truth=new Scanner(fis_truth);
    #     FileInputStream fis_predict=new FileInputStream("out_predict.txt");
    #     Scanner sc_p=new Scanner(fis_predict);
    #     FileOutputStream fos_err=new FileOutputStream("errs.txt");
    #     PrintWriter pw_err=new PrintWriter(fos_err);
    #
    #
    #
    #     int w=sc_truth.nextInt();
    #     int h=sc_truth.nextInt();
    #     int step=sc_truth.nextInt();
    #
    #     sc_truth.nextLine();
    #     sc_p.nextLine();
    #
    #     for(int s=0;s<step;s++) {
    #         int[] errs=new int[h];
    #         for (int i = 0; i < h; i++) {
    #             BitVector true_bv=MathUtils.bitvectorFromString(sc_truth.nextLine());
    #             //System.out.println(sc_truth.nextLine());
    #             BitVector predict_bv=MathUtils.bitvectorFromString(sc_p.nextLine());
    #             //System.out.println(sc_p.nextLine());
    #
    #             predict_bv.xor(true_bv);
    #             errs[i]=(int)MathUtils.sumOfLongs(predict_bv.elements());
    #         }
    #         pw_err.println(MathUtils.sumOfInts(errs));
    #     }
    #     pw_err.close();
    # }


def findByColXY(cols, x, y):
    for c in cols:
        v=c.getCoord();
        if(v[0]==x and v[1]==y): return c;

    return None;

from enum import Enum
class Dir(Enum):
    UP=1
    DOWN=2

def testLadder():
    # FileOutputStream fos=new FileOutputStream("out.txt");
    #  PrintWriter pw=new PrintWriter(fos);

    # FileOutputStream fos_in=new FileOutputStream("in.txt");
    # PrintWriter pw_in=new PrintWriter(fos_in);

    W=95
    H=95
    begX=0
    begY=0
    stepSize=20

    map = [[0 for j in range(H)] for i in range(W)]
    myArray=[[0 for j in range(H)] for i in range(W)]
    inp=[]
    inp=[0 for i in range(H*W)]
    STEPS=25;
    TOTAL_STEPS=1000;
    STEP_SIZE=STEPS;

    setting=HTMSettings.HTMSettings.getDefaultSettings();
    setting.debug=True;

    setting.activationThreshold = 1;
    setting.minOverlap = 1;
    setting.desiredLocalActivity = 3;
    setting.connectedPct=1;
    setting.connectedPerm=0.01;
    setting.xInput=W;
    setting.yInput=H;
    setting.potentialRadius=4;
    setting.xDimension=10;
    setting.yDimension=10;
    setting.initialInhibitionRadius=1;

    # pw.print(setting.xDimension + " ");
    # pw.print(setting.yDimension + " ");
    # pw.print(TOTAL_STEPS);
    # pw.println();
    #
    # pw_in.print(setting.xDimension + " ");
    # pw_in.print(setting.yDimension + " ");
    # pw_in.print(TOTAL_STEPS);
    # pw_in.println();

    r=Region(setting,verySimpleMapper());

    sp=SpatialPooler(setting);
    x=begX
    y=begY
    for  i in range(x,x+stepSize):
        for  j in range(y,y+stepSize):
            map[i][j] = 1;

    for step in range(TOTAL_STEPS):
        print("DATA:\n");
        index = 0;
        for k in range(W):
            for m in range(H):
                inp[index] = map[k][m];
                # pw_in.print(in[index]);
                index=index+1;
            # pw_in.println()
        # pw_in.println();

        for  i in range(x,x+stepSize):
            for  j in range(y,y+stepSize):
                if i<len(map) and j<len(map[0]):
                    map[i][j] = 0

        x=x+STEP_SIZE;
        y=y+STEP_SIZE;
        if(x>W):
            x=0;
            y=0;

        for  i in range(x,x+stepSize):
            for  j in range(y,y+stepSize):
                if i<len(map) and j<len(map[0]):
                    map[i][j] = 1

        for c in r.getColumns():
            c.setIsActive(False);
        ov=sp.updateOverlaps(r.getColumns(), inp);
        sp.inhibitionPhase(r.getColumns(), ov);
        sp.learningPhase(r.getColumns(), inp, ov);


        cols=r.getColumns();
        for i in range(setting.xDimension):
            for j in range(setting.yDimension):
                state=1 if findByColXY(cols,i,j).getIsActive() else 0;
                print(str(state)+" ")
                # pw.print(state);
                # pw.print(" ");
            print("\n")
        print("\n")
            # pw.println();
        # pw.println();

        # /*System.out.println("BOOST:");
        # cols=r.getColumns();
        # for(int i=0;i<settings.xDimension;i++)
        # {
        #     for(int j=0;j<settings.yDimension;j++) {
        #         System.out.print(cols.get(i*settings.yDimension+j).getProximalDendrite().getBoostFactor()+" ");
        #     }
        #     System.out.println();
        # }*/
    # pw.close();

#     def testLearning()
#     {
#         int[] in=new int[]{1,1,1,1,1,0,1,1, 1,1,1,1, 1,1,1,1};
#         BitVector input=new BitVector(in.length);
#         MathUtils.assign(input, in);
#
#         HTMSettings settings=HTMSettings.getDefaultSettings();
#         HTMSettings.debug=true;
#
#         settings.activationThreshold = 1;
#         settings.minOverlap = 1;
#         settings.desiredLocalActivity = 1;
#         settings.connectedPct=1;
#         settings.xInput=input.size();
#         settings.yInput=1;
#         settings.potentialRadius=2;
#         settings.xDimension=4;
#         settings.yDimension=1;
#         settings.initialInhibitionRadius=1;
#         settings.permanenceInc=0.2;
#         settings.permanenceDec=0.2;
#
#         Region r=new Region(settings,new SimpleMapper());
#         SpatialPooler sp=new SpatialPooler(settings);
#         r.getColumns().get(0).getProximalDendrite().getPotentialSynapses().get(4).setPermanence(0.5);
#         r.getColumns().get(0).getProximalDendrite().getPotentialSynapses().get(5).setPermanence(0.5);
#         int[] ov=sp.updateOverlaps(r.getColumns(), input);
#         sp.inhibitionPhase(r.getColumns(),ov);
#         sp.learningPhase(r.getColumns(), input, ov);
#
#         double v=r.getColumns().get(0).getProximalDendrite().getPotentialSynapses().get(4).getPermanence();
#         Assert.assertTrue(v == 0.7);
#         v=r.getColumns().get(0).getProximalDendrite().getPotentialSynapses().get(5).getPermanence();
#         Assert.assertTrue(v == 0.3);
#
#     }
#
#     public void testUpdateActiveDutyCycle() {
#         Method method = null;
#         try {
#             Method[] m = SpatialPooler.class.getMethods();
#             method = SpatialPooler.class.getDeclaredMethod("updateActiveDutyCycle", ArrayList.class);
#         } catch (NoSuchMethodException e) {
#             e.printStackTrace();
#         }
#         method.setAccessible(true);
#
#
#         int[] in=new int[]{1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1};
#         BitVector input=new BitVector(in.length);
#         MathUtils.assign(input, in);
#
#         HTMSettings settings=HTMSettings.getDefaultSettings();
#         HTMSettings.debug=true;
#
#         settings.activationThreshold = 1;
#         settings.minOverlap = 1;
#         settings.desiredLocalActivity = 1;
#         settings.connectedPct=1;
#         settings.xInput=input.size();
#         settings.yInput=1;
#         settings.potentialRadius=2;
#         settings.xDimension=4;
#         settings.yDimension=1;
#         settings.initialInhibitionRadius=1;
#         try {
#             Region r=new Region(settings,new SimpleMapper());
#
#             SpatialPooler sp=new SpatialPooler(settings);
#             int[] overlaps=sp.updateOverlaps(r.getColumns(),input);
#             sp.inhibitionPhase(r.getColumns(), overlaps);
#             method.invoke(sp, r.getColumns());
#             sp.inhibitionPhase(r.getColumns(), overlaps);
#             method.invoke(sp, r.getColumns());
#             sp.inhibitionPhase(r.getColumns(), overlaps);
#             method.invoke(sp, r.getColumns());
#             sp.inhibitionPhase(r.getColumns(), overlaps);
#             method.invoke(sp, r.getColumns());
#
#             Assert.assertTrue(sp.getActiveDutyCycles().length == r.getColumns().size());
#             Assert.assertTrue(sp.getActiveDutyCycles()[0] == 4);
#
#
#             in=new int[]{1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,0};
#             input=new BitVector(in.length);
#             MathUtils.assign(input, in);
#
#             r=new Region(settings, new SimpleMapper());
#             sp=new SpatialPooler(settings);
#             overlaps=sp.updateOverlaps( r.getColumns(),input);
#             sp.inhibitionPhase(r.getColumns(), overlaps);
#             method.invoke(sp, r.getColumns());
#             sp.inhibitionPhase(r.getColumns(), overlaps);
#             method.invoke(sp, r.getColumns());
#             sp.inhibitionPhase(r.getColumns(), overlaps);
#             method.invoke(sp, r.getColumns());
#             sp.inhibitionPhase(r.getColumns(), overlaps);
#             method.invoke(sp, r.getColumns());
#
#             Assert.assertTrue(sp.getActiveDutyCycles().length == r.getColumns().size());
#             Assert.assertTrue(sp.getActiveDutyCycles()[0]==0);
#             Assert.assertTrue(sp.getActiveDutyCycles()[1]==3);
#             Assert.assertTrue(sp.getActiveDutyCycles()[2]==3);
#             Assert.assertTrue(sp.getActiveDutyCycles()[3]==2);
#
#         } catch (IllegalAccessException e) {
#             e.printStackTrace();
#         } catch (InvocationTargetException e) {
#             e.printStackTrace();
#         }
#     }
#
#     public void testUpdateSynapses() {
#         int[] in=new int[]{1,1,1,1,1,0,1,1, 1,1,1,1, 1,1,1,1};
#         BitVector input=new BitVector(in.length);
#         MathUtils.assign(input, in);
#
#         HTMSettings settings=HTMSettings.getDefaultSettings();
#         HTMSettings.debug=true;
#
#         settings.activationThreshold = 1;
#         settings.minOverlap = 1;
#         settings.desiredLocalActivity = 1;
#         settings.connectedPct=1;
#         settings.xInput=input.size();
#         settings.yInput=1;
#         settings.potentialRadius=2;
#         settings.xDimension=4;
#         settings.yDimension=1;
#         settings.initialInhibitionRadius=1;
#         settings.permanenceInc=0.2;
#         settings.permanenceDec=0.2;
#         Region r=new Region(settings,new SimpleMapper());
#
#         SpatialPooler sp=new SpatialPooler(settings);
#         r.getColumns().get(0).getProximalDendrite().getPotentialSynapses().get(4).setPermanence(0.5);
#         sp.updateSynapses(r.getColumns(),input);
#         double v=r.getColumns().get(0).getProximalDendrite().getPotentialSynapses().get(4).getPermanence();
#         Assert.assertTrue(v==0.7);
#
#
#         r.getColumns().get(0).getProximalDendrite().getPotentialSynapses().get(5).setPermanence(0.5);
#         sp.updateSynapses(r.getColumns(),input);
#         v=r.getColumns().get(0).getProximalDendrite().getPotentialSynapses().get(5).getPermanence();
#         Assert.assertTrue(v==0.3);
#     }
#
#     public void testInhibitionPhase() {
#         int[] in=new int[]{1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,0};
#         BitVector input=new BitVector(in.length);
#         MathUtils.assign(input, in);
#
#         HTMSettings settings=HTMSettings.getDefaultSettings();
#         HTMSettings.debug=true;
#
#         settings.activationThreshold = 1;
#         settings.minOverlap = 1;
#         settings.desiredLocalActivity = 1;
#         settings.connectedPct=1;
#         settings.xInput=input.size();
#         settings.yInput=1;
#         settings.potentialRadius=2;
#         settings.xDimension=4;
#         settings.yDimension=1;
#         settings.initialInhibitionRadius=1;
#
#         Region r=new Region(settings,new SimpleMapper());
#
#         SpatialPooler sp=new SpatialPooler(settings);
#         sp.seed=10;
#         int[] overlaps=sp.updateOverlaps( r.getColumns(),input);
#         ArrayList<Column> cols=sp.inhibitionPhase(r.getColumns(), overlaps);
#
#         Assert.assertTrue(cols.size()==2);
#
#         r=new Region(settings,new SimpleMapper());
#         sp=new SpatialPooler(settings);
#         overlaps=sp.updateOverlaps( r.getColumns(),input);
#         // ожидаем разные результаты теста из-за рандомного шафла
#         cols=sp.inhibitionPhase(r.getColumns(), overlaps);
#         Assert.assertTrue(cols.size()==2);
#         cols=sp.inhibitionPhase(r.getColumns(), overlaps);
#         Assert.assertTrue(cols.size()==2);
#         cols=sp.inhibitionPhase(r.getColumns(), overlaps);
#         Assert.assertTrue(cols.size()==2);
#         cols=sp.inhibitionPhase(r.getColumns(), overlaps);
#         Assert.assertTrue(cols.size()==1);
#     }
#
#     public void testOverlapOnOnes() {
#         int[] in=new int[]{1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1};
#         BitVector input=new BitVector(in.length);
#         MathUtils.assign(input, in);
#
#         HTMSettings settings=HTMSettings.getDefaultSettings();
#         HTMSettings.debug=true;
#
#         settings.activationThreshold = 1;
#         settings.minOverlap = 1;
#         settings.desiredLocalActivity = 1;
#         settings.connectedPct=1;
#         settings.xInput=input.size();
#         settings.yInput=1;
#         settings.potentialRadius=2;
#         settings.xDimension=4;
#         settings.yDimension=1;
#
#         Region r=new Region(settings,new SimpleMapper());
#
#         SpatialPooler sp=new SpatialPooler(settings);
#         int[] overlaps=sp.updateOverlaps( r.getColumns(),input);
#
#         int[] groundtruth=new int[]{5,5,5,5};
#         for (int i = 0; i < groundtruth.length; i++)
#             assertTrue(overlaps[i]==groundtruth[i]);
#
#         settings.potentialRadius=2;
#         settings.xDimension=1;
#         settings.yDimension=1;
#
#         r=new Region(settings,new SimpleMapper());
#         sp=new SpatialPooler(settings);
#         overlaps=sp.updateOverlaps( r.getColumns(),input);
#
#         groundtruth=new int[]{5};
#         for (int i = 0; i < groundtruth.length; i++)
#             assertTrue(overlaps[i]==groundtruth[i]);
#
#
#         settings.potentialRadius=2;
#         settings.xDimension=16;
#         settings.yDimension=1;
#
#         r=new Region(settings,new SimpleMapper());
#         sp=new SpatialPooler(settings);
#         overlaps=sp.updateOverlaps( r.getColumns(),input);
#
#         groundtruth=new int[]{3,4,5,5, 5,5,5,5, 5,5,5,5, 5,5,4,3};
#         for (int i = 0; i < groundtruth.length; i++)
#             assertTrue(overlaps[i]==groundtruth[i]);
#     }
#
#     public void testOverlapOnNotOnes() {
#         int[] in=new int[]{1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,0};
#         BitVector input=new BitVector(in.length);
#         MathUtils.assign(input, in);
#
#         HTMSettings settings=HTMSettings.getDefaultSettings();
#         HTMSettings.debug=true;
#
#         settings.activationThreshold = 1;
#         settings.minOverlap = 1;
#         settings.desiredLocalActivity = 1;
#         settings.connectedPct=1;
#         settings.xInput=input.size();
#         settings.yInput=1;
#         settings.potentialRadius=2;
#         settings.xDimension=4;
#         settings.yDimension=1;
#
#         Region r=new Region(settings,new SimpleMapper());
#
#         SpatialPooler sp=new SpatialPooler(settings);
#         int[] overlaps=sp.updateOverlaps( r.getColumns(),input);
#
#         int[] groundtruth=new int[]{3,2, 3,2};
#         for (int i = 0; i < groundtruth.length; i++)
#             assertTrue(overlaps[i]==groundtruth[i]);
#     }
#
def testHTMConstructuion():
    setting = HTMSettings.HTMSettings.getDefaultSettings()
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


    r = Region(setting,simpleMapper())

    assert len(r.getColumns()) == 4
    assert r.getInputH() == 1
    assert r.getInputW() == 5
    assert len(r.getColumns()[0].getNeighbors())==2
    v=r.getColumns()[r.getColumns()[0].getNeighbors()[0]].getCoord();
    assert v[0]==1.0 and v[1]==0.0

if __name__ == "__main__":
    print(1234)
    testHTMConstructuion()
    testLadder()