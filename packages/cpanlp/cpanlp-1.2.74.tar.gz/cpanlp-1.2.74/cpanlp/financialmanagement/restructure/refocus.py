class Refocus:
    def __init__(self, years_of_operation, core_business, non_core_businesses):
        self.years_of_operation = years_of_operation
        self.core_business = core_business
        self.non_core_businesses = non_core_businesses
        self._dependents = []
    def attach(self, dependent):
        self._dependents.append(dependent)
    def detach(self, dependent):
        self._dependents.remove(dependent)
    def notify(self):
        for dependent in self._dependents:
            dependent.update()
    def sell_non_core_assets(self, asset):
        # 企业出售非核心资产
        pass

    def optimize_resources(self):
        # 企业进行组织和流程改进
        pass

    def focus_on_core_business(self):
        # 企业将精力集中在核心业务上
        pass
