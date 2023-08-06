# `unstac`

CLI tool for making GeoPackages from static
[STAC](https://stacspec.org) catalogs.

## Installation

```
pip install unstac
```

or

```
git clone https://gitlab.com/multione/unstac.git
pip install .
```

## Usage

```
$ unstac --help
                                                            
 Usage: unstac [OPTIONS] URL                                
                                                            
 Crawl through a static SpatioTemporal Asset Catalog from   
 URL and dump assets into GeoPackage                        
 --out-file defaults to a file named after the catalog      
 Title, in the working directory                            
 --workers defaults to number of available CPU threads      
                                                            
╭─ Arguments ──────────────────────────────────────────────╮
│ *    url      TEXT  [default: None] [required]           │
╰──────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────╮
│ --out-file        TEXT     [default: None]               │
│ --workers         INTEGER  [default: 16]                 │
│ --help                     Show this message and exit.   │
╰──────────────────────────────────────────────────────────╯
```

For example:

```
$ unstac https://s3.eu-central-1.wasabisys.com/stac/odse/catalog.json
parsing Open Environmental Data Cube Europe

```

## License

This project is licensed under the terms of the [MIT license](./LICENSE).
