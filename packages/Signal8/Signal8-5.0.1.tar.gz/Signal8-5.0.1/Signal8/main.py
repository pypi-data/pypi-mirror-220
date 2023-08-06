import signal8
import numpy as np
import matplotlib.pyplot as plt

from itertools import product
from shapely import Point, LineString, MultiLineString, Polygon

CORNERS = list(product((1, -1), repeat=2))
BOUNDARIES = [LineString([CORNERS[0], CORNERS[2]]),
              LineString([CORNERS[2], CORNERS[3]]),
              LineString([CORNERS[3], CORNERS[1]]),
              LineString([CORNERS[1], CORNERS[0]])]
SQUARE = Polygon([CORNERS[2], CORNERS[0], CORNERS[1], CORNERS[3]])


def test_coeffs(given_list):
    coeffs = np.array(given_list).reshape(-1, 3)
    lines = get_lines_from_coeffs(coeffs)
    valid_lines = get_valid_lines(lines)
    regions = create_regions(valid_lines)

    for region in regions:
        plt.fill(*region.exterior.xy, alpha=0.5)

def get_lines_from_coeffs(coeffs):
    lines = []
    equations = np.reshape(coeffs, (-1, 3))
    for equation in equations:
        a, b, c = equation

        if a == 0:  # Horizontal line
            start, end = (-1, -c/b), (1, -c/b)
        elif b == 0:  # Vertical line
            start, end = (-c/a, -1), (-c/a, 1)
        else:
            slope = a / -b
            if abs(slope) >= 1:
                y1 = (-a + c) / -b
                y2 = (a + c) / -b
                start, end = (-1, y1), (1, y2)
            else:
                x1 = (-b + c) / -a
                x2 = (b + c) / -a
                start, end = (x1, -1), (x2, 1)

        lines.append(LineString([start, end]))

    return lines

def get_valid_lines(lines):
    valid_lines = list(BOUNDARIES)

    for line in lines:
        intersection = SQUARE.intersection(line)
        if not intersection.is_empty and not intersection.geom_type == 'Point':
            coords = np.array(intersection.coords)
            if np.any(np.abs(coords) == 1, axis=1).all():
                valid_lines.append(intersection)

    return valid_lines

def create_regions(valid_lines, distance=2e-11):
    lines = MultiLineString(valid_lines).buffer(distance=distance)
    boundary = lines.convex_hull
    polygons = boundary.difference(lines)
    regions = [polygons] if polygons.geom_type == 'Polygon' else list(polygons.geoms)
    return regions




env = signal8.env()
given_list = [1, 1, 0.95, 1, -1, 0.95, -1, 1, 0.95, -1, -1, 0.95]
problem_instance = 'corners'
# test_coeffs(given_list)

agent_radius = env.unwrapped.world.agents[0].radius
obstacle_radius = env.unwrapped.world.large_obstacles[0].radius

for i in range(100):
    env.reset(options={'problem_instance': problem_instance})
    start_state = env.state()
    start = start_state[0:2]
    goal = start_state[2:4]
    obstacles = start_state[4:].reshape(-1, 2)
    
    agent_with_size = Point(start).buffer(agent_radius)
    goal_with_size = Point(goal).buffer(agent_radius)
    obstacles_with_size = [Point(obs_pos).buffer(obstacle_radius) for obs_pos in obstacles]

    for obstacle in obstacles_with_size:
        plt.fill(*obstacle.exterior.xy, alpha=0.5, color='red')
    
    plt.fill(*agent_with_size.exterior.xy, alpha=0.5, color='green')
    plt.fill(*goal_with_size.exterior.xy, alpha=0.5, color='green')

plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.show()
a=3