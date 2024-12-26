from pyomo.environ import *
from pyomo.opt import SolverFactory
from model import model
import sys
import numpy as np
import matplotlib.pyplot as plt
# import runner_g

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
    
    solver = SolverFactory('glpk')
    if problem_number == '-b':
        model.apply_discount() 
    

    # if problem_number == '-g':
    #     runner_g.g()

    instance = model.create_instance(data=data) 
    #instance.h[2] = 1
    def print_A_B_C(cost):
        print(f"1: {instance.h[1]()}  2: {instance.h[2]()}  Cost: {cost} Rev: {instance.revenue()}")

    #instance.write('model.lp', io_options={'symbolic_solver_labels': True})

#    for cost in range(300,600):
#        cost = cost
#        instance.Price_of_ore_to_alloy = cost
#        solver.solve(instance)
#        print_A_B_C(cost)
#    results = solver.solve(instance)


    
    # instance.Price_of_ore_to_alloy = 0
    # for cost in range(120,600):
    #     instance.contract_cost[1] = 100*cost
    #     solver.solve(instance)
    #     print_A_B_C(cost)
    # results = solver.solve(instance)
    
    
    
    Container_cost_to_be_sent_depot_list=[]
    revenue_changing_Container_cost_to_be_sent_depot_list = []

    for cost in range (100):
        new_cost =  50*cost
        instance.Container_cost_to_be_sent_depot['Main', 'Tehran'] = new_cost
        solver.solve(instance)
        revenue = instance.revenue()
        Container_cost_to_be_sent_depot_list.append(new_cost)
        revenue_changing_Container_cost_to_be_sent_depot_list.append(revenue)
    results = solver.solve(instance)    
        
    Container_cost_to_be_sent_depot_np = np.array(Container_cost_to_be_sent_depot_list)
    revenue_changing_Container_cost_to_be_sent_depot_np = np.array(revenue_changing_Container_cost_to_be_sent_depot_list)


    plt.plot(Container_cost_to_be_sent_depot_np, revenue_changing_Container_cost_to_be_sent_depot_np)
    plt.show()



    # depot_Tehran_min_to_recieve_change_list = []
    # revenue_depend_on_tehran_min_to_recieve = []

    # for capacity  in range (65):
    #     new_capacity = capacity
    #     instance.depots_min_to_receive['Tehran'] = new_capacity
    #     solver.solve(instance)
    #     revenue = instance.revenue()
    #     print(new_capacity)
    #     revenue_depend_on_tehran_min_to_recieve.append(revenue)
    #     depot_Tehran_min_to_recieve_change_list.append(new_capacity)
    # results = solver.solve(instance)    
    
    # depot_Tehran_min_to_recieve_change_np = np.array(depot_Tehran_min_to_recieve_change_list)
    # revenue_depend_on_tehran_max_to_recieve_np = np.array(revenue_depend_on_tehran_min_to_recieve)
    # plt.plot(depot_Tehran_min_to_recieve_change_np, revenue_depend_on_tehran_max_to_recieve_np)
    # plt.show()


    
        











    #instance.display()
    file_name = 'results.yaml'
    try:
        results.write(filename=file_name,format='yaml')
        print(f"results saved in {file_name}")
    except Exception as e:
        print(e)
