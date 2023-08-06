class OperatingPerformance:
    def __init__(self, independent,profitability=None, solvency=None, efficiency=None, growth=None, cash_flow=None):
        self.profitability = profitability
        self.solvency = solvency
        self.efficiency = efficiency
        self.growth = growth
        self.cash_flow = cash_flow
        self._independent = independent
        self._independent.attach(self)
        
    def update(self):
        # 观察者收到通知后需要执行的操作
        print("Received notification from subject.")
    def unsubscribe(self):
        self._independent.detach(self)
    def calculate_profitability(self):
        # 计算盈利能力
        pass

    def calculate_solvency(self):
        # 计算偿债能力
        pass

    def calculate_efficiency(self):
        # 计算经营效率
        pass

    def calculate_growth(self):
        # 计算成长性
        pass

    def calculate_cash_flow(self):
        # 计算现金流状况
        pass
