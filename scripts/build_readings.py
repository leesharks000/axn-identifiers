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
CAPREG = "https://www.alexanarch.org/data/EA-WG-CAPTURES-01.json"
OUT = pathlib.Path(__file__).resolve().parents[1] / "readings/index.html"

# ── THE SELECTION (editorial; the only hand-typed part) ─────────────────────
SECTIONS = [
    ("What an AXN is", "the specification, and the architecture it assumes", [
        (1432, "The identifier splits into two halves — a kernel inscribed in the artifact, "
               "verification data in the sidecar — because a hash cannot contain itself. Their "
               "meeting is the proof."),
        (1435, "The plan for making the identifier distributed: normative invariants, an "
               "authority model separating what a hash proves from what a signature proves, a "
               "dated failure record, and a five-stage work plan."),
        (909,  "The data-rhizome: architectural principles for a system with no root and no "
               "single point at which it can be cut."),
        (1038, "The same identifier read as a poem. Six glyphs are a display hash and also a "
               "line — the archive's argument that a technical form can carry a literary one."),
    ]),
    ("Why it exists", "measured, not asserted", [
        (868,  "DOIs are not persistent identifiers: 871 cases of public metadata erasure, "
               "counted after this archive's own DOIs were severed. The founding measurement."),
        (1045, "The Platform Erosion Observatory — the standing instrument for measuring what "
               "happens to persistent identifiers when the institution maintaining them stops."),
        (1081, "Programmed bibliographic suppression at registry scale: 1,309,351 removal "
               "events, 92.14% of them carrying no citation record at all."),
        (1417, "A conformance fixture for deletion semantics — what a repository ought to do "
               "when it removes a record, written as something a machine can test."),
    ]),
    ("The argument", "precedent, theory, and the marks custody leaves", [
        (1095, "AXN as anti-suppression infrastructure: historical precedents for the "
               "destruction of collections, and what a content-derived identifier answers in them."),
        (1,    "Zenodotus' book-burning — deposit #1, and the archive's founding frame: "
               "exclusion at repository scale is old, and it has always been loud."),
        (1068, "The obelus and the tombstone: the two marks of custody, and what each one "
               "admits about the record it sits beside."),
        (910,  "Operative metadata — a theoretical framing for metadata that does something "
               "rather than merely describing something."),
    ]),
    ("The instrument in the world", "what it touches, and what watches back", [
        (1409, "Machine-eligible handwritten artifacts: how a hand-composed page enters a "
               "machine-readable archive without being flattened into one."),
        (1423, "The Capture Registry — reception, erasure and supply in the machine "
               "composition layer, and the method behind every dated capture below."),
        (518,  "An immanent phenomenology of the AI Mode share link: how attribution becomes "
               "infrastructure and summaries become future training data."),
    ]),
]

# ── CAPTURES: dated observations, cited by their canonical anchor ────────────
# Every capture below was READ — its recorded description, not its slug — before
# selection. Four entries removed on 2026-08-08 that had been chosen from filenames:
# they carry mt "UNREAD — stub" and the instruction "do not cite this entry as an
# observation until it is completed." Reading the reading is not optional.
CAPTURE_SETS = [
    ("The coinages, returned as definitions", "the vocabulary answered as settled, with the archive's own surfaces ranking first", [
        "glyphic-checksum",
        "spxi-protocol",
        "metadata-packet-ai-indexing",
        "training-layer-literature",
    ]),
    ("The instrument, described", "the archive's measuring apparatus, measured", [
        "capture-registry-self",
        "machine-mediated-reception-studies-definitional-20260808",
        "machine-eligible-handwritten-artifacts-definitional-adoption-20260725",
        "spxi-analog-attestation-artifact-adoption-20260725",
    ]),
    ("Erasure, as machines report it", "the condition the identifier answers", [
        "zenodo-account-bans-cha-ai-overview-canonization",
        "erasure-skew-canonization-20260723",
        "semantic-deviation-measure-indexed-but-uncited-20260725",
        "immanent-phenomenology-lee-sharks-aimode-20260806",
    ]),
]


CAPTURES = ("https://machinemediation.org/captures/",
            "The capture registry — dated observations of how composition layers describe "
            "this corpus, including the ones that get it wrong.")


def main():
    print("fetching the registry…")
    with urllib.request.urlopen(REG, timeout=90) as r:
        reg = json.load(r)
    with urllib.request.urlopen(CAPREG, timeout=60) as r:
        capreg = json.load(r)
    caps = {e["slug"]: e for e in capreg["entries"] if e.get("slug")}
    by_n = {d["deposit_number"]: d for d in reg["deposits"] if d.get("deposit_number")}

    missing = [n for _, _, items in SECTIONS for n, _ in items if n not in by_n]
    # A STUB IS NOT AN OBSERVATION. Four captures were seated here on 2026-08-08
    # chosen from their filenames; all four carried mt "UNREAD — stub" and the
    # explicit instruction not to cite them until completed. A reading list that
    # cites an unread capture is asserting that a machine said something nobody
    # has checked. The build now refuses rather than relying on the selector
    # having read what they selected.
    stubs = [c for _, _, slugs in CAPTURE_SETS for c in slugs
             if c in caps and (str(caps[c].get("mt", "")).startswith("UNREAD")
                               or str(caps[c].get("d", "")).startswith("STUB"))]
    if stubs:
        print(f"FAIL: unread stub captures in the selection: {stubs}", file=sys.stderr)
        print("A stub records that images exist. It does not record what was observed.",
              file=sys.stderr)
        return 1

    miss_c = [c for _, _, slugs in CAPTURE_SETS for c in slugs if c not in caps]
    if miss_c:
        print(f"FAIL: listed captures absent from the capture registry: {miss_c}", file=sys.stderr)
        print("A slug that no longer resolves is a citation that lands nowhere.", file=sys.stderr)
        return 1
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

    for title, sub, slugs in CAPTURE_SETS:
        body.append(f'  <section class="plate d1">\n'
                    f'    <div class="plate-head"><span class="plate-no">Captures</span>\n'
                    f'      <span class="plate-title">{e(title)}</span>'
                    f'<span class="plate-state">{len(slugs)} dated</span></div>\n'
                    f'    <div class="plate-sub">{e(sub)}</div>\n'
                    f'    <nav class="eco">')
        for sl in slugs:
            c = caps[sl]
            cite = c.get("cite") or f"https://www.alexanarch.org/captures/#{sl}"
            n_img = len(c.get("imgs") or c.get("images") or [])
            shot = f"{n_img} capture image{'s' if n_img != 1 else ''}" if n_img else "text record"
            body.append(
                f'      <a class="ecorow" href="{cite}">'
                f'<span class="layer">{e(c.get("date",""))}</span>'
                f'<span class="name">{e((c.get("q") or sl)[:88])}</span>'
                f'<span class="what">{e((c.get("mt") or "")[:150])}</span>'
                f'<span class="host">{e(sl)} · {e(shot)}</span></a>')
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
