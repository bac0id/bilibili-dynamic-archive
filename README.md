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
