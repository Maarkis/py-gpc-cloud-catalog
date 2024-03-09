class Service:
    def __init__(
        self, service_id: str, name: str, display_name: str, business_entity_name: str
    ) -> None:
        self.service_id = service_id
        self.name = name
        self.display_name = display_name
        self.business_entity_name = business_entity_name
