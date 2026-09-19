"""Render documentation views from the unchanged rev7 source. No photos are generated.

Requires OpenSCAD 2021.01 or compatible and Pillow. Outputs are CAD views,
not mesh validation. The derived socket is a Boolean subtraction of the exact
shared ball_snap_post module; it is not the source's silicone_positive mode.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "system_rev7_perforated_score.scad"
VIEWS = {
    "system-cad": (
        "CAD PREVIEW | rev7 default 4 x 4",
        "Separate rigid panel and silicone envelope; socket cores subtracted for illustration.",
        '''color([0.26,0.48,0.64]) panel_part();
translate([0,0,panel_thickness+10]) color([0.92,0.66,0.30])
    difference() { silicone_array(); place_units() ball_snap_post(); }
''', "0,0,12,63,0,32,260"),
    "mold-exploded-cad": (
        "CAD RENDER | three-piece mold, exploded",
        "Upper: socket-core lid | Middle: cavity piece | Lower: pad-face lid. Scoring OFF.",
        '''color([0.32,0.52,0.69]) translate([0,0,unit_height+show_exploded_gap]) top_lid_assembly();
color([0.79,0.80,0.77]) center_piece_assembly();
color([0.45,0.63,0.75]) translate([0,0,-show_exploded_gap]) bottom_lid_assembly();
''', "0,0,13,69,0,33,350"),
    "socket-detail-cad": (
        "CAD SECTION PREVIEW | shared post and derived socket",
        "8 curved silicone support fins; 4 smaller post ribs. Fit and demolding untested.",
        '''color([0.92,0.66,0.30]) translate([16,0,0]) difference() {
    silicone_unit(); ball_snap_post();
    translate([-30,-30,-1]) cube([60,30,25]);
}
color([0.26,0.48,0.64]) translate([-12,0,0]) union() {
    translate([-7,-7,-2]) cube([14,14,2]); ball_snap_post();
}
''', "0,0,5,68,0,12,110"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--openscad", default="openscad")
    parser.add_argument("--output", type=Path, default=ROOT / "assets/images")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    source = SOURCE.read_text(encoding="utf-8")
    marker = "// TOOL MODE SWITCH"
    if source.count(marker) != 1:
        raise SystemExit("Source dispatch marker changed; review render wrapper first.")
    prefix = source.split(marker)[0]
    version = subprocess.run([args.openscad, "--version"], capture_output=True, text=True, check=True)
    manifest = {"source": SOURCE.relative_to(ROOT).as_posix(),
                "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                "openscad": (version.stdout + version.stderr).strip(),
                "method": "OpenCSG preview or CGAL render per image flags; source dispatch replaced only for documentation scenes",
                "parameters": "source defaults; score flags false; fn=72",
                "images": {}}
    title_font = body_font = ImageFont.load_default()
    for font in ("DejaVuSans.ttf", "arial.ttf"):
        try:
            title_font = ImageFont.truetype(font, 26)
            body_font = ImageFont.truetype(font, 18)
            break
        except OSError:
            pass
    with tempfile.TemporaryDirectory(prefix="hoplon-render-") as temp:
        for name, (title, caption, scene, camera) in VIEWS.items():
            wrapper = Path(temp) / f"{name}.scad"
            raw = Path(temp) / f"{name}.png"
            wrapper.write_text(prefix + "\n" + scene, encoding="utf-8")
            render_flag = "--render" if name == "mold-exploded-cad" else "--preview"
            command = [args.openscad, render_flag, "--csglimit=1000000", "--imgsize=1400,950",
                       "--projection=o", "--colorscheme=Tomorrow", "--camera=" + camera,
                       "--viewall", "--autocenter", "-o", str(raw), str(wrapper)]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            if "ERROR:" in result.stderr or "WARNING:" in result.stderr:
                raise RuntimeError(result.stderr)
            render = Image.open(raw).convert("RGB")
            image = Image.new("RGB", (1400, 1060), "#f7f8fa")
            image.paste(render, (0, 100))
            draw = ImageDraw.Draw(image)
            draw.text((28, 18), title, font=title_font, fill="#172c3c")
            draw.text((28, 58), caption, font=body_font, fill="#344958")
            out = args.output / f"{name}.png"
            image.save(out)  # Fresh PNG: no copied EXIF, text, or source-machine paths.
            manifest["images"][out.name] = {"sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
                                            "camera": camera, "scene": scene,
                                            "flags": [render_flag, "--csglimit=1000000", "--projection=o", "--viewall", "--autocenter"]}
            print(out.name)
    (args.output / "render-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
