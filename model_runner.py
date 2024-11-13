from pyomo.environ import *
from pyomo.opt import SolverFactory
from model import model


if __name__ == "__main__":
    data = DataPortal()
    data.load(filename='params.dat')
    instance = model.create_instance(data=data)
    solver = SolverFactory('glpk')
    results = solver.solve(instance)
    instance.display()
    results.write(filename='results.yaml',format='yaml')
