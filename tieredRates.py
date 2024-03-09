from unitPrice import UnitPrice


class TieredRates:

    def __init__(self, start_usage_amount: float, unit_price: UnitPrice) -> None:
        self.start_usage_amount = start_usage_amount
        self.unit_price = unit_price

    @staticmethod
    def create_tiered_rates(list):
        tiered_rates: list[TieredRates] = []
        for tier in list:
            tiered_rates.append(
                TieredRates(
                    start_usage_amount=tier.start_usage_amount,
                    unit_price=UnitPrice(
                        currency_code=tier.unit_price.currency_code,
                        nanos=tier.unit_price.nanos,
                    ),
                )
            )
        return tiered_rates
