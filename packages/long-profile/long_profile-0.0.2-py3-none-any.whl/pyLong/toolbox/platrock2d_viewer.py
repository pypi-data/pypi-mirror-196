import os
from math import ceil

import numpy as np
from scipy.interpolate import interp1d
import tables

from pyLong.profiles.zprofile import zProfile
from pyLong.toolbox.trajectory import Trajectory

class PlatRock2DViewer:
    def __init__(self):
        self._name = "new platrock-2D viewer"
        
        self._hdf5 = None
        
        self.reset()
        
        self._g = 9.81
        
    # methods:
    # - from_hdf5
    # - get_ends
    # - get_starts
    # - trajectory
    # - get_trajectories
    # - reset      
    
    def from_hdf5(self, filename, zprofile, dx=1.):
        if not isinstance(filename, str) or not isinstance(zprofile, zProfile) or not isinstance(dx, (int, float)):
            return False
        
        if not os.path.isfile(filename):
            return False
        
        if not 0 < dx:
            return False
        
        try:
            hdf5 = tables.open_file(filename)
        except:
            hdf5 = None
            return False
        
        try:
            children = hdf5.root.__members__
        except:
            children = []
            return False
        
        if 'rocks' not in children:
            return False
        
        try:
            children = hdf5.get_node("/rocks")
        except:
            children = []
            return False
        
        if 'start_data' not in children or 'contacts' not in children:
            return False
        
        start_data = hdf5.get_node("/rocks/start_data")
        n = len(start_data)
        
        if not 1 < n:
            return False
        
        self._dx = dx
        self._hdf5 = hdf5
        self._n = n
        
        self._starts = self.get_starts()
        self._ends = self.get_ends()
        
        if not len(self._starts) == self._n or not len(self._ends) == self._n:
            self.reset()
            return False
        
        if not zprofile.x[0] <= min(self._starts) or not max(self._ends) <= zprofile.x[-1]:
            self.reset()
            return False
        
        self._zprofile = zprofile
        
        trajectories = self.get_trajectories()
        self._trajectories = trajectories
        
        if not len(self._trajectories) == self._n:
            self.reset()
            return False
        
        heights = self.get_heights()
        self._heights = heights
        
        if not len(self._heights) == self._n:
            self.reset()
            return False
        
        return True
    
    def get_starts(self):
        if self._hdf5:
            starts = []
            for i in range(self._n):
                data = self._hdf5.get_node(f"/rocks/contacts/{i}").read()
                if int(data[0,0]) == 0:
                    start = float(data[0, 1])
                    starts.append(start)
        else:
            starts = []
            
        return starts
    
    def get_ends(self):
        if self._hdf5:
            ends = []
            for i in range(self._n):
                data = self._hdf5.get_node(f"/rocks/contacts/{i}").read()
                if int(data[-1, 0]) in [5, 6]:
                    end = float(data[-1, 1])
                    ends.append(end)
        else:
            ends = []
            
        return ends
    
    def get_heights(self):
        heights = []
        
        for trajectory in self._trajectories:
            height = trajectory.duplicate()
            
            height.xz = [(x, z - self._zprofile.interpolate(x)) for x, z in trajectory.xz]
            
            heights.append(height)
            
        return heights
    
    def get_trajectories(self):
        trajectories = []
        
        for i in range(self._n):
            trajectory = Trajectory()
            
            data = self._hdf5.get_node(f"/rocks/contacts/{i}").read()
            
            trajectory.xz = [(float(data[0, 1]), float(data[0, 2])),
                             (float(data[-1, 1]), float(data[-1, 2]))]
            
            n = len(data)
            
            for j in range(n-1):
                code = int(data[j, 0])

                x_start = float(data[j, 1])
                x_end = float(data[j+1, 1])

                z_start = float(data[j, 2])
                z_end = float(data[j+1, 2])

                vx_start = float(data[j, 3])
                vz_start = float(data[j, 4])

                trajectory.add_point((x_start, z_start))
                trajectory.add_point((x_end, z_end))

                if (x_end - x_start) / self._dx > 1:
                    n = ceil((x_end - x_start) / self._dx)

                    for x in np.linspace(x_start, x_end, n+1):
                        if x == x_start or x == x_end:
                            continue

                        x = float(x)

                        if code in [0, 1, 2]:
                            z = -0.5 * self._g * ((x - x_start) / vx_start)**2 + vz_start * ((x - x_start) / vx_start) + z_start
                            trajectory.add_point((x, z))

                        elif code in [3, 4, 8]:
                            trajectory.add_point((x, self._zprofile.interpolate(x)))

            trajectories.append(trajectory)
        
        return trajectories
    
    def reset(self):
        self._hdf5 = None
        
        self._n = 0
        
        self._dx = 1.
        
        self._zprofile = None
        
        self._starts = []
        
        self._ends = []
        
        self._trajectories = []
        
        self._heights = []
        
    def trajectory(self, i):
        if not self._hdf5:
            return
        
        if not 0 <= i < self._n:
            return
        
        return self._trajectories[i]
    
    def height(self, i):
        if not self._hdf5:
            return
        
        if not 0 <= i < self._n:
            return
        
        return self._heights[i]
    
    def heights_at(self, x, stats=True):
        if not isinstance(x, (int, float)):
            return
        
        if not self._zprofile.x[0] <= x <= self._zprofile.x[-1]:
            return
        
        if not min(self._starts) <= x <= max(self._ends):
            return
        
        if not isinstance(stats, bool):
            return
        
        heights = []
        
        for height in self._heights:
            h = height.interpolate(x)
            if h is not None:
                heights.append(h)
            
        if stats:
            statistics = {}
            statistics['size'] = len(heights)
            statistics['maximum'] = max(heights)
            statistics['minimum'] = min(heights)
            statistics['mean'] = np.mean(heights)
            statistics['std'] = np.std(heights)
            statistics['median'] = np.median(heights)
            
            return heights, statistics
        else:
            return heights
    
    def heights_between(self, x_start, x_end, dx, stats=True):
        if not isinstance(x_start, (int, float)) or not isinstance(x_end, (int, float)) or not isinstance(dx, (int, float)):
            return
        
        if not self._zprofile.x[0] <= x_start < x_end <= self._zprofile.x[-1]:
            return
        
        if not min(self._starts) <= x_start < x_end <= max(self._ends):
            return
        
        if not 0 < dx <= x_end - x_start:
            return
        
        if not isinstance(stats, bool):
            return
        
        heights = []
        
        if (x_end - x_start) / dx > 1:
            n = ceil((x_end - x_start) / dx)

            for x in np.linspace(x_start, x_end, n+1):
                heights += self.heights_at(x, stats=False)
                
        if stats:
            statistics = {}
            statistics['size'] = len(heights)
            statistics['maximum'] = max(heights)
            statistics['minimum'] = min(heights)
            statistics['mean'] = np.mean(heights)
            statistics['std'] = np.std(heights)
            statistics['median'] = np.median(heights)
            
            return heights, statistics
        else:
            return heights
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(title, str):
            self._name = name
            
    @property
    def n(self):
        return self._n 
    
    def __repr__(self):
        return self._title
    
    @property
    def starts(self):
        return list(self._starts)
    
    @property
    def ends(self):
        return list(self._ends)