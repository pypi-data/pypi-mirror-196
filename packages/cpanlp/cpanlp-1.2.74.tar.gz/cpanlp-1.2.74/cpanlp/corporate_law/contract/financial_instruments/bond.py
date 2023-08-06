from cpanlp.corporate_law.contract.financial_instruments.financial_instrument import *

class Bond(FinancialInstrument):
    """
    #### A class representing a bond financial instrument.
    
    Attributes:
    - parties (list[str]): A list of parties involved in the bond agreement.
    - value (float): The monetary value of the bond.
    - rate (float): The interest rate of the bond.
    - currency (str): The currency of the bond.
    - domestic (bool): Whether the bond is domestic or international.
    - outstanding_balance (float): The outstanding balance of the bond.
    - date (str): The date of the bond issuance.
        
    Methods:
    - calculate_interest(): Calculate the interest of the bond based on its rate and outstanding balance.
    
    """
    def __init__(self,independent,parties=None,value=None, rate=None, currency=None,domestic=None,issue_date=None, maturity_date=None,consideration=None, obligations=None,outstanding_balance=None):
        super().__init__(parties, consideration,obligations, value)
        self.rate = rate if rate is not None else 0.0
        self.currency = currency
        self.domestic = domestic
        self.outstanding_balance = outstanding_balance if outstanding_balance is not None else 0.0
        self.issue_date=issue_date
        self.maturity_date=maturity_date
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
    def calculate_interest(self):
        """
        Calculate the interest of the bond based on its rate and outstanding balance.
    
        Returns:
        The interest amount of the bond.
        """
        return self.rate * self.outstanding_balance
    