from shapely.geometry import Polygon, Point
from shapely.affinity import rotate
from gsd.pygsd import GSDFile
from math import pi, tan, cos, acos, sin
import numpy as np
import Make_points
import ReadFile
import gsd.hoomd
import matplotlib.pyplot as plt
import json

class ShapelyBuild():

    def make_polygons(self, posX, posY, orientation, frame_count, config):
        polygons = []
        hex_rad = 1.0
        x = 0
        y = 0
        Polygons = []
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

        for frame in range(frame_count):
            frames = []
            s = 0
            particle = 0
            for i in range(len(orientation[0])): 
                if s < config['particles_count'][particle]:
                    polX = []
                    polY = []
                    for point in range(len(Polygons[particle])):
                        polX.append(Polygons[particle][point][0] + posX[frame][0][i])
                        polY.append(Polygons[particle][point][1] + posY[frame][0][i])
                    rotate_angle = acos(orientation[frame][i][0]) * 180/pi
                    Figure = Polygon(zip(polX, polY))
                    frames.append(rotate(Figure, 
                                         rotate_angle, 
                                         origin = Point(posX[frame][0][i], posY[frame][0][i]), 
                                         use_radians = False))
                    s += 1
                if s == config['particles_count'][particle]:
                    particle = config['particles_count'].index(s) + 1
                    if s == config['particles_count'][-1]:
                        particle = 0
                    s = 0
            polygons.append([frames])
        return polygons

    def PlotPolygons(self, config):
        #Read data from .gsd file
        position = []
        orientation = []
        with GSDFile(open("hex_flake.gsd", "rb")) as f:
            trajectory = gsd.hoomd.HOOMDTrajectory(f)
            frame_count = f.nframes
            for i in range(frame_count):
                position.append(trajectory[i].particles.position)
                orientation.append(trajectory[i].particles.orientation)

        #Shape this data to normal view
        posX = []
        posY = []
        for frame in range(frame_count):
            frameX = []
            frameY = []
            for i in range(len(position[frame])):
                frameX.append(position[frame][i][0])
                frameY.append(position[frame][i][1])
            posX.append([frameX])
            posY.append([frameY])

        polygons = ShapelyBuild.make_polygons(self, posX, posY, orientation, frame_count, config)

        colors = ['b', 'r', 'g', 'c ', 'y', 'k', 'm']

        with open('log_free_volume.dat', 'r', encoding = 'utf-8') as f:
            free_volume = []
            time = []
            next(f)
            for line in f:
                if line == '':
                    break
                d = line.split('\t')
                time.append(float(d[0]))
                free_volume.append(4 * config['particles_radius'][0]**2 * 
                config['particles_sides_count'][0] * sin(2 * pi/config['particles_sides_count'][0])
                / (float(d[1].replace('\n', ' ')) * 2) * 10**2)
        print(free_volume)
        plt.plot(time, free_volume)
        plt.show()
        
'''
        for frame in range(frame_count):
            plt.figure(frame)
            s = 0
            particle = 0
            for i in range(len(polygons[frame][0])):
                if s < config['particles_count'][particle]:
                    plt.plot(*polygons[frame][0][i].exterior.xy, color = colors[particle], linewidth = 0.5)
                    s += 1
                if s == config['particles_count'][particle]:
                    particle = config['particles_count'].index(s) + 1
                    if s == config['particles_count'][-1]:
                        particle = 0
                    s = 0
            plt.axes().set_aspect(1.0)
            plt.savefig("frame_" + str(frame) + ".png", dpi = 96)
'''