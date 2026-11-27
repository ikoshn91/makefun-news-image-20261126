# The World in One Day — Thursday 26 November 2026

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/news-image-20261126)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node 22](https://img.shields.io/badge/Node-22-green)](https://nodejs.org)

Entry for the [make.fun](https://make.fun) bounty
[news-image-20261126](https://make.fun/bounty/news-image-20261126):
one image summing up the world's news of Thursday 26 November 2026.

## The image

A "World Frontpage": 40 dated stories across 10 regions, 13 illustrated
lead cards with vector scenes drawn in code, a UTC timeline strip, a world
map with numbered pins, per-story trust tags (OFFICIAL / REPORTED / CLAIM /
CONFIRMED) with a HOW SURE legend, a big-numbers strip, and a DATE CHECK box
listing other-days' stories that were left out.

Top stories: Kyiv hit by missiles and drones · Gaza strikes kill nine ·
Cairo tanker inferno toll reaches 31 · Bears stun Lions 39–35 on
Thanksgiving · Eagles stun Cowboys 39–38.

## How it is built

`gen_image.py` (Python + Pillow, run locally) draws `entry.png`
(1024×1024, deterministic — two runs write identical bytes).
`main.ts` (Node 22, standard library only, no network) copies `entry.png`
to the output directory.

```sh
python3 gen_image.py entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
