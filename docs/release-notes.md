# Hoplon-Arrays 0.1.0 — Prototype source release

**Prepared release notes; not yet published.** The proposed identifier is `0.1.0`, recorded in [VERSION](../VERSION). The CAD revision is still rev7. No Git tag or hosted release has been created.

Hoplon-Arrays is a modular system for routing and managing cables underneath a desk. Silicone units snap onto a separate rigid, printed panel, which attaches to the desk underside with adhesive. This initial snapshot shares the current design and build research so the project can be inspected and developed further.

## Included in this snapshot

- The unchanged canonical [rev7 SCAD source](../system_rev7_perforated_score.scad), with 4 × 4 units on 23.4 mm pitch, eight curved support fins per unit and four alignment ribs per post. Scoring is off by default.
- Three regenerated print candidates: [socket-core lid](../exports/rev7-default/top_lid.stl), [pad-face lid](../exports/rev7-default/bottom_lid.stl) and [separate rigid panel](../exports/rev7-default/panel.stl). They passed the documented computational mesh checks; physical printability and fit are not established.
- A [silicone positive reference](../exports/rev7-default/silicone_positive_reference.stl) that shows the external envelope but has **no socket**. It is not a finished silicone part or a required print.
- A [proposed DIY build guide](build-guide.md), [parameters](parameters.md), [validation and artifact inventory](validation.md), three CAD images and reproducible export/inspection/render scripts.
- Owner-used BBDINO 40A silicone and adhesive references, and a calculated candidate set of four M6 × 45 bolts, four nuts and eight washers, subject to dry-fit verification.
- The custom [personal/noncommercial license](../LICENSE.md). Business use, including internal business use, and paid/for-profit use are not granted by these terms. See [scope and legal limits](licensing.md).

## Known limitations

**This is not a complete printable mold kit.** The center mold piece is present in the SCAD source, but its STL is withheld because the regenerated mesh contains 24 zero-area triangles. The failed candidate is excluded from the release archive. [Export-quality investigation](validation.md#center-piece-export-gate)

The casting sequence is proposed, and the following remain unverified: selected printing settings, liquid-tight mold seating, cavity filling and air escape, release of Shore 40A sockets from the cores, snap durability, flash removal, adhesive retention and cable loading. Manufacturer product-page information is recorded, but a matching 40A TDS/SDS and several process/material values remain outstanding. The adhesive listing has conflicting specifications; measure the actual tape before designing around it.

The nominal socketed silicone volume is 36.857 mL for 16 units, excluding unmeasured flash, overflow and handling losses. It is not a final mixing quantity or a mass recipe. No physical test results or performance claims are inferred from the CAD renders.

The original root STLs and legacy quote/STEP/drawing package are excluded. The old meshes differ from the current source, and the quote geometry remains unverified. Do not combine them with this snapshot.

## Future updates

- Resolve the center-piece export issue and validate a complete matched set.
- Add physical build, fit, casting, adhesive and cable-routing evidence, with actual settings and measurements.
- Review and implement panel-back adhesive-fitting slits once their form and dimensions are established. They are **absent from this version**.
- Add the planned [photos and demonstration video](photos.md), including under-desk installation and cable adjustment.

To report a problem, include the source hash, version, parameter overrides, affected mode, tool versions and reproducible steps. For physical observations, include material/process details and privacy-checked images. Start with the [README](../README.md); publication actions are tracked separately in the [release checklist](release-checklist.md).
