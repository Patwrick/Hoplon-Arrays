# Photos, CAD images and future video

No physical prototype photos were present in the inspected repository. The three current images are generated from the canonical source, with no photographic or test claims. Do not substitute the old quote drawings or concept art for current-model evidence.

## Existing CAD images

| File | View and caption | Location |
| --- | --- | --- |
| [system-cad.png](../assets/images/system-cad.png) | CAD preview: separate rigid panel and lifted 4 × 4 silicone array; shared post geometry subtracted for illustrative sockets | README main image |
| [mold-exploded-cad.png](../assets/images/mold-exploded-cad.png) | CAD render: core lid / center piece / pad-face lid in assembly orientation, separated for visibility; default scoring off | README and build-guide orientation reference |
| [socket-detail-cad.png](../assets/images/socket-detail-cad.png) | CAD preview section: derived socket and shared ball post; eight support fins versus four post ribs | README and build-guide fit reference |

Run `python scripts/render_cad.py --openscad openscad` from the repository root (OpenSCAD and Pillow required). The script reads the unchanged SCAD and replaces only its view dispatch in a temporary file. The system scene lifts socketed unit envelopes 10 mm above their nominal panel seating plane. The socket illustration subtracts `ball_snap_post()` from `silicone_unit()` and cuts away half for visibility; that is a documentation view, not a new production source mode. The exploded mold uses the source assembly modules with spacing for visibility. The script does not edit the SCAD.

The [render manifest](../assets/images/render-manifest.json) records the source hash, OpenSCAD version, scenes, camera settings, and output hashes. Main/detail images use OpenCSG previews; the exploded mold uses CGAL rendering. Previews may have display artifacts. The rendered images have been opened and checked visually; they contain no desktop, faces, labels from private correspondence, or copied image metadata. Each is freshly written as an RGB PNG without source EXIF or location fields.

## Photos still needed

These filenames are planned handoff names, not links to missing files. Save reviewed copies under `assets/images/` only after removing private details and metadata. Preserve unredacted originals outside the public repository.

| Planned filename | View | Proposed caption | Placement | Must demonstrate |
| --- | --- | --- | --- | --- |
| `panel-assembled-photo.jpg` | Under-desk three-quarter and side view with routed cables | Physical cable-management prototype under a desk, [material/product], [test date], [configuration] | README main image beside CAD | Desk attachment, separate rigid panel and attached units, cable path and clearance; no performance inference |
| `panel-adhesive-photo.jpg` | Panel back before mounting and its contact with the desk underside | Adhesive mounting trial with [tape identity], [desk finish], [configuration] | Build-guide mounting step | Actual tape layout, contact area and access; identify whether any future slits are present |
| `unit-separated-photo.jpg` | Single demolded unit, pad and underside | One cast Shore 40A unit before assembly | Build guide inspection | Rounded-square pad, center column, eight curved support fins; scale included |
| `socket-post-photo.jpg` | Macro of socket beside a post, additional underside angle | Molded socket and four post alignment ribs | README attachment detail / fit step | Socket opening and keyed recesses; all four ribs identifiable across views; defects visible |
| `mold-three-pieces-photo.jpg` | Both faces of all three printed pieces | Printed mold parts, labeled by contacting silicone face | Build guide orientation | Core lid, center cavity openings, pad-face lid, both bleed grooves and seating walls |
| `bolt-stack-dry-fit-photo.jpg` | Side of closed stack plus one measured corner | Dry fit with four through-bolts, washers and nuts | Build guide hardware | Measured 32 mm nominal corner stack, seated faces, actual head/washer clearances and thread projection |
| `mold-open-fill-photo.jpg` | Center on pad-face lid before closing, then partly lowered core lid | Proposed filling sequence in a documented trial | Build guide filling | Open cavity access, fill level and observed air/overflow paths; panel outside mold |
| `demolding-photo.jpg` | Lid opening and socket being gently released in separate frames | Physical demolding trial, [material/process] | Build guide demolding | Actual release direction, ball undercut, tool placement and any tears or broken posts |
| `flash-detail-photo.jpg` | Macro before and after trimming with scale | Flash result, scoring [off / exact enabled configuration] | Build guide flash / validation | Flash thickness/bridges, any scoring marks and damage; manual trimming distinguished from tearing |

Capture an uncropped context view as well as each close-up. Record source hash, parameters, printer/material/process, silicone product, cure schedule, release treatment, and trial outcome alongside the image. Avoid identifiable people, shipping labels, supplier screens, correspondence, home/work location, serial numbers, and background reflections. Inspect EXIF/GPS, author fields, filenames, embedded thumbnails, and visible text before publication. Obtain permission for any identifiable person or third-party image. A cleaned image does not remove private metadata from older Git objects or original copies.

## Future demonstration video

The owner plans to add a video in a future update. No recording or public URL is available yet; do not add a broken embed or present the CAD views as filmed results. A suggested working filename is `hoplon-arrays-under-desk-demo.mp4`, with the public caption “Hoplon-Arrays: under-desk mounting and cable routing — [configuration/date].” Add its reviewed link to the README and build guide once available.

Suggested sequence:

1. Establish the underside of the desk, the cable route and the intended panel location.
2. Show the separate panel, one silicone unit and the snap/socket interface; identify the actual silicone and adhesive used.
3. Show the panel back, adhesive placement and mounting. If adhesive-fitting slits have been added in a later revision, identify that revision rather than implying the current files contain them.
4. Demonstrate placing, adjusting and removing cables, showing the panel attachment and unit behavior without claiming an unmeasured load or life rating.
5. Include short build clips if available: three mold pieces, open filling, cure conditions, demolding and flash inspection. Label any unfilmed steps as proposed.

Record the source/configuration, material batches, desk finish, print settings and relevant measured results in the video description. Review visible backgrounds, screens, shipping labels, audio, faces and video/container metadata before publication. Use only owned or authorized footage/music. A demonstration documents the shown trial; it does not establish general performance.
