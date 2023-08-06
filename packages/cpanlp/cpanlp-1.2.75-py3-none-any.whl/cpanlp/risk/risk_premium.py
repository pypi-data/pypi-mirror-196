class RiskPremium:
    """
    A class to represent the risk premium associated with an investment.

    Attributes
    ----------
    risk_nature : str
        the nature of the risk, such as market risk or credit risk
    risk_level : str
        the level of risk, such as high, medium, or low
    return_rate : float
        the return associated with the risk, expressed as a percentage
    term : str
        the term of the investment, such as short-term or long-term

    Methods
    -------
    calculate_premium(price: float) -> float:
        Calculates the risk premium associated with the investment based on the current market price.
    """

    def __init__(self, independent,risk_nature, risk_level, return_rate, term):
        """
        Constructs all the necessary attributes for the RiskPremium object.

        Parameters
        ----------
        risk_nature : str
            the nature of the risk, such as market risk or credit risk
        risk_level : str
            the level of risk, such as high, medium, or low
        return_rate : float
            the return associated with the risk, expressed as a percentage
        term : str
            the term of the investment, such as short-term or long-term
        """
        self.risk_nature = risk_nature
        self.risk_level = risk_level
        self.return_rate = return_rate
        self.term = term
        self._independent = independent
        self._independent.attach(self)
        self._dependents = []
    def attach(self, dependent):
        self._dependents.append(dependent)
    def detach(self, dependent):
        self._dependents.remove(dependent)
    def notify(self):
        for dependent in self._dependents:
            dependent.update()
    def update(self):
        # 观察者收到通知后需要执行的操作
        print("Received notification from subject.")

    def calculate_premium(self, price):
        """
        Calculates the risk premium associated with the investment based on the current market price.

        Parameters
        ----------
        price : float
            the current market price of the investment

        Returns
        -------
        float
            the risk premium associated with the investment, expressed as a percentage
        """
        # implementation details to calculate risk premium based on current market price

