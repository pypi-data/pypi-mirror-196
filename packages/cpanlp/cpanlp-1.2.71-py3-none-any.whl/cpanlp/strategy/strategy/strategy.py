from cpanlp.decorator.witheffects import *
class Strategy:
    def __init__(self, company, market_focus, impact,time_horizon):
        self.company = company
        self.time_horizon = time_horizon
        self.market_focus = market_focus
        self.impact = impact
        self.decision = None
        self._dependents = []
    def attach(self, dependent):
        self._dependents.append(dependent)
    def detach(self, dependent):
        self._dependents.remove(dependent)
    def notify(self):
        for dependent in self._dependents:
            dependent.update()
