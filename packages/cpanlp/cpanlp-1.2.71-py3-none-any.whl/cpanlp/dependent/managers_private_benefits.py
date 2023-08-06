class ManagersPrivateBenefits:
    """
    #### A class to represent managers' private benefits, which are the benefits that the company's management may gain for their personal interests.

    Attributes:
    -----------
    private_jets: bool
        Whether the managers have access to private jets.
    luxury_cars: bool
        Whether the managers have access to luxury cars.
    high_compensation: bool
        Whether the managers are receiving high compensation.
    stock_options: bool
        Whether the managers have access to stock options.
    decision_control: bool
        Whether the managers have significant control over company decision making.

    Methods:
    --------
    calculate_total_private_benefits():
        Calculates the total private benefits.
    """

    def __init__(self,independent, private_jets, luxury_cars, high_compensation, stock_options,decision_control):
        self.private_jets = private_jets
        self.luxury_cars = luxury_cars
        self.high_compensation = high_compensation
        self.stock_options = stock_options
        self.decision_control = decision_control
        self._independent = independent
        self._independent.attach(self)
    def update(self):
        # 观察者收到通知后需要执行的操作
        print("Received notification from subject.")
    def unsubscribe(self):
        self._independent.detach(self)
    def calculate_total_private_benefits(self):
        """
        Calculates the total private benefits.
        """
        total_benefits = 0.0

        if self.private_jets:
            total_benefits += 1000000  # Value of private jet usage
        if self.luxury_cars:
            total_benefits += 50000  # Value of luxury car usage
        if self.high_compensation:
            total_benefits += 1000000  # Value of high compensation
        if self.stock_options:
            total_benefits += 500000  # Value of stock options
        if self.decision_control:
            total_benefits += 2000000  # Value of decision control

        return total_benefits
