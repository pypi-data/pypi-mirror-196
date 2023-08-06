from cpanlp.corporate_law.contract.financial_instruments.bond import *

class GreenBond(Bond):
    """
    A class to represent a green bond used to finance environmentally-friendly projects.

    Attributes
    ----------
    - issuer : str
        the name of the issuer of the bond
    - issue_date : str
        the date the bond was issued
    - maturity_date : str
        the date the bond will mature
    - principal_amount : float
        the principal amount of the bond
    - coupon_rate : float
        the coupon rate of the bond
    - project_type : str
        the type of environmentally-friendly project the bond is financing
    - project_description : str
        a description of the environmentally-friendly project the bond is financing
    - certification : str
        the certification or verification standard used to verify the environmentally-friendly nature of the project

    Methods
    -------
    get_yield_to_maturity(market_price: float) -> float:
        Calculates the yield to maturity of the bond based on its current market price.

    get_duration() -> float:
        Calculates the duration of the bond.
    """

    def __init__(self,independent, issuer, issue_date, maturity_date, principal_amount, project_type, project_description, certification,parties,value, rate, currency,domestic,consideration, obligations,outstanding_balance):
        super().__init__(independent,parties,value, rate, currency,domestic,issue_date, maturity_date,consideration, obligations,outstanding_balance)
        self.issuer = issuer
        self.principal_amount = principal_amount
        self.project_type = project_type
        self.project_description = project_description
        self.certification = certification
    def get_yield_to_maturity(self, market_price):
        """
        Calculates the yield to maturity of the bond based on its current market price.
    
        Parameters
        ----------
        market_price : float
            the current market price of the bond
    
        Returns
        -------
        float
            the yield to maturity of the bond as a percentage
        """
        # implementation details to calculate yield to maturity
    
    def get_duration(self):
        """
        Calculates the duration of the bond.
    
        Returns
        -------
        float
            the duration of the bond in years
        """
        # implementation details to calculate bond duration
        pass
    