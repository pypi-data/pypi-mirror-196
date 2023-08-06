class ESG:
    """
    A class to represent the environmental, social, and governance (ESG) performance of a company.

    Attributes
    ----------
    - company_name : str
        the name of the company
    - environmental_score : float
        the company's score on environmental performance, ranging from 0 to 100
    - social_score : float
        the company's score on social performance, ranging from 0 to 100
    - governance_score : float
        the company's score on governance performance, ranging from 0 to 100

    Methods
    -------
    - get_overall_score() -> float:
        Calculates the overall ESG score of the company based on its environmental, social, and governance scores.
    """

    def __init__(self,independent, company_name, environmental_score, social_score, governance_score):
        self.company_name = company_name
        self.environmental_score = environmental_score
        self.social_score = social_score
        self.governance_score = governance_score
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
    def get_overall_score(self):
        """
        Calculates the overall ESG score of the company based on its environmental, social, and governance scores.

        Returns
        -------
        float
            the overall ESG score of the company, ranging from 0 to 100
        """
        # implementation details to calculate overall ESG score

