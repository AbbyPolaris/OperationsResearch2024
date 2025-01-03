from pyomo.environ import *
from pyomo.opt import SolverFactory
from model import model
import sys
import numpy as np
import matplotlib.pyplot as plt
from plotly import graph_objects as go

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
        model.apply_discount()

    #if not problem_number in ['-a','-b','-c','-d','-e','-f','-g','-h','-i']:
    #   sys.exit(0)

    print(f"results for problem: {problem_number}")
    data = DataPortal()
    data.load(filename='params.dat')    

    if problem_number != '-a':
        model.apply_discount() 

    instance = model.create_instance(data=data) 
    instance.write('model.lp', io_options={'symbolic_solver_labels': True})
    solver = SolverFactory('glpk')
    reserved_dmtrTehran = 20

    def d():
        for cost in range(300, 400):
            instance.Price_of_ore_to_alloy = cost
            solver.solve(instance)
            print(f"Price of ore to alloy: {instance.Price_of_ore_to_alloy()}, Use Main?: {instance.h['Main']()}")

    if problem_number == '-d':
        d()



    def e():
        instance.Price_of_ore_to_alloy = 0
        for cost in range(900, 1050):
            instance.contract_cost[1] = 100 * cost
            solver.solve(instance)
            print(f"Fac1 contract cost: {instance.contract_cost[1]()}, Buy from Fac1: {instance.h[1]()}, Buy from Fac2: {instance.h[2]()}")

    if problem_number == '-e':
        e()


    def g_2():
        depot_Tehran_min_to_recieve_change_list = []
        revenue_depend_on_tehran_min_to_recieve = []

        for capacity in range(20,65):
            instance.depots_min_to_receive['Tehran'] = capacity
            solver.solve(instance)
            revenue = instance.revenue()
            print(f"Tehran minimum receive: {capacity}, Revenue {instance.revenue()}, buy from Fac2: {instance.h[2]()}") 
            revenue_depend_on_tehran_min_to_recieve.append(revenue)
            depot_Tehran_min_to_recieve_change_list.append(capacity)
        depot_Tehran_min_to_recieve_change_np = np.array(depot_Tehran_min_to_recieve_change_list)
        revenue_depend_on_tehran_max_to_recieve_np = np.array(revenue_depend_on_tehran_min_to_recieve)

        plt.xlabel("Tehran minimum receive")
        plt.ylabel("Revenue")
        plt.plot(depot_Tehran_min_to_recieve_change_np, revenue_depend_on_tehran_max_to_recieve_np)
        plt.show()

    def g_3():
        Container_cost_to_be_sent_depot_list=[]
        revenue_changing_Container_cost_to_be_sent_depot_list = []

        for cost in range (100):
            new_cost =  50*cost
            instance.Container_cost_to_be_sent_depot['Main', 'Tehran'] = new_cost
            solver.solve(instance)
            revenue = instance.revenue()
            print(f"Container cost from Main to Tehran: {new_cost}, Revenue{instance.revenue()}")
            Container_cost_to_be_sent_depot_list.append(new_cost)
            revenue_changing_Container_cost_to_be_sent_depot_list.append(revenue)
            
        Container_cost_to_be_sent_depot_np = np.array(Container_cost_to_be_sent_depot_list)
        revenue_changing_Container_cost_to_be_sent_depot_np = np.array(revenue_changing_Container_cost_to_be_sent_depot_list)


        plt.plot(Container_cost_to_be_sent_depot_np, revenue_changing_Container_cost_to_be_sent_depot_np)

        plt.xlabel("Container cost Main->Tehran")
        plt.ylabel("Revenue")
        plt.show()

    def g():
        price_of_alloy_fac_2_alloy_b_set = np.arange(0,(instance.price_of_alloy_fac[2,'B']())*3,1)#for c
        max_ore_2_set = np.arange(0,(instance.Max_ore[2]()),100)#for b
        object = np.zeros(shape=(len(price_of_alloy_fac_2_alloy_b_set),len(max_ore_2_set)))
        for i,V1 in enumerate(price_of_alloy_fac_2_alloy_b_set):
            for j,V2 in enumerate(max_ore_2_set):
                instance.price_of_alloy_fac[2,'B'] = V1
                instance.Max_ore[2] = V2
                solver.solve(instance)
                object[i,j] = instance.revenue()

        fig = go.Figure(data=[go.Surface(z=object, x=max_ore_2_set, y=price_of_alloy_fac_2_alloy_b_set)])
        fig.update_layout(title='3D Surface Plot', autosize=True,
                        scene=dict(
                            xaxis_title='maximum of extractable ore number 2',
                            yaxis_title='price of alloy b from factory 2',
                            zaxis_title='Object'))
        fig.show()
        plt.show()#?

    if problem_number == '-g':
        #g()
        g_2()
        g_3()
        

    if problem_number in ['-a','-b']:
        results = solver.solve(instance)
        print(results)
        instance.display()
    result_file_name = 'results.yaml'
    try:
        results.write(filename=result_file_name,format='yaml')
        print(f"results saved in {result_file_name}")
    except Exception as e:
        print(f"no results saved.")


