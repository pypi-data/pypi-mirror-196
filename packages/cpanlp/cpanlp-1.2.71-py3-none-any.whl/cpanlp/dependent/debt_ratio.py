class DebtRatio:
    """
    #### A class to represent debt ratio, which is the ratio of total debt to total assets.
    
    Attributes:
    -----------
    total_debt: float
        Total amount of debt.
    total_assets: float
        Total amount of assets.
    
    Methods:
    --------
    calculate_debt_ratio():
        Calculates the debt ratio.
    assess_financial_risk():
        Assesses the level of financial risk based on the debt ratio.
    evaluate_financing_ability():
        Evaluates the company's financing ability based on the debt ratio.
    """
    
    def __init__(self, independent, total_debt, total_assets):
        self.total_debt = total_debt
        self.total_assets = total_assets
        self._independent = independent
        self._independent.attach(self)
    def update(self):
        # 观察者收到通知后需要执行的操作
        print("Received notification from subject.")
    def unsubscribe(self):
        self._independent.detach(self)
    def calculate_debt_ratio(self):
        """
        Calculates the debt ratio.
        """
        return self.total_debt / self.total_assets
    
    def assess_financial_risk(self):
        """
        Assesses the level of financial risk based on the debt ratio.
        """
        debt_ratio = self.calculate_debt_ratio()
        if debt_ratio < 0.5:
            return "Low financial risk."
        elif 0.5 <= debt_ratio < 0.8:
            return "Moderate financial risk."
        else:
            return "High financial risk."
    
    def evaluate_financing_ability(self):
        """
        Evaluates the company's financing ability based on the debt ratio.
        """
        debt_ratio = self.calculate_debt_ratio()
        if debt_ratio < 0.5:
            return "Good financing ability."
        elif 0.5 <= debt_ratio < 0.8:
            return "Fair financing ability."
        else:
            return "Poor financing ability."
