from cpanlp.corporate_law.entities.LLC import *

class SOE(LLC):
    def __init__(self, name, industry, state_ownership_percentage,type,capital):
        super().__init__(name,type,capital)
        self.name = name
        self.industry = industry
        self.state_ownership_percentage = state_ownership_percentage

    def is_strategically_important(self):
        if self.industry in ['energy', 'telecommunications', 'transportation']:
            return True
        else:
            return False

    def has_political_goals(self):
        return True

    def has_profit_goals(self):
        return True

    def get_state_influence(self):
        if self.state_ownership_percentage >= 50:
            return "High"
        else:
            return "Low"
