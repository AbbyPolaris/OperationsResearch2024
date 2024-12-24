from pyomo.environ import *
from pyomo.opt import SolverFactory
from model import model
import sys
import runner_g

"""
problem_dict={
    '-a':'الف',
    '-b':'ب',
    '-c':'ج',
    '-d':'د',
    '-e':'ه',
    '-f':'و',
    '-g':'ز',
    '-h':'ح',
    '-i':'ط',
}
"""

if __name__ == "__main__":

    try:
        problem_number = sys.argv[1]
    except:
        problem_number = '-a'

    if not problem_number in ['-a','-b','-c','-d','-e','-f','-g','-h','-i']:
        sys.exit(0)

    print(f"results for problem: {problem_number}")
    data = DataPortal()
    data.load(filename='params.dat')    
    instance = model.create_instance(data=data) 
    instance.write('model.lp', io_options={'symbolic_solver_labels': True})
    solver = SolverFactory('glpk')
    
    if problem_number == '-g':
        pass#runner_g.g(instance=instance)

    if problem_number == '-b':
        model.apply_discount()  
    if problem_number in ['-a','-b']:
        results = solver.solve(instance)
        print(results)
    instance.display()
    file_name = 'results.yaml'
    try:
        results.write(filename=file_name,format='yaml')
        print(f"results saved in {file_name}")
    except Exception as e:
        print(e)
