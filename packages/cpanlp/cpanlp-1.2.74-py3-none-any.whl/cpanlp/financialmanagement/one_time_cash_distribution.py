class OneTimeCashDistribution:
    """
    #### A class representing one-time cash distribution.

    Attributes:
        amount (float): The amount of cash distributed to shareholders.
        reason (str): The reason for the one-time cash distribution.

    Methods:
        __init__(self, amount, reason): Constructs a OneTimeCashDistribution object with the specified amount and reason.
    """

    def __init__(self, amount, reason):
        """
        Constructs a OneTimeCashDistribution object with the specified amount and reason.

        Args:
            amount (float): The amount of cash distributed to shareholders.
            reason (str): The reason for the one-time cash distribution.
        """
        self.amount = amount
        self.reason = reason
        self._dependents = []
    def attach(self, dependent):
        self._dependents.append(dependent)
    def detach(self, dependent):
        self._dependents.remove(dependent)
    def notify(self):
        for dependent in self._dependents:
            dependent.update()
