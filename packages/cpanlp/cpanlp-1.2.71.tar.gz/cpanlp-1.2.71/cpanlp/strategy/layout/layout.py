class Layout:
    def __init__(self, market_position, resource_allocation, competitive_environment):
        self.market_position = market_position
        self.resource_allocation = resource_allocation
        self.competitive_environment = competitive_environment
        self._dependents = []
    def attach(self, dependent):
        self._dependents.append(dependent)
    def detach(self, dependent):
        self._dependents.remove(dependent)
    def notify(self):
        for dependent in self._dependents:
            dependent.update()
    def set_market_position(self, market_position):
        self.market_position = market_position

    def set_resource_allocation(self, resource_allocation):
        self.resource_allocation = resource_allocation

    def set_competitive_environment(self, competitive_environment):
        self.competitive_environment = competitive_environment
