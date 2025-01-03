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
        for cost in range(1100, 1300):
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
        

    def h():
        # Increase all prices
        instance = model.create_instance(data=data) 
        solver.solve(instance)
        previous_revenue = instance.revenue()
        print(previous_revenue)
        factories_list = instance.Factories
        depots_list = instance.Depots
        Markets_list = instance.Markets

        for factory in factories_list:
            for depot in depots_list:
                instance.Container_cost_to_be_sent_depot[factory, depot] = 110 / 100 * instance.Container_cost_to_be_sent_depot[factory, depot]()

        for depot in depots_list:
            for market in Markets_list:
                instance.Container_cost_to_be_sent_market[depot, market] = 110 / 100 * instance.Container_cost_to_be_sent_market[depot, market]()

        solver.solve(instance)
        new_revenue = instance.revenue()
        print(f'For a 10% increase in costs, previous revenue is {previous_revenue} and new revenue is {new_revenue}')

        # Decrease all prices
        instance = model.create_instance(data=data) 
        solver.solve(instance)
        previous_revenue = instance.revenue()

        for factory in factories_list:
            for depot in depots_list:
                instance.Container_cost_to_be_sent_depot[factory, depot] = (90 / 100) * instance.Container_cost_to_be_sent_depot[factory, depot]()

        for depot in depots_list:
            for market in Markets_list:
                instance.Container_cost_to_be_sent_market[depot, market] = (90 / 100) * instance.Container_cost_to_be_sent_market[depot, market]()

        solver.solve(instance)
        new_revenue = instance.revenue()
        print(f'For a 10% reduction in costs, previous revenue is {previous_revenue} and new revenue is {new_revenue}')

    def h_1():
        # Single price analysis: shipping from factory 1 to depot Isfahan
        instance = model.create_instance(data=data) 
        Container_cost_to_be_sent_1_to_Isfahan = []
        revenue_changing_Container_cost_to_be_sent_1_to_Isfahan = []

        the_least_cost = instance.Container_cost_to_be_sent_depot[1, 'Isfahan']() * (90 / 100)
        cost_step = instance.Container_cost_to_be_sent_depot[1, 'Isfahan']() / 100

        for cost in range(21):
            new_cost = cost * cost_step + the_least_cost
            instance.Container_cost_to_be_sent_depot[1, 'Isfahan'] = new_cost
            solver.solve(instance)
            revenue = instance.revenue()
            Container_cost_to_be_sent_1_to_Isfahan.append(new_cost)
            revenue_changing_Container_cost_to_be_sent_1_to_Isfahan.append(revenue)

        Container_cost_to_be_sent_1_to_Isfahan_np = np.array(Container_cost_to_be_sent_1_to_Isfahan)
        revenue_changing_Container_cost_to_be_sent_1_to_isfahan_np = np.array(revenue_changing_Container_cost_to_be_sent_1_to_Isfahan)
        plt.xlabel("Container transp. cost, Fac1->Isfahan")
        plt.ylabel("Revenue")
        plt.plot(Container_cost_to_be_sent_1_to_Isfahan_np, revenue_changing_Container_cost_to_be_sent_1_to_isfahan_np)
        plt.show()

    def h_2():
        # Single price analysis: shipping from depot Isfahan to Mashhad
        instance = model.create_instance(data=data) 
        Container_cost_to_be_sent_isfahan_to_mashhad = []
        revenue_changing_Container_cost_to_be_sent_isfahan_to_mashhad = []

        the_least_cost = instance.Container_cost_to_be_sent_market['Isfahan', 'Mashhad']() * (90 / 100)
        cost_step = instance.Container_cost_to_be_sent_market['Isfahan', 'Mashhad']() / 100

        for cost in range(21):
            new_cost = cost * cost_step + the_least_cost
            instance.Container_cost_to_be_sent_market['Isfahan', 'Mashhad'] = new_cost
            solver.solve(instance)
            revenue = instance.revenue()
            Container_cost_to_be_sent_isfahan_to_mashhad.append(new_cost)
            revenue_changing_Container_cost_to_be_sent_isfahan_to_mashhad.append(revenue)

        Container_cost_to_be_sent_Isfahan_to_mashhad_np = np.array(Container_cost_to_be_sent_isfahan_to_mashhad)
        revenue_changing_Container_cost_to_be_sent_isfahan_to_mashhad_np = np.array(revenue_changing_Container_cost_to_be_sent_isfahan_to_mashhad)
        plt.xlabel("Container transp. cost, Isfahan->Mashhad")
        plt.ylabel("Revenue")
        plt.plot(Container_cost_to_be_sent_Isfahan_to_mashhad_np, revenue_changing_Container_cost_to_be_sent_isfahan_to_mashhad_np)
        plt.show()

    
    if problem_number == '-h':
        h()
        h_1()
        h_2()

    def i():
        instance.containers_to_Abadan = Var(instance.Depots,within= NonNegativeIntegers)
        instance.Abadan_Alloys = Var(instance.Depots,instance.Alloys,within= NonNegativeReals)
        cost_data = {'Tehran':120,
                     'Isfahan':110}
        instance.cost_to_Abadan = Param(instance.Depots,initialize=cost_data, within=NonNegativeReals)
        def Abadan_G_rule(instance,i):
            return instance.containers_to_Abadan[i]*instance.container_cap >= sum(instance.Abadan_Alloys[i,j] for j in instance.Alloys)
        
        instance.Abadan_limit_G = Constraint(instance.Depots,rule=Abadan_G_rule)
        def Abadan_Q_rule(instance,i):
            return  sum(instance.Abadan_Alloys[i,j] for j in instance.Alloys)>= 10000
        
        instance.Abadan_limit_Q = Constraint(instance.Depots,rule=Abadan_Q_rule)
        instance.sell_prices_Abadan = Param(instance.Alloys, within=NonNegativeReals,default=0.0,mutable=True)
        instance.apply_Abadan()
        for p in range(200,10000,1000):
            instance.sell_prices_Abadan['A'] = p
            solver.solve(instance)
            print(instance.revenue())
            print(f"Price of A: {p}, Sell A? {(instance.Abadan_Alloys['Isfahan','A']())}")
        instance.sell_prices_Abadan['A'] = 0
        for p in range(200,10000,1000):
            instance.sell_prices_Abadan['B'] = p
            solver.solve(instance)
            print(f"Price of B: {p}, Sell B? {sum(instance.Abadan_Alloys[i,'B']() for i in instance.Depots)}")

    if problem_number == '-i':
        i()


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


