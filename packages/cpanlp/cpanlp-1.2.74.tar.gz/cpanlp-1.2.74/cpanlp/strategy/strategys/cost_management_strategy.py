from cpanlp.strategy.strategys.strategy import *

class CostManagementStrategy(Strategy):
    """
    #### A class representing cost management strategies for a company.

    Attributes:
    -----------
    production_cost: float
        The total production cost of the company.
    logistics_cost: float
        The total logistics cost of the company.
    supply_chain_cost: float
        The total supply chain cost of the company.
    waste_cost: float
        The total waste cost of the company.

    Methods:
    --------
    optimize_production_process():
        Optimizes the production process to reduce production cost.
    improve_logistics():
        Implements measures to improve logistics and reduce logistics cost.
    streamline_supply_chain():
        Streamlines the supply chain to reduce supply chain cost.
    reduce_waste():
        Implements measures to reduce waste and waste cost.
    """

    def __init__(self, company, market_focus, impact,time_horizon,production_cost, logistics_cost, supply_chain_cost, waste_cost):
        super().__init__(company, market_focus, impact,time_horizon)
        self.production_cost = production_cost
        self.logistics_cost = logistics_cost
        self.supply_chain_cost = supply_chain_cost
        self.waste_cost = waste_cost

    def optimize_production_process(self):
        """
        Optimizes the production process to reduce production cost.
        """
        # Code to optimize the production process goes here.
        self.production_cost *= 0.95

    def improve_logistics(self):
        """
        Implements measures to improve logistics and reduce logistics cost.
        """
        # Code to improve logistics goes here.
        self.logistics_cost *= 0.95

    def streamline_supply_chain(self):
        """
        Streamlines the supply chain to reduce supply chain cost.
        """
        # Code to streamline the supply chain goes here.
        self.supply_chain_cost *= 0.95

    def reduce_waste(self):
        """
        Implements measures to reduce waste and waste cost.
        """
        # Code to reduce waste goes here.
        self.waste_cost *= 0.95
