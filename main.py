import os
from datetime import datetime
from typing import List
from google.cloud import billing_v1
import asyncio
import json

from category import Category
from geoTaxonomy import GeoTaxonomy
from pricingExpression import PricingExpression
from pricingInfo import PricingInfo
from service import Service
from sku import Sku
from tieredRates import TieredRates


async def main():
    client: billing_v1.CloudBillingAsyncClient = billing_v1.CloudCatalogAsyncClient()

    services = await get_services_gpc(client)
    services_to_json(services)

    # first or default (None)
    # get Compute Engine (6F81-5844-456A) service of GCP
    services_computer = next(
        (
            e
            for e in services
            if e.display_name == "Compute Engine" and e.service_id == "6F81-5844-456A"
        ),
        None,
    )

    if services_computer is None:
        print("Service Compute Engine (6F81-5844-456A) not found")
        return

    print("Obtained service:", services_computer.name)

    skus = await get_skus_gpc(
        client,
        billing_v1.ListSkusRequest(parent=services_computer.name, currency_code="BRL"),
    )
    skus_to_json(skus)
    # filter skus by regions southamerica
    skus_southamerica = list(
        filter(
            lambda sku: "southamerica-east1" in sku.geo_taxonomy.regions
            or "southamerica-east1" in sku.service_regions,
            skus,
        )
    )
    skus_to_json(skus_southamerica, "skus_southamerica")


async def get_services_gpc(client: billing_v1.CloudBillingAsyncClient) -> List[Service]:
    try:
        request = billing_v1.ListServicesRequest()
        services: List[Service] = []
        async for response in await client.list_services(request=request):
            service = Service(
                response.service_id,
                response.name,
                response.display_name,
                response.business_entity_name,
            )
            services.append(service)
        return services
    except Exception as e:
        print("Exception when calling CloudBillingClient.list_services: %s\n" % e)


def services_to_json(services: List[Service]) -> None:
    services_data = []
    for service in services:
        services_data.append(
            {
                "service_id": service.service_id,
                "name": service.name,
                "display_name": service.display_name,
                "business_entity_name": service.business_entity_name,
            }
        )

    create_json("services", services_data)


async def get_skus_gpc(
    client: billing_v1.CloudBillingAsyncClient, request: billing_v1.ListSkusRequest
) -> List[Sku]:
    try:
        skus = []
        async for response in await client.list_skus(request=request):

            sku = Sku()
            pricing_info: list[PricingInfo] = []
            tiered_rates: list[TieredRates] = []
            sku.name = response.name
            sku.sku_id = response.sku_id
            sku.description = response.description
            sku.category = Category(
                service_display_name=response.category.service_display_name,
                resource_family=response.category.resource_family,
                resource_group=response.category.resource_group,
                usage_type=response.category.usage_type,
            )
            sku.service_regions = list(response.service_regions)
            for pricing in response.pricing_info:
                pricingInfo = PricingInfo(
                    effective_time=pricing.effective_time,
                    currency_conversion_rate=pricing.currency_conversion_rate,
                    pricing_expression=PricingExpression(
                        usage_unit=pricing.pricing_expression.usage_unit,
                        display_quantity=pricing.pricing_expression.display_quantity,
                        tiered_rates=TieredRates.create_tiered_rates(
                            pricing.pricing_expression.tiered_rates
                        ),
                        usage_unit_description=pricing.pricing_expression.usage_unit_description,
                        base_unit=pricing.pricing_expression.base_unit,
                        base_unit_description=pricing.pricing_expression.base_unit_description,
                        base_unit_conversion_factor=pricing.pricing_expression.base_unit_conversion_factor,
                    ),
                )
                pricing_info.append(pricingInfo)

            sku.pricing_info = pricing_info
            sku.service_provider_name = response.service_provider_name
            sku.geo_taxonomy = GeoTaxonomy(
                type_=response.geo_taxonomy.type_,
                regions=list(response.geo_taxonomy.regions),
            )
            skus.append(sku)
        return skus

    except Exception as e:
        print("Exception when calling CloudBillingClient.list_skus: %s\n" % e)


def skus_to_json(skus: List[Sku], name_file: str = "skus") -> None:
    skus_data = []
    for sku in skus:
        skus_data.append(
            {
                "name": sku.name,
                "sku_id": sku.sku_id,
                "description": sku.description,
                "category": {
                    "service_display_name": sku.category.service_display_name,
                    "resource_family": sku.category.resource_family,
                    "resource_group": sku.category.resource_group,
                    "usage_type": sku.category.usage_type,
                },
                "service_regions": sku.service_regions,
                "pricing_info": list(
                    map(
                        lambda pricing_info: {
                            "effective_time": pricing_info.effective_time.isoformat(),
                            "currency_conversion_rate": pricing_info.currency_conversion_rate,
                            "pricing_expression": {
                                "usage_unit": pricing_info.pricing_expression.usage_unit,
                                "display_quantity": pricing_info.pricing_expression.display_quantity,
                                "tiered_rates": list(
                                    map(
                                        lambda tiered_rate: {
                                            "start_usage_amount": tiered_rate.start_usage_amount,
                                            "unit_price": {
                                                "currency_code": tiered_rate.unit_price.currency_code,
                                                "nanos": tiered_rate.unit_price.nanos,
                                            },
                                        },
                                        pricing_info.pricing_expression.tiered_rates,
                                    )
                                ),
                                "usage_unit_description": pricing_info.pricing_expression.usage_unit_description,
                                "base_unit": pricing_info.pricing_expression.base_unit,
                                "base_unit_description": pricing_info.pricing_expression.base_unit_description,
                                "base_unit_conversion_factor": pricing_info.pricing_expression.base_unit_conversion_factor,
                            },
                        },
                        sku.pricing_info,
                    )
                ),
                "service_provider_name": sku.service_provider_name,
                "geo_taxonomy": {
                    "type_": sku.geo_taxonomy.type_,
                    "regions": list(map(lambda x: x, sku.geo_taxonomy.regions)),
                },
            }
        )

    create_json(name_file, skus_data)


def create_json(name_file: str, list: list) -> None:
    os.makedirs("json", exist_ok=True)
    dir = "json/" + name_file + ".json"

    with open(dir, "w") as outfile:
        json.dump(list, outfile, indent=4)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
