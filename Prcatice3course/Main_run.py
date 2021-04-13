import Run_hoomd
import Shapely_polygon
import ReadFile

config = ReadFile.ReadFile().ReadFile('ConfigureFile.json')

Run_hoomd.Run_hoomd().hoomd_build(config)
Shapely_polygon.ShapelyBuild().PlotPolygons(config)