from math import sin, pi, cos, tan

class Make_points():

    def calc_side_length(self, rad_mul, num_sides):
        """Side length given the radius (circumradius):
        i/e the distance from the center to a vertex
        """
        side_length = 2 * (rad_mul / 2) * sin(pi / num_sides)

        # Apothem, i/e distance from the center of the polygon
        # to the midpoint of any side, given the side length
        tn = 2 * tan(pi / num_sides)
        apothem = side_length / tn
        return apothem, side_length

    def make_points(self, rad_mul, num_sides, hex_rad, x, y):
        pointsX = []
        pointsY = []
        angle = 2 * pi / num_sides
        apothem, side_length = Make_points.calc_side_length(self, rad_mul, num_sides)
        pointsX.append((x - side_length / 2) * hex_rad)
        pointsY.append((y - apothem) * hex_rad)
        for pdx in range(num_sides):
            angle = 2 * pi / num_sides * pdx
            x = cos(angle) * side_length * hex_rad
            y = sin(angle) * side_length * hex_rad
            pointsX.append(pointsX[- 1] + x)
            pointsY.append(pointsY[- 1] + y)
        return pointsX, pointsY