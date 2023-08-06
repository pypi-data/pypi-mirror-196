class Spinoff:
    """
    #### A class representing spinoff assets.

    Attributes:
        name (str): The name of the spinoff company.
        parent_company (str): The name of the parent company.
        assets (list): A list of assets spun off from the parent company.

    Methods:
        __init__(self, name, parent_company, assets): Constructs a Spinoff object with the specified name, parent company, and assets.
    """

    def __init__(self, name, parent_company, assets):
        """
        Constructs a Spinoff object with the specified name, parent company, and assets.

        Args:
            name (str): The name of the spinoff company.
            parent_company (str): The name of the parent company.
            assets (list): A list of assets spun off from the parent company.
        """
        self.name = name
        self.parent_company = parent_company
        self.assets = assets
        self._dependents = []
    def attach(self, dependent):
        self._dependents.append(dependent)
    def detach(self, dependent):
        self._dependents.remove(dependent)
    def notify(self):
        for dependent in self._dependents:
            dependent.update()
