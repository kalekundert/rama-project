#!/usr/bin/env python

from __future__ import division

import sys
import vector
import pylab

input = sys.argv[1]
backbone = 'N', 'CA', 'C'
coordinates = []
phis = []
psis = []

# Read in coordinate data from the PDB file.

with open(input) as file:
    for line in file:
        field_type = line[0:6].strip()

        if field_type == 'ATOM':
            atom_name = line[12:16].strip()

            if atom_name in backbone:
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])

                coordinate = x, y, z
                coordinates.append(coordinate)

# Calculate all the phi and psi torsions.

num_residues = len(coordinates) // 3 - 2

for i in range(1, num_residues):
    v1 = coordinates[3 * i - 1]
    v2 = coordinates[3 * i + 0]
    v3 = coordinates[3 * i + 1]
    v4 = coordinates[3 * i + 2]
    v5 = coordinates[3 * i + 3]

    phi = vector.torsion(v1, v2, v3, v4)
    psi = vector.torsion(v2, v3, v4, v5)

    phis.append(phi)
    psis.append(psi)

# Generate the Ramachandran plot.

pylab.plot(phis, psis, '.')
pylab.xlabel('Phi')
pylab.ylabel('Psi')
pylab.xlim(-180, 180)
pylab.ylim(-180, 180)
pylab.xticks(range(-180, 181, 90))
pylab.yticks(range(-180, 181, 90))
pylab.grid(True)
pylab.show()
