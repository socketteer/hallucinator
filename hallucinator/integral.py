import hallucinator as hl
import numpy as np


def integrate_vectors(vectors):
    endpoint = np.array([0, 0])
    new_endpoints = np.array([[0, 0]])
    for v in vectors:
        endpoint = np.add(endpoint, v)
        new_endpoints = np.append(new_endpoints, [endpoint], axis=0)
    return new_endpoints


def draw_path(vectors, endpoints, scene):
    for i, vector in enumerate(vectors):
        scene.add_object(hl.arrow(p0=endpoints[i], direction=vector, length=1, head_length=0.3), name=f"arrow{i}")


# plots one dimensional phase integral (like clothoid) of complex pattern
# currently samples along y=0
# TODO arbitrary path
def plot_phase_integral(pattern, plot_range, resolution, scene):
    num_samples = (plot_range[1] - plot_range[0]) * resolution
    sample_points = [(p, 0) for p in np.linspace(plot_range[0], plot_range[1], num_samples)]
    sampled_vectors = np.array([pattern(p) for p in sample_points])
    endpoints = integrate_vectors(sampled_vectors)
    draw_path(sampled_vectors, endpoints, scene)
    return endpoints


