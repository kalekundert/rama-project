#!/usr/bin/env python2

""" 
Make a Ramachandran plot for the given structure or structures.  If multiple 
structures are given, the resulting plot will combine points from all of them.

Usage:
    fancy-rama.py [options] <pdb_file_or_tag>...

Options:
    --filter=FILTER         Specify what kinds of residues to plot.
    --plot=PLOT             Specify how the plot should be rendered.
    --blur=BLUR             Specify how much the plot should be smoothed.
    --quiet                 Suppress the GUI.
"""

from __future__ import division

def pdb_from_file_or_tag(file_or_tag):
    import os
    import requests

    if os.path.exists(file_or_tag):
        with open(file_or_tag) as file:
            return file.read()
    else:
        url = 'http://www.rcsb.org/pdb/files/{0}.pdb'.format(path_or_tag)
        return requests.get(url).text

def atoms_from_pdb(pdb):
    import collections

    atoms = []
    Atom = collections.namedtuple('Atom', 'xyz residue')
    backbone = 'N', 'CA', 'C'

    for line in pdb.split('\n'):
        field_type = line[0:6].strip()

        if field_type == 'ATOM':
            atom_name = line[12:16].strip()
            residue_name = line[17:20].upper().strip()

            if atom_name in backbone:
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])

                xyz = x, y, z
                atom = Atom(xyz, residue_name)
                atoms.append(atom)

    return atoms

def torsions_from_atoms(atoms):
    import vector
    import collections

    torsions = []
    RamaInfo = collections.namedtuple('RamaInfo', 'phi psi residue')
    num_residues = len(atoms) // 3 - 2

    try:
        for i in range(1, num_residues):
            v1 = atoms[3 * i - 1].xyz
            v2 = atoms[3 * i + 0].xyz
            v3 = atoms[3 * i + 1].xyz
            v4 = atoms[3 * i + 2].xyz
            v5 = atoms[3 * i + 3].xyz

            phi = vector.torsion(v1, v2, v3, v4)
            psi = vector.torsion(v2, v3, v4, v5)
            residue = atoms[3 * i].residue

            rama_info = RamaInfo(phi, psi, residue)
            torsions.append(rama_info)

    except ZeroDivisionError:
        return []
    
    else:
        return torsions

def filter_torsions(torsions, phis, psis, filter):
    for index, rama_info in enumerate(torsions):
        phi, psi, residue = rama_info

        if filter == 'normal':
            if residue == 'GLY': continue
            if residue == 'PRO': continue

        elif filter == 'gly':
            if residue != 'GLY': continue

        elif filter == 'pro':
            if residue != 'PRO': continue

        elif filter == 'pre-pro':
            if index == len(torsions) - 1: continue
            if torsions[index + 1].residue != 'PRO': continue

        else:
            raise ValueError("Unknown filter '{}'.".format(filter))

        phis.append(phi)
        psis.append(psi)

def make_rama_plot(phi, psi, style=None, blur=None):
    import numpy as np
    import matplotlib.pyplot as plt

    import warnings
    warnings.simplefilter('ignore')

    if style is None or style == 'scatter':
        plt.plot(phi, psi, '.')

    elif style == 'heatmap' or style == 'contour':
        hist_shape = (-180, 180), (-180, 180)
        plot_shape = hist_shape[0] + hist_shape[1]

        # Make a 2D histogram of the data.

        hist_shape = (-180, 180), (-180, 180)
        bins, x_edges, y_edges = np.histogram2d(
                psi, phi, bins=180, range=hist_shape)

        heatmap = np.log10(bins)
        heatmap[bins == 0] = 0

        # Apply gaussian smoothing.

        if style == 'contour' and blur is None:
            blur = 2.0

        if blur is not None:
            import scipy.ndimage
            heatmap = scipy.ndimage.gaussian_filter(
                    heatmap, sigma=blur, order=0)

        # Calculate the center of each bin.

        x_centers = 0.5 * (x_edges[1:] + x_edges[:-1])
        y_centers = 0.5 * (y_edges[1:] + y_edges[:-1])
        x, y = np.meshgrid(x_centers, y_centers)

        # Plot the data.

        if style == 'heatmap':
            plt.imshow(heatmap, extent=plot_shape, origin='lower')
        if style == 'contour':
            plt.contour(x, y, heatmap)

    else:
        raise ValueError("Unknown plot style '{}'.".format(style))

    plt.xlabel('Phi')
    plt.ylabel('Psi')
    plt.xticks(np.arange(-180, 181, 90))
    plt.yticks(np.arange(-180, 181, 90))
    plt.xlim(-180,180)
    plt.ylim(-180,180)
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    import docopt

    arguments = docopt.docopt(__doc__.strip())
    pdbs = arguments['<pdb_file_or_tag>']
    filter = arguments['--filter']
    style = arguments['--plot']
    blur = float(arguments['--blur'])
    quiet = arguments['--quiet']

    phis, psis = [], []

    for file_or_tag in pdbs:
        pdb = pdb_from_file_or_tag(file_or_tag)
        atoms = atoms_from_pdb(pdb)
        torsions = torsions_from_atoms(atoms)
        filter_torsions(torsions, phis, psis, filter)

    if not quiet:
        make_rama_plot(phis, psis, style, blur)

