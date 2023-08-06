class MarketCompetition:
    """
    #### A class representing market competition in a specific industry.

    Attributes:
    -----------
    firms : list
        A list of the firms or companies competing in the market.
    buyers : int
        The number of buyers in the market.
    sellers : int
        The number of sellers in the market.
    price_control : bool
        Indicates whether firms have control over the price of goods and services.
    innovation : bool
        Indicates whether firms must continuously improve and innovate to stay competitive.
    """

    def __init__(self, firms, buyers, sellers, price_control, innovation):
        """
        Initializes a MarketCompetition object with the specified attributes.

        Parameters:
        -----------
        firms : list
            A list of the firms or companies competing in the market.
        buyers : int
            The number of buyers in the market.
        sellers : int
            The number of sellers in the market.
        price_control : bool
            Indicates whether firms have control over the price of goods and services.
        innovation : bool
            Indicates whether firms must continuously improve and innovate to stay competitive.
        """
        self.firms = firms
        self.buyers = buyers
        self.sellers = sellers
        self.price_control = price_control
        self.innovation = innovation
        self._dependents = []
    def attach(self, dependent):
        self._dependents.append(dependent)
    def detach(self, dependent):
        self._dependents.remove(dependent)
    def notify(self):
        for dependent in self._dependents:
            dependent.update()
