# Validation and artifact inventory

Audit date: 2026-09-19. The current source was inspected and exported locally with **OpenSCAD 2021.01**; mesh measurements used Python 3.10.11 and NumPy 2.2.6. No original CAD geometry or original STL was changed. CAD renders are illustrations, not physical test evidence. See [parameters](parameters.md) for the complete configuration and [release checklist](release-checklist.md) for publication gates.

## Current release candidates

The source is [system_rev7_perforated_score.scad](../system_rev7_perforated_score.scad). Its audited defaults are 4 × 4, 22 mm pads, 23.4 mm pitch, eight silicone support fins, four post ribs, and all scoring switches off. Source SHA-256 and portable reproduction commands appear in the [manifest](../exports/rev7-default/manifest.json). This is an **incomplete printable set**: the center-piece export is withheld pending the mesh issue below.

| File / mode | Measured STL bounds (mm) | Connected components | Result / role |
| --- | --- | ---: | --- |
| [bottom_lid.stl](../exports/rev7-default/bottom_lid.stl) | 130.600006 × 130.600006 × 11 | 1 | Mesh checks pass; printed tooling |
| `center_piece` (no public STL) | 130.600006 × 130.600006 × 16 | 1 | **Withheld: 24 zero-area triangles** |
| [top_lid.stl](../exports/rev7-default/top_lid.stl) | 130.600006 × 130.600006 × 16.097620 | 1 | Mesh checks pass; printed tooling with socket cores |
| [panel.stl](../exports/rev7-default/panel.stl) | 94.599976 × 94.599976 × 10.097620 | 1 | Mesh checks pass; separate rigid panel |
| [silicone_positive_reference.stl](../exports/rev7-default/silicone_positive_reference.stl) | 92.199997 × 92.199997 × 16 | 16 | Mesh checks pass; **solid reference without sockets**, not tooling or finished silicone |

“Mesh checks pass” means finite vertices, no triangle area at or below 10⁻¹² mm², every exact-coordinate edge shared by two triangles, consistent oriented edges, positive signed component volumes, and the expected component count. The checker does not weld vertices or repair inputs. Intentional separate silicone-array members count as 16 solids. The panel and each mold component should be one solid.

These checks do not exhaustively test self-intersections, prove slicer suitability, printability, mold sealing, physical socket fit, Shore 40A behavior, cure compatibility, demolding, durability or flash removal. STL is unitless: import as millimeters and confirm dimensions. Small differences from analytical dimensions arise from tessellation and float32 serialization.

## Center-piece export gate

OpenSCAD's CGAL render reported `Simple: yes`; the exported center mesh has one connected component, no open/nonmanifold edges and consistent winding. However, **24 triangles are exactly collinear**, with three distinct vertices. They lie on the upper cavity-face relief plane at approximately z = 15.92 mm. The legacy center STL similarly contains 40 zero-area triangles. A clean render or edge-manifold test alone would miss this limitation.

An additional OFF export was actually run from the same source/mode. That OpenSCAD version writes approximately six significant digits in OFF: the output had 37,100 triangles, 116 exact zero-area triangles and 164 at or below the 10⁻¹² mm² threshold. It did not resolve the issue and is also withheld. This comparison does not establish whether all degeneracies originate in triangulation or coordinate rounding.

The raw candidates remain outside the publishable repository. Do not silently remove triangles or edit mechanical features to make a validator pass. The proposed next step is to compare a genuinely higher-precision export/triangulation against the same CGAL solid, then validate any replacement triangulation for closed topology, no degenerate faces, unchanged surface/volume and slicer interpretation. This is an export-quality investigation; no unintended solid overlap has been established. A mechanical change, if ultimately necessary, needs a separate proposal describing the affected face-relief geometry and owner approval. No source change was made here.

## Original and legacy artifacts

These originals remain locally preserved and are excluded from the proposed public archive. Their names do not establish a matched configuration.

| Existing original | Observed result | Status |
| --- | --- | --- |
| `system_rev7 (bottom_lid).stl` | 112.4 × 112.4 × 11 mm | Smaller than canonical tooling; stale/unmatched |
| `system_rev7 (center_piece).stl` | 112.4 × 112.4 × 16 mm; 40 degenerate triangles | Stale/unmatched; mesh-quality issue |
| `system_rev7 (top_lid).stl` | 112.4 × 112.4 × 16.09762 mm | Stale/unmatched; do not pair with new center/panel |
| `system_rev7 (top_lid) (no score).stl` | Same outer bounds; different volume from other old lid | Stale/unmatched variant; filename insufficient to recover overrides |
| `system_rev7 (panel).stl` | 76.399994 × 76.399994 × 11.09762 mm | Stale/unmatched; current panel is 94.6 wide and 2 mm thick |
| `Silicone_Positive_REV7.stl` | 16 components; matching current bounds; gross volume 38,220.456986 mm³ | Consistent with current positive bounds/volume, but triangle set differs; provenance unverified and sockets absent |
| `LSR_quote_package_v1/system_rev7_perforated_score.scad` | 3 × 3, 23.2 pitch, 3.8 margins, scoring enabled, 2.6 stem, 3 mm panel; other changes | Noncanonical legacy source |
| `LSR_quote_package_v1/generate_button_step_files.py` | Independent CadQuery reconstruction; 3 × 3, 2.8 mm pad, **zero support fins** | Not an export of current SCAD; not executed |
| Quote STEP/STL/PDF package | Generated from divergent scripts/settings; previously reported overlap | **Unverified legacy reference; excluded pending separate review** |

The original positive has 34,240 triangles; regeneration has 33,216. Their bounds agree and gross volumes differ by approximately 0.000036 mm³, but sorted triangle comparison at four decimal places does not match. That supports dimensional consistency, not proof of exact surface equivalence or original generation settings. Use the regenerated reference with recorded provenance.

The quote drawing script was inspected without execution. It reads literal constants from its CadQuery generator, so its schematic dimensions need not match either SCAD copy; it also carries the old Shore 15A industrial LSR target. Neither successful STEP import nor these drawings would resolve the reported geometry concern. No current STEP manufacturing download was created. Legitimate intersections that union fins, columns, pads and post stems into one solid are not evidence of a defect.

## Design-intent comparison

The current source implements separate printed panel and mold, eight curved silicone support fins, four post-alignment ribs, the shared panel/lid post module, three mold pieces, dual-face perimeter channels and seating walls, four corner through-holes, and outer 2 mm opening bevels. No carrier, printed female receiver, carrier clip, hex-nut trap or block ejector is implemented.

Two qualifications matter: scoring is present as code but **disabled in all current defaults**, and `silicone_positive` remains a solid external positive. The reusable-mold intent, complete filling/air escape, socket release and clean trimming are not demonstrated physical results. There is no dedicated cavity-to-perimeter vent network or injection port. Filling must take place while cavities are accessible; closing the lids does not establish an assured air-escape path.

## Nominal silicone volume

An analytical wrapper outside the repository called the unchanged `silicone_unit()` module and, separately, `difference() { silicone_unit(); ball_snap_post(); }`. These exports each passed closed one-component mesh checks and CGAL reported `Simple: yes`. The subtraction includes the stem, ball and all four alignment ribs as a union, so overlap is not double-counted.

| Quantity | Mesh volume |
| --- | ---: |
| One external positive | 2,388.778583 mm³ |
| One socket-bearing nominal part | 2,303.569969 mm³ |
| Core displacement per unit | 85.208613 mm³ |
| 16 socket-bearing nominal parts | **36.857120 mL** |

This is a **nominal part-volume estimate**, not the complete closed-mold void or a ready-to-mix batch quantity. It excludes face-relief/parting flash, residual perimeter-channel clearance volume, spills and mixing-container losses. Overflow allowance requires a measured trial; no arbitrary percentage is supplied. The owner has now identified a BBDINO 40A silicone product; documented mixed density and resulting mass remain TODO. See the [build guide](build-guide.md#quantity).

## Planned panel mounting change

The owner-approved application is under-desk cable routing and management. The panel back is intended to attach to the desk underside with the [owner-used adhesive](build-guide.md#owner-used-materials). Identifying the application and products does not add physical test evidence to the mesh checks above.

The requested future feature is adhesive-fitting slits in the panel's bottom/back. The current `panel_part()` is a union of the plain 2 mm panel base and its posts; it contains no slit cuts. This documentation update leaves the canonical source, all exported meshes and the CAD images unchanged.

The affected mechanical module would be `panel_part()` in the canonical SCAD, with its panel export, manifest and illustrations regenerated after an approved change. First establish the intended slit form and location, measured adhesive dimensions and handling clearance. Then assess remaining panel thickness, post-root clearance, contact area, print orientation and support access. Validate the resulting mesh and dimensions, dry-fit the actual tape, and trial mounting, removal and cable loading against the actual desk finish. No slit width, depth, spacing, tape load rating or tested bond strength is established. Keep this proposal separate from the center-mold export issue.

## Reproduce the checks

The files can be inspected without running any project scripts. For regeneration, the tools actually used in this preparation were:

| Task | Recorded environment |
| --- | --- |
| SCAD export and CAD views | OpenSCAD 2021.01 |
| Initial mesh inspection and volume calculations | Python 3.10.11, NumPy 2.2.6 |
| Documentation image composition | Python 3.12.14, Pillow 12.3.0 |
| Final local package checks | Python 3.12.14; packaging uses the standard library |

The scripts do not install dependencies automatically. `inspect_stl.py` and `export_rev7.py` require NumPy; `render_cad.py` requires Pillow and OpenSCAD. `package_review.py` requires only Python. These are recorded environments, not a claim that every other version works. The supplied `.gitattributes` preserves canonical SCAD bytes and binary assets across Git checkouts; changing source line endings would change its recorded hash even if the geometry stayed the same.

Use an already installed OpenSCAD CLI and Python with NumPy. This preparation did not install applications or run the bundled legacy executable. Read scripts before running them. The export script leaves candidates and raw diagnostics **outside the repository**, refuses a nonempty output folder, and returns a nonzero exit status if any mesh gate fails. The currently expected all-mode result includes the center failure above. It does not publish or promote candidates.

From the repository root, with `openscad` on PATH:

```powershell
python -B scripts/export_rev7.py --openscad openscad --output ../Hoplon-Arrays-candidates
```

If OpenSCAD is not on PATH, replace `openscad` with the installed CLI executable path locally; do not put machine-specific paths into public documents. The equivalent single-component command is:

```powershell
openscad --export-format binstl --hardwarnings -o ../Hoplon-Arrays-candidates/center_piece.stl -D 'tool_mode="center_piece"' system_rev7_perforated_score.scad
```

Create that external output directory first when using the direct command. For diagnostic OFF export, use the same command with output extension `.off` and omit `--export-format binstl`.

```powershell
python -B scripts/inspect_stl.py exports/rev7-default/bottom_lid.stl exports/rev7-default/top_lid.stl exports/rev7-default/panel.stl exports/rev7-default/silicone_positive_reference.stl
```

`inspect_stl.py` prints a JSON report using basenames; `--output` can save it to an external private review folder. Its `--compare` option compares rounded triangle sets and should not be interpreted as a complete geometric Boolean comparison. The export script was exercised on `bottom_lid`; its refusal to write candidates inside the repository was also checked. The other candidates were produced with the recorded direct OpenSCAD commands and inspected by the same checker.

## Checks still required

- Resolve the center STL export-quality gate and regenerate a complete matched set from a recorded source/configuration.
- Inspect every intended print in the chosen slicer: scale, layer preview, thin post ribs, supports, accessible removal surfaces and sealing faces.
- Verify the calculated M6 fastener selection against actual purchased hardware, hole fit and flat seating; no tightening torque has been established.
- Perform the small Shore 40A compatibility/socket trial and document material datasheet, print process, fill method, voids, socket stripping and flash trimming.
- Test the complete proposed fill/demold sequence before presenting it as demonstrated.
- Review licensing, history/privacy findings and the exact proposed public file list before authorizing publication.

General mesh self-intersection proof, robust mesh-to-mesh surface-equivalence testing, STEP-to-current-SCAD equivalence, slicer validation and physical testing were not completed. CadQuery/OCP, trimesh and manifold3d were unavailable in the inspected Python environments. Their absence did not prevent source, topology, volume and provenance checks with the installed tools.
