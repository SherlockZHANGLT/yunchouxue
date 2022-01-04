import gurobipy as gb
from gurobipy import GRB
import numpy as np
xinrate=np.load('xinrate.npy')  #加载文件
baselen=np.load('baselen.npy')  #   8*8地方距离
dlist_train=np.load('dlist_train.npy')  #   20*8*8*7出行需求
IDL=np.load('IDL.npy')  #   8*8行驶时间
xinlist_train=np.load('xinlist_train.npy')*xinrate  #   20*8初始车辆分布
dis_income=2.28 #距离单价
time_income=0.63    #时段单价
empty_cost=0.70 #调度距离单价

dlist_test=np.load('dlist_test.npy')  #   20*8*8*7出行需求
xinlist_test=np.load('xinlist_test.npy')*xinrate  #   20*8初始车辆分布

sum=0.0

for i in range(20):
    for j in range(8):
        xinlist_train[i][j]=round(xinlist_train[i][j])
for i in range(10):
    for j in range(8):
        xinlist_test[i][j]=round(xinlist_test[i][j])

dlist=dlist_train
xinlist=xinlist_train

for n in range(20): 
    #dlist=dlist_train[m]    #出行需求 8*8*7
    #xinlist=xinlist_train[m]    #初始分布 8

    # Model formulation
    m = gb.Model('Question'+str(n))
    A0 = m.addVars(64, lb=0, vtype=GRB.INTEGER, name='A0')  #时段1的运载数
    A1 = m.addVars(64, lb=0, vtype=GRB.INTEGER, name='A1')
    A2 = m.addVars(64, lb=0, vtype=GRB.INTEGER, name='A2')
    A3 = m.addVars(64, lb=0, vtype=GRB.INTEGER, name='A3')
    A4 = m.addVars(64, lb=0, vtype=GRB.INTEGER, name='A4')
    A5 = m.addVars(64, lb=0, vtype=GRB.INTEGER, name='A5')

    B0 = m.addVars(64, lb=0, vtype=GRB.INTEGER, name='B0')  #时段1的调度数
    B1 = m.addVars(64, lb=0, vtype=GRB.INTEGER, name='B1')
    B2 = m.addVars(64, lb=0, vtype=GRB.INTEGER, name='B2')
    B3 = m.addVars(64, lb=0, vtype=GRB.INTEGER, name='B3')
    B4 = m.addVars(64, lb=0, vtype=GRB.INTEGER, name='B4')
    B5 = m.addVars(64, lb=0, vtype=GRB.INTEGER, name='B5')

    #运载数小于需求量
    m.addConstrs((A0[i] <= dlist[n][i//8][i%8][1] for i in range(64)), 'c1')
    m.addConstrs((A1[i] <= dlist[n][i//8][i%8][2] for i in range(64)), 'c2')
    m.addConstrs((A2[i] <= dlist[n][i//8][i%8][3] for i in range(64)), 'c3')
    m.addConstrs((A3[i] <= dlist[n][i//8][i%8][4] for i in range(64)), 'c4')
    m.addConstrs((A4[i] <= dlist[n][i//8][i%8][5] for i in range(64)), 'c5')
    m.addConstrs((A5[i] <= dlist[n][i//8][i%8][6] for i in range(64)), 'c6')
    

    #拒绝自我调度
    m.addConstrs((A0[i*8+i] == 0 for i in range(8)), 'd1')
    m.addConstrs((A1[i*8+i] == 0 for i in range(8)), 'd2')
    m.addConstrs((A2[i*8+i] == 0 for i in range(8)), 'd3')
    m.addConstrs((A3[i*8+i] == 0 for i in range(8)), 'd4')
    m.addConstrs((A4[i*8+i] == 0 for i in range(8)), 'd5')
    m.addConstrs((A5[i*8+i] == 0 for i in range(8)), 'd6')
    m.addConstrs((B0[i*8+i] == 0 for i in range(8)), 'd7')
    m.addConstrs((B1[i*8+i] == 0 for i in range(8)), 'd8')
    m.addConstrs((B2[i*8+i] == 0 for i in range(8)), 'd9')
    m.addConstrs((B3[i*8+i] == 0 for i in range(8)), 'd10')
    m.addConstrs((B4[i*8+i] == 0 for i in range(8)), 'd11')
    m.addConstrs((B5[i*8+i] == 0 for i in range(8)), 'd12')

    #车辆数目限制
    m.addConstrs((A0[i*8]+A0[i*8+1]+A0[i*8+2]+A0[i*8+3]+A0[i*8+4]+A0[i*8+5]+A0[i*8+6]+A0[i*8+7]+B0[i*8]+B0[i*8+1]+B0[i*8+2]+B0[i*8+3]+B0[i*8+4]+B0[i*8+5]+B0[i*8+6]+B0[i*8+7] <= xinlist[n][i] for i in range(8)), 'e0')
    m.addConstrs((A1[i*8]+A1[i*8+1]+A1[i*8+2]+A1[i*8+3]+A1[i*8+4]+A1[i*8+5]+A1[i*8+6]+A1[i*8+7]+B1[i*8]+B1[i*8+1]+B1[i*8+2]+B1[i*8+3]+B1[i*8+4]+B1[i*8+5]+B1[i*8+6]+B1[i*8+7] <= xinlist[n][i]-(A0[i*8]+A0[i*8+1]+A0[i*8+2]+A0[i*8+3]+A0[i*8+4]+A0[i*8+5]+A0[i*8+6]+A0[i*8+7]+B0[i*8]+B0[i*8+1]+B0[i*8+2]+B0[i*8+3]+B0[i*8+4]+B0[i*8+5]+B0[i*8+6]+B0[i*8+7])+(A0[i]+A0[8+i]+A0[16+i]+A0[24+i]+A0[32+i]+A0[40+i]+A0[48+i]+A0[56+i]+B0[i]+B0[8+i]+B0[16+i]+B0[24+i]+B0[32+i]+B0[40+i]+B0[48+i]+B0[56+i]) for i in range(8)), 'e1')
    m.addConstrs((A2[i*8]+A2[i*8+1]+A2[i*8+2]+A2[i*8+3]+A2[i*8+4]+A2[i*8+5]+A2[i*8+6]+A2[i*8+7]+B2[i*8]+B2[i*8+1]+B2[i*8+2]+B2[i*8+3]+B2[i*8+4]+B2[i*8+5]+B2[i*8+6]+B2[i*8+7] <= xinlist[n][i]-(A0[i*8]+A0[i*8+1]+A0[i*8+2]+A0[i*8+3]+A0[i*8+4]+A0[i*8+5]+A0[i*8+6]+A0[i*8+7]+B0[i*8]+B0[i*8+1]+B0[i*8+2]+B0[i*8+3]+B0[i*8+4]+B0[i*8+5]+B0[i*8+6]+B0[i*8+7])+(A0[i]+A0[8+i]+A0[16+i]+A0[24+i]+A0[32+i]+A0[40+i]+A0[48+i]+A0[56+i]+B0[i]+B0[8+i]+B0[16+i]+B0[24+i]+B0[32+i]+B0[40+i]+B0[48+i]+B0[56+i])-(A1[i*8]+A1[i*8+1]+A1[i*8+2]+A1[i*8+3]+A1[i*8+4]+A1[i*8+5]+A1[i*8+6]+A1[i*8+7]+B1[i*8]+B1[i*8+1]+B1[i*8+2]+B1[i*8+3]+B1[i*8+4]+B1[i*8+5]+B1[i*8+6]+B1[i*8+7])+(A1[i]+A1[8+i]+A1[16+i]+A1[24+i]+A1[32+i]+A1[40+i]+A1[48+i]+A1[56+i]+B1[i]+B1[8+i]+B1[16+i]+B1[24+i]+B1[32+i]+B1[40+i]+B1[48+i]+B1[56+i]) for i in range(8)), 'e2')
    m.addConstrs((A3[i*8]+A3[i*8+1]+A3[i*8+2]+A3[i*8+3]+A3[i*8+4]+A3[i*8+5]+A3[i*8+6]+A3[i*8+7]+B3[i*8]+B3[i*8+1]+B3[i*8+2]+B3[i*8+3]+B3[i*8+4]+B3[i*8+5]+B3[i*8+6]+B3[i*8+7] <= xinlist[n][i]-(A0[i*8]+A0[i*8+1]+A0[i*8+2]+A0[i*8+3]+A0[i*8+4]+A0[i*8+5]+A0[i*8+6]+A0[i*8+7]+B0[i*8]+B0[i*8+1]+B0[i*8+2]+B0[i*8+3]+B0[i*8+4]+B0[i*8+5]+B0[i*8+6]+B0[i*8+7])+(A0[i]+A0[8+i]+A0[16+i]+A0[24+i]+A0[32+i]+A0[40+i]+A0[48+i]+A0[56+i]+B0[i]+B0[8+i]+B0[16+i]+B0[24+i]+B0[32+i]+B0[40+i]+B0[48+i]+B0[56+i])-(A1[i*8]+A1[i*8+1]+A1[i*8+2]+A1[i*8+3]+A1[i*8+4]+A1[i*8+5]+A1[i*8+6]+A1[i*8+7]+B1[i*8]+B1[i*8+1]+B1[i*8+2]+B1[i*8+3]+B1[i*8+4]+B1[i*8+5]+B1[i*8+6]+B1[i*8+7])+(A1[i]+A1[8+i]+A1[16+i]+A1[24+i]+A1[32+i]+A1[40+i]+A1[48+i]+A1[56+i]+B1[i]+B1[8+i]+B1[16+i]+B1[24+i]+B1[32+i]+B1[40+i]+B1[48+i]+B1[56+i])-(A2[i*8]+A2[i*8+1]+A2[i*8+2]+A2[i*8+3]+A2[i*8+4]+A2[i*8+5]+A2[i*8+6]+A2[i*8+7]+B2[i*8]+B2[i*8+1]+B2[i*8+2]+B2[i*8+3]+B2[i*8+4]+B2[i*8+5]+B2[i*8+6]+B2[i*8+7])+(A2[i]+A2[8+i]+A2[16+i]+A2[24+i]+A2[32+i]+A2[40+i]+A2[48+i]+A2[56+i]+B2[i]+B2[8+i]+B2[16+i]+B2[24+i]+B2[32+i]+B2[40+i]+B2[48+i]+B2[56+i]) for i in range(8)), 'e3')
    m.addConstrs((A4[i*8]+A4[i*8+1]+A4[i*8+2]+A4[i*8+3]+A4[i*8+4]+A4[i*8+5]+A4[i*8+6]+A4[i*8+7]+B4[i*8]+B4[i*8+1]+B4[i*8+2]+B4[i*8+3]+B4[i*8+4]+B4[i*8+5]+B4[i*8+6]+B4[i*8+7] <= xinlist[n][i]-(A0[i*8]+A0[i*8+1]+A0[i*8+2]+A0[i*8+3]+A0[i*8+4]+A0[i*8+5]+A0[i*8+6]+A0[i*8+7]+B0[i*8]+B0[i*8+1]+B0[i*8+2]+B0[i*8+3]+B0[i*8+4]+B0[i*8+5]+B0[i*8+6]+B0[i*8+7])+(A0[i]+A0[8+i]+A0[16+i]+A0[24+i]+A0[32+i]+A0[40+i]+A0[48+i]+A0[56+i]+B0[i]+B0[8+i]+B0[16+i]+B0[24+i]+B0[32+i]+B0[40+i]+B0[48+i]+B0[56+i])-(A1[i*8]+A1[i*8+1]+A1[i*8+2]+A1[i*8+3]+A1[i*8+4]+A1[i*8+5]+A1[i*8+6]+A1[i*8+7]+B1[i*8]+B1[i*8+1]+B1[i*8+2]+B1[i*8+3]+B1[i*8+4]+B1[i*8+5]+B1[i*8+6]+B1[i*8+7])+(A1[i]+A1[8+i]+A1[16+i]+A1[24+i]+A1[32+i]+A1[40+i]+A1[48+i]+A1[56+i]+B1[i]+B1[8+i]+B1[16+i]+B1[24+i]+B1[32+i]+B1[40+i]+B1[48+i]+B1[56+i])-(A2[i*8]+A2[i*8+1]+A2[i*8+2]+A2[i*8+3]+A2[i*8+4]+A2[i*8+5]+A2[i*8+6]+A2[i*8+7]+B2[i*8]+B2[i*8+1]+B2[i*8+2]+B2[i*8+3]+B2[i*8+4]+B2[i*8+5]+B2[i*8+6]+B2[i*8+7])+(A2[i]+A2[8+i]+A2[16+i]+A2[24+i]+A2[32+i]+A2[40+i]+A2[48+i]+A2[56+i]+B2[i]+B2[8+i]+B2[16+i]+B2[24+i]+B2[32+i]+B2[40+i]+B2[48+i]+B2[56+i])-(A3[i*8]+A3[i*8+1]+A3[i*8+2]+A3[i*8+3]+A3[i*8+4]+A3[i*8+5]+A3[i*8+6]+A3[i*8+7]+B3[i*8]+B3[i*8+1]+B3[i*8+2]+B3[i*8+3]+B3[i*8+4]+B3[i*8+5]+B3[i*8+6]+B3[i*8+7])+(A3[i]+A3[8+i]+A3[16+i]+A3[24+i]+A3[32+i]+A3[40+i]+A3[48+i]+A3[56+i]+B3[i]+B3[8+i]+B3[16+i]+B3[24+i]+B3[32+i]+B3[40+i]+B3[48+i]+B3[56+i]) for i in range(8)), 'e4')
    m.addConstrs((A5[i*8]+A5[i*8+1]+A5[i*8+2]+A5[i*8+3]+A5[i*8+4]+A5[i*8+5]+A5[i*8+6]+A5[i*8+7]+B5[i*8]+B5[i*8+1]+B5[i*8+2]+B5[i*8+3]+B5[i*8+4]+B5[i*8+5]+B5[i*8+6]+B5[i*8+7] <= xinlist[n][i]-(A0[i*8]+A0[i*8+1]+A0[i*8+2]+A0[i*8+3]+A0[i*8+4]+A0[i*8+5]+A0[i*8+6]+A0[i*8+7]+B0[i*8]+B0[i*8+1]+B0[i*8+2]+B0[i*8+3]+B0[i*8+4]+B0[i*8+5]+B0[i*8+6]+B0[i*8+7])+(A0[i]+A0[8+i]+A0[16+i]+A0[24+i]+A0[32+i]+A0[40+i]+A0[48+i]+A0[56+i]+B0[i]+B0[8+i]+B0[16+i]+B0[24+i]+B0[32+i]+B0[40+i]+B0[48+i]+B0[56+i])-(A1[i*8]+A1[i*8+1]+A1[i*8+2]+A1[i*8+3]+A1[i*8+4]+A1[i*8+5]+A1[i*8+6]+A1[i*8+7]+B1[i*8]+B1[i*8+1]+B1[i*8+2]+B1[i*8+3]+B1[i*8+4]+B1[i*8+5]+B1[i*8+6]+B1[i*8+7])+(A1[i]+A1[8+i]+A1[16+i]+A1[24+i]+A1[32+i]+A1[40+i]+A1[48+i]+A1[56+i]+B1[i]+B1[8+i]+B1[16+i]+B1[24+i]+B1[32+i]+B1[40+i]+B1[48+i]+B1[56+i])-(A2[i*8]+A2[i*8+1]+A2[i*8+2]+A2[i*8+3]+A2[i*8+4]+A2[i*8+5]+A2[i*8+6]+A2[i*8+7]+B2[i*8]+B2[i*8+1]+B2[i*8+2]+B2[i*8+3]+B2[i*8+4]+B2[i*8+5]+B2[i*8+6]+B2[i*8+7])+(A2[i]+A2[8+i]+A2[16+i]+A2[24+i]+A2[32+i]+A2[40+i]+A2[48+i]+A2[56+i]+B2[i]+B2[8+i]+B2[16+i]+B2[24+i]+B2[32+i]+B2[40+i]+B2[48+i]+B2[56+i])-(A3[i*8]+A3[i*8+1]+A3[i*8+2]+A3[i*8+3]+A3[i*8+4]+A3[i*8+5]+A3[i*8+6]+A3[i*8+7]+B3[i*8]+B3[i*8+1]+B3[i*8+2]+B3[i*8+3]+B3[i*8+4]+B3[i*8+5]+B3[i*8+6]+B3[i*8+7])+(A3[i]+A3[8+i]+A3[16+i]+A3[24+i]+A3[32+i]+A3[40+i]+A3[48+i]+A3[56+i]+B3[i]+B3[8+i]+B3[16+i]+B3[24+i]+B3[32+i]+B3[40+i]+B3[48+i]+B3[56+i])-(A4[i*8]+A4[i*8+1]+A4[i*8+2]+A4[i*8+3]+A4[i*8+4]+A4[i*8+5]+A4[i*8+6]+A4[i*8+7]+B4[i*8]+B4[i*8+1]+B4[i*8+2]+B4[i*8+3]+B4[i*8+4]+B4[i*8+5]+B4[i*8+6]+B4[i*8+7])+(A4[i]+A4[8+i]+A4[16+i]+A4[24+i]+A4[32+i]+A4[40+i]+A4[48+i]+A4[56+i]+B4[i]+B4[8+i]+B4[16+i]+B4[24+i]+B4[32+i]+B4[40+i]+B4[48+i]+B4[56+i]) for i in range(8)), 'e5')

    for i in range(64):
        if(i==0):
            goal=(A0[0]+A1[0]+A2[0]+A3[0]+A4[0]+A5[0])*(baselen[0][0]*dis_income+IDL[0][0]*time_income)-(B0[0]+B1[0]+B2[0]+B3[0]+B4[0]+B5[0])*baselen[0][0]*empty_cost
        else:
            goal=goal+(A0[i]+A1[i]+A2[i]+A3[i]+A4[i]+A5[i])*(baselen[i//8][i%8]*dis_income+IDL[i//8][i%8]*time_income)-(B0[i]+B1[i]+B2[i]+B3[i]+B4[i]+B5[i])*baselen[i//8][i%8]*empty_cost

    m.setObjective(goal, GRB.MAXIMIZE)
    m.optimize()
    for v in m.getVars():
        if('B' in v.varName):
            if(int(v.x)!=0):
                print('%s %g' % (v.varName, v.x))
        #print('%s %g' % (v.varName, v.x))
    sum+=float(m.objVal)
    print('ending.............................................................')
print(sum)