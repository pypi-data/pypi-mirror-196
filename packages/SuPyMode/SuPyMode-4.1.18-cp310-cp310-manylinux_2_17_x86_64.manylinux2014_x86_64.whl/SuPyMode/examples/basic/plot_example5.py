"""
7x7 Coupler
===========
"""

# %%
# Importing the package dependencies: FiberFusing, PyFinitDiff
from FiberFusing import Geometry, Fused7, BackGround
from FiberFusing.fiber_catalogue import DCF1300S_33
from PyFinitDiff.boundaries import Boundaries2D
from SuPyMode.solver import SuPySolver
from SuPyMode.profiles import AlphaProfile


# %%
# Generating the fiber structure
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Here we make use of the FiberFusing to generate a fiber structure that we use
# as the cladding. The refractive index of the strcture is defined using PyOptik.
wavelength = 1.55e-6

index = 1.4444

air = BackGround(index=1)

clad = Fused7(fiber_radius=62.5e-6, fusion_degree=0.6, index=index)

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
    y_bounds='centering-bottom',
    n=40,
    index_scrambling=1e-5,
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
    boundaries=Boundaries2D(top='symmetric', right='symmetric'),
    n_computed_mode=3,
    n_sorted_mode=2
)

_ = solver.add_modes(
    boundaries=Boundaries2D(top='symmetric', right='anti-symmetric'),
    n_computed_mode=3,
    n_sorted_mode=2
)

_ = solver.add_modes(
    boundaries=Boundaries2D(top='anti-symmetric', right='symmetric'),
    n_computed_mode=3,
    n_sorted_mode=2
)

_ = solver.add_modes(
    boundaries=Boundaries2D(top='anti-symmetric', right='anti-symmetric'),
    n_computed_mode=3,
    n_sorted_mode=2
)

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
_ = superset.label_supermodes('LP01', 'LP21_v', 'LP11_v', 'LP31_v', 'LP11_h', 'LP31_h', 'LP21_h', 'LP31_h')

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
