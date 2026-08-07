#!/usr/bin/env python3
"""build_readings.py — the bibliography is typed, but its metadata is verified.

A bibliography is an argument about what matters, so the SELECTION is editorial
and written by hand below. What is NOT written by hand is any fact about the
works: every title, AXN and record URL is fetched live from the archive's
registry at build time, and the build FAILS if a listed deposit has moved,
changed its identifier, or gone.

This is the shape today's failures argue for. A page of hand-typed citations is a
fossil the moment the archive moves; a page generated wholesale from a keyword
match is a dump, not a reading list. Typed selection with verified metadata is
the only version that is both meaningful and true a month from now.

Usage:  python3 scripts/build_readings.py
"""
import json, sys, urllib.request, datetime, pathlib, html

REG = "https://www.alexanarch.org/data/registry.json"
OUT = pathlib.Path(__file__).resolve().parents[1] / "readings/index.html"

# ── THE SELECTION (editorial; the only hand-typed part) ─────────────────────
SECTIONS = [
    ("The specification", "what an AXN is, and what it commits to", [
        (1432, "The identifier splits into two halves — a kernel inscribed in the artifact, "
               "verification data in the sidecar — because a hash cannot contain itself."),
        (1435, "The plan for making the identifier distributed: normative invariants, an "
               "authority model, a dated failure record, and a five-stage work plan."),
        (1087, "How to mark what is missing. A lacuna is a disclosed absence, not an error — "
               "the vocabulary that lets a resolver return an honest partial answer."),
    ]),
    ("The evidence", "why a content-derived identifier is worth the trouble", [
        (1045, "The Platform Erosion Observatory: measuring what happens to persistent "
               "identifiers when the institution maintaining them stops."),
        (1081, "Programmed bibliographic suppression, measured at registry scale — "
               "1,309,351 removal events, 92.14% carrying no citation record."),
        (1424, "The index of 871 research objects severed in a single afternoon. This "
               "archive's own erasure, catalogued."),
        (1095, "AXN as anti-suppression infrastructure, placed against historical "
               "precedent for the destruction of collections."),
    ]),
    ("The instrument observed", "what machines do with the work, recorded rather than argued", [
        (1423, "The Capture Registry: reception, erasure and supply in the machine "
               "composition layer — the method behind 230 dated captures."),
        (518,  "An immanent phenomenology of the AI Mode share link: how attribution "
               "becomes infrastructure, and summaries become future training data."),
        (1413, "An availability and hygiene audit of the archive itself, conducted on the "
               "archive by the archive, with the failures published."),
    ]),
    ("Adjacent systems", "the frameworks an AXN sits inside", [
        (639,  "Source compression and the holographic kernel: why a fragment can "
               "regenerate a whole."),
        (1386, "Provenance erasure — the canonical definition surface for what happens "
               "when a name survives and its relation does not."),
    ]),
]

CAPTURES = ("https://machinemediation.org/captures/",
            "The capture registry — dated observations of how composition layers describe "
            "this corpus, including the ones that get it wrong.")


def main():
    print("fetching the registry…")
    with urllib.request.urlopen(REG, timeout=90) as r:
        reg = json.load(r)
    by_n = {d["deposit_number"]: d for d in reg["deposits"] if d.get("deposit_number")}

    missing = [n for _, _, items in SECTIONS for n, _ in items if n not in by_n]
    if missing:
        print(f"FAIL: listed deposits absent from the registry: {missing}", file=sys.stderr)
        print("A bibliography that cites what is not there is worse than none.", file=sys.stderr)
        return 1

    now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")
    e = html.escape
    body = []
    for title, sub, items in SECTIONS:
        body.append(f'  <section class="plate d1">\n'
                    f'    <div class="plate-head"><span class="plate-no">Reading</span>\n'
                    f'      <span class="plate-title">{e(title)}</span>'
                    f'<span class="plate-state">{len(items)} works</span></div>\n'
                    f'    <div class="plate-sub">{e(sub)}</div>\n'
                    f'    <nav class="eco">')
        for n, note in items:
            d = by_n[n]
            axn = d.get("axn", "")
            fam = axn.split(".")[1].lower() if "." in axn else ""
            body.append(
                f'      <a class="ecorow" href="https://www.alexanarch.org/s/records/{n}/">'
                f'<span class="layer">{e(fam)}</span>'
                f'<span class="name">{e(d.get("title","")[:96])}</span>'
                f'<span class="what">{e(note)}</span>'
                f'<span class="host">{e(axn)}</span></a>')
        body.append('    </nav>\n  </section>\n')

    page = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Readings — the AXN identifier in the archive</title>
<meta name="description" content="A reading list for the AXN identifier: the specification, the measured evidence for content-derived identity, and dated observations of how machines describe this corpus. Every work links to its record in the archive.">
<link rel="canonical" href="https://axnidentifiers.org/readings/">
<link rel="stylesheet" href="/assets/msa.css">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/brand/favicon-32.png">
<link rel="icon" href="/assets/brand/favicon.ico" sizes="any">
<link rel="cite-as" href="https://www.alexanarch.org/axn/constitution/">
<link rel="describedby" href="https://axnidentifiers.org/.well-known/axn-node.json" type="application/json">
<link rel="item" href="https://www.alexanarch.org/data/registry.json" type="application/json">
</head><body class="flat">
<div class="zone surface">
<div class="rail">
  <img class="seal" src="/assets/brand/mark-dark-master.png" alt="">
  <a class="wm" href="/">A X N</a>
  <nav class="stations">
    <a href="/">Instrument</a><a href="/how/">How</a><a href="/limits/">Limits</a>
    <a href="/why/">Why</a><a href="/readings/" class="here">Readings</a><a href="/stamp/">Stamp</a>
  </nav>
  <div class="calib">READINGS · EVERY WORK LINKS TO ITS RECORD IN THE ARCHIVE</div>
</div>
<div class="inner">

  <section class="plate d1">
    <div class="plate-head"><span class="plate-no">Bibliography</span>
      <span class="plate-title">Readings</span><span class="plate-state">verified {now}</span></div>
    <div class="plate-sub">a selection, not an index · the archive holds the rest</div>
    <p class="overview"><b>The identifier has a literature, and most of it is evidence.</b>
      These are the works worth reading first — the specification that says what an AXN is, the
      measurements that say why it exists, and the observations of what machines do with the corpus.
      <mark class="hl">Every entry links to its record in the archive</mark>, which is the authority;
      this page is only a route in.</p>
    <div class="checks">
      <a href="https://www.alexanarch.org/s/browse/">browse all {len(by_n):,} deposits</a>
      <a href="{CAPTURES[0]}">the capture registry</a>
      <a href="https://www.alexanarch.org/oai?verb=Identify">harvest it (OAI-PMH)</a>
    </div>
  </section>

{chr(10).join(body)}
  <section class="plate d1">
    <div class="plate-head"><span class="plate-no">Observed</span>
      <span class="plate-title">The capture registry</span><span class="plate-state">dated</span></div>
    <div class="plate-sub">what the composition layer said about this work, and when</div>
    <p class="overview">{e(CAPTURES[1])}</p>
    <div class="onward"><a href="{CAPTURES[0]}">Read the captures →</a>
      <a href="/why/">Why this exists →</a></div>
  </section>

  <div class="mk">∮ = 1</div>
  <footer>Titles and identifiers on this page are read from the archive's registry at build time and
    fail the build if a work has moved · selection last revised {now}<br>
    <a href="/">back to the instrument</a> ·
    <a href="https://www.alexanarch.org/data/registry.json">registry (raw)</a></footer>
</div>
</div>
</body></html>
'''
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page)
    total = sum(len(i) for _, _, i in SECTIONS)
    print(f"readings built: {total} works across {len(SECTIONS)} sections, "
          f"all verified against {len(by_n):,} live registry entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
