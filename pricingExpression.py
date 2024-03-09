from tieredRates import TieredRates


class PricingExpression:
    def __init__(
        self,
        usage_unit: str,
        display_quantity: int,
        tiered_rates: list[TieredRates],
        usage_unit_description: str,
        base_unit: str,
        base_unit_description: str,
        base_unit_conversion_factor: float,
    ) -> None:
        self.usage_unit = usage_unit
        self.display_quantity = display_quantity
        self.tiered_rates = tiered_rates
        self.usage_unit_description = usage_unit_description
        self.base_unit = base_unit
        self.base_unit_description = base_unit_description
        self.base_unit_conversion_factor = base_unit_conversion_factor
