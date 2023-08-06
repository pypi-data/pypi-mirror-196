class SocialCapital:
    """
    A class representing a social capital object that measures the value derived from an individual or organization's social networks and relationships.
    
    Features:
    - Network diversity: Social capital is enhanced by having connections with a diverse range of individuals and groups. This can include connections within and outside of one's industry or profession, as well as connections with individuals from different backgrounds or cultures.
    - Trust and reciprocity: Social capital is strengthened by trust and reciprocity between individuals and groups. This can include a willingness to share information and resources, provide support, and engage in mutually beneficial exchanges.
    - Reputation: Social capital is influenced by the reputation of individuals and organizations within their social networks. A positive reputation can enhance trust and reciprocity, while a negative reputation can reduce social capital.
    - Access to resources: Social capital can provide access to resources such as knowledge, information, and funding. Individuals and organizations with strong social capital are more likely to have access to these resources through their social networks.
    
    Args:
        - network_diversity (float): The diversity of the individual or organization's social networks.
        - trust_reciprocity (float): The level of trust and reciprocity between the individual or organization and - its social networks.
        - reputation (float): The reputation of the individual or organization within its social networks.
        - access_to_resources (float): The level of access to resources that the individual or organization derives - from its social networks.

    Attributes:
        social_capital_score (float): The overall social capital score of the individual or organization.
    """

    def __init__(self,independent, network_diversity, trust_reciprocity, reputation, access_to_resources):
        self.network_diversity = network_diversity
        self.trust_reciprocity = trust_reciprocity
        self.reputation = reputation
        self.access_to_resources = access_to_resources
        self.social_capital_score = None
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
    def calculate_social_capital_score(self):
        """
        Calculates the overall social capital score of the individual or organization.

        Returns:
            float: The overall social capital score of the individual or organization.
        """
        self.social_capital_score = (self.network_diversity + self.trust_reciprocity + self.reputation + self.access_to_resources) / 4
        return self.social_capital_score
