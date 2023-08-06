import numpy as np

from pyLong.profiles.zprofile import zProfile
from pyLong.misc.intersect import intersection


class Mezap:
    _counter = 0
    
    def __init__(self):
        Mezap._counter += 1
        
        self._title = f"Mezap n°{Mezap._counter}"
        
        self._zprofile = None
        
        self._start = None
        
        self._energy_angles = []
        
        self._distances = []
        
        self._areas = []
        
        self._cumulated_areas = []
        
        self._normalized_areas = []
        
        self._denominators = []
        
        self._intersections = []
        
        self._colors = []
        
        self._limits = np.array([
                                   [1.000e-02, 5.300e+01, 5.600e+01, 5.900e+01],
                                   [2.000e-02, 5.300e+01, 5.600e+01, 5.900e+01],
                                   [3.000e-02, 5.300e+01, 5.600e+01, 5.900e+01],
                                   [4.000e-02, 5.300e+01, 5.600e+01, 5.900e+01],
                                   [5.000e-02, 5.300e+01, 5.600e+01, 5.900e+01],
                                   [6.000e-02, 5.300e+01, 5.600e+01, 5.900e+01],
                                   [7.000e-02, 5.300e+01, 5.600e+01, 5.900e+01],
                                   [8.000e-02, 5.300e+01, 5.600e+01, 5.900e+01],
                                   [9.000e-02, 5.300e+01, 5.600e+01, 5.900e+01],
                                   [1.000e-01, 5.276e+01, 5.587e+01, 5.900e+01],
                                   [1.100e-01, 5.213e+01, 5.523e+01, 5.873e+01],
                                   [1.200e-01, 5.152e+01, 5.459e+01, 5.804e+01],
                                   [1.300e-01, 5.091e+01, 5.397e+01, 5.737e+01],
                                   [1.400e-01, 5.031e+01, 5.335e+01, 5.670e+01],
                                   [1.500e-01, 4.971e+01, 5.274e+01, 5.604e+01],
                                   [1.600e-01, 4.912e+01, 5.213e+01, 5.539e+01],
                                   [1.700e-01, 4.854e+01, 5.153e+01, 5.475e+01],
                                   [1.800e-01, 4.797e+01, 5.094e+01, 5.411e+01],
                                   [1.900e-01, 4.740e+01, 5.036e+01, 5.348e+01],
                                   [2.000e-01, 4.683e+01, 4.978e+01, 5.286e+01],
                                   [2.100e-01, 4.628e+01, 4.920e+01, 5.225e+01],
                                   [2.200e-01, 4.573e+01, 4.864e+01, 5.164e+01],
                                   [2.300e-01, 4.518e+01, 4.808e+01, 5.104e+01],
                                   [2.400e-01, 4.464e+01, 4.753e+01, 5.045e+01],
                                   [2.500e-01, 4.411e+01, 4.698e+01, 4.986e+01],
                                   [2.600e-01, 4.359e+01, 4.644e+01, 4.928e+01],
                                   [2.700e-01, 4.307e+01, 4.591e+01, 4.871e+01],
                                   [2.800e-01, 4.255e+01, 4.538e+01, 4.814e+01],
                                   [2.900e-01, 4.204e+01, 4.485e+01, 4.758e+01],
                                   [3.000e-01, 4.154e+01, 4.434e+01, 4.703e+01],
                                   [3.100e-01, 4.104e+01, 4.383e+01, 4.648e+01],
                                   [3.200e-01, 4.055e+01, 4.332e+01, 4.594e+01],
                                   [3.300e-01, 4.006e+01, 4.282e+01, 4.541e+01],
                                   [3.400e-01, 3.958e+01, 4.233e+01, 4.488e+01],
                                   [3.500e-01, 3.911e+01, 4.184e+01, 4.436e+01],
                                   [3.600e-01, 3.864e+01, 4.136e+01, 4.384e+01],
                                   [3.700e-01, 3.817e+01, 4.088e+01, 4.333e+01],
                                   [3.800e-01, 3.771e+01, 4.041e+01, 4.283e+01],
                                   [3.900e-01, 3.726e+01, 3.994e+01, 4.233e+01],
                                   [4.000e-01, 3.681e+01, 3.948e+01, 4.184e+01],
                                   [4.100e-01, 3.636e+01, 3.903e+01, 4.135e+01],
                                   [4.200e-01, 3.592e+01, 3.857e+01, 4.087e+01],
                                   [4.300e-01, 3.549e+01, 3.813e+01, 4.040e+01],
                                   [4.400e-01, 3.506e+01, 3.769e+01, 3.993e+01],
                                   [4.500e-01, 3.464e+01, 3.725e+01, 3.946e+01],
                                   [4.600e-01, 3.422e+01, 3.682e+01, 3.901e+01],
                                   [4.700e-01, 3.380e+01, 3.639e+01, 3.855e+01],
                                   [4.800e-01, 3.339e+01, 3.597e+01, 3.810e+01],
                                   [4.900e-01, 3.298e+01, 3.556e+01, 3.766e+01],
                                   [5.000e-01, 3.258e+01, 3.515e+01, 3.722e+01],
                                   [5.100e-01, 3.218e+01, 3.474e+01, 3.679e+01],
                                   [5.200e-01, 3.179e+01, 3.434e+01, 3.636e+01],
                                   [5.300e-01, 3.140e+01, 3.394e+01, 3.594e+01],
                                   [5.400e-01, 3.102e+01, 3.354e+01, 3.552e+01],
                                   [5.500e-01, 3.064e+01, 3.315e+01, 3.511e+01],
                                   [5.600e-01, 3.026e+01, 3.277e+01, 3.470e+01],
                                   [5.700e-01, 2.989e+01, 3.239e+01, 3.430e+01],
                                   [5.800e-01, 2.952e+01, 3.201e+01, 3.390e+01],
                                   [5.900e-01, 2.916e+01, 3.164e+01, 3.351e+01],
                                   [6.000e-01, 2.880e+01, 3.127e+01, 3.312e+01],
                                   [6.100e-01, 2.845e+01, 3.091e+01, 3.273e+01],
                                   [6.200e-01, 2.809e+01, 3.055e+01, 3.235e+01],
                                   [6.300e-01, 2.775e+01, 3.019e+01, 3.198e+01],
                                   [6.400e-01, 2.740e+01, 2.984e+01, 3.160e+01],
                                   [6.500e-01, 2.706e+01, 2.950e+01, 3.124e+01],
                                   [6.600e-01, 2.673e+01, 2.915e+01, 3.087e+01],
                                   [6.700e-01, 2.640e+01, 2.881e+01, 3.052e+01],
                                   [6.800e-01, 2.607e+01, 2.848e+01, 3.016e+01],
                                   [6.900e-01, 2.600e+01, 2.814e+01, 3.000e+01],
                                   [7.000e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [7.100e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [7.200e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [7.300e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [7.400e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [7.500e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [7.600e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [7.700e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [7.800e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [7.900e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [8.000e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [8.100e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [8.200e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [8.300e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [8.400e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [8.500e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [8.600e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [8.700e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [8.800e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [8.900e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [9.000e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [9.100e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [9.200e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [9.300e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [9.400e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [9.500e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [9.600e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [9.700e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [9.800e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [9.900e-01, 2.600e+01, 2.800e+01, 3.000e+01],
                                   [1.000e+00, 2.600e+01, 2.800e+01, 3.000e+01]])
        
    """
    Methods:
    - run
    - intersections
    """
    
    def print_intersections(self):
        print("+-------------------------+-------------------+")
        print("|", "angle d'énergie (deg)".center(23), "|", "aire normalisée".center(17), "|")
        print("+=========================+===================+")
        
        if len(self._intersections) == 0:
            return
        
        for angle, area in self._intersections:
            print("|", f"{round(angle, 2)}".center(23), "|", f"{round(area, 2)}".center(17), "|")
            print("+-------------------------+-------------------+")
    
    def run(self, zprofile, x_start=0.):
        if not isinstance(x_start, (int, float)) or not isinstance(zprofile, zProfile):
            return False
        
        if not zprofile.x[0] <= x_start <= zprofile.x[-1]:
            return False
        
        self._zprofile = zprofile.duplicate()
        
        self._start = (x_start, zprofile.interpolate(x_start))
        
        self._zprofile.add_point(self._start)
        self._zprofile.translate(dimension='X', value=-x_start)
        
        indexes = []
        for i, x in enumerate(self._zprofile.x):
            if x < 0.:
                indexes.append(i)
                
        indexes.reverse()
        for i in indexes:
            self._zprofile.remove_point(i)
            
        x = np.array(self._zprofile.x)
        z = np.array(self._zprofile.z)
        
        x_start = x[0]
        z_start = z[0]
        
        distances = np.zeros(len(x))
        distances[1:] = np.sqrt((x[1:] - x[:-1])**2 + (z[1:] - z[:-1])**2)
        distances = np.cumsum(distances)
        
        energy_angles = np.zeros(len(x))
        
        energy_angles[1:] = np.degrees([np.arctan2(np.abs(z_start - z), np.abs(x_start - x)) for x, z in zip(x[1:], z[1:])])
        
        areas = np.zeros(len(x))
        
        areas[1:] = (x[1:] + x[:-1]) * (z[:-1] - z[1:])
        areas /= 2.
        
        cumulated_areas = np.cumsum(areas)
        
        denominators = np.ones(len(x))
        denominators[1:] = (z_start - z[1:])**2
        
        normalized_areas = cumulated_areas / denominators
        
        self._distances = distances
        self._energy_angles = energy_angles
        self._areas = areas
        self._cumulated_areas = cumulated_areas
        self._denominators = denominators
        self._normalized_areas = normalized_areas
        
        intersections = []
        colors = []

        areas, angles = intersection(self._normalized_areas[1:], self._energy_angles[1:], self._limits[:,0], self._limits[:,3])

        for area, angle in zip(areas, angles):
            intersections.append((float(angle), float(area)))
            colors.append(['Red', 'Red'])

        areas, angles = intersection(self._normalized_areas[1:], self._energy_angles[1:], self._limits[:,0], self._limits[:,2])

        for area, angle in zip(areas, angles):
            intersections.append((float(angle), float(area)))
            colors.append(['Orange', 'Orange'])

        areas, angles = intersection(self._normalized_areas[1:], self._energy_angles[1:], self._limits[:,0], self._limits[:,1])

        for area, angle in zip(areas, angles):
            intersections.append((float(angle), float(area)))
            colors.append(['Green', 'Green'])
            
        self._intersections = intersections
        self._colors = colors
        
        return True
        
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        if isinstance(title, str):
            self._title = title
            
    @property
    def zprofile(self):
        return self._zprofile
        
    @property
    def start(self):
        return self._start
    
    @property
    def energy_angles(self):
        return list(self._energy_angles)
    
    @property
    def distances(self):
        return list(self._distances)
            
    @property
    def areas(self):
        return list(self._areas)
    
    @property
    def cumulated_areas(self):
        return list(self._cumulated_areas)
    
    @property
    def denominators(self):
        return list(self._denominators)
            
    @property
    def normalized_areas(self):
        return list(self._normalized_areas)
    
    @property
    def intersections(self):
        return list(self._intersections)
        
    def __repr__(self):
        return f"{self._title}"

    def __del__(self):
        Mezap._counter -= 1