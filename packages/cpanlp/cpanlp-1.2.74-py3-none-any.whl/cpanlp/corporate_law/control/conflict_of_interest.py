class ConflictOfInterest:
    """
    A class representing a conflict of interest object that identifies situations where competing interests may interfere with impartiality.
    
    Features:
    - Multiple roles or relationships: Conflicts of interest can arise when an individual or organization has multiple roles or relationships that may create competing interests, such as serving as both a consultant and an auditor for the same client.
    - Financial interests: Conflicts of interest can be financial in nature, such as when an individual or organization has a financial stake in the outcome of a decision or transaction.
    - Personal interests: Conflicts of interest can also be personal in nature, such as when an individual's personal relationships or beliefs may interfere with their ability to act impartially.
    - Confidentiality: Conflicts of interest can also arise when an individual or organization has access to confidential information that may be used to benefit their own interests.
    Args:
        - multiple_roles (bool): Whether the individual or organization has multiple roles or relationships that may create competing interests.
        - financial_interests (bool): Whether the conflict of interest is financial in nature.
        - personal_interests (bool): Whether the conflict of interest is personal in nature.
        - access_to_confidential_information (bool): Whether the individual or organization has access to confidential information that may be used to benefit their own interests.

    Attributes:
        - has_conflict (bool): Whether a conflict of interest exists.
    """

    def __init__(self,independent, multiple_roles, financial_interests, personal_interests, access_to_confidential_information):
        self.multiple_roles = multiple_roles
        self.financial_interests = financial_interests
        self.personal_interests = personal_interests
        self.access_to_confidential_information = access_to_confidential_information
        self.has_conflict = False
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
    def check_conflict_of_interest(self):
        """
        Checks whether a conflict of interest exists.

        Returns:
            bool: True if a conflict of interest exists, otherwise False.
        """
        if self.multiple_roles or self.financial_interests or self.personal_interests or self.access_to_confidential_information:
            self.has_conflict = True
        return self.has_conflict
