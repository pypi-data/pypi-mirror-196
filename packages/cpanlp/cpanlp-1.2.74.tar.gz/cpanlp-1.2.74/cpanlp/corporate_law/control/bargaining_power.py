class BargainingPower:
    
    def __init__(self, resources, market_position, technological_abilities, supplier_competition, customer_competition, cost_structure):
        self.resources = resources
        self.market_position = market_position
        self.technological_abilities = technological_abilities
        self.supplier_competition = supplier_competition
        self.customer_competition = customer_competition
        self.cost_structure = cost_structure
        self._dependents = []
    def attach(self, dependent):
        self._dependents.append(dependent)
    def detach(self, dependent):
        self._dependents.remove(dependent)
    def notify(self):
        for dependent in self._dependents:
            dependent.update()
    def calculate_bargaining_power(self):
        power = 0
        if self.resources:
            power += 1
        if self.market_position:
            power += 1
        if self.technological_abilities:
            power += 1
        if self.supplier_competition:
            power += 1
        if self.customer_competition:
            power += 1
        if self.cost_structure:
            power += 1
        return power
