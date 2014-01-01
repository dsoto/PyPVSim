def excess_supply(demand, supply, dt):
    '''
    returns the energy that wasn't consumed by the load on an
    instantaneous basis
    that is if the supply was greater than the load, add that to the
    accumulated energy
    '''
    lsd = load_supply_difference(demand, supply, dt)
    return -lsd[lsd<0].sum()

def excess_demand(demand, supply, dt):
    '''
    returns the energy demanded by the load but not met by the supply on
    an instantaneous basis
    '''
    lsd = load_supply_difference(demand, supply, dt)
    return lsd[lsd>0].sum()

def load_supply_difference(demand, supply, dt):
    return (demand - supply) * dt

def fraction_excess_supply(demand, supply, dt):
    return excess_supply(demand, supply, dt) / supply.sum() / dt

def fraction_excess_demand(demand, supply, dt):
    return excess_demand(demand, supply, dt) / demand.sum() / dt
