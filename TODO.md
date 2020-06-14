# 6/5/20

aliasing on pinch zones, 3 pinches. Do all generate zones&pinches? Or self-similar?
generalize
better sampling by grid:
    need to make points sampled always the same.
    the grid should be shifted over exactly, not approximately
    
the pinch zones come from moire between the zone plate and the perspective warped zone plate
and the moire with the sampling pixels reveals complexity
what about pinch zone and pinch zone? How might I warp it? A fresnel hyperbola...

Features
    Contour maps for parabolas (fourier, fresnel), circles, ellipse. Compare to zone plates

Code
    Improve argument specification for perspective code
    Profile perspective code

Explore
    Opencv keyboard interaction for zone plate scene exploration? (or is matplotlib enough?) Change xy plane range?
        https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_mouse_handling/py_mouse_handling.html
    Helper function for stacking and displaying images?

Display
    Helper function for interpolation video, filenames?
    Non-square videos
    Parameters on first frame of video?
        https://www.geeksforgeeks.org/python-opencv-cv2-puttext-method/


# 10/26/19

function to modify existing surface/path object with texture

fix repeated code for adding disturbances

3d diffeq fields
diffeq translation methods / class

scene types:
    full color (x, y, z, (R, G, B))

group/paraobject
    make density individual attribute
    make density variable
    autonaming
    transformations
        mirroring
        projection
            pinhole

scene
    RGB scene
    autonaming

object
    go through everything and make sure it all follows one convention
    ellipses
    solid shapes and surfaces
    rectangle, circle etc in 3d
    convert 2d to flat 3d
    change vectors to use transforms instead of lambdas?
    vertices w adjacency

sampler
    random sampling
    planes & other parametric -- find bounds based on transform & perspective
    clipping


filled surfaces
obstructing objects

optics
    ray
        shading
        lenses, mirrors
    waves
        integrate
        interference from >2 sources
        diffraction
    testbench
        symbols


BUGS

wavelengths arent correct?
images also flipped 90 degrees?
videos switch red/blue and rotated 90 degrees
video dimensions error unless square?

