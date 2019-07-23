import hallucinator


def ripple(num_crests, wavelength, center=(0, 0)):
    rip = hallucinator.Group(species='ripple')
    for i in range(num_crests):
        rip.add_component(hallucinator.circle(r=(i + 1) * wavelength, c=center))
    return rip
