class BondYield:
    """
    #### A class representing a bond yield object that calculates the yield on a bond.
    
    Features:
    - Coupon rate: The coupon rate is the interest rate that a bond pays to its investors. This rate can be fixed or variable, and it is typically set when the bond is issued.
    - Maturity: The maturity date is the date on which the principal amount of the bond is due to be repaid. The longer the time until maturity, the higher the bond yield is likely to be.
    - Credit rating: The credit rating of the bond issuer indicates the likelihood of the bond issuer defaulting on its obligations. Bonds with a higher credit rating generally have lower yields, while those with lower ratings typically have higher yields.
    - Market conditions: The current market conditions, including inflation rates and interest rates, can also affect bond yields.



    Args:
        - face_value (float): The face value of the bond.
        - coupon_rate (float): The coupon rate of the bond.
        - market_price (float): The current market price of the bond.
        - years_to_maturity (float): The number of years until the bond matures.
        - credit_rating (str): The credit rating of the bond issuer.

    Attributes:
        - yield_to_maturity (float): The yield to maturity of the bond.
    """

    def __init__(self, independent, face_value, coupon_rate, market_price, years_to_maturity, credit_rating):
        self.face_value = face_value
        self.coupon_rate = coupon_rate
        self.market_price = market_price
        self.years_to_maturity = years_to_maturity
        self.credit_rating = credit_rating
        self.yield_to_maturity = 0.0
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
    def calculate_yield_to_maturity(self):
        """
        Calculates the yield to maturity of the bond.

        Returns:
            float: The yield to maturity of the bond.
        """
        coupon_payment = self.face_value * self.coupon_rate
        years_remaining = self.years_to_maturity
        total_payments = coupon_payment
        while years_remaining > 0:
            total_payments += coupon_payment / ((1 + self.yield_to_maturity) ** years_remaining)
            years_remaining -= 1
        self.yield_to_maturity = (coupon_payment + (self.face_value - self.market_price) / self.years_to_maturity) / ((self.face_value + self.market_price) / 2)
        return self.yield_to_maturity
