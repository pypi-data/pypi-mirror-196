class ManagerialTalent:
    """
    #### A class representing a managerial talent object that measures the skills and abilities of a manager.
    
    Features:
    - Leadership skills: Managers with strong leadership skills can inspire and motivate employees, build a positive culture, and drive performance.
    - Communication skills: Effective communication is essential for managers to convey expectations and feedback, build relationships, and foster collaboration.
    - Decision-making abilities: Managers must make decisions that align with organizational goals and objectives, and they must be able to do so quickly and confidently.
    - Strategic thinking: Managers must have the ability to think strategically, analyze data, and identify opportunities for growth and improvement.
    
    Args:
        - leadership_skills (float): The strength of the manager's leadership skills.
        - communication_skills (float): The strength of the manager's communication skills.
        - decision_making_ability (float): The strength of the manager's decision-making ability.
        - strategic_thinking (float): The strength of the manager's strategic thinking.

    Attributes:
        - talent_score (float): The overall talent score of the manager.
    """

    def __init__(self, independent,leadership_skills, communication_skills, decision_making_ability, strategic_thinking):
        self.leadership_skills = leadership_skills
        self.communication_skills = communication_skills
        self.decision_making_ability = decision_making_ability
        self.strategic_thinking = strategic_thinking
        self.talent_score = None
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
    def calculate_talent_score(self):
        """
        Calculates the overall talent score of the manager.

        Returns:
            float: The overall talent score of the manager.
        """
        self.talent_score = (self.leadership_skills + self.communication_skills + self.decision_making_ability + self.strategic_thinking) / 4
        return self.talent_score
