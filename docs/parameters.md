# Rev7 source and parameters

The canonical design for this preparation is the root [system_rev7_perforated_score.scad](../system_rev7_perforated_score.scad), unchanged during documentation work. The older copy inside the quote package is a different configuration. No original Customizer JSON preset or recorded export override file was found. Comments such as “change to 20” are history, not active parameter values.

All dimensions below are millimeters. The recorded source SHA-256 is `52bff07c70fd33cc4247b62ed5b2c33dbb560772f9617580dee63a37e3ac0839`; this fingerprints the audited working-file bytes, including line endings. The [export manifest](../exports/rev7-default/manifest.json) records every top-level assignment as source text, including derived expressions. Its assignments are provenance, not a Customizer preset. Only `tool_mode` was overridden for the generated candidates. See [validation](validation.md) before treating any candidate as printable.

## Active geometry

| Parameter / result | Current value | Meaning |
| --- | ---: | --- |
| `rows`, `cols` | 4, 4 | 16 separate silicone units / 16 posts |
| `top_size`, `top_corner_radius` | 22, 6 | Rounded-square pad size and corner radius |
| `top_thickness`, `top_bevel_inset` | 3, 0 | Pad thickness; no pad bevel inset |
| `unit_height` | 16 | Silicone positive overall height |
| `edge_gap_x`, `edge_gap_y` | 1.4, 1.4 | Pad-edge gaps |
| `pitch_x`, `pitch_y` | 23.4, 23.4 | Center-to-center array pitch |
| `field_margin_x`, `field_margin_y` | 1.2, 1.2 | Margin beyond outer pads |
| `field_w`, `field_d`, `field_corner_radius` | 94.6, 94.6, 5 | Panel / field outline |
| `column_d` | 9 | Central silicone column diameter |
| Column height | 13 | `unit_height - top_thickness` |
| `fin_count`, `fin_thickness` | 8, 1.2 | Curved silicone support fins; distinct from post ribs |
| `fin_attach_bot_frac`, `fin_attach_top_frac` | 0.60, 0.80 | Fin outer radii 6.6 at column end and 8.8 at pad end |
| `fin_root_overlap`, `fin_end_overlap` | 0.35, 0.20 | Intentional overlaps that join fins to column/pad |
| `fin_neck_extra`, `fin_steps` | 0.10, 40 | Curved-fin profile control and sampling |
| `$fn`, `EPS` | 72, 0.001 | Circular tessellation and Boolean epsilon |

The support-fin profile extends to z = 13.2 in the upright positive and intentionally enters the pad that begins at z = 13. That overlap is part of the union. It is not an unintended loose body or proof of an invalid final solid.

## Shared attachment geometry

Both `top_lid_snap_posts()` and `panel_part()` call **the same `ball_snap_post()` module**. The lid mirrors these posts into the silicone cavity; the separate panel presents them outward for attachment.

| Parameter / result | Current value |
| --- | ---: |
| `snap_stem_d`, `snap_stem_h` | 1.6, 6 |
| `snap_ball_d`, `snap_ball_sink` | 5, 0.4 |
| Ball-center distance from mounting face | 5.6 |
| Nominal post depth / height | 8.1 |
| `snap_fin_enable`, `snap_fin_count` | true, 4 |
| `snap_fin_thickness`, `snap_fin_outer_d` | 0.6, 4.6 |
| `snap_fin_stem_overlap`, `snap_fin_base_overlap` | 0.12, 0.10 |
| `snap_fin_top_clearance`, `snap_fin_tip_taper` | 0.10, 0 |
| Alignment-fin local z limits | −0.10 to 5.50 |
| `panel_thickness` | 2 |
| Nominal panel including posts | 94.6 × 94.6 × 10.1 |

The 72-segment exported ball reaches approximately 8.09762 mm above its mounting face, slightly less than its nominal 8.1 mm extent. Matching CAD posts do not establish a workable printed socket fit: shrinkage, surface finish, cure and printer error remain untested. The source positive **does not subtract this core**, so `silicone_positive` is a visual reference, not a finished socket-bearing part.

## Mold and fastener geometry

| Parameter / result | Current value |
| --- | ---: |
| `mold_wall`, `clamp_flange` | 0, 18 |
| `tool_w`, `tool_d` | 130.6, 130.6 |
| `lid_thickness` | 8 each |
| Center thickness | 16 |
| `mold_edge_bevel` | 2 |
| `cavity_face_relief` | 0.08 |
| `fit_clearance` | 0.20 |
| `bleed_channel_w`, `bleed_channel_depth` | 3, 3 on both faces |
| Seating-wall nominal section | 2.6 wide, 3 high; 0.2 clearance at each side |
| `bolt_hole_enable`, count | true, 4 aligned through-holes |
| `bolt_hole_d`, `bolt_edge_margin` | 6.7, 7.5 |
| Hole center coordinates | x = ±54.45, y = ±54.45 |
| Hole center spacing | 108.9 × 108.9 |
| Closed stack at bolt line | 8 + 16 + 8 = **32** |

The closed assembly uses center z = 0…16, bottom-lid exterior z = −8, and top-lid exterior z = 24. The walls nest inside the center's channels; their 3 mm heights must not be added again to the bolt stack. Export-wrapper z positions differ from assembled positions: bottom lid 0…11; center 0…16; top lid approximately 0.00238…16.1. These file heights are not additive for fastener sizing.

The 6.7 mm CAD hole is a clearance hole, not an M6.7 thread. A calculated candidate is four M6 × 45 bolts (under-head length), four matching M6 nuts and eight flat washers. The [build guide](build-guide.md#bolt-length-and-clearance) records the standards-based washer/nut assumptions, length calculation and required fit trial. There are no nut traps. A 12 mm washer outside diameter fits on the outer planar face: each bolt center is 8.85 mm from the bevel's planar boundary, giving 2.85 mm margin beyond a 6 mm radius washer. Check actual head/washer dimensions and printed surfaces before purchase/use.

There are perimeter overflow trenches on both center faces and matching seating walls. There is **no dedicated injection port or explicit local vent channel from each cavity to those perimeter trenches**. Filling and air escape during closure remain a physical test requirement.

## Scoring features are currently off

`score_enable = false`, `score_top_enable = false`, and `score_bottom_enable = false`. Therefore none of the matched scoring teeth or pockets appears in the audited default set. `score_dot_enable = true` alone does not activate them.

The dormant values are: offset 1.2, continuous line width 0, pocket depth 0.60, web target 0.08, derived tooth height 0.52, fit clearance 0.20, dot diameter 0.80, side-dot pitch 4 and column-side dot count 18. These are experimental controls, not a demonstrated tear specification. Activating them requires coordinated regeneration of the center and corresponding lids and inspection for unintended collisions, clearance and flash behavior. Do not turn them on merely to match an older filename.

## Modes and customization

| `tool_mode` | Result |
| --- | --- |
| `silicone_positive` (source default) | 16 separate solid external positives; sockets absent |
| `center_piece` | Cavity block; current STL quality gate unresolved |
| `top_lid` | Socket-forming core lid and seating wall |
| `bottom_lid` | Pad-face closure and seating wall; no block ejectors |
| `panel` | Separate rigid panel with 16 posts |
| `exploded_mold` | Visual assembly reference only |
| `exploded_system` | Visual mold, solid positives and separate panel |

The source's final `else` also selects `exploded_system` for an unrecognized string; a typo can silently export the wrong scene. The supplied export script restricts modes to named individual parts/reference models.

To explore a change, retain the canonical file and work on a clearly named local copy. Record all overrides, regenerate every affected mating part, and repeat dimensional, topology and physical-fit checks. Row/column count, pitch, pad/column dimensions, posts, channels and score settings are mechanically coupled. No supported parameter range or tolerance budget has been validated. Keep the original external pad/column/eight-fin structure unless an owner-approved mechanical change explicitly replaces it.
