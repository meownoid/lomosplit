# Lomo Split

Utility for splitting LomoKino film scans.

![](https://habrastorage.org/webt/gw/d6/tl/gwd6tlto_wdpyidujmulm-i6elo.jpeg)

### Installation
```bash
git clone https://github.com/meownoid/lomosplit.git
cd lomosplit
python setup.py install
```

### Usage

Simple usage:
```bash
python -m lomosplit [INPUT_FOLDER]
```

Advanced usage:
```bash
python -m lomosplit -o output \
 --quiet \
 --template "picture_{idx:05d}" \
 --format png \
 --rotate-image left \
 --rotate-frame right \
 --frame-min-height 500 \
 --frame-max-height 900 \
 --adjust-to-max-height \
 [INPUT_FOLDER]
```