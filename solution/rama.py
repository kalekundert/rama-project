#!/usr/bin/env python

from __future__ import division

import sys
import vector
import pylab

input = sys.argv[1]
backbone = 'N', 'CA', 'C'
coordinates = []
phi = []
psi = []

# Read in coordinate data from the PDB file.

with open(input) as file:
    for line in file:
        field_type = line[0:6].strip()

        if field_type == 'ATOM':
            atom_name = line[12:16].strip()
            chain_id = line[21:22].strip()

            if atom_name in backbone and chain_id == 'A':
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])

                coordinate = x, y, z
                coordinates.append(coordinate)

# Calculate phi, psi, and omega torsion angles.

num_phi = len(coordinates) // 3 - 2
num_psi = len(coordinates) // 3 - 2

for i in range(num_phi):
    v1 = coordinates[3 * i + 2]
    v2 = coordinates[3 * i + 3]
    v3 = coordinates[3 * i + 4]
    v4 = coordinates[3 * i + 5]

    angle = vector.torsion(v1, v2, v3, v4)
    phi.append(angle)

for i in range(num_psi):
    v1 = coordinates[3 * i + 3]
    v2 = coordinates[3 * i + 4]
    v3 = coordinates[3 * i + 5]
    v4 = coordinates[3 * i + 6]

    angle = vector.torsion(v1, v2, v3, v4)
    psi.append(angle)

# Generate the Ramachandran plot.

pylab.title("Ramachandran Plot (%s)" % input)
pylab.plot(phi, psi, '.')
pylab.xlabel('Phi')
pylab.ylabel('Psi')
pylab.xlim(-180, 180)
pylab.ylim(-180, 180)
pylab.xticks(range(-180, 181, 90))
pylab.yticks(range(-180, 181, 90))
pylab.grid(True)
pylab.show()
