import numpy as np

class Airfoil:

    def __init__(self, naca_code: str): # using 4 digit naca codes where
                                        # index 0 -> max. camber | index 1 -> max. camber location | index 2-3 -> thickness
        self._max_camber = int(naca_code[0]) / 100
        self._max_camber_location = int(naca_code[1]) / 10
        self._thickness = int(naca_code[2:]) / 100

        self._is_symmetric = (self._max_camber == 0) and (self._max_camber_location == 0)

    def generate_coords(self, resolution: int):

        max_cam = self._max_camber
        max_cam_loc = self._max_camber_location
        thickness = self._thickness

        beta = np.linspace(0, np.pi, resolution)    # cosine spacing clusters points
        x_coords = (1 - np.cos(beta)) / 2           # near leading and trailing edge


        y_thickness = 5 * thickness * (
                    (0.2969 * np.sqrt(x_coords))
                    - (0.1260 * x_coords)               # empirical curve fit for naca airfoil
                    - (0.3516 * (x_coords ** 2))        # where x_coords^4 term is .1036 rather than .1015
                    + (0.2843 * (x_coords ** 3))        # used in classic definition, leading to a
                    - (0.1036 * (x_coords ** 4))        # 'closed' trailing edge (closed definition)
        )

        if self._is_symmetric:

            y_camber = np.zeros_like(x_coords)
            dycam_dx = np.zeros_like(x_coords)

        else:

            y_camber = np.where(
                x_coords < max_cam_loc, # condition

                ((max_cam / (max_cam_loc ** 2) * (2 * max_cam_loc * x_coords - (x_coords ** 2)))),  # x < p, condition True

                ((max_cam / ((1 - max_cam_loc) ** 2))   # x >= p, condition False
                 * ((1 - (2 * max_cam_loc)) + (2 * max_cam_loc * x_coords) - (x_coords ** 2)))
            )   # x < p for before max. camber achieved, x >= p for at and after max. camber achieved

            dycam_dx = np.where(
                x_coords < max_cam_loc, #condition

                (2 * max_cam / (max_cam_loc ** 2))
                * (max_cam_loc - x_coords),

                (2 * max_cam / ((1 - max_cam_loc) ** 2))
                * (max_cam_loc - x_coords)
            )

        theta = np.arctan(dycam_dx)

        x_upper_surface = x_coords - y_thickness * np.sin(theta)
        y_upper_surface = y_camber + y_thickness * np.cos(theta)

        x_lower_surface = x_coords + y_thickness * np.sin(theta)
        y_lower_surface = y_camber - y_thickness * np.cos(theta)

        return x_upper_surface, y_upper_surface, x_lower_surface, y_lower_surface