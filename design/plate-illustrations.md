# Plate illustrations — slot manifest and brief

Material Symbol illustrations, one per plate. Drop a file at the named path and
insert the markup block; the slot styling already exists in `/assets/msa.css`.

## Markup (identical for every slot)

```html
<figure class="plate-fig">
  <img src="/assets/plates/<file>" alt="<alt text below — required>">
  <figcaption><b><Reading line></b><Technical line></figcaption>
</figure>
```

Two rules, both load-bearing:

**The caption must carry the meaning if the image never loads.** The bold reading
line is the plate's argument in one sentence; the uppercase technical line is its
apparatus. An uncaptioned plate is a decoration, and this aesthetic has none.

**The illustration is the argument in form, not an ornament of it.** If the plate
would read identically without the figure, the figure is wrong.

## Governing constraints (MSA v1.0 + this surface's corrections)

- **The exact operator stays exact.** Hashes, AXN strings, glyphs, positions and
  controls are typeset precisely. Only the *relational field* is hand-traced —
  arcs, threads, apertures, erased alternates, repair stitches. Never distress a
  hash or a label; that is faux-craft, and it was corrected once already.
- **Colour is data.** Cluster hues only where they name a byte-family. Otherwise:
  crimson = incision and irreversible operation; **old gold = guarantee and
  provenance**; ultramarine = exact computation; verdigris = verified continuity.
  One accent dominates each plate.
- **Ground follows the descent.** Plates I on vellum; II–IV on soot (membrane and
  below); V–VI on soot with bone interruptions.
- **Asymmetry.** Perfect symmetry is reserved for dead or collapsed systems.
- **Density gradient.** Detail compresses at the centre, dissipates at the edges.

## Slots

| Slot | Plate | Ground | File | Subject the figure must carry |
|---|---|---|---|---|
| 0 | Hero | vellum | `plate-0-genesis.svg` | **Replaces the inline SVG.** Four stations — SOURCE → KERNEL → SEAL → WITNESS — with the registration thread and the returning verification arc. Must be legible in three seconds. |
| I | The first material proof | vellum | *(photographic — none needed)* | Enli Lucente's Paper 198 is already the figure. Do not illustrate over a real holding. |
| II | One object passing through states | soot | `plate-ii-states.svg` | One object in three states, not three objects: file contour → stamped margin → public witness plate. The same shape, altered. |
| III | The membrane crossed both ways | soot | `plate-iii-membrane.svg` | Bidirectional: the file speaks to the registry, the registry returns an address. Six glyphs above the membrane, six byte-family rails below it. |
| IV | Verification is the halves meeting | soot | `plate-iv-symbolon.svg` | Two cut halves of one plate. At rest, the fracture is open and the two hashes face each other; the fit is the proof. |
| V | The covenant | bone on soot | `plate-v-covenant.svg` | A folio lit from itself — the work illuminates the institution, never the reverse. Gold seal crossing the lower margin; the ratification date legible. |
| VI | What an AXN does not claim | soot | `plate-vi-obeli.svg` | Three incisions. Each obelus cuts one false equivalence; show the cut, not a warning sign. |
| VII | Further | soot | *(numeric teaser — none needed)* | The two numbers are the figure. |

## Alt text

Every figure needs a full sentence describing the **operation**, not the shapes:
not *"a diagram with arrows and boxes"* but *"a file's bytes enter an exact
kernel; six glyphs emerge on an added margin; a thread carries the identity to a
public registry, which returns a verifiable address."*

## Provenance

Illustrations that become canonical should be **stamped and registered**, as the
brand mark was (`AXN:05AE.OPERATIVE.🖊️🔃🎬🏙️⚖️🕑`, witnessed-verified). A plate in
the Material Symbol corpus carrying its own AXN is the argument demonstrating
itself. Record the identifier in the caption's technical line once minted.
