"""Read STL meshes without executing them. Requires NumPy; never repairs input.

Checks finite coordinates, triangle area, edge incidence/winding, connected
components and signed volume. These tests do NOT detect every self-intersection
or establish mechanical performance. Optional --compare checks triangle sets at
the stated rounding precision, not a general Boolean equivalence test.
"""
import argparse
import hashlib
import json
import struct
from pathlib import Path

import numpy as np


def load_stl(path):
    data = Path(path).read_bytes()
    if len(data) >= 84:
        count = struct.unpack_from('<I', data, 80)[0]
        if len(data) == 84 + count * 50:
            dtype = np.dtype([('normal', '<f4', 3), ('vertices', '<f4', (3, 3)), ('attr', '<u2')])
            return np.frombuffer(data, dtype=dtype, count=count, offset=84)['vertices'].astype(float)
    vertices = []
    for line in data.decode('ascii').splitlines():
        values = line.strip().split()
        if values and values[0] == 'vertex':
            vertices.append([float(x) for x in values[1:4]])
    return np.asarray(vertices, dtype=float).reshape((-1, 3, 3))


def inspect(path):
    tri = load_stl(path)
    if not len(tri) or not np.isfinite(tri).all():
        raise ValueError('Empty mesh or nonfinite coordinates')
    # Exact shared STL coordinates: no welding, tolerance repair, or topology changes.
    vertices, inverse = np.unique(tri.reshape((-1, 3)), axis=0, return_inverse=True)
    faces = inverse.reshape((-1, 3))
    edges = np.concatenate((faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]))
    sorted_edges = np.sort(edges, axis=1)
    unique_edges, edge_map, counts = np.unique(sorted_edges, axis=0, return_inverse=True, return_counts=True)
    directions = np.where(edges[:, 0] < edges[:, 1], 1, -1)
    orientation = np.bincount(edge_map, weights=directions)
    parent = np.arange(len(vertices))

    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for a, b in unique_edges:
        ra, rb = root(a), root(b)
        if ra != rb:
            parent[rb] = ra
    labels = np.asarray([root(i) for i in range(len(vertices))])
    face_labels = labels[faces[:, 0]]
    volumes = np.einsum('ij,ij->i', tri[:, 0], np.cross(tri[:, 1], tri[:, 2])) / 6.0
    areas = np.linalg.norm(np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]), axis=1) / 2
    components = []
    for label in np.unique(face_labels):
        mask = face_labels == label
        points = tri[mask].reshape((-1, 3))
        components.append({'triangles': int(mask.sum()), 'volume_mm3': float(volumes[mask].sum()),
                           'bounds_mm': [points.min(axis=0).tolist(), points.max(axis=0).tolist()]})
    components.sort(key=lambda c: (-c['volume_mm3'], c['bounds_mm'][0]))
    return {'file': Path(path).name, 'sha256': hashlib.sha256(Path(path).read_bytes()).hexdigest(),
            'triangles': len(tri), 'vertices': len(vertices),
            'bounds_mm': [vertices.min(axis=0).tolist(), vertices.max(axis=0).tolist()],
            'dimensions_mm': np.ptp(vertices, axis=0).tolist(),
            'boundary_edges': int((counts == 1).sum()), 'nonmanifold_edges': int((counts > 2).sum()),
            'inconsistent_winding_edges': int((orientation != 0).sum()),
            'degenerate_triangles': int((areas <= 1e-12).sum()),
            'signed_volume_mm3': float(volumes.sum()), 'components': components,
            'limits': 'No general self-intersection, material, slicer, print, or physical-fit test.'}


def triangle_keys(path, decimals):
    tri = np.round(load_stl(path), decimals)
    # Vertex sort removes face order/orientation; winding is inspected separately.
    return sorted(tuple(sorted(tuple(float(x) for x in v) for v in face)) for face in tri)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('files', nargs='+', type=Path)
    p.add_argument('--compare', type=Path, help='Compare every input with this STL')
    p.add_argument('--decimals', type=int, default=4)
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    result = [inspect(path) for path in args.files]
    if args.compare:
        reference = triangle_keys(args.compare, args.decimals)
        for path, entry in zip(args.files, result):
            entry['comparison'] = {'reference': args.compare.name, 'rounding_decimal_places_mm': args.decimals,
                                   'same_triangle_set': triangle_keys(path, args.decimals) == reference}
    output = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(output, encoding='utf-8')
    else:
        print(output, end='')


if __name__ == '__main__':
    main()
