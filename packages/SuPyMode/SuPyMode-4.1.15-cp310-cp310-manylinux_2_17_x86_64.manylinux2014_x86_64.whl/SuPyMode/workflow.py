from FiberFusing import Geometry, BackGround
import FiberFusing
from SuPyMode.solver import SuPySolver
import FiberFusing.fiber_catalogue as fiber_catalogue


def workflow(*fibers_model,
                  resolution: int = 200,
                  fusion_degree: float = 0.85,
                  wavelength: float = 1.55e-6,
                  n_sorted_mode: int = 15,
                  plot_geometry: bool = False,
                  plot_field: bool = False,
                  generate_report: bool = False,
                  save_superset: bool = True):

    match len(fibers_model):
        case 1:
            clad_structure = FiberFusing.Fused1
        case 2:
            clad_structure = FiberFusing.Fused2
        case 3:
            clad_structure = FiberFusing.Fused3
        case 4:
            clad_structure = FiberFusing.Fused4

    silica_index = fiber_catalogue.get_silica_index(wavelength=wavelength)

    clad = clad_structure(
        fiber_radius=62.5e-6,
        fusion_degree=0.85,
        index=silica_index,
        core_position_scrambling=0
    )

    fibers_structures = []

    for n, fiber in enumerate(fibers_model):
        fibers_structures.append(
            fiber(wavelength=wavelength, position=clad.cores[n])
        )

    filename = "_".join(
        [clad_structure.__name__] +
        [fiber.__name__ for fiber in fibers_model] +
        [str(resolution)] +
        [f'wavelength_{wavelength}'] +
        [f"fusion_{fusion_degree}"]
    )

    geometry = Geometry(
        background=BackGround(index=1),
        structures=[clad],
        x_bounds='centering-left',
        y_bounds='centering',
        n=resolution,
        index_scrambling=0,
        gaussian_filter=None,
        boundary_pad_factor=1.1
    )

    geometry.add_fiber(*fibers_structures)

    if plot_geometry:
        geometry.plot().show()

    solver = SuPySolver(
        geometry=geometry,
        tolerance=1e-5,
        max_iter=1000,
        show_iteration=True,
        accuracy=2,
        show_eigenvalues=False,
        extrapolation_order=1
    )

    solver.init_superset(
        wavelength=wavelength,
        n_step=500,
        itr_i=1.0,
        itr_f=0.05
    )

    solver.add_modes(
        n_computed_mode=n_sorted_mode + 10,
        n_sorted_mode=n_sorted_mode,
        auto_labeling=False,
        boundaries={
            'right': 'symmetric',
            'left': 'zero',
            'top': 'zero',
            'bottom': 'zero'
        }
    )

    solver.superset.sorting_modes('beta')

    if plot_field:
        figure = solver.superset.plot(plot_type='field')
        figure.show_colorbar = False
        figure.show_ticks = False
        figure.x_label = ''
        figure.y_label = ''
        figure.show()

    if save_superset:
        solver.superset.save_instance(
            filename=filename,
            directory='auto'
        )

    solver.superset.generate_report(
        filename=filename + ".pdf",
        directory='auto',
    )

# -
