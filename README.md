# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/MAO55555/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/MAO55555/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122/reward?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A deterministic, high-contrast, editorial broadsheet intelligence poster summarizing the verified world news of **SUNDAY, 22 NOVEMBER 2026**.

## Overview

The image synthesizes verified factual developments across 7 key regions and fields into an executive-level single-image briefing:
- **Climate / UN (Lead Story)**: UN COP31 climate negotiations in Antalya collapse without a final cover agreement after record two-day overtime; EU, Panama, and Marshall Islands reject draft text omitting fossil fuel phase-out language; COP31 president Murat Kurum and UN chief Guterres acknowledge diplomatic impasse.
- **Middle East / Gulf**: Iran's IRGC claims two commercial supertankers exploded after striking naval mines east of the Strait of Hormuz (unconfirmed Iranian claim; UKMTO reported incident in Gulf of Oman); nationwide rolling power cuts begin across Iran; Houthis claim strike on Saudi Rabigh oil refinery.
- **Europe / Ukraine**: Russian Shahed drone collapses a section of a five-storey residential building in Dymer near Kyiv (at least 6 killed, boy rescued from rubble); supermarket strike in Vyshneve kills two; regional day of mourning declared for Nov 23.
- **Africa**: RSF-blamed drone strikes hit Khartoum and Omdurman, killing 4 and damaging a UN facility with staff inside; Nigeria's Bayelsa boat disaster death toll rises to 29 with 50+ survivors.
- **Asia-Pacific**: France urges UN Security Council action following Myanmar military junta's formal rejection of the ICJ genocide ruling regarding the Rohingya; road access restored to Fukushima's snow-isolated Kitashiobara village (~1,000 residents).
- **Americas**: US Democrats secure 258+ House seats (largest congressional majority this century) as Chuck Hubbard is projected to defeat Rep. Virginia Foxx in NC-5; Florida's St. Johns River crests at major flood stage from Cocoa to DeLand.
- **Global Sport**: Max Verstappen wins the Las Vegas Grand Prix from pole position after 35 lead changes (Norris 2nd, Piastri 3rd); Carlos Alcaraz defeats Alexander Zverev 6-2, 7-6(7) in Turin to capture his first ATP Finals championship title.

## Image Specifications

- **Format**: PNG (magic bytes `89 50 4E 47 0D 0A 1A 0A`)
- **Dimensions**: Exactly 1024 × 1024 pixels
- **File Size**: ~500 KiB (strictly under the 1 MiB / 1,048,576 byte limit)
- **Determinism**: Baked at build time; byte-identical across multiple executions
- **Legibility**: Engineered with high-contrast color cards, tactical diagrams, and vector world map pins to ensure crisp legibility even when scaled down to 300px.

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
