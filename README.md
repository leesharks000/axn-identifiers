# AXN Identifiers — product surface

The public door for the AXN content-derived identifier system: stamp, verify, registry lookup, constitution.

**The archive is the authority; this is the door.** Canonical derivation (`scripts/axn_lib.py`), the central
registry (`data/axn-central-registry.json`), the AXN Constitution, and all governance live in
[leesharks000/alexanarch](https://github.com/leesharks000/alexanarch) and serve from **alexanarch.org**.
This repo carries only the axnidentifiers.org presentation surface and its design language.

- `index.html` — current live landing (migrated from alexanarch/axnidentifiers-site, 2026-08-06)
- `design/specimen-v0.1.html` — design language R1 ("The Critical Edition, Sealed", TACHYON)
- `design/specimen-v0.2.html` — R2, Kimi feedback integrated · **status: proposal, awaiting MANUS ratification**

Deploys via Vercel (static). Domains: axnidentifiers.org / .com — registration pending (see WAVE notes in
alexanarch data/workplan/).

Design laws (SIG·0 of the specimen): color is data (16 byte-cluster hues only) · one type family, three
voices · one mechanical interaction · no social proof · production self-hosts all assets · errors corrected
by amendment and tombstone, never silence.
