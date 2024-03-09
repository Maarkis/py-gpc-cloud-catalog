class UnitPrice:
    def __init__(self, currency_code: str, nanos: int) -> None:
        self.currency_code = currency_code
        self.nanos = nanos
