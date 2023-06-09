from pyai.optimisers.optimiser import Optimiser
from pyai.layers.layer import Layer
from pyai.backend.utilities import epsilon
from collections import defaultdict
import numpy as np

class Nadam(Optimiser):
    name = 'nadam'

    def __init__(self, eta: float = 0.001, beta_1: float = 0.9, beta_2: float = 0.999, bias_correction: bool = True) -> None:
        self.eta = eta
        self.beta_1 = beta_1
        self.one_sub_beta_1 = 1 - beta_1
        self.beta_2 = beta_2
        self.one_sub_beta_2 = 1 - beta_2
        self.bias_correction = bias_correction
        self.m = defaultdict(lambda : defaultdict(lambda : 0))
        self.v = defaultdict(lambda : defaultdict(lambda : 0))
        self.iterations = defaultdict(lambda : 0)
        self.epsilon = epsilon()

    def optimise_gradients(self, layer: Layer, gradients: list[np.ndarray]) -> list[np.ndarray]:
        iteration = self.iterations[layer] = self.iterations[layer] + 1

        layer_M = self.m[layer]
        layer_V = self.v[layer]

        for i in range(len(gradients)):
            corrected_M = layer_M[i] = self.beta_1 * layer_M[i] + self.one_sub_beta_1 * gradients[i]
            corrected_V = layer_V[i] = self.beta_2 * layer_V[i] + self.one_sub_beta_2 * np.square(gradients[i])

            if self.bias_correction:
                corrected_M = layer_M[i] / (1 - np.power(self.beta_1, iteration))
                corrected_V = layer_V[i] / (1 - np.power(self.beta_2, iteration))

            corrected_M = self.beta_1 * corrected_M + self.one_sub_beta_1 * gradients[i]

            gradients[i] = -self.eta * corrected_M / (np.sqrt(corrected_V) + self.epsilon)
        return gradients