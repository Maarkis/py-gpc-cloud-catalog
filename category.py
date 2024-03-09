class Category:

    def __init__(
        self,
        service_display_name: str,
        resource_family: str,
        resource_group: str,
        usage_type: str,
    ) -> None:
        self.service_display_name = service_display_name
        self.resource_family = resource_family
        self.resource_group = resource_group
        self.usage_type = usage_type
