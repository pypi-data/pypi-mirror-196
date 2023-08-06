class CashFlowRights:
    """
    A class to represent cash flow rights, which refer to a shareholder's right to receive a portion of a company's cash flows.
    
    Features
    ----------
    - Entitlement to cash flows: Shareholders with cash flow rights are entitled to receive a portion of a company's cash flows, which can come in the form of dividends, share buybacks, or other distributions.
    - Priority of cash flows: The amount of cash flows received by shareholders with cash flow rights is typically prioritized over the amount received by shareholders with other types of rights, such as voting rights or liquidation rights.
    - Influence on valuation: Cash flow rights can have a significant impact on a company's valuation, as they are a key determinant of a company's ability to generate cash flows and pay dividends.
    - Risk and return: Cash flow rights can be a source of risk and return for shareholders, as the amount and timing of cash flows can be uncertain and can vary based on a company's financial performance.

    Attributes
    ----------
    - shareholder_name : str
        the name of the shareholder
    - type_of_shares : str
        the type of shares that provide cash flow rights
    - entitlement_to_cash_flows : bool
        a flag indicating whether the shareholder is entitled to receive a portion of the company's cash flows
    - priority_of_cash_flows : bool
        a flag indicating whether the amount of cash flows received by the shareholder is prioritized over the amount received by shareholders with other types of rights
    - influence_on_valuation : bool
        a flag indicating whether cash flow rights have a significant impact on a company's valuation
    - risk_and_return : bool
        a flag indicating whether cash flow rights are a source of risk and return for shareholders

    Methods
    -------
    receive_dividends(amount):
        Receives a portion of the company's cash flows in the form of dividends.
    participate_in_share_buybacks(amount):
        Participates in the company's share buyback program to receive a portion of the company's cash flows.
    assess_impact_on_valuation():
        Assesses the impact of cash flow rights on the company's valuation.
    """

    def __init__(self, shareholder_name: str, type_of_shares: str):
        """
        Constructs all the necessary attributes for the CashFlowRights object.

        Parameters
        ----------
        shareholder_name : str
            the name of the shareholder
        type_of_shares : str
            the type of shares that provide cash flow rights
        """
        self.shareholder_name = shareholder_name
        self.type_of_shares = type_of_shares
        self.entitlement_to_cash_flows = True
        self.priority_of_cash_flows = True
        self.influence_on_valuation = True
        self.risk_and_return = True

    def receive_dividends(self, amount: float):
        """
        Receives a portion of the company's cash flows in the form of dividends.

        Parameters
        ----------
        amount : float
            the amount of cash flows to be received
        """
        # implementation details to receive dividends

    def participate_in_share_buybacks(self, amount: float):
        """
        Participates in the company's share buyback program to receive a portion of the company's cash flows.

        Parameters
        ----------
        amount : float
            the amount of cash flows to be received
        """
        # implementation details to participate in share
