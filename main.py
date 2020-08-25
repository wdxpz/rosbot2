from goto import GoToPose

pts = [(0.2, 0.2), (0.4, 0.4)]

def builtRoute(points):
    route = []
    for i in range(len(points)):
        pt = {
            'position': {
                'x': points[i][0],
                'y': points[i][1]
            },
            'quaternion': {
                'r1': 0,
                'r2': 0,
                'r3': 0,
                'r4': 1
        }
    route.append(pt)
    return route



