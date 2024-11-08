from pyomo.environ import *
import constants
infinity = float('inf')
model = AbstractModel()

model.Metals = Set()
model.Ore = Set()
model.Alloys = Set()
model.Factories = Set()
model.Depots = Set()
model.Markets = Set()

container_cap = constants.container_cap
#parameters
model.A_comb_min = Param(model.Metals, within=NonNegativeReals, default=0.0)
model.A_comb_max = Param(model.Metals, within=NonNegativeReals, default=infinity)
model.B_comb_min = Param(model.Metals, within=NonNegativeReals, default=0.0)
model.B_comb_max = Param(model.Metals, within=NonNegativeReals, default=infinity)
model.min_buy_fac = Param(model.Factories,within=NonNegativeReals)
model.max_buy_fac = Param(model.Factories,within=NonNegativeReals)

model.Max_ore = Param(model.Ore,within=NonNegativeReals)
model.Ore_cost = Param(model.Ore,within=NonNegativeReals)
model.Ore_combination = Param(model.Ore, model.Metals, within=NonNegativeReals)

model.Container_min_to_be_sent_depot = Param(model.Factories, model.Depots, within=NonNegativeIntegers)
model.Container_Max_to_be_sent_depot = Param(model.Factories, model.Depots, within=NonNegativeIntegers)
model.depots_min_to_receive = Param(model.Depots, within=NonNegativeIntegers)
model.depots_Max_to_receive = Param(model.Depots, within=NonNegativeIntegers)
model.Container_min_to_be_sent_market = Param(model.Depots, model.Markets, within= NonNegativeIntegers)
model.Container_Max_to_be_sent_market = Param(model.Depots, model.Markets, within= NonNegativeIntegers)

#variables
model.Z = Var(model.Ore,model.Alloys, within=NonNegativeReals) # ?
model.F = Var(model.Ore,model.Alloys, within=NonNegativeReals) # ?
model.A = Var(model.Ore,model.Alloys, within=NonNegativeReals) # ?
model.C = Var(model.Ore,model.Alloys, within=NonNegativeReals) # ?
model.U = Var(model.Alloys,within=NonNegativeReals)
model.t = Var(model.Alloys,model.Factories,model.Depots)
model.Extracted_ore = Var(model.Ore,within=NonNegativeReals) # Si in paper
model.h = Var(model.Factories,within= Boolean)
model.B = Var(model.Factories, model.Depots, within=NonNegativeIntegers)
model.g = Var(model.Alloys, model.Depots, model.Markets, within=NonNegativeReals)
model.G = Var(model.Depots, model.Markets, within= NonNegativeIntegers)
model.l = Var(model.Markets, within= Boolean)

#rule for maximum extraction of ore.
def Max_extracted_ore_rule(model,i):
    return model.Extracted_ore[i] <= model.Max_ore[i]
model.Max_extracted_ore_limit = Constraint(model.Ore,rule=Max_extracted_ore_rule)


#alloy weight is sum of metals weights in it.
def Alloy_sum_rule(model,j):
    return model.U[j] == sum(model.Z[i,j] for i in model.Ore)+\
                         sum(model.C[i,j] for i in model.Ore)+\
                         sum(model.A[i,j] for i in model.Ore)+\
                         sum(model.F[i,j] for i in model.Ore)
model.Alloy_sum_limit = Constraint(model.Alloys,rule=Alloy_sum_rule)

#metals in alloys should be less than(or equal to) extracted metals from Ore.
def Metal_sum_rule_Z(model,i):
    return sum(model.Z[i,j] for j in Model.Alloys) <= model.Extracted_ore[i]*model.Ore_combination[i,'Zinc']
model.Metal_sum_limit_Z = Constraint(model.Ore,rule=Max_extracted_ore_rule)

def Metal_sum_rule_F(model,i):
    return sum(model.F[i,j] for j in Model.Alloys) <= model.Extracted_ore[i]*model.Ore_combination[i,'Iron']
model.Metal_sum_limit_F = Constraint(model.Ore,rule=Max_extracted_ore_rule)

def Metal_sum_rule_C(model,i):
    return sum(model.C[i,j] for j in Model.Alloys) <= model.Extracted_ore[i]*model.Ore_combination[i,'Copper']
model.Metal_sum_limit_C = Constraint(model.Ore,rule=Max_extracted_ore_rule)

def Metal_sum_rule_A(model,i):
    return sum(model.A[i,j] for j in Model.Alloys) <= model.Extracted_ore[i]*model.Ore_combination[i,'Aluminum']
model.Metal_sum_limit_A = Constraint(model.Ore,rule=Max_extracted_ore_rule)

#percentage of metals in alloys limitations.
def Metal_in_alloy_rule_A_Z(model):
    value = sum(model.Z[i,'A'] for i in model.Ore)
    return inequality(model.A_comb_min['Zinc']*model.U['A'],value,model.A_comb_max['Zinc']*model.U['A'])
model.Metal_in_alloy_limit_A_Z = Constraint(rule=Metal_in_alloy_rule_A_Z)
def Metal_in_alloy_rule_A_C(model):
    value = sum(model.C[i,'A'] for i in model.Ore)
    return inequality(model.A_comb_min['Copper']*model.U['A'],value,model.A_comb_max['Copper']*model.U['A'])
model.Metal_in_alloy_limit_A_C = Constraint(rule=Metal_in_alloy_rule_A_C)
def Metal_in_alloy_rule_A_A(model):
    value = sum(model.A[i,'A'] for i in model.Ore)
    return inequality(model.A_comb_min['Aluminum']*model.U['A'],value,model.A_comb_max['Aluminum']*model.U['A'])
model.Metal_in_alloy_limit_A_A = Constraint(rule=Metal_in_alloy_rule_A_A)
def Metal_in_alloy_rule_A_F(model):
    value = sum(model.F[i,'A'] for i in model.Ore)
    return inequality(model.A_comb_min['Iron']*model.U['A'],value,model.A_comb_max['Iron']*model.U['A'])
model.Metal_in_alloy_limit_A_F = Constraint(rule=Metal_in_alloy_rule_A_F)

def Metal_in_alloy_rule_B_Z(model):
    value = sum(model.Z[i,'B'] for i in model.Ore)
    return inequality(model.B_comb_min['Zinc']*model.U['B'],value,model.B_comb_max['Zinc']*model.U['B'])
model.Metal_in_alloy_limit_B_Z = Constraint(rule=Metal_in_alloy_rule_B_Z)
def Metal_in_alloy_rule_B_C(model):
    value = sum(model.C[i,'B'] for i in model.Ore)
    return inequality(model.B_comb_min['Copper']*model.U['B'],value,model.B_comb_max['Copper']*model.U['B'])
model.Metal_in_alloy_limit_B_C = Constraint(rule=Metal_in_alloy_rule_B_C)
def Metal_in_alloy_rule_B_A(model):
    value = sum(model.A[i,'B'] for i in model.Ore)
    return inequality(model.B_comb_min['Aluminum']*model.U['B'],value,model.B_comb_max['Aluminum']*model.U['B'])
model.Metal_in_alloy_limit_B_A = Constraint(rule=Metal_in_alloy_rule_B_A)
def Metal_in_alloy_rule_B_F(model):
    value = sum(model.F[i,'B'] for i in model.Ore)
    return inequality(model.B_comb_min['Iron']*model.U['B'],value,model.B_comb_max['Iron']*model.U['B'])
model.Metal_in_alloy_limit_B_F = Constraint(rule=Metal_in_alloy_rule_B_F)

#exported alloy from main fac should be less than (or equal to)  
def Export_from_main_fac_rule(model,i):
    return model.U[i] >= sum(model.t[i,'Main',k] for k in model.Depots)
model.Export_from_main_fac_limit = Constraint(model.Alloys,rule=Export_from_main_fac_rule)

#limits of buying from factories
def buy_from_fac_rule(model,i):
    return inequality(model.min_buy_fac[i]*model.h[i] ,sum(sum(model.t[i,j,k] for k in model.Depots)\
                                                for j in model.Alloys),model.max_buy_fac[i]*model.h[i])
model.buy_from_fac_limit= Constraint(model.Factories,rule=buy_from_fac_rule)

#limit for Alloys in one container from fac to depot.
def container_rule(model,i,j):
    return sum(model.t[a,i,j] for a in model.Alloys) <= model.B[i,j]*container_cap
model.container_limit = Constraint(model.Factories, model.Depots, rule=container_rule)

#limit for transporting from fac to depots No1.#TODO correction
def transportation_rule(model,i,j):
    return inequality(model.Container_min_to_be_sent_depot[i,j]*model.h[i],model.B[i,j],\
                      model.Container_Max_to_be_sent_depot[i,j]*model.h[i])
model.transportation_limit = Constraint(model.Factories,model.Depots, rule= transportation_rule)

#limit for transporting from fac to depots No2.
def transportation_rule2(model,j):
    return inequality(model.depots_min_to_receive[j],sum(model.B[i,j] for i in model.Factories),\
                      model.depots_Max_to_receive[j])
model.transportation_limit2 = Constraint(model.Depots,rule= transportation_rule2)

#limit for transporting from depots to markets.
def transp_from_dep_to_marker_rule(model,i,k):
    return sum(model.t[i,j,k] for j in model.Factories) >= sum(model.g[i,k,l] for l in model.Markets)
model.transp_from_dep_to_marker_limit = Constraint(model.Alloys,model.Depots, rule= transp_from_dep_to_marker_rule)

#limits for Alloys in containers transporting from depots to markets
def container_rule2(model,i,j):
    return sum(model.g[l,i,j] for l in model.Alloys) <= model.G[i,j]*container_cap
model.container_limit2 = Constraint(model.Depots, model.Markets, rule=container_rule2)

#limit for containers to be sent to markets.
def market_sell_rule(model,i,j):
    return inequality(model.Container_min_to_be_sent_market[i,j]*model.l[j],\
                      model.G[i,j],model.Container_min_to_be_sent_market[i,j]*model.l[j])
model.market_sell_limit = Constraint(model.Markets, rule= market_sell_rule)



