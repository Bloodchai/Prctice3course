from math import *
import Make_points
import sys
import json
import numpy as np
import hoomd
import hoomd.hpmc

class Run_hoomd():

    def make_grid(self, a1, a2, N):
        gridX = []
        gridY = []
        x_gap = a1[0]/N
        y_gap = a2[1]/N
        x_mid = a1[0]/2
        y_mid = a2[1]/2
        gridX.append(-x_mid)
        gridY.append(-y_mid)
        for i in range(0, N, 1):
            gridX.append(gridX[i] + x_gap)
            gridY.append(gridY[i] + y_gap)
        return gridX, gridY

    def hoomd_build(self, config):
        hex_rad = 1.0
        a1 = [2, 0, 0]
        a2 = [0, 2, 0]
        x = 0
        y = 0

        Polygons = []
        hex_verts = []
        for particle in range(len(config['particles_sides_count'])):
            PolygonX, PolygonY = Make_points.Make_points().make_points(config['particles_radius'][particle],
                                                                       config['particles_sides_count'][particle],
                                                                       hex_rad,
                                                                       x, 
                                                                       y)
            Figure = []
            for point in range(len(PolygonX)):
                Figure.append([PolygonX[point], PolygonY[point]])
            Polygons.append(Figure)
            hex_verts.append(Figure[:-1])

        hoomd.context.initialize("--mode=cpu")
        
        types = []
        diameters=[]
        coords = []
        N = sum(config['particles_count'])

        gridX, gridY = Run_hoomd.make_grid(self, a1, a2, N)

        types_name = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        pos = 0
        for particle in range(len(config['particles_count'])):
            i = 0
            while i < config['particles_count'][particle]:
                p_hex = [gridX[pos], gridY[pos], 0]
                coords.append(p_hex)
                types.append(types_name[particle])
                i += 1
                pos += 1
                diameters.append(2 * hex_rad)

        uc = hoomd.lattice.unitcell(N = N,
                                    a1 = a1,
                                    a2 = a2,
                                    a3 = [0, 0, 1],
                                    dimensions = 2,
                                    position = coords,
                                    diameter = diameters,
                                    type_name = types)

        system = hoomd.init.create_lattice(unitcell = uc, n = [8, 8])

        '''
        Lx = system.box.Lx
        Ly = system.box.Ly
        N = len(system.particles)
        '''

        if config['iters_count'] == 0:
            mc = hoomd.hpmc.integrate.convex_polygon(d = 0.01, a = 0.01, seed = config['seed'][0])
        else:
            mc = hoomd.hpmc.integrate.simple_polygon(d = 0.01, a = 0.01, seed = config['seed'][1])
        for name in range(len(config['particles_count'])):
            mc.shape_param.set(types_name[name], vertices = hex_verts[name])

        hoomd.hpmc.compute.free_volume(mc = mc, seed = 123, test_type = 'B', nsample = 1000)
        log = hoomd.analyze.log(quantities = ['hpmc_free_volume'], 
                                period = 100, 
                                filename = 'log_free_volume.dat', 
                                overwrite = True)
        dump = hoomd.dump.gsd("hex_flake.gsd", 
                              period = 10000, 
                              group = hoomd.group.all(), 
                              overwrite = True)
        log1 = hoomd.analyze.log(filename = "log-output.log",
                                 quantities = ['lx', 'ly', 'N', 'volume'],
                                 period = 1000,
                                 overwrite = True)
        hoomd.run(100000)
