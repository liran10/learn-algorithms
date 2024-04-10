from gurobipy import *
import pandas as pd
import numpy as np

Nodes=['1','2','3','4','5','6','7']
Arcs={
      ('1','2'):15,
      ('1','4'):25,
      ('1','3'):45,
      ('2','5'):30,
      ('2','4'):2,
      ('4','7'):50,
      ('4','3'):2,
      ('3','6'):25,
      ('5','7'):2,
      ('6','7'):1
      }
model=Model('dual problem')
'''添加决策变量'''
X={}
for key in Arcs.keys():
      index='x_'+key[0]+','+key[1]
      X[key]=model.addVar(vtype=GRB.BINARY,name=index)

'''添加目标函数'''
obj=LinExpr(0)
for key in Arcs.keys():
      obj.addTerms(Arcs[key],X[key])

model.setObjective(obj,GRB.MINIMIZE)

'''约束1、约束2'''
lhs_1=LinExpr(0)
lhs_2=LinExpr(0)
for key in Arcs.keys():
      if key[0]=='1':
            lhs_1.addTerms(1,X[key])
      elif key[1]=='7':
            lhs_2.addTerms(1,X[key])
model.addConstr(lhs_1==1,name='start flow')
model.addConstr(lhs_2==1,name='end flow')

'''约束3'''
for node in Nodes:
      lhs=LinExpr(0)
      if node !='1' and node !='7':
            for key in Arcs.keys():
                  if key[1] ==node:
                        lhs.addTerms(1,X[key])
                  elif key[0] ==node:
                        lhs.addTerms(-1,X[key])
      model.addConstr(lhs == 0, name='flow conservation')

model.write('model_spp.lp')
model.optimize()

print('Objective:',model.Objval)
for var in model.getVars():
      if var.x>0:
            print(var.varname,'\t',var.x)