import json
import multiprocessing as mp
import time
import warnings
from pathlib import Path
from typing import Iterable, Union

import geopandas as gp
import pystac
import rich
import shapely.geometry as shpg
from rich.console import Console

COLLECTION_FIELDS = (
    "id",
    "title",
    "description",
    "providers",
    "keywords",
    "license",
)


def serialize_ogr_unfriendlies(data: dict) -> dict:
    for k, v in data.items():
        if isinstance(
            v,
            (
                Iterable,
                dict,
            ),
        ):
            data[k] = json.dumps(v)
    return data


def retry_resource_from_error(
    err: Union[str, Exception],
    iteration: int = 0,
    max_retries: int = 10,
    delay_seconds: float = 0.5,
) -> Union[pystac.Item, pystac.Collection]:
    if isinstance(err, Exception):
        err = str(err)

    stac_file, *__ = filter(
        lambda s: s.endswith(".json"),
        err.split(),
    )

    print(f"retrying {stac_file} {iteration+1}/{max_retries}")

    try:
        return pystac.Item.from_file(stac_file)

    except Exception as e:
        if iteration == max_retries:
            warnings.warn(f"max ({max_retries}) retries reached")
            raise e

        time.sleep(delay_seconds)
        return retry_resource_from_error(
            stac_file,
            iteration=iteration + 1,
            max_retries=max_retries,
            delay_seconds=delay_seconds,
        )


def explode_item(
    item: pystac.Item,
    **collection_metadata: dict,
) -> list[dict]:
    _item = item.properties | {
        "item_id": item.id,
        "item_bbox": item.bbox,
    }
    _item = serialize_ogr_unfriendlies(_item)
    _item["geometry"] = shpg.shape(item.geometry)
    return [
        _item
        | serialize_ogr_unfriendlies(asset.to_dict())
        | {"asset_id": asset_id}
        | collection_metadata
        for asset_id, asset in item.get_assets().items()
    ]


def explode_collection(
    col: pystac.Collection,
) -> list[dict]:
    assets = []
    _items = col.get_items()
    _col = col.to_dict()
    collection_metadata = {
        f"collection_{field}": _col[field] for field in COLLECTION_FIELDS
    }
    collection_metadata = serialize_ogr_unfriendlies(collection_metadata)
    while True:
        try:
            item = next(_items)

        except StopIteration:
            return assets

        except Exception as e:
            warnings.warn(str(e))
            item = retry_resource_from_error(e)

        assets += explode_item(item, **collection_metadata)


def collections_with_retry(cat: pystac.Catalog) -> Iterable[pystac.Collection]:
    cols = cat.get_collections()
    while True:
        try:
            yield next(cols)

        except StopIteration as e:
            break

        except Exception as e:
            warnings.warn(str(e))
            yield retry_resource_from_error(e)


def catalogue2gpkg(
    url: str,
    out_file: str = None,
    workers: int = mp.cpu_count(),
):
    """
    Crawl through a static SpatioTemporal Asset Catalog from URL and dump assets into GeoPackage

    --out-file defaults to a file named after the catalog Title, in the working directory

    --workers defaults to number of available CPU threads
    """
    cat = pystac.Catalog.from_file(url)
    rich.print(f"parsing [italic]{cat.title}[/italic]")

    out_file = out_file or cat.title.lower().replace(" ", "_") + ".gpkg"
    out_file = Path(out_file)

    all_assets = []

    console = Console()

    with console.status("working...") as status:
        with mp.Pool(workers) as pool:
            for i, assets in enumerate(
                pool.imap_unordered(
                    explode_collection,
                    collections_with_retry(cat),
                ),
            ):
                all_assets += assets
                status.update(f"found {i+1} collections, {len(all_assets)} assets")

        status.update("writing dataset to GPKG")
        df = gp.GeoDataFrame(all_assets)
        df.to_file(out_file, driver="GPKG")
        console.print(
            f"catalogue ({len(all_assets)} assets) dumped to {out_file.absolute()}"
        )


def main():
    import typer

    typer.run(catalogue2gpkg)
