class FinancialCondition:
    """
    #### Financial condition refers to a company's overall financial health and ability to meet its financial obligations. It can be evaluated through various financial ratios, such as liquidity, solvency, and profitability ratios.
    """
    def __init__(self, independent, liquidity_ratio, solvency_ratio, profitability_ratio, market_conditions):
        self.liquidity_ratio = liquidity_ratio
        self.solvency_ratio = solvency_ratio
        self.profitability_ratio = profitability_ratio
        self.market_conditions = market_conditions
        self._independent = independent
        self._independent.attach(self)
    def update(self):
        # 观察者收到通知后需要执行的操作
        print("Received notification from subject.")
    def evaluate(self):
        if self.liquidity_ratio < 1:
            print("The company may have difficulty meeting its short-term obligations.")
        if self.solvency_ratio < 1:
            print("The company may have difficulty meeting its long-term obligations.")
        if self.profitability_ratio < 0:
            print("The company may have difficulty generating profits.")
        if self.market_conditions == "unfavorable":
            print("The company's financial condition may be negatively impacted by current market conditions.")
        else:
            print("The company's financial condition is stable.")
