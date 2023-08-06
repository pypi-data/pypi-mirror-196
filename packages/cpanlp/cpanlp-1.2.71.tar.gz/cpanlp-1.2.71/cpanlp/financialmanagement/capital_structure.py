class CapitalStructure:
    """
    A class representing the capital structure of a company.

    Attributes:
    -----------
    debt: float
        The total amount of debt the company has.
    equity: float
        The total amount of equity the company has.

    Methods:
    --------
    get_debt_ratio():
        Calculates and returns the debt ratio of the company.
    get_equity_ratio():
        Calculates and returns the equity ratio of the company.
    get_weighted_average_cost_of_capital(debt_rate, equity_rate, tax_rate):
        Calculates and returns the weighted average cost of capital (WACC) of the company.
    """

    def __init__(self, independent, debt, equity):
        """
        Initializes a new instance of the CapitalStructure class.

        Parameters:
        -----------
        debt: float
            The total amount of debt the company has.
        equity: float
            The total amount of equity the company has.
        """
        self.debt = debt
        self.equity = equity
        self._independent = independent
        self._independent.attach(self)
    def update(self):
        # 观察者收到通知后需要执行的操作
        print("Received notification from subject.")

    def get_debt_ratio(self):
        """
        Calculates and returns the debt ratio of the company.

        Returns:
        --------
        float:
            The debt ratio of the company.
        """
        total = self.debt + self.equity
        if total == 0:
            return 0
        return self.debt / total

    def get_equity_ratio(self):
        """
        Calculates and returns the equity ratio of the company.

        Returns:
        --------
        float:
            The equity ratio of the company.
        """
        total = self.debt + self.equity
        if total == 0:
            return 0
        return self.equity / total

    def get_weighted_average_cost_of_capital(self, debt_rate, equity_rate, tax_rate):
        """
        Calculates and returns the weighted average cost of capital (WACC) of the company.

        Parameters:
        -----------
        debt_rate: float
            The interest rate on the company's debt.
        equity_rate: float
            The required rate of return on the company's equity.
        tax_rate: float
            The corporate tax rate.

        Returns:
        --------
        float:
            The weighted average cost of capital (WACC) of the company.
        """
        debt_weight = self.get_debt_ratio()
        equity_weight = self.get_equity_ratio()

        cost_of_debt = debt_rate * (1 - tax_rate)
        cost_of_equity = equity_rate

        wacc = (debt_weight * cost_of_debt) + (equity_weight * cost_of_equity)

        return wacc
