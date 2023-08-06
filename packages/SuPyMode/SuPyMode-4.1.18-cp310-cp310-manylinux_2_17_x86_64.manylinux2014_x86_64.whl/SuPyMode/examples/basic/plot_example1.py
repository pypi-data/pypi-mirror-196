"""
1x1 Coupler
===========
"""

# %%
# Importing the package dependencies: FiberFusing, PyFinitDiff
from FiberFusing import Geometry, Fused1, BackGround
from FiberFusing.fiber_catalogue import DCF1300S_33
from PyFinitDiff.boundaries import Boundaries2D
from SuPyMode.solver import SuPySolver
from SuPyMode.profiles import AlphaProfile


# %%
# Generating the fiber structure
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Here we make use of the FiberFusing to generate a fiber structure that we use
# as the cladding.
wavelength = 1.55e-6

index = 1.4444

air = BackGround(index=1)

clad = Fused1(fiber_radius=62.5e-6, index=index)

_ = clad.plot().show()

# %%
# Creating the geometry rasterization
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The cladding being defined we create the cores that are distributed at
# each (virtual) center of the cladding.
# All the components: air -- cladding -- cores, are inputed into a geometry class
# that will generate the mesh which will be used in the finit-difference matrix.
fibers = [
    DCF1300S_33(wavelength=wavelength, position=core) for core in clad.cores
]

geometry = Geometry(
    background=air,
    structures=[clad],
    x_bounds='centering-left',
    y_bounds='centering-top',
    n=40,
    index_scrambling=1e-6,
    gaussian_filter=0.1
)

geometry.add_fiber(*fibers)

_ = geometry.plot().show()

# %%
# We here create the solver class and generate the superset which
# will contains the supermodes to be computed.
solver = SuPySolver(
    geometry=geometry,
    tolerance=1e-8,
    max_iter=10000,
    show_iteration=False  # Put this to True to see the computing progression
)

solver.init_superset(
    wavelength=wavelength,
    n_step=500,
    itr_i=1.0,
    itr_f=0.05
)


# %%
# We now add supermodes for different type of attributes such as boundaries.
# By default the solver assume no boundaries in the system.
_ = solver.add_modes(
    boundaries=Boundaries2D(right='symmetric', bottom='symmetric'),
    n_computed_mode=4,
    n_sorted_mode=2
)

_ = solver.add_modes(
    boundaries=Boundaries2D(right='symmetric', bottom='anti-symmetric'),
    n_computed_mode=4,
    n_sorted_mode=2
)

# One important thing to understand here is as the probleme has a circular symmetry
# and no boundary condition are given to fix them the computed eigen vector
# which are supposed to represents the propgating modes are allowed to turn.
# This, in return ruin the field-sorting method that ensure a coherent distribution
# of the mode through the z-profile of the coupler.
# This 1x1 coupler case is a perfect show case for this problem.
# In order to fix this a break of symmetry is needed either fixing the boundary condition
# with symmetries or adding some asymmetrical structure.

# %%
# The modes are now computed [can take a few minutes], the modes are concatenated
# in a superset class that we can access with the get_set() function. This class
# can be used to analyse the data
superset = solver.get_set()

# %%
# Field computation: :math:`E_{i,j}`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ = superset.plot(plot_type='field', itr_list=[1.0, 0.05]).show()

# %%
# After mode visualization we can name them for an easier further analyze.
# This step is, however, not mandatory.
_ = superset.label_supermodes('LP01', 'LP02', 'LP11_v', 'LP11_h')

# %%
# Effective index: :math:`n^{eff}_{i,j}`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ = superset.plot(plot_type='index').show()

# %%
# Modal normalized coupling: :math:`C_{i,j}`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ = superset.plot(plot_type='normalized-coupling').show()

# %%
# Adiabatic criterion: :math:`\tilde{C}_{i,j}`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ = superset.plot(plot_type='adiabatic').show()
