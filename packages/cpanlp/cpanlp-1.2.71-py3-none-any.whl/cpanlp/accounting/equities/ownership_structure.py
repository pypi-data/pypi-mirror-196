class OwnershipStructure:
    """
    #### A class representing an ownership structure object that describes the way in which ownership of a company is distributed.
    
    Features:
    - Concentration of ownership: Ownership structure can be concentrated when a small number of individuals or entities hold a large percentage of shares in the company.
    - Institutional ownership: Institutional investors, such as mutual funds and pension funds, can play a significant role in ownership structure.
    - Insider ownership: Insider ownership refers to the percentage of shares held by individuals who are directly involved in the management of the company, such as executives and board members.
    - Shareholder activism: Shareholder activism refers to the use of shareholder rights to influence the decision-making and governance of the company.

    Args:
        - concentration_of_ownership (float): The percentage of shares held by the largest shareholders.
        - institutional_ownership (float): The percentage of shares held by institutional investors.
        - insider_ownership (float): The percentage of shares held by insiders.
        - shareholder_activism (bool): Whether shareholder activism is present.

    Attributes:
        - ownership_description (str): A description of the ownership structure.
    """

    def __init__(self,independent, concentration_of_ownership, institutional_ownership, insider_ownership, shareholder_activism):
        self.concentration_of_ownership = concentration_of_ownership
        self.institutional_ownership = institutional_ownership
        self.insider_ownership = insider_ownership
        self.shareholder_activism = shareholder_activism
        self.ownership_description = None
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
    def describe_ownership_structure(self):
        """
        Describes the ownership structure.

        Returns:
            str: A description of the ownership structure.
        """
        description = "The ownership structure of the company is "
        if self.concentration_of_ownership >= 50:
            description += "highly concentrated, with the largest shareholders holding {:.2f}% of shares. ".format(self.concentration_of_ownership)
        elif self.concentration_of_ownership >= 20:
            description += "moderately concentrated, with the largest shareholders holding {:.2f}% of shares. ".format(self.concentration_of_ownership)
        else:
            description += "widely dispersed, with no single shareholder holding a significant percentage of shares. "
        if self.institutional_ownership >= 50:
            description += "Institutional investors hold a significant percentage of shares, with {:.2f}% of shares held by these investors. ".format(self.institutional_ownership)
        elif self.institutional_ownership >= 20:
            description += "A moderate percentage of shares are held by institutional investors, with {:.2f}% of shares held by these investors. ".format(self.institutional_ownership)
        else:
            description += "Few shares are held by institutional investors. "
        if self.insider_ownership >= 10:
            description += "Insiders hold a significant percentage of shares, with {:.2f}% of shares held by these individuals. ".format(self.insider_ownership)
        else:
            description += "Insiders hold a relatively small percentage of shares. "
        if self.shareholder_activism:
            description += "There is also evidence of shareholder activism within the company."
        else:
            description += "There is no evidence of shareholder activism within the company."
        self.ownership_description = description
        return self.ownership_description
