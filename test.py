from pyomo.environ import *
from pyomo.opt import SolverFactory
import numpy as np
# load data
products = ['Doors', 'Windows']
plants = ['Plant1', 'Plant2', 'Plant3']
profit_rate_list = [3, 5]
hours_avail_list = [4, 12, 18]
hours_per_batch_list = [[1, 0], [0, 2], [3, 2]]

# parse lists into dictionaries
profit_rate = dict(zip(products, profit_rate_list))
hours_available = dict(zip(plants, hours_avail_list))
hours_per_batch = {
    pl: {pr: hours_per_batch_list[i][j] for j, pr in enumerate(products)}
    for i, pl in enumerate(plants)
}


### MODEL CONSTRUCTION ###
# Declaration
model = ConcreteModel()

# Decision Variables
model.weekly_prod = Var(products, domain=NonNegativeReals)

# Objective
model.profit = Objective(
    expr=sum(profit_rate[pr] * model.weekly_prod[pr] for pr in products),
    sense=maximize,
)

# Constraints
model.capacity = ConstraintList()
for pl in plants:
    model.capacity.add(
        sum(hours_per_batch[pl][pr] * model.weekly_prod[pr] for pr in products)
        <= hours_available[pl]
    )

### SOLUTION ###
solver = SolverFactory('glpk')
solver.solve(model)

### OUTPUT ###

# note that we're using f-strings for output here which is a little different and cleaner than in the video
print(f"Maximum Profit = ${1000*model.profit():,.2f}")
for j in products:
    print(f"Batches of {j} = {model.weekly_prod[j]():.1f}")

model.write('model.lp', io_options={'symbolic_solver_labels': True})
