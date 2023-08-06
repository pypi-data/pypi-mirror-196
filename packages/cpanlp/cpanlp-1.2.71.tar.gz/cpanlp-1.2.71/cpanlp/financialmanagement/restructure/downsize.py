class Downsize:
    """
    #### A class to represent the characteristics of a downsizing event in financial management.
    #### downsizing refers to the strategy of reducing the size of an enterprise in order to cut costs, enhance competitiveness, and improve efficiency. This can involve measures such as staff layoffs, asset or business unit sales, and streamlining of business processes.
    """

    def __init__(self, workforce_reduction, asset_sale, operation_consolidation, process_streamlining, cost_cutting, 
                 structure_change):
        self.workforce_reduction = workforce_reduction
        self.asset_sale = asset_sale
        self.operation_consolidation = operation_consolidation
        self.process_streamlining = process_streamlining
        self.cost_cutting = cost_cutting
        self.structure_change = structure_change
        self._dependents = []
    def attach(self, dependent):
        self._dependents.append(dependent)
    def detach(self, dependent):
        self._dependents.remove(dependent)
    def notify(self):
        for dependent in self._dependents:
            dependent.update()

