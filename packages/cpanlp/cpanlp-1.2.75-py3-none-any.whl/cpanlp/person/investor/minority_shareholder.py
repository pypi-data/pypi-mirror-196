class MinorityShareholders:
    """
    A class to represent minority shareholders, who own less than 50% of a company's shares.
    
    Features
    ----------
    - Limited control: Minority shareholders have limited control over the company's decision-making process, as they own less than 50% of the shares.
    - Vulnerability to majority shareholders: Minority shareholders are vulnerable to the actions of majority shareholders, who have greater control over the company and may make decisions that are not in the minority shareholders' best interests.
    - Protection of rights: Minority shareholders have legal rights that protect them from unfair treatment by the majority shareholders, such as the right to information, the right to vote on important matters, and the right to sell their shares.
    - Need for representation: Minority shareholders may need to be represented by a shareholder representative to ensure that their interests are protected.
    
    Attributes
    ----------
    - company_name : str
        the name of the company
    - percentage_of_shares : float
        the percentage of shares owned by the minority shareholders
    - legal_protections : bool
        a flag indicating whether the minority shareholders have legal rights that protect them from unfair treatment by the majority shareholders
    - vulnerability : bool
        a flag indicating whether the minority shareholders are vulnerable to the actions of the majority shareholders
    - need_for_representation : bool
        a flag indicating whether the minority shareholders need to be represented by a shareholder representative to ensure that their interests are protected

    Methods
    -------
    - exercise_voting_rights():
        Exercises the minority shareholders' voting rights on important matters.
    - seek_legal_protections():
        Seeks legal protections to ensure fair treatment of minority shareholders.
    - seek_representation():
        Seeks representation by a shareholder representative to ensure that the minority shareholders' interests are protected.
    """

    def __init__(self, company_name: str, percentage_of_shares: float):
        """
        Constructs all the necessary attributes for the MinorityShareholders object.

        Parameters
        ----------
        company_name : str
            the name of the company
        percentage_of_shares : float
            the percentage of shares owned by the minority shareholders
        """
        self.company_name = company_name
        self.percentage_of_shares = percentage_of_shares
        self.legal_protections = True
        self.vulnerability = True
        self.need_for_representation = True

    def exercise_voting_rights(self):
        """
        Exercises the minority shareholders' voting rights on important matters.
        """
        # implementation details to exercise voting rights

    def seek_legal_protections(self):
        """
        Seeks legal protections to ensure fair treatment of minority shareholders.
        """
        # implementation details to seek legal protections

    def seek_representation(self):
        """
        Seeks representation by a shareholder representative to ensure that the minority shareholders' interests are protected.
        """
        # implementation details to seek representation
