"""Generate review candidates from the unchanged canonical SCAD; never publish.

Requires OpenSCAD and NumPy. Output must be a new or empty directory. A failing
mesh is retained there for diagnosis and flagged in manifest.json, not promoted
to approved printable downloads. See docs/validation.md for current limitations.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from inspect_stl import inspect

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'system_rev7_perforated_score.scad'
MODES = ('bottom_lid', 'center_piece', 'top_lid', 'panel', 'silicone_positive')


def filename(mode):
    return ('silicone_positive_reference' if mode == 'silicone_positive' else mode) + '.stl'


def source_manifest(version):
    text = SOURCE.read_text(encoding='utf-8')
    assignments = dict(re.findall(r'^([A-Za-z_$][\w$]*)\s*=\s*([^;]+);', text, flags=re.MULTILINE))
    return {'source': SOURCE.name, 'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            'units': 'mm', 'openscad_version': version, 'configuration': 'Source defaults; only tool_mode overridden.',
            'source_assignments': {k: v.strip() for k, v in assignments.items()},
            'validation_scope': 'CGAL export plus mesh topology, winding, finite coordinates, area and volume. No general self-intersection, slicer, print or physical-fit test.',
            'artifacts': []}


def mesh_result(mode, path, count):
    result = inspect(path)
    expected = count if mode == 'silicone_positive' else 1
    result['mode'] = mode
    result['command_from_repository_root'] = ['openscad', '--export-format', 'binstl', '--hardwarnings',
                                               '-o', '<output>/' + filename(mode), '-D',
                                               'tool_mode="' + mode + '"', SOURCE.name]
    result['expected_components'] = expected
    result['mesh_checks_passed'] = (len(result['components']) == expected
        and all(result[k] == 0 for k in ('boundary_edges', 'nonmanifold_edges',
                'inconsistent_winding_edges', 'degenerate_triangles'))
        and all(c['volume_mm3'] > 0 for c in result['components']))
    result['role'] = ('Positive visual reference; lacks molded socket.' if mode == 'silicone_positive'
                      else 'Printed panel.' if mode == 'panel' else 'Printed mold component.')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--openscad', default='openscad', help='Installed OpenSCAD CLI executable')
    parser.add_argument('--output', type=Path, required=True, help='New or empty candidate directory')
    parser.add_argument('--modes', choices=MODES, nargs='+', default=list(MODES))
    args = parser.parse_args()
    target = args.output.resolve()
    if target == ROOT or ROOT in target.parents:
        parser.error('Candidate output must be outside the repository; it contains raw logs and potentially failing meshes.')
    if target.exists() and any(target.iterdir()):
        parser.error('Output directory is not empty; refusing to overwrite work.')
    version_run = subprocess.run([args.openscad, '--version'], text=True, capture_output=True, check=True)
    version = (version_run.stdout + version_run.stderr).strip()
    manifest = source_manifest(version)
    params = manifest['source_assignments']
    # Fail safely if rows/cols cease to be simple literal source parameters.
    count = int(params['rows']) * int(params['cols'])
    target.mkdir(parents=True, exist_ok=True)
    for mode in dict.fromkeys(args.modes):
        output = target / filename(mode)
        command = [args.openscad, '--export-format', 'binstl', '--hardwarnings', '-o', str(output),
                   '-D', 'tool_mode="' + mode + '"', str(SOURCE)]
        completed = subprocess.run(command, text=True, capture_output=True)
        # Raw diagnostics belong only in the private candidate folder, never a release package.
        (target / (mode + '.log')).write_text(completed.stdout + completed.stderr, encoding='utf-8')
        if completed.returncode or not output.exists() or 'ERROR:' in completed.stderr:
            manifest['artifacts'].append({'mode': mode, 'mesh_checks_passed': False, 'export_failed': True})
            continue
        result = mesh_result(mode, output, count)
        manifest['artifacts'].append(result)
        print(mode + ': ' + ('mesh checks pass' if result['mesh_checks_passed'] else 'REVIEW REQUIRED'), flush=True)
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != manifest['source_sha256']:
        raise RuntimeError('Source changed while exports were running; candidates cannot be treated as a matched set.')
    (target / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    raise SystemExit(0 if all(x['mesh_checks_passed'] for x in manifest['artifacts']) else 1)


if __name__ == '__main__':
    main()
