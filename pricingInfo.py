from datetime import datetime
from pricingExpression import PricingExpression


class PricingInfo:
    def __init__(
        self,
        effective_time: datetime,
        pricing_expression: PricingExpression,
        currency_conversion_rate: int,
    ) -> None:
        self.effective_time = effective_time
        self.pricing_expression = pricing_expression
        self.currency_conversion_rate = currency_conversion_rate
