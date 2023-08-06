class PointPare(object):

    def __init__(self):
        self._pared_points = []
        self._points = []
        self._point_map = {}

    def clear_points(self):
        self._points = []
        self._point_map = {}

    def add_point(self, point):
        self._points.append(point)

    def add_points(self, points):
        if len(points):
            if isinstance(points[0], list):
                self._points.extend(points)
            else:
                self._points.extend(list(_chunks(points, 3)))

    def pare_points(self):
        self._pared_points = []
        tmp = {}
        for index, pt in enumerate(self._points):
            dim = 0
            c_prev = []
            new_point = False
            while dim < len(pt):
                c = str(pt[dim])
                if dim == 0 and c not in tmp:
                    tmp[c] = {}
                elif dim == 1 and c not in tmp[c_prev[0]]:
                    tmp[c_prev[0]][c] = {}
                elif dim == 2 and c not in tmp[c_prev[0]][c_prev[1]]:
                    tmp[c_prev[0]][c_prev[1]][c] = -1
                    new_point = True

                c_prev.append(c)
                dim += 1

            if new_point:
                # print("new point")
                pared_index = len(self._pared_points)
                tmp[c_prev[0]][c_prev[1]][c_prev[2]] = pared_index
                self._pared_points.append(pt)
            else:
                # print("old point")
                pared_index = tmp[c_prev[0]][c_prev[1]][c_prev[2]]

            self._point_map[index] = pared_index

    def get_pared_index(self, point_index):
        """
        Return the pared node index for the original
        node position.
        """
        return self._point_map[point_index]

    def get_pared_points(self):
        return self._pared_points


def _chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
