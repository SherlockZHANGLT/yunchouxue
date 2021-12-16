import gurobipy as gb
from gurobipy import GRB
# Parameters
Demand = [5, 6, 10, 7, 4, 6]
# Model formulation
m = gb.Model('Question1')
xi = m.addVars(6, lb=0, vtype=GRB.INTEGER, name='xi')
m.addConstrs((xi[i]+xi[(i+5)%6] >= Demand[i] for i in range(6)), 'c1')
m.setObjective(xi[0]+xi[1]+xi[2]+xi[3]+xi[4]+xi[5], GRB.MINIMIZE)
m.optimize()
for v in m.getVars():
    print('%s %g' % (v.varName, v.x))
print('Obj: %g' % m.objVal)