# DIY build guide: Shore 40A silicone

This is a **proposed prototype workflow**, derived from the current rev7 CAD. A documented physical casting, print profile, socket-fit trial, and Shore 40A performance test have not been established. Review [validation](validation.md) before buying materials or printing. This is a two-part silicone pour-and-cure process; the older industrial LSR quote workflow is not the DIY process.

The intended application is cable routing and management underneath a desk. The rigid panel attaches to the desk underside using mounting adhesive, with the silicone units facing downward. The owner has identified the materials used below; this records their selection without claiming a documented load, adhesion or durability test.

### Owner-used materials

| Material | Owner-provided product link | Documentation status |
| --- | --- | --- |
| Silicone | [BBDINO 40A clear silicone kit, ASIN B0FHHBGSQK](https://www.amazon.com/dp/B0FHHBGSQK) | Matches the manufacturer's 1.1 kg / 2.42 lb 40A clear product; nominal manufacturer specifications and remaining documentation gaps are below. |
| Panel mounting adhesive | [Mounting tape, ASIN B0FPQ3VWPB](https://www.amazon.com/dp/B0FPQ3VWPB) | Owner-reported panel adhesive; confirm exact tape grade, supplied dimensions and application instructions from its packaging/manufacturer. |

Links were checked on 2026-09-19 and have shopping-history/tracking parameters removed. These are product references, not affiliate links or evidence of supplier endorsement. Verify the supplied variant and batch; a marketplace listing is not a substitute for a matching technical datasheet or SDS.

The adhesive listing needs clarification: its selected title/variant says 0.39 inch × 10 feet, while shared details mention 2 inch / 50 mm width. The title invokes 3M, but the brand/manufacturer fields identify P7yaumy, and the title and bullets disagree on removable versus permanent bonding. Treat this as the owner's exact purchase reference, not a verified 3M grade. Measure the actual roll and confirm packaging/instructions before sizing the planned slits or specifying installation conditions. No attributable manufacturer instructions were located for this tape during this review. [Owner-linked tape listing](https://www.amazon.com/dp/B0FPQ3VWPB)

## 1. Choose a matched set

Use the root [rev7 source](../system_rev7_perforated_score.scad), the configuration in [parameters](parameters.md), and the regenerated exports listed in [validation](validation.md). Do not combine the original root-level STLs, quote-package files, or differently sized exports with this set. A filename or a comment that a lid was printed does not establish matching dimensions.

**Current gate:** the regenerated center-piece STL has zero-area triangles and is withheld from the printable-download list. Resolve and validate that export before a full build; the following is a proposed procedure for a complete matched set, not a claim that all required print files are cleared.

The default model has 16 units in a 4 × 4 array. Each unit has a nominal 22 × 22 mm rounded-square pad, 3 mm pad thickness, 16 mm overall height, a 9 mm center column, and **eight curved support fins**. The distinct attachment post has **four small alignment ribs**. Unit pitch is 23.4 mm in both directions. Dimensions are millimeters; STL does not encode units, so verify the slicer imports millimeters without scaling.

| Part | Quantity | Purpose / source mode |
| --- | ---: | --- |
| Center piece (export withheld) | 1 | Printed cavity tooling; source mode `center_piece`; resolve [mesh issue](validation.md) first |
| [Top lid](../exports/rev7-default/top_lid.stl) | 1 | Printed tooling carrying socket-forming ball cores; `top_lid` |
| [Bottom lid](../exports/rev7-default/bottom_lid.stl) | 1 | Printed pad-face closure; `bottom_lid` |
| [Rigid panel](../exports/rev7-default/panel.stl) | 1 | Separate final component carrying attachment posts; `panel` |
| Owner-linked BBDINO 40A two-part silicone | Trial, then measured batch | Product link above; manufacturer instructions, quantity and compatibility still require verification |
| Owner-linked panel mounting tape | Amount/layout to establish in a mounting trial | Applies to the rigid panel back and desk underside; not silicone or mold assembly |
| M6 × 45 mm fully threaded bolts, 1 mm pitch | 4 | Calculated candidate, under-head length; see below |
| Matching M6 nuts, 5 mm thick for this calculation | 4 | External nuts; no modeled nut traps |
| M6 flat washers, 6.4 mm ID × 12 mm OD × 1.6 mm thick | 8 | One under each bolt head and one under each nut |

Also prepare a suitable printer and slicer, calipers, matched tools for the fasteners, a stable protected work surface, compatible mixing containers and stirrers, the measuring equipment specified by the chosen silicone, a timer, a blunt opening spatula, trimming tools, and the PPE required by the materials' safety data sheets. Surface sealer and release treatment depend on compatibility and trial results. BBDINO calls for vacuum degassing for this product; suitable equipment and its detailed procedure must be established before mixing.

The panel is not part of the silicone mold. The `silicone_positive` mode is an external-shape reference: **it contains no subtracted socket** and is neither the finished silicone part nor a print required for assembly. There are no printed female receivers, carrier array, carrier holes, retaining clips, or block ejector inserts in this bill of materials.

### Bolt length and clearance

The source creates four aligned **6.7 mm CAD clearance holes**, not M6 threads. Their centers are at X/Y = ±54.45 mm. The nominal closed mold thickness at those holes is:

```text
bottom lid body + center body + top lid body = 8 + 16 + 8 = 32 mm
required under-head length = closed stack + washers + nut thickness + projection
                          = 32 + (2 × 1.6) + 5 + 2 = 42.2 mm
candidate standard length = 45 mm
nominal projection beyond the 5 mm nut = 45 − 32 − 3.2 − 5 = 4.8 mm
```

Nut thickness must be **added** to the required bolt length: the nut sits outside the stack and occupies threaded length. A formula subtracting nut thickness would under-size the bolt. The 2 mm projection is a calculation allowance, not a tested engagement requirement. The seating walls nest into the center piece, so their 3 mm height is not added again.

Candidate dimensions are supported by the [Accu M6 × 45 DIN 933 bolt specification](https://www.accu.co.uk/full-thread-hexagon-bolts/18876-SEBF-M6-45-A2), [Würth M6 DIN 934 nut specification](https://eshop.wuerth.de/Hexagon-nut-DIN-934-steel-I6I-I8I-plain-NUT-HEX-DIN934-I8I-WS10-M6/03106.sku/en/US/EUR/), and [Würth ISO 7089 washer dimensions](https://eshop.wuerth.de/-/515002106.sku/de/DE/EUR/). These are dimensional references, not a procurement requirement or supplier endorsement. Different nut standards and washer variants can change the length calculation; measure the actual hardware.

At each lid's outer face, the hole center is 8.85 mm from the start of the 2 mm outer bevel. A 12 mm washer leaves 2.85 mm of nominal flat material beyond its outside edge. A 10 mm-across-flats hex head/nut has an approximately 11.55 mm corner envelope, within that washer diameter. The geometry provides nominal footprint clearance; printer tolerances, washer centering, surface flatness, tool access, bearing strength, and actual hardware fit still need a dry-fit check. Do not add countersinks or nut traps. No clamping torque is validated.

## 2. Print and inspect

These are orientation suggestions to evaluate in a slicer, not tested settings. Printer, print material, nozzle, layer height, support process, and demonstrated mold lifetime are not established.

| Component | Suggested starting orientation | What to inspect before printing |
| --- | --- | --- |
| Top lid | Rotate so its broad exterior face is on the bed; posts and seating wall point upward | The exported lowest-Z surface is the core tips, not a useful default build face. Inspect ball undersides and thin ribs; supports must be removable without changing socket-forming surfaces. |
| Bottom lid | Broad exterior face on bed; seating wall upward | Preserve the flat pad-contact face, seating wall, and external opening bevels. |
| Center | Evaluate narrow column-side openings toward the bed and broad pad openings upward | Inspect every internal overhang and both bleed trenches. All support must remain accessible through the openings; reject a strategy that traps support or scars inaccessible cavity surfaces. |
| Panel | Flat back on bed, posts upward | Inspect the same ball undercuts and ribs as the top lid, plus flatness of the 2 mm panel base. |

Check mold footprint 130.6 × 130.6 mm, center thickness 16 mm, each lid body 8 mm, panel footprint 94.6 × 94.6 mm, 23.4 mm post pitch, nominal 5 mm ball diameter, 1.6 mm stem diameter, 0.6 mm rib thickness, and 4.6 mm rib outside diameter. Nominal post reach from its contact surface is 8.1 mm; see [validation](validation.md) for triangulated-mesh bounds.

Remove support remnants and loose debris. Inspect the 1.2 mm support-fin cavity features, post surfaces, seams, holes, and seating walls for damage or unintended blockage. Smoothness on the tooling becomes texture on the casting. Any coating changes dimensions; evaluate it on a trial first. Printed walls and parting faces are not assumed liquid-tight.

## 3. Dry-fit the stack and understand its faces

![CAD render of the three mold pieces separated vertically](../assets/images/mold-exploded-cad.png)

*CAD render, not a physical build: socket-core lid above the center piece, pad-face lid below. The upper lid's cores face downward and are mostly hidden by its body in this view. Scoring is disabled.*

The assembly coordinate system is useful even though each export has been moved onto Z ≥ 0:

```text
                       TOP LID: broad exterior faces upward
                       ball cores and seating wall point DOWN
center upper face z=16  narrow column/fins openings; sockets form here
                       silicone cavity, with pad at lower end
center lower face z=0   broad rounded-square PAD openings
                       BOTTOM LID: contact face and wall point UP
                       broad exterior faces downward
```

Seat the bottom lid's wall into the center's lower peripheral trench; align all four holes. Lower the top lid with its cores centered in the upper openings and its wall entering the upper trench. Each lid wall is nominally 2.6 mm wide in a 3 mm trench, with 0.2 mm modeled clearance on each side and **no extra nominal depth clearance**. Confirm full seating without force. Neither lid's wall height belongs on top of the closed 32 mm bolt-line stack.

Fit all bolts, washers, and nuts. Confirm each bolt passes freely, washers lie flat, threads project beyond the nuts, and the broad parting lands meet uniformly. Do not use bolt force to correct interference, warped faces, or blocked wall seats. Record any printer-dependent clearance problem before considering a separately reviewed geometry change.

Both center faces have peripheral overflow/bleed trenches. They are largely occupied by the seating walls when closed. The model does not contain a dedicated injection port or an independently validated vent network; the trenches are separated from the cavities by mold-face land. Do not assume a ring-shaped trench guarantees that trapped air can escape.

## 4. Select the material and run a small trial

**Shore 40A is the target cured hardness, not a complete formulation.** The owner uses the BBDINO product linked above. Its identity resolves the earlier product-selection gap; it does not validate its behavior in this mold. Do not substitute an older hardness, sealant, caulk, or urethane.

The [official BBDINO 40A product page](https://bbdino.com/products/bbdino-40a-clear-silicone-mold-making-trial-kit-gp-platinum-cure-high-hardness) reports the nominal specifications below. These are manufacturer product-page statements, not project measurements. A matching 40A TDS/SDS was not located through the [official downloads page](https://bbdino.com/pages/documents-download) during this review. Obtain the current documents for the delivered product and complete the unresolved fields before mixing:

| Required material/process information | Status |
| --- | --- |
| Product identity | Owner-linked BBDINO 40A clear silicone kit, ASIN B0FHHBGSQK; confirm delivered variant/batch |
| Nominal hardness / chemistry | Manufacturer page: Shore A 40 ± 2, platinum cure; suitability for this casting geometry requires trial |
| A:B ratio and measurement basis | Manufacturer page: 1A:1B by weight or volume; confirm supplied instructions and use one consistent measurement basis |
| Working time | Manufacturer page: about 30 minutes around 23°C; full mixing/pre-mixing method and batch limits require selected manufacturer's technical datasheet |
| Cure/demold time and any post-cure | Manufacturer page: about 3 hours cure around 23°C; demold criteria, temperature limits and post-cure require selected manufacturer's technical datasheet |
| Density, shrinkage and expected viscosity | requires selected manufacturer's technical datasheet |
| Print/coating compatibility; sealer and release products/procedure | requires selected manufacturer's technical datasheet |
| Vacuum degassing | Manufacturer page calls for vacuum degassing; equipment, procedure and timings require selected manufacturer's technical datasheet |
| PPE, ventilation, spill response, storage and disposal | requires selected manufacturer's technical datasheet **and safety data sheets for both parts and all treatments** |

Read the current official technical and safety documents for this BBDINO product. The Smooth-On references below provide general handling examples; their recipes are not instructions for BBDINO. The [Smooth-On document library](https://www.smooth-on.com/documents/) illustrates the separate technical-bulletin and SDS records to obtain.

Clean and fully prepare a small sample of the actual print material using the intended surface finish, coating, and release treatment. Cure a small silicone sample against it before committing to the mold. Check for tackiness, adhesion, coating transfer, and dimensional change. Surface contamination or treatment can inhibit cure, and a sealer is not a universal fix. [Smooth-On cure-inhibition guidance](https://www.smooth-on.com/support/faq/104/)

For the casting trial and subsequent batches, clean the actual cavity faces, both lids and every socket core using the compatible method established in the sample test. Apply any required sealer/release treatment according to its official instructions, including drying or curing time, and repeat the dry-fit after treatment. Avoid pooled treatment that obscures fine features. Release choice depends on the contacting materials; the sample result and selected product instructions govern this mold. [Manufacturer release guidance](https://support.smooth-on.com/knowledgebase.php?article=49)

After that compatibility check, cast **one existing cavity** with the full matched mold stack and trial demolding and attachment to one panel post. This reduces the batch while keeping the actual geometry. Assess complete pad/fin fill, socket/rib detail, leakage, and whether Shore 40A can stretch off the core and onto the panel without tearing or breaking a post. Do not interpret a successful cure coupon as proof of socket fit or full-array fill.

## 5. Measure and mix

Prepare the dry-fitted tooling and open-fill work area before combining components. Use the ventilation, eye protection, gloves and other precautions required by the selected SDS; glove material can itself affect compatibility, as illustrated by [Smooth-On's silicone handling instructions](https://www.smooth-on.com/products/smooth-sil-940/). Do not adopt that example product's temperatures, ratios or timings unless it is the product actually selected.

Measure A and B using one consistent measurement basis and a ratio explicitly permitted by the selected product. Confirm the supplied BBDINO instructions before using either advertised 1:1 option. Follow the product's mixing method and include the container sides and bottom; do not guess the ratio or extend working time with undocumented additives. [General manufacturer mixing guidance](https://support.smooth-on.com/knowledgebase.php?article=43)

BBDINO's linked product page calls for vacuum degassing. Obtain its detailed procedure and use purpose-built equipment according to its instructions, within the working time and with the prescribed expansion space. Degassing the mixture does not solve a blocked cavity air path. No pressure process or improvised pressure equipment is specified here. [General manufacturer explanation of degassing](https://support.smooth-on.com/knowledgebase.php?article=47)

### Quantity

Do not use the volume of the unsocketed `silicone_positive` export as the final material requirement. The calculation must use validated cavity solids and subtract the **intersection** of the socket-forming ball, stem, and four ribs with those cavities:

```text
net unit volume = cavity volume − volume displaced inside cavity by lid cores
batch volume = net unit volume × cavities filled
             + measured intentional overflow/flash volume + measured handling loss
batch mass = batch volume × selected product's documented mixed density
```

A temporary analysis of the unchanged source modules produced valid closed meshes for one positive unit and for `silicone_unit()` minus `ball_snap_post()`. The positive volume was 2,388.779 mm³; subtracting 85.209 mm³ of core intersection gives **2,303.570 mm³ (2.304 mL) per nominal socketed unit**, or **36.857 mL for 16**. This is a geometric part-volume estimate at the default tessellation, not a complete mixing quantity. It does not yet include cavity face-relief details, overflow, flash, or handling loss. See [validation](validation.md) for method and limits.

**TODO before a full batch:** account for the actual closed cavity's face relief, then measure overflow and mixing-container loss in the trial. The perimeter trench's gross volume is not the overflow allowance because the seating wall displaces most of it. No density, shrinkage correction, percentage allowance, or mass estimate is assumed. Record the trial's actual batch and leftover quantity for the next build.

## 6. Fill while open, then close and cure

The following sequence is inferred from cavity orientation and needs a physical trial:

1. Set the bottom lid exterior-down on a stable level surface. Seat the center with broad pad cavities down against that lid and narrow column openings upward. Leave the top lid off.
2. With the column-side mouths **open to the air**, fill the selected cavity or cavities with the mixed silicone. Work slowly enough to let displaced air return through the still-open mouths. Check the lower pad regions and eight fin cavities in the trial; a full-looking mouth does not prove these regions filled.
3. Lower the top lid evenly with its ball cores pointing down into the filled cavities. Air and excess silicone need to leave across the still-open parting gap **before** the lands and seating walls close. Do not immediately tighten the bolts or force a lid that resists seating. Stop the trial if the seating wall closes the available escape route too early, or if trapped air/leakage prevents complete fill; document the defect for a separate design review.
4. Once seating is confirmed, fit the four fastener sets and bring them up gradually and evenly in a diagonal sequence. Use only enough force to keep the verified faces seated; no torque specification is available. Watch for bowing and washer indentation. Do not pour into the completely sealed assembly.
5. Leave the stack supported and undisturbed for the selected product's specified cure under its specified conditions. Do not accelerate cure with unvalidated heating of printed tooling. Follow any required post-cure after confirming material and tooling compatibility.

## 7. Open and demold

After the specified cure, remove all nuts, washers and bolts. A proposed removal sequence is to support and invert the closed stack so the **top lid's broad exterior rests downward** and the pad-side bottom lid faces upward. Use the outer edge bevel as a lead-in for a blunt spatula to separate the bottom lid gently; keep the tool away from cavities, ribs and sealing lands.

The broad pads must exit through the **broad pad-side openings**. With the center and top lid supported, progressively free one pad and its fins, then ease its socket off the ball core. Support the silicone near the socket as access allows; do not yank on thin fins, twist the slender printed core, or lever a blade inside a socket. This one-at-a-time approach is proposed to avoid pulling all 16 undercuts at once. Its practicality with Shore 40A remains unverified. Stop if tearing, binding or post damage begins.

Remove the center when the units are free. Inspect both tooling faces, seating walls, posts and ribs before reuse. No successful reuse count is documented.

## 8. Trim, inspect and attach

![CAD section preview of a ball post and the matching derived silicone socket](../assets/images/socket-detail-cad.png)

*CAD section preview: the post has four alignment ribs; the silicone unit has eight larger curved support fins. The socket shown here is derived by subtracting the shared post geometry for illustration; the source's `silicone_positive` mode does not include it. Fit and demolding remain untested.*

The source includes experimental scoring/perforation modules, but **all three scoring enable flags are false in the canonical defaults**. Therefore do not expect the matched default exports to provide scored flash. An explicitly enabled variant needs a new matched export set and separate interference/flash tests; the presence of teeth and pockets would still not establish precise or tool-free tearing.

Inspect any flash before removal. On a scrap section, assess where a tear propagates; stop if it enters the pad, fins, or socket. As a fallback, support the cured part on a cutting surface and trim small amounts with appropriate sharp scissors or a craft blade, keeping hands clear of the cutting path. Leave questionable material for review rather than nicking the socket or stretching a tear into a functional surface.

Reject uncured/tacky areas, voids at the socket or fin roots, torn fins, blocked rib recesses, or damaged posts. Align the four socket rib recesses with the panel's four post ribs and press each unit straight onto its matched post while supporting the panel. Do not force a poor fit. Record attachment/removal behavior and inspect for tears or cracked posts; no retention force, durability, protective performance or suitability for contact with the body is established.

Capture the dimensions, actual print settings/material, silicone product and lot, datasheet revisions, measured ratio, conditions, timing, batch quantity, treatment, and trial outcomes. Use the [photo handoff](photos.md) to document the process without exposing private details.

## 9. Fit underneath the desk and route cables

The intended installed orientation has the rigid panel's flat back facing upward against the desk underside, with the posts and silicone units downward. Use the owner-linked mounting tape only after checking its exact instructions and compatibility with both the actual printed material and desk finish. Record surface preparation, tape layout/contact area, application pressure and required dwell time from that tape's manufacturer; no universal values or overhead load rating are established here.

First trial the adhesive on a representative surface and inspect attachment before adding cable runs. Document cable placement, adjustment, any panel peeling or unit release, and the actual cable sizes and loading. Leave enough cable slack to avoid pulling on plugs or using the panel as an unverified strain-relief anchor. Do not infer a load rating from the listing title.

**Planned panel change:** add adhesive-fitting slits to the panel's bottom/back for easier fitting. They are not present in `panel_part()` or the current panel STL. Before a geometry change, establish the intended slit form, measured tape width/thickness, placement and clearance, remaining panel thickness, and any effect on post roots and adhesive contact. See the [pending change and validation plan](validation.md#planned-panel-mounting-change). No slit dimensions or new print orientation are assumed here.

A future demonstration video should show the real mounting and cable-routing process, distinguish the present panel from any later slit-equipped revision, and record the configuration used. The [photo and video handoff](photos.md) lists the planned shots; no video link is published yet.
