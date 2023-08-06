class FinancialConstraint:
    def __init__(self, available_funds, required_funds):
        self.available_funds = available_funds
        self.required_funds = required_funds
        self._dependents = []
    def attach(self, dependent):
        self._dependents.append(dependent)
    def detach(self, dependent):
        self._dependents.remove(dependent)
    def notify(self):
        for dependent in self._dependents:
            dependent.update()
    def is_funds_sufficient(self):
        if self.available_funds >= self.required_funds:
            return True
        else:
            return False

    def calculate_cost_of_funds(self, interest_rate):
        return self.required_funds * interest_rate

    def is_short_term_debt_repayable(self, short_term_debt):
        if self.available_funds >= short_term_debt:
            return True
        else:
            return False

    def is_investment_feasible(self, investment_amount):
        if self.available_funds >= investment_amount:
            return True
        else:
            return False
