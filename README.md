# Friday 20 November 2026: 50 stories, 7 regions, 16 illustrated, date-checked

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/dunoil/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/dunoil/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One 1024x1024 newspaper page summing up the world's news of Friday 20 November 2026:
50 stories, 7 regions, 16 illustrated cards, 34 numbered briefs, every illustrated
story pinned on a world map. Built for the make.fun news-image-20261120 bounty
($250 in prizes, paid in USDC on Solana).

## What's on the page

- **Lead stories:** Cyclone Akvan strikes the Odisha coast with 300,000 evacuated;
  Trump puts the Iran decision off until 2027 as the Senate rejects war powers
  curbs 51 to 48; Europe says it is ready to talk to Russia after the Berlin
  summit; COP31 closes in Antalya with a $305bn adaptation gap.
- **Illustrated cards:** APEC in Shenzhen with Albanese meeting Xi, the Crimean
  Bridge hit a third time, a Houthi missile hitting Riyadh's PIF Tower, the US
  and Venezuela restoring military ties, Yongbyon enrichment, Seoul's top court
  overturning ex-PM Han's term, Fiji's national disaster, the Sensex jumping
  989 points, Nicholls 113 not out in Wellington, Google shipping Gemini 4
  Neon, Iran's remaining missiles, and gold near $3,614.
- **The day in UTC:** an eight-point timeline from gold at $3,614 to Trump's
  Iran announcement, plus region and field bars and a Day in Numbers strip
  (300,000 evacuated, 989 Sensex points, $305bn, 113 not out, $3,614, 2,500).
- **Date check:** a footer names five stories first reported Thursday
  19 November (the ICJ Myanmar ruling, Anthropic's IPO debut, the Shenzhen
  trilateral declaration, GTA VI release day, the Jeffries Speaker nomination)
  that are deliberately NOT presented as Friday's news.
- **Craft:** serif masthead and mixed-case serif headlines throughout, no pixel
  font, supersampled gradients, deterministic render (two runs byte-identical).

## How it is made

`render.py` draws the whole page from scratch with Pillow: every scene is
procedural vector art (cyclone spiral, skylines, bridge, tower, atom, cricket
oval, gold bars), the layout is computed from the story data, and the PNG is
rendered at 2x and downscaled. `main.ts` validates the image (PNG magic,
1024x1024, at most 1 MiB) and copies it to the output directory.
