from category import Category
from geoTaxonomy import GeoTaxonomy
from pricingInfo import PricingInfo


class Sku:
    def __init__(self) -> None:
        pass

    name: str
    sku_id: str
    description: str
    category: Category
    service_regions: list[str]
    pricing_info: list[PricingInfo]
    service_provider_name: str
    geo_taxonomy: GeoTaxonomy
