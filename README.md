# bilibili-dynamic-archive

Monitors Bilibili user's dynamics, automatically fetching new updates and archiving them on the Internet Archive's Wayback Machine.

## Install

Install from `main` branch:

```shell
pip install -e .
```

## Run

Start archiving:

```shell
bili-archive BILIBILI_UID
```

Example:

```shell
bili-archive 1868902080
```

## Test

Run unit tests:

```shell
python -m unittest
```

## License

Licensed under the GNU General Public License v3.

Full text: [LICENSE](LICENSE)

## Attribution

* bac0id/save-page-now-api

    License: GNU General Public License v3

    https://github.com/bac0id/save-page-now-api
* Nemo2011/bilibili-api

    License: GNU General Public License v3 or later

    https://github.com/Nemo2011/bilibili-api
