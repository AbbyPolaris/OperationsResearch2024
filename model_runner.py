from pyomo.environ import *
from pyomo.opt import SolverFactory
from model import model


if __name__ == "__main__":
    data = DataPortal()
    data.load(filename='/home/abby/OR_project/params.dat')
    instance = model.create_instance(data=data)
    #instance.pprint()
    solver = SolverFactory('glpk')
    results = solver.solve(instance)
    instance.display()
