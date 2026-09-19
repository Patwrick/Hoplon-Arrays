"""Build and inspect an allowlisted LOCAL REVIEW ZIP outside this repository.

This does not publish, create a Git release/tag, approve licensing, or sanitize
Git history. Only the exact files in docs/release-files.txt may be included.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "system_rev7_perforated_score.scad"
EXPORT_MANIFEST = "exports/rev7-default/manifest.json"
RENDER_MANIFEST = "assets/images/render-manifest.json"


def under(path, root):
    return path == root or root in path.parents


def checked_path(name):
    """Accept ordinary, canonical relative files only; never follow reparse points."""
    relative = PurePosixPath(name)
    if (not name or "\\" in name or ":" in name or relative.is_absolute()
            or ".." in relative.parts or relative.as_posix() != name):
        raise ValueError(f"Invalid relative path: {name}")
    path = ROOT
    for part in relative.parts:
        path /= part
        entry = path.lstat()
        # Windows junctions are reparse points but need not be reported as symlinks.
        if (stat.S_ISLNK(entry.st_mode)
                or getattr(entry, "st_file_attributes", 0) & 0x400):
            raise ValueError(f"Symlink or reparse point is not allowed: {name}")
    if not under(path.resolve(), ROOT) or not stat.S_ISREG(path.stat().st_mode):
        raise ValueError(f"Not a regular repository file: {name}")
    return path


def check_provenance(contents):
    """Check recorded provenance, not mechanical correctness or physical fitness."""
    source_hash = hashlib.sha256(contents[SOURCE]).hexdigest()
    verified = set()
    for manifest_name, kind in ((EXPORT_MANIFEST, "artifacts"), (RENDER_MANIFEST, "images")):
        manifest = json.loads(contents[manifest_name])
        if manifest.get("source") != SOURCE or manifest.get("source_sha256") != source_hash:
            raise ValueError(f"Source SHA-256 mismatch: {manifest_name}; review/rebuild derived assets")
        if kind == "artifacts":
            entries = manifest[kind]
        else:
            entries = [{"file": name, **values} for name, values in manifest[kind].items()]
        for entry in entries:
            name = entry.get("file", "")
            if not name or PurePosixPath(name).name != name or "\\" in name:
                raise ValueError(f"Invalid artifact filename in {manifest_name}")
            relative = (PurePosixPath(manifest_name).parent / name).as_posix()
            if relative in verified:
                raise ValueError(f"Duplicate artifact record: {relative}")
            if relative not in contents:
                raise ValueError(f"Manifest artifact omitted from allowlist: {relative}")
            if kind == "artifacts" and entry.get("mesh_checks_passed") is not True:
                raise ValueError(f"Manifest reports unverified mesh: {relative}")
            digest = entry.get("sha256", "")
            if (not re.fullmatch(r"[0-9a-f]{64}", digest)
                    or hashlib.sha256(contents[relative]).hexdigest() != digest):
                raise ValueError(f"Artifact SHA-256 mismatch: {relative}")
            verified.add(relative)
    for name in contents:
        if (PurePosixPath(name).suffix.lower() == ".stl" or name.startswith("assets/images/")) and name != RENDER_MANIFEST:
            if name not in verified:
                raise ValueError(f"Artifact has no checked provenance: {name}")
    return {"source": SOURCE, "source_sha256": source_hash,
            "manifests": [EXPORT_MANIFEST, RENDER_MANIFEST], "verified_artifacts": len(verified)}


def check_links(files):
    allowed = set(files)
    errors = []
    for relative in files:
        if not relative.endswith(".md"):
            continue
        path = ROOT / relative
        body = path.read_text(encoding="utf-8")
        for match in re.finditer(r'!?\[[^\]]*\]\(([^)]+)\)', body):
            link, _, fragment = match.group(1).strip("<>").partition("#")
            if re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", link):
                continue
            target = (path.parent / link).resolve() if link else path
            if not under(target, ROOT):
                errors.append(f"{relative}: link escapes repository")
            elif not target.exists():
                errors.append(f"{relative}: missing target {link}")
            elif target.is_file() and target.relative_to(ROOT).as_posix() not in allowed:
                errors.append(f"{relative}: target omitted from archive: {link}")
            elif fragment and target.suffix == ".md":
                headings = re.findall(r"^#{1,6}\s+(.+)$", target.read_text(encoding="utf-8"), re.MULTILINE)
                anchors = {re.sub(r"[^\w -]", "", h.lower()).replace(" ", "-") for h in headings}
                if fragment not in anchors:
                    errors.append(f"{relative}: missing heading {link}#{fragment}")
    if errors:
        raise ValueError("\n".join(errors))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    operation = parser.add_mutually_exclusive_group(required=True)
    operation.add_argument("--output", type=Path,
                           help="A new .zip path outside the repository (never overwritten)")
    operation.add_argument("--check", action="store_true",
                           help="Validate the current allowlist, links and provenance without writing a ZIP")
    args = parser.parse_args()
    output = args.output.resolve() if args.output else None
    if output:
        if under(output, ROOT) or output.suffix.lower() != ".zip":
            raise SystemExit("Choose a .zip output path outside the repository.")
        if output.exists():
            raise SystemExit("Output already exists; select a new review archive filename.")
    files = [line.strip() for line in checked_path("docs/release-files.txt").read_text(encoding="utf-8").splitlines()
             if line.strip() and not line.lstrip().startswith("#")]
    if len(files) != len(set(files)):
        raise SystemExit("Duplicate archive entries")
    contents = {}
    for name in files:
        path = checked_path(name)
        if any(part.lower() in (".git", "lsr_quote_package_v1", "__pycache__") for part in Path(name).parts):
            raise SystemExit("Excluded directory in allowlist")
        if path.suffix.lower() in (".exe", ".pyc", ".zip", ".pdf", ".step", ".key", ".pem"):
            raise SystemExit("Unapproved artifact type in allowlist")
        # Package precisely the bytes checked below, even if a file changes later.
        contents[name] = path.read_bytes()
    for required in (SOURCE, EXPORT_MANIFEST, RENDER_MANIFEST, "docs/release-files.txt", "LICENSE.md"):
        if required not in contents:
            raise ValueError(f"Required release file omitted: {required}")
    proposed_release = None
    if (ROOT / "VERSION").exists():
        if "VERSION" not in contents:
            raise ValueError("VERSION exists but is omitted from the allowlist")
        proposed_release = contents["VERSION"].decode("utf-8").strip()
        if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?", proposed_release):
            raise ValueError("VERSION must contain a release identifier such as 0.1.0")
    check_links(files)
    provenance = check_provenance(contents)
    hashes = {name: hashlib.sha256(content).hexdigest() for name, content in contents.items()}
    checks = ["Markdown local targets included", "exact allowlist; no reparse points",
              "source and artifact provenance SHA-256"]
    if args.check:
        print(json.dumps({"status": "checks passed; no archive written", "proposed_release": proposed_release,
                          "file_count": len(files), "provenance": provenance, "checks": checks}, indent=2))
        return
    manifest = {"status": "LOCAL REVIEW ONLY; owner publication approval and rights/attribution review pending",
                "proposed_release": proposed_release, "provenance": provenance,
                "files_sha256": hashes,
                "limits": "File checks do not approve privacy, history, licensing, mechanical or physical performance."}
    output.parent.mkdir(parents=True, exist_ok=True)
    # Fixed timestamps and permissions avoid carrying machine/user metadata.
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in files:
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 19, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, contents[name])
        info = zipfile.ZipInfo("REVIEW-MANIFEST.json", date_time=(2026, 9, 19, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        archive.writestr(info, json.dumps(manifest, indent=2) + "\n")
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise SystemExit("Archive CRC test failed")
        if sorted(archive.namelist()) != sorted(files + ["REVIEW-MANIFEST.json"]):
            raise SystemExit("Archive allowlist mismatch")
        for name, digest in hashes.items():
            if hashlib.sha256(archive.read(name)).hexdigest() != digest:
                raise SystemExit(f"Archived content differs: {name}")
    print(json.dumps({"archive": output.name, "file_count": len(files) + 1,
                      "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                      "proposed_release": proposed_release,
                      "checks": checks + ["CRC", "every member SHA-256"]}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError) as error:
        raise SystemExit(f"Review package check failed: {error}") from None
