# 0.1.0 release candidate checklist

**Prepared scope: first prototype source release, 0.1.0. Publication is not authorized.** The owner has requested preparation with the current files and later updates. [Release notes](release-notes.md) and [changelog](../CHANGELOG.md) make that limited scope explicit. No push, tag, hosted release, visibility change, history rewrite, staging or commit is part of this preparation. The review archive is a file allowlist, not a Git history export.

## Publication blockers / owner decisions

- [ ] Approve public disclosure and the exact proposed files in [release-files.txt](release-files.txt). Review the actual ZIP and its `REVIEW-MANIFEST.json` before publishing.
- [x] Add the owner-requested personal/noncommercial license, excluding business and profit-making permission. [LICENSE.md](../LICENSE.md) and the [scope notes](licensing.md) distinguish CAD/hardware, scripts, documentation and assets, preserve third-party terms and explain functional-hardware limits.
- [ ] Confirm the authority to license each included contribution and its required attribution. The custom license is added; ownership and third-party clearance are not established by adding it. Legal review of the wording is advisable, particularly for physical-product restrictions. Do not describe this restricted-use project as open source.
- [ ] If publishing Git history, approve or remediate its owner-linked author attribution. Deletion or `.gitignore` changes cannot remove old Git objects. If attribution must change, review a separately authorized, backed-up history-remediation plan first; no rewrite has been run. The curated file archive contains no Git author metadata.
- [ ] If publishing Git history, review the intended branch and reachable objects explicitly. Earlier captured/local objects still retain excluded legacy material, including an embedded personal path; auxiliary refs and reflogs change as local tools operate. The refreshed audit found prepared-file snapshots in current auxiliary refs and older legacy objects retained locally, including unreachable objects. Do not publish the `.git` directory, a mirror or an all-ref bundle. No local objects or refs have been purged.
- [x] Exclude the entire original legacy quote package from this candidate. STEP geometry and drawings are unverified and differ from current SCAD; an earlier overlap concern remains unresolved. The bundled executable and bytecode also have privacy/redistribution concerns. They remain private local references pending any separate review.
- [x] Prepare the current files as a prototype source release with the limitations in [validation](validation.md) documented. The center STL and physical validation are deferred; they prevent a complete-printable-kit or proven-build claim, not preparation of this honestly limited source snapshot. Mechanical changes remain separate proposals.
- [ ] Authorize publication explicitly. Preparing this candidate does not authorize publishing the repository or archive.

## Before claiming a demonstrated DIY build

- [ ] Resolve the center-piece export's zero-area triangles and validate a complete matched set before advertising a complete printable mold download. This requires an explicit export/triangulation investigation; no automatic mesh or mechanical repair was applied.
- [x] Record the owner-approved under-desk cable-management purpose and owner-used silicone/adhesive links in the [build guide](build-guide.md#owner-used-materials).
- [ ] Confirm the supplied BBDINO 40A variant and record matching official technical/SDS revisions. Complete unresolved product-specific fields in the [build guide](build-guide.md).
- [ ] Record printer/material/process and verified orientations; inspect sealing, post/rib detail, support access and dimensions.
- [ ] Dry-fit the calculated four M6 × 45 mm fasteners, four nuts and eight washers with the actual hardware. Confirm the 32 mm nominal bolt-line stack, full lid seating, head/washer clearance and thread engagement.
- [ ] Run a surface/cure compatibility sample and one-cavity fill, demold and snap-fit trial. Observe air escape, complete pad/fin fill, release from the ball cores and any damage.
- [ ] Measure overflow and handling loss before selecting a full casting batch. Use documented product density before any volume-to-mass conversion.
- [ ] If enabling scoring, regenerate a matched set and test interference, flash and trimming. Default scoring is off. No precise/tool-free tear is demonstrated.
- [ ] Confirm exact mounting-tape identity/dimensions and manufacturer application guidance; trial adhesion to the actual printed panel and desk finish before making mounting or cable-load claims.
- [ ] Add the physical evidence in [photos](photos.md), including failures and dimensions. Complete physical tests before changing claims; CAD checks alone do not certify printability, fit, cure compatibility, durability, or suitability for a particular use.

These process items may remain openly documented prototype limitations if the owner approves a prototype-only source release; they block claims of a proven build.

## Preparation checks

- [x] Record `0.1.0` in [VERSION](../VERSION), prepare [release notes](release-notes.md) and a [changelog](../CHANGELOG.md), and identify the mechanical design as rev7.
- [x] Original CAD, STLs and quote assets retained in place. No original geometry changed.
- [x] Canonical source and default values read; old exports distinguished from regenerated ones.
- [x] Local current/staged/untracked files and locally available Git objects/metadata inspected. Detailed redacted audit evidence kept outside the publishable repository.
- [x] No likely credentials found by the local checks performed. This is bounded scan coverage, not a guarantee. Any subsequently discovered real credential requires owner rotation/revocation as well as cleanup.
- [x] Current-source images generated and reviewed; original physical photos were absent. New image metadata checked.
- [x] Quote package and original root STLs excluded by explicit archive allowlist and local ignore rules. Ignore rules are not history cleanup.
- [x] Harden archive construction to reject changed source/assets, failed or unmanifested export candidates, path traversal and symlink/junction paths. Preserve SCAD and binary bytes with [Git attributes](../.gitattributes).

The local audit included normal branch refs, auxiliary capture refs, reflogs, all available objects, commit identity fields, and local origin configuration. Remote server state, hosted releases, LFS servers, forks, other clones, and cloud copies were not accessed. New captured objects or refs may be created by local tooling after the audit; recheck immediately before any Git publication. Original CAD/STEP/PDF metadata and the bundled executable received supported local inspection; see the private audit handoff for exact limitations. Never upload private originals to a scanning service.

## Build and inspect the review archive

The [packaging script](../scripts/package_review.py) checks local Markdown targets/anchors, the exact file list, and source/export/image hashes against the provenance manifests. It rejects failed or unrecorded mesh/image assets and symlinks/junctions. `--check` performs validation without writing a ZIP. `--output` requires a new ZIP path **outside the repository**, writes the checked file bytes plus an internal manifest, then rereads the archive to check names, CRCs and member hashes. The manifest records the proposed version; it does not imply that a Git tag or release exists. The script refuses overwrites and never publishes.

```sh
python -B scripts/package_review.py --check
python -B scripts/package_review.py --output ../Hoplon-Arrays-release-review/Hoplon-Arrays-0.1.0-prototype-review.zip
```

After any edit, create a new candidate filename and inspect it again. Do not zip the repository directory wholesale: `.gitignore` does not control an arbitrary ZIP operation. Exclude `.git`, originals/backups, supplier correspondence, raw/private audits, executable installers and bytecode. Review staged changes independently before an eventual commit.

## Publication handoff after owner approval

1. Approve the exact package contents, rights/attribution and applicable Git-history scope above. Preserve the excluded originals and private review records.
2. If publishing the repository, stage only the explicit paths in `release-files.txt` after removing its comment lines; inspect that exact staged set and approve a commit. Do not use a blanket add or publish auxiliary refs. No files are staged by the preparation scripts.
3. Use the reviewed `0.1.0` notes for the initial prototype release and identify it as a prerelease/experimental snapshot. Create a tag or hosted release only after explicit authorization; use an explicitly approved branch/ref for any push.
4. Attach the inspected curated archive and its checksum, rather than an unreviewed working-directory ZIP. Check the final hosted files and links after publication. Replace the notes' "not yet published" status and changelog's prepared status only when publication actually occurs.

The missing photos/video, slit design, selected-product process documents and physical tests remain future work. Do not silently turn those omissions into assertions of validation when preparing the public description.

## Optional improvements after the gates

- Add physical build photos and measured results as evidence becomes available.
- Add the planned under-desk demonstration video when available, following the [photo/video handoff](photos.md#future-demonstration-video).
- Review the planned panel-back adhesive-fitting slits, establish dimensions and validate a new panel revision before documenting them as implemented. See the [pending geometry proposal](validation.md#planned-panel-mounting-change).
- Add a selected-product batch worksheet once density and measured losses are known.
- Expand mesh checks with an independent self-intersection/solid validator and slicer review.
- Add tested print profiles and a reproducible compatibility/retention test protocol.
- Consider geometry changes only through a separately reviewed proposal with affected files, measured defects and validation criteria.
