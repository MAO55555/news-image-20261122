# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/MAO55555/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/MAO55555/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A deterministic, high-contrast, editorial broadsheet intelligence poster summarizing the verified world news of **SUNDAY, 22 NOVEMBER 2026**.

## Overview

The image synthesizes verified factual developments across 7 key regions and fields into an executive-level single-image briefing:
- **Middle East / Gulf**: Bahrain air defenses intercept Iranian drone & missile strikes; commercial oil tankers hit near the Strait of Hormuz; US CENTCOM firmly refutes claims of a downed F-16; Qatar facilitates emergency mediation in Tehran; displaced Palestinians protest Israeli strikes along the Gaza 'Yellow Line'.
- **Climate / COP31 (Antalya)**: UN COP31 summit pushes into a second day of unscheduled overtime as ~200 nations deadlock over fossil fuel phase-out language and climate finance mechanisms on a third draft text.
- **Europe / Baltic & NATO**: Russian military-linked cargo vessel *Sparta II* catches fire after a drone strike in the Gulf of Finland (16 crew safely evacuated); NATO Sec-Gen Mark Rutte pledges to defend "every inch" of Poland; Brussels Airport warns of flight cancellations ahead of a national ATC strike.
- **UN / Geneva**: Disarmament negotiations fail to reach a binding prohibition on lethal autonomous weapons systems ('killer robots'), agreeing to a 2-year diplomatic timetable extending to 2028.
- **Asia-Pacific**: Magnitude-7.2 earthquake off Indonesia's Maluku (no tsunami threat); International Court of Justice (ICJ) rules Myanmar committed genocide against the Rohingya; heavy mountain snowfall isolates 1,000+ residents in Fukushima, Japan.
- **Americas / Extreme Weather**: Relentless storms spark historic St. Johns River flooding in Central Florida, triggering urgent evacuation warnings.
- **Global Sport**: Max Verstappen takes pole position ahead of George Russell at the Las Vegas Grand Prix (04:00 UTC Nov 22) after Kimi Antonelli is penalized to P6; Carlos Alcaraz faces Alexander Zverev in the ATP Finals championship match.

## Image Specifications

- **Format**: PNG (magic bytes `89 50 4E 47 0D 0A 1A 0A`)
- **Dimensions**: Exactly 1024 × 1024 pixels
- **File Size**: ~500 KiB (strictly under the 1 MiB / 1,048,576 byte limit)
- **Determinism**: Baked at build time; byte-identical across multiple executions
- **Legibility**: Engineered with high-contrast color cards, tactical radar diagrams, and vector world map pins to ensure crisp legibility even when scaled down to 300px.

## How to Run

Requirements: Node.js 22+ (standard library only, no external dependencies or network required).

```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

To re-bake the image from source:

```bash
python3 scripts/generate_image.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=7j61hdbp&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
