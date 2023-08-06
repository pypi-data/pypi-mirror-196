from cpanlp.informations.information import *
class PeerInformation(Information):
    """
    A class to represent the peer information of a company.

    Attributes
    ----------
    company_name : str
        the name of the company
    industry : str
        the industry that the company belongs to
    business_type : str
        the business type or operating model of the company
    comparison_metrics : dict
        a dictionary of comparison metrics and values with other companies in the same industry and business type

    Methods
    -------
    add_comparison_metric(metric_name: str, value: float):
        Adds a comparison metric and its value to the comparison metrics dictionary.
    """

    def __init__(self, message,company_name, industry, business_type):
        """
        Constructs all the necessary attributes for the PeerInformation object.

        Parameters
        ----------
        company_name : str
            the name of the company
        industry : str
            the industry that the company belongs to
        business_type : str
            the business type or operating model of the company
        """
        super().__init__(message)
        self.company_name = company_name
        self.industry = industry
        self.business_type = business_type
        self.comparison_metrics = {}

    def add_comparison_metric(self, metric_name: str, value: float):
        """
        Adds a comparison metric and its value to the comparison metrics dictionary.

        Parameters
        ----------
        metric_name : str
            the name of the comparison metric
        value : float
            the value of the comparison metric
        """
        self.comparison_metrics[metric_name] = value

