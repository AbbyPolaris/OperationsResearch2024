from pyomo.environ import *
from pyomo.opt import SolverFactory
from model import model
import sys
import numpy as np
import matplotlib.pyplot as plt
from plotly import graph_objects as go


def g(instance):
    solver = SolverFactory('glpk')
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
