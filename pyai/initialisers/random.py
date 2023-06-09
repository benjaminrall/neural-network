from pyai.initialisers.initialiser import Initialiser
import numpy as np

class RandomNormal(Initialiser):
    name = 'random_normal'

    def __init__(self, mean: float = 0.0, stddev: float = 0.05) -> None:
        self.mean = mean
        self.stddev = stddev
    
    def call(self, shape: tuple) -> np.ndarray:
        return np.random.normal(self.mean, self.stddev, shape)
    
class RandomUniform(Initialiser):
    name = 'random_uniform'

    def __init__(self, low: float = -0.05, high: float = 0.05) -> None:
        self.low = low
        self.high = high
    
    def call(self, shape: tuple) -> np.ndarray:
        return np.random.uniform(self.low, self.high, shape)