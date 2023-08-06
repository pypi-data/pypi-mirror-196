from dataclasses import dataclass
from io import StringIO
from itertools import groupby
from multiprocessing.pool import ThreadPool
from typing import List, Tuple
from xml.dom import minidom

import requests
from numpy import arange
from owslib.csw import CatalogueServiceWeb
from owslib.iso import CI_OnlineResource, CI_ResponsibleParty, MD_Metadata


@dataclass
class CopernicusMarineDatasetService:
    protocol: str
    uri: str


@dataclass
class CopernicusMarineProductDataset:
    dataset_id: str
    services: List[CopernicusMarineDatasetService]


@dataclass
class CopernicusMarineProductProvider:
    name: str
    roles: List[str]
    url: str
    email: str


@dataclass
class CopernicusMarineProduct:
    title: str
    product_id: str
    thumbnail: str
    description: str
    providers: List[CopernicusMarineProductProvider]
    created: str
    bbox: List[float]
    temporal_extent: List[str]
    keywords: List[str]
    datasets: List[CopernicusMarineProductDataset]


@dataclass
class CopernicusMarineCatalogue:
    products: List[CopernicusMarineProduct]


ENDPOINT = (
    "https://cmems-catalog-ro.cls.fr"
    + "/geonetwork/srv/eng/csw-MYOCEAN-CORE-PRODUCTS"
)
COUNT_ENDPOINT = (
    ENDPOINT
    + "?SERVICE=CSW&REQUEST=GetRecords&VERSION=2.0.2&resultType=hits"
    + "&outputFormat=application/xml"
)


def count_products() -> int:
    """
    Retrieve max number of datasets in csw from csw node
    """
    xml_file = requests.get(COUNT_ENDPOINT, allow_redirects=True)
    csw_header = minidom.parse(StringIO(xml_file.text))
    root = csw_header.documentElement
    search_results = root.getElementsByTagName("csw:SearchResults")[0]
    nproduct_tot = search_results.getAttribute("numberOfRecordsMatched")
    return int(nproduct_tot)


def parse_catalogue() -> CopernicusMarineCatalogue:
    def get_csw_records(slicing_tuple: Tuple[int, int]) -> List[MD_Metadata]:
        """
        Launch csw requests in parallel and gather all results in list
        """
        ndatasets, start_position = slicing_tuple
        csw = CatalogueServiceWeb(ENDPOINT, timeout=60)
        csw.getrecords2(
            esn="full",
            outputschema="http://www.isotc211.org/2005/gmd",
            startposition=start_position,
            maxrecords=ndatasets,
        )
        csw_records: List[MD_Metadata] = csw.records.values()
        return csw_records

    pool = ThreadPool()
    nproduct_per_page, nproduct_tot = 10, count_products()
    start_positions = arange(1, nproduct_tot, nproduct_per_page, dtype=int)
    results = pool.map(
        get_csw_records,
        zip([nproduct_per_page] * len(start_positions), start_positions),
    )
    products: List[CopernicusMarineProduct] = [
        product
        for csw_records in results
        for product in list(map(record_to_product, csw_records))
    ]
    return CopernicusMarineCatalogue(
        products=sorted(products, key=lambda product: product.title)
    )


def record_to_product(csw_record: MD_Metadata) -> CopernicusMarineProduct:
    return CopernicusMarineProduct(
        title=csw_record.identification.title,
        product_id=csw_record.identification.alternatetitle,
        thumbnail=csw_record.identification.graphicoverview[0],
        description="".join(csw_record.identification.abstract),
        providers=get_providers(csw_record),
        created=get_created(csw_record),
        bbox=get_bounding_box(csw_record),
        temporal_extent=get_temporal_extent(csw_record),
        keywords=get_keywords(csw_record),
        datasets=record_datasets(csw_record.distribution.online),
    )


def get_created(csw_record: MD_Metadata) -> str:
    return csw_record.identification.date[0].date


def get_bounding_box(csw_record: MD_Metadata) -> List[float]:
    return [
        csw_record.identification.extent.boundingBox.minx,
        csw_record.identification.extent.boundingBox.miny,
        csw_record.identification.extent.boundingBox.maxx,
        csw_record.identification.extent.boundingBox.maxy,
    ]


def get_temporal_extent(csw_record: MD_Metadata) -> List[str]:
    return [
        csw_record.identification.temporalextent_start,
        csw_record.identification.temporalextent_end,
    ]


def get_keywords(csw_record: MD_Metadata) -> List[str]:
    return list(
        map(
            lambda keyword: keyword.thesaurus["title"],
            csw_record.identification.keywords2,
        )
    )


def get_providers(
    csw_record: MD_Metadata,
) -> List[CopernicusMarineProductProvider]:
    def to_provider(
        responsible_party: CI_ResponsibleParty,
    ) -> CopernicusMarineProductProvider:
        return CopernicusMarineProductProvider(
            name=responsible_party.organization,
            roles=[responsible_party.role],
            url=responsible_party.onlineresource,
            email=responsible_party.email,
        )

    return list(map(to_provider, csw_record.identification.contact))


def record_datasets(
    online_resources: List[CI_OnlineResource],
) -> List[CopernicusMarineProductDataset]:
    online_resources_by_name = groupby(
        online_resources, lambda online_resource: online_resource.name
    )

    def to_service(
        online_resource: CI_OnlineResource,
    ) -> CopernicusMarineDatasetService:
        return CopernicusMarineDatasetService(
            protocol=online_resource.protocol, uri=online_resource.url
        )

    def to_dataset(
        item: Tuple[str, CI_OnlineResource]
    ) -> CopernicusMarineProductDataset:
        return CopernicusMarineProductDataset(
            dataset_id=item[0],
            services=sorted(
                map(to_service, item[1]), key=lambda service: service.protocol
            ),
        )

    return sorted(
        map(to_dataset, online_resources_by_name),
        key=lambda dataset: dataset.dataset_id,
    )
