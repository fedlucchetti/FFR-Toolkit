import numpy as np

class Constants():
    def __init__(self):
        self.fs        = 24414.0
        self.dt        = 1/self.fs
        self.Nt        = 2048
        self.Nf        = 1024
        self.df        = self.fs/self.Nt
        self.t         = self.dt*np.array([x for x in range(self.Nt)])
        self.f         = self.df*np.array([x for x in range(self.Nf)])
