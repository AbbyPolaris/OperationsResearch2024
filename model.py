from pyomo.environ import *
infinity = float('inf')
model = AbstractModel(name='OR1')

model.Ore = Set()
model.Alloys = Set()
model.Metals = Set()
model.Factories = Set()
model.Depots = Set()
model.Markets = Set()

#parameters
M = 999999999
epsilon = 1e-9
model.discount_percentage = 0.05

#model parameters
model.min_buy_fac = Param(model.Factories,within=NonNegativeReals, default=0.0)
model.max_buy_fac = Param(model.Factories,within=NonNegativeReals, default=infinity)
model.discount_margin = Param(model.Factories, within=NonNegativeReals, default=infinity)
model.contract_cost = Param(model.Factories,within= NonNegativeReals, mutable=True)
model.A_comb_min = Param(model.Metals, within=NonNegativeReals, default=0.0)
model.A_comb_max = Param(model.Metals, within=NonNegativeReals, default=infinity)
model.B_comb_min = Param(model.Metals, within=NonNegativeReals, default=0.0)
model.B_comb_max = Param(model.Metals, within=NonNegativeReals, default=infinity)
model.price_of_alloy_fac = Param(model.Factories, model.Alloys, within=NonNegativeReals,mutable=True)
model.Price_of_ore_to_alloy= Param(within=NonNegativeReals,mutable=True)
model.Max_ore = Param(model.Ore,within=NonNegativeReals, mutable = True)
model.Ore_cost = Param(model.Ore,within=NonNegativeReals, mutable=True)
model.Ore_combination = Param(model.Ore, model.Metals, within=NonNegativeReals)
model.container_cap = Param(within= NonNegativeIntegers, mutable=True)
model.Container_min_to_be_sent_depot = Param(model.Factories, model.Depots, within=NonNegativeIntegers)
model.Container_Max_to_be_sent_depot = Param(model.Factories, model.Depots, within=NonNegativeIntegers)
model.Container_cost_to_be_sent_depot = Param(model.Factories, model.Depots , within=NonNegativeReals, mutable=True)
model.depots_min_to_receive = Param(model.Depots, within=NonNegativeIntegers, mutable=True)
model.depots_Max_to_receive = Param(model.Depots, within=NonNegativeIntegers)
model.Container_min_to_be_sent_market = Param(model.Depots, model.Markets, within= NonNegativeIntegers)
model.Container_Max_to_be_sent_market = Param(model.Depots, model.Markets, within= NonNegativeIntegers)
model.Container_cost_to_be_sent_market = Param(model.Depots ,model.Markets, within= NonNegativeReals, mutable=True)
model.Max_market_demand = Param(model.Markets,model.Alloys, within= NonNegativeReals)
model.Market_price = Param(model.Markets , model.Alloys , within= NonNegativeReals)

#variables
model.Z = Var(model.Ore,model.Alloys, within=NonNegativeReals)
model.F = Var(model.Ore,model.Alloys, within=NonNegativeReals)
model.A = Var(model.Ore,model.Alloys, within=NonNegativeReals)
model.C = Var(model.Ore,model.Alloys, within=NonNegativeReals) 
model.U = Var(model.Alloys,within=NonNegativeReals)
model.t = Var(model.Alloys,model.Factories,model.Depots, within=NonNegativeReals)
model.Extracted_ore = Var(model.Ore,within=NonNegativeReals) # defined as S in the report
model.h = Var(model.Factories,within= Binary)
model.B = Var(model.Factories, model.Depots, within=NonNegativeIntegers)
model.g = Var(model.Alloys, model.Depots, model.Markets, within=NonNegativeReals)
model.G = Var(model.Depots, model.Markets, within= NonNegativeIntegers)
model.l = Var(model.Depots, model.Markets, within= Binary)
model.d = Var([1,2], within= Binary) #added for -b
model.R = Var(model.Alloys,[1,2], within= NonNegativeReals, initialize=0) #added for -b

#rule for maximum extraction of ore.
def Max_extracted_ore_rule(model,i):
    return model.Extracted_ore[i] <= model.Max_ore[i]
model.Max_extracted_ore_limit = Constraint(model.Ore,rule=Max_extracted_ore_rule)

#alloy weight is sum of metals weights in it.
def Alloy_sum_rule(model,j):
    return model.U[j] <= sum(model.Z[i,j] for i in model.Ore)+\
                         sum(model.C[i,j] for i in model.Ore)+\
                         sum(model.A[i,j] for i in model.Ore)+\
                         sum(model.F[i,j] for i in model.Ore)
model.Alloy_sum_limit = Constraint(model.Alloys,rule=Alloy_sum_rule)

#metals in alloys should be less than(or equal to) extracted metals from Ore.
def Metal_sum_rule_Z(model,i):
    return sum(model.Z[i,j] for j in model.Alloys) <= model.Extracted_ore[i]*model.Ore_combination[i,'Zinc']
model.Metal_sum_limit_Z = Constraint(model.Ore,rule=Metal_sum_rule_Z)

def Metal_sum_rule_F(model,i):
    return sum(model.F[i,j] for j in model.Alloys) <= model.Extracted_ore[i]*model.Ore_combination[i,'Iron']
model.Metal_sum_limit_F = Constraint(model.Ore,rule=Metal_sum_rule_F)

def Metal_sum_rule_C(model,i):
    return sum(model.C[i,j] for j in model.Alloys) <= model.Extracted_ore[i]*model.Ore_combination[i,'Copper']
model.Metal_sum_limit_C = Constraint(model.Ore,rule=Metal_sum_rule_C)

def Metal_sum_rule_A(model,i):
    return sum(model.A[i,j] for j in model.Alloys) <= model.Extracted_ore[i]*model.Ore_combination[i,'Aluminum']
model.Metal_sum_limit_A = Constraint(model.Ore,rule=Metal_sum_rule_A)

#percentage of metals in alloys limitations. f is bottom limit and t is top limit.
def Metal_in_alloy_rule_A_Z_f(model):
    value = sum(model.Z[i,'A'] for i in model.Ore)
    return model.A_comb_min['Zinc']*model.U['A']<=value
model.Metal_in_alloy_limit_A_Z_f = Constraint(rule=Metal_in_alloy_rule_A_Z_f)
def Metal_in_alloy_rule_A_Z_t(model):
    value = sum(model.Z[i,'A'] for i in model.Ore)
    return value<=model.A_comb_max['Zinc']*model.U['A']
model.Metal_in_alloy_limit_A_Z_t = Constraint(rule=Metal_in_alloy_rule_A_Z_t)

def Metal_in_alloy_rule_A_C_f(model):
    value = sum(model.C[i,'A'] for i in model.Ore)
    return model.A_comb_min['Copper']*model.U['A']<=value
model.Metal_in_alloy_limit_A_C_f = Constraint(rule=Metal_in_alloy_rule_A_C_f)
def Metal_in_alloy_rule_A_C_t(model):
    value = sum(model.C[i,'A'] for i in model.Ore)
    return value<=model.A_comb_max['Copper']*model.U['A']
model.Metal_in_alloy_limit_A_C_t = Constraint(rule=Metal_in_alloy_rule_A_C_t)

def Metal_in_alloy_rule_A_A_f(model):
    value = sum(model.A[i,'A'] for i in model.Ore)
    return model.A_comb_min['Aluminum']*model.U['A']<=value
model.Metal_in_alloy_limit_A_A_f = Constraint(rule=Metal_in_alloy_rule_A_A_f)
def Metal_in_alloy_rule_A_A_t(model):
    value = sum(model.A[i,'A'] for i in model.Ore)
    return value<=model.A_comb_max['Aluminum']*model.U['A']
model.Metal_in_alloy_limit_A_A_t = Constraint(rule=Metal_in_alloy_rule_A_A_t)

def Metal_in_alloy_rule_A_F_f(model):
    value = sum(model.F[i,'A'] for i in model.Ore)
    return model.A_comb_min['Iron']*model.U['A']<=value
model.Metal_in_alloy_limit_A_F_f = Constraint(rule=Metal_in_alloy_rule_A_F_f)
def Metal_in_alloy_rule_A_F_t(model):
    value = sum(model.F[i,'A'] for i in model.Ore)
    return value<=model.A_comb_max['Iron']*model.U['A']
model.Metal_in_alloy_limit_A_F_t = Constraint(rule=Metal_in_alloy_rule_A_F_t)

def Metal_in_alloy_rule_B_Z_f(model):
    value = sum(model.Z[i,'B'] for i in model.Ore)
    return model.B_comb_min['Zinc']*model.U['B']<=value
model.Metal_in_alloy_limit_B_Z_f = Constraint(rule=Metal_in_alloy_rule_B_Z_f)
def Metal_in_alloy_rule_B_Z_t(model):
    value = sum(model.Z[i,'B'] for i in model.Ore)
    return value<=model.B_comb_max['Zinc']*model.U['B']
model.Metal_in_alloy_limit_B_Z_t = Constraint(rule=Metal_in_alloy_rule_B_Z_t)

def Metal_in_alloy_rule_B_C_f(model):
    value = sum(model.C[i,'B'] for i in model.Ore)
    return model.B_comb_min['Copper']*model.U['B']<=value
model.Metal_in_alloy_limit_B_C_f = Constraint(rule=Metal_in_alloy_rule_B_C_f)
def Metal_in_alloy_rule_B_C_t(model):
    value = sum(model.C[i,'B'] for i in model.Ore)
    return value<=model.B_comb_max['Copper']*model.U['B']
model.Metal_in_alloy_limit_B_C_t = Constraint(rule=Metal_in_alloy_rule_B_C_t)

def Metal_in_alloy_rule_B_A_f(model):
    value = sum(model.A[i,'B'] for i in model.Ore)
    return model.B_comb_min['Aluminum']*model.U['B']<=value
model.Metal_in_alloy_limit_B_A_f = Constraint(rule=Metal_in_alloy_rule_B_A_f)
def Metal_in_alloy_rule_B_A_t(model):
    value = sum(model.A[i,'B'] for i in model.Ore)
    return value<=model.B_comb_max['Aluminum']*model.U['B']
model.Metal_in_alloy_limit_B_A_t = Constraint(rule=Metal_in_alloy_rule_B_A_t)

def Metal_in_alloy_rule_B_F_f(model):
    value = sum(model.F[i,'B'] for i in model.Ore)
    return model.B_comb_min['Iron']*model.U['B']<=value
model.Metal_in_alloy_limit_B_F_f = Constraint(rule=Metal_in_alloy_rule_B_F_f)
def Metal_in_alloy_rule_B_F_t(model):
    value = sum(model.F[i,'B'] for i in model.Ore)
    return value<=model.B_comb_max['Iron']*model.U['B']
model.Metal_in_alloy_limit_B_F_t = Constraint(rule=Metal_in_alloy_rule_B_F_t)

#exported alloy from main fac should be less than (or equal to)  
def Export_from_main_fac_rule(model,i):
    return model.U[i] >= sum(model.t[i,'Main',k] for k in model.Depots)
model.Export_from_main_fac_limit = Constraint(model.Alloys,rule=Export_from_main_fac_rule)

#limits of buying from factories.
def buy_from_fac_rule_f(model,i):
    value = sum(sum(model.t[j,i,k] for k in model.Depots)\
                                                for j in model.Alloys)
    return model.min_buy_fac[i]*model.h[i]<=value
model.buy_from_fac_limit_f= Constraint([1,2],rule=buy_from_fac_rule_f)
def buy_from_fac_rule_t(model,i):
    value = sum(sum(model.t[j,i,k] for k in model.Depots)\
                                                for j in model.Alloys)
    return value<=model.max_buy_fac[i]*model.h[i]
model.buy_from_fac_limit_t= Constraint([1,2],rule=buy_from_fac_rule_t)

#limit for Alloys in one container from fac to depot.
def container_rule(model,i,j):
    return sum(model.t[a,i,j] for a in model.Alloys) <= model.B[i,j]*model.container_cap
model.container_limit = Constraint(model.Factories, model.Depots, rule=container_rule)

#limit for transporting from fac to depots No1.#TODO correction
def transportation_rule_t(model,i,j):
    return model.B[i,j]<= model.Container_Max_to_be_sent_depot[i,j]*model.h[i]
model.transportation_limit_t = Constraint(model.Factories,model.Depots, rule= transportation_rule_t)
def transportation_rule_f(model,i,j):
    return model.Container_min_to_be_sent_depot[i,j]*model.h[i]<=model.B[i,j]
model.transportation_limit_f = Constraint(model.Factories,model.Depots, rule= transportation_rule_f)

#limit for transporting from fac to depots No2.
def transportation_rule2(model,j):
    return inequality(model.depots_min_to_receive[j],sum(model.B[i,j] for i in model.Factories),\
                      model.depots_Max_to_receive[j])
model.transportation_limit2 = Constraint(model.Depots,rule= transportation_rule2)


#limit for transporting from depots to markets.
def transp_from_dep_to_market_rule(model,i,k):
    return sum(model.t[i,j,k] for j in model.Factories) >= sum(model.g[i,k,l] for l in model.Markets)
model.transp_from_dep_to_market_limit = Constraint(model.Alloys,model.Depots,\
                                                rule= transp_from_dep_to_market_rule)

#limits for Alloys in containers transporting from depots to markets

##TODO empty containers can be sent!!!
def container_rule2(model,i,j):
    return sum(model.g[l,i,j] for l in model.Alloys) <= model.G[i,j]*model.container_cap
model.container_limit2 = Constraint(model.Depots, model.Markets, rule=container_rule2)

#limit for containers to be sent to markets.
def market_sell_rule_f(model,i,j):
    return model.Container_min_to_be_sent_market[i,j]*model.l[i,j]<=model.G[i,j]
model.market_sell_limit_f = Constraint(model.Depots,model.Markets, rule= market_sell_rule_f)
def market_sell_rule_t(model,i,j):
    return model.G[i,j]<=model.Container_min_to_be_sent_market[i,j]*model.l[i,j]
model.market_sell_limit_t = Constraint(model.Depots,model.Markets, rule= market_sell_rule_t)

#maximum market demands.
def max_market_demand_rule(model,k,i):
    return sum(model.g[i,j,k] for j in model.Depots) <= model.Max_market_demand[k,i]
model.max_market_demand_limit = Constraint(model.Markets, model.Alloys, rule= max_market_demand_rule)

def revenue_rule_no_discount(model):
    return sum(sum(model.Market_price[m,j]*sum(model.g[j,k,m] for k in model.Depots) for j in model.Alloys) for m in model.Markets)-\
           sum(model.Extracted_ore[i]*model.Ore_cost[i] for i in model.Ore)-\
           sum(model.U[u]*model.Price_of_ore_to_alloy for u in model.Alloys)-\
           sum(sum(model.price_of_alloy_fac[u,j]*sum(model.t[j,u,k] for k in model.Depots) for j in model.Alloys) for u in model.Factories)-\
           sum(model.h[u]*model.contract_cost[u] for u in model.Factories)-\
           sum(sum(model.Container_cost_to_be_sent_depot[i,j]*model.B[i,j] for j in model.Depots) for i in model.Factories)-\
           sum(sum(model.G[i,j]*model.Container_cost_to_be_sent_market[i,j] for j in model.Markets) for i in model.Depots)

#added for -b
model.revenue = Objective(rule=revenue_rule_no_discount, sense=maximize)

def discount_rule_1(model,u):
    return sum(sum(model.t[j,u,k] for j in model.Alloys) for k in model.Depots)+epsilon <= model.d[u]*model.discount_margin[u] +\
                                                                                  model.discount_margin[u]

def discount_rule_2(model,u):
    return sum(sum(model.t[j,u,k] for j in model.Alloys) for k in model.Depots) >= model.discount_margin[u]*model.d[u]

def discount_rule_3(model,u,j):
    return sum(model.t[j,u,k] for k in model.Depots) >= model.R[j,u]

def discount_rule_4(model,u):
    return sum(model.R[j,u] for j in model.Alloys) <= model.d[u]*M


#added for Abadan
def Abadan_G_rule(model,i):
    return model.containers_to_Abadan[i]*model.container_cap >= sum(model.Abadan_Alloys[i,j] for j in model.Alloys)

def transp_from_dep_to_market_rule_abadan_added(model,i,k):
    return sum(model.t[i,j,k] for j in model.Factories) >= sum(model.g[i,k,l] for l in model.Markets)+model.Abadan_Alloys[k,i]

def revenue_Abadan_added(model):
        return sum(sum(model.Market_price[m,j]*sum(model.g[j,k,m] for k in model.Depots) for j in model.Alloys) for m in model.Markets)-\
           sum(model.Extracted_ore[i]*model.Ore_cost[i] for i in model.Ore)-\
           sum(model.U[u]*model.Price_of_ore_to_alloy for u in model.Alloys)-\
           sum(sum(model.price_of_alloy_fac[u,j]*sum(model.t[j,u,k] for k in model.Depots) for j in model.Alloys) for u in model.Factories)-\
           sum(model.h[u]*model.contract_cost[u] for u in model.Factories)-\
           sum(sum(model.Container_cost_to_be_sent_depot[i,j]*model.B[i,j] for j in model.Depots) for i in model.Factories)-\
           sum(sum(model.G[i,j]*model.Container_cost_to_be_sent_market[i,j] for j in model.Markets) for i in model.Depots)+\
           sum(sum(model.discount_percentage*model.R[j,u]*model.price_of_alloy_fac[u,j] for u in [1,2]) for j in model.Alloys)+\
           sum(sum(model.Abadan_Alloys[i,j] for i in model.Depots)*model.sell_prices_Abadan[j] for j in model.Alloys)-\
           sum(model.containers_to_Abadan[i]*model.cost_to_Abadan[i] for i in model.Depots)

def revenue_rule_discount_added(model):
    return sum(sum(model.Market_price[m,j]*sum(model.g[j,k,m] for k in model.Depots) for j in model.Alloys) for m in model.Markets)-\
           sum(model.Extracted_ore[i]*model.Ore_cost[i] for i in model.Ore)-\
           sum(model.U[u]*model.Price_of_ore_to_alloy for u in model.Alloys)-\
           sum(sum(model.price_of_alloy_fac[u,j]*sum(model.t[j,u,k] for k in model.Depots) for j in model.Alloys) for u in model.Factories)-\
           sum(model.h[u]*model.contract_cost[u] for u in model.Factories)-\
           sum(sum(model.Container_cost_to_be_sent_depot[i,j]*model.B[i,j] for j in model.Depots) for i in model.Factories)-\
           sum(sum(model.G[i,j]*model.Container_cost_to_be_sent_market[i,j] for j in model.Markets) for i in model.Depots)+\
           sum(sum(model.discount_percentage*model.R[j,u]*model.price_of_alloy_fac[u,j] for u in [1,2]) for j in model.Alloys)

def apply_Abadan_rule():
    cost_data = {'Tehran':120,
                 'Isfahan':110}
  
    model.add_component('containers_to_Abadan',Var(model.Depots,within= NonNegativeIntegers))
    model.add_component('Abadan_Alloys',Var(model.Depots,model.Alloys,within= NonNegativeReals))
    model.add_component('sell_prices_Abadan',Param(model.Alloys, within=NonNegativeReals,default=0,mutable=True))
    model.add_component('cost_to_Abadan',Param(model.Depots,initialize=cost_data, within=NonNegativeReals))   
    model.Abadan_G_limit = Constraint(model.Depots,rule=Abadan_G_rule)
    model.transp_from_dep_to_market_Abadan_added_limit = Constraint(model.Alloys,model.Depots,\
                                                rule= transp_from_dep_to_market_rule_abadan_added)
    model.del_component('revenue')
    model.add_component('revenue',Objective(rule=revenue_Abadan_added, sense=maximize))

def apply_discount_rule():
    model.discount_limit_1 = Constraint([1,2],rule=discount_rule_1)
    model.discount_limit_2 = Constraint([1,2],rule=discount_rule_2)
    model.discount_limit_3 = Constraint([1,2],model.Alloys,rule=discount_rule_3)
    model.discount_limit_4 = Constraint([1,2],rule=discount_rule_4)
    model.del_component('revenue')
    model.add_component('revenue',Objective(rule=revenue_rule_discount_added, sense=maximize))

model.apply_discount = apply_discount_rule
model.apply_Abadan = apply_Abadan_rule