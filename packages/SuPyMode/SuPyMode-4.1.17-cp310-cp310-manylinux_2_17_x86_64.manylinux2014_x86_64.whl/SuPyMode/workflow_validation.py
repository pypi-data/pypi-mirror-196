from FiberFusing import Geometry, BackGround, Circle
import FiberFusing
from SuPyMode.solver import SuPySolver
import FiberFusing.fiber_catalogue as fiber_catalogue
from FiberFusing.fiber_catalogue import GenericFiber


class GradientFiber(GenericFiber):
    def __init__(self, delta_n: float, clad_diameter: float, core_diameter: float, wavelength: float, position: tuple = (0, 0)):
        self.core_diameter = core_diameter
        self.clad_diameter = clad_diameter
        self.delta_n = delta_n
        super().__init__(wavelength=wavelength, position=position)

    def post_init(self):
        self.add_air()

        self.add_next_structure_with_index(
            name='outer-clad',
            structure_index=self.silica_index,
            radius=self.clad_diameter / 2 * 1e-6
        )

        self.add_next_structure_with_index(
            name='core',
            structure_index=self.silica_index + self.delta_n,
            radius=self.core_diameter / 2 * 1e-6,
            graded_index_factor=self.delta_n
        )


def workflow10(diameter_list,
             resolution: int = 200,
             wavelength: float = 1.55e-6,
             n_sorted_mode: int = 15,
             delta_n: float = 0,
             plot_geometry: bool = False,
             plot_cladding: bool = False,
             fusion_degree: float = 0.85,
             initial_itr: float = 1.0,
             final_itr: float = 0.05,
             n_step: int = 500,
             plot_field: bool = False,
             compute_modes: bool = True,
             generate_report: bool = False,
             compute_anti_symmetric: bool = False,
             save_superset: bool = True,
             filename: str = 'auto'):

    clad_structure = FiberFusing.Fused10

    silica_index = fiber_catalogue.get_silica_index(wavelength=wavelength)

    capillary_tube = Circle(index=silica_index - 0.004, position=(0, 0), radius=300e-6)

    clad = clad_structure(
        fiber_radius=62.5e-6,
        index=silica_index,
        core_position_scrambling=0
    )

    fibers_structures = []

    for n, diameter in enumerate(diameter_list):
        fiber = GradientFiber(
            delta_n=delta_n,
            wavelength=wavelength,
            position=clad.cores[n],
            core_diameter=diameter,
            clad_diameter=83 if n in [7, 8, 9] else 125
        )

        fibers_structures.append(fiber)

    if plot_cladding:
        clad.plot().show()

    geometry = Geometry(
        background=BackGround(index=1),
        structures=[capillary_tube],
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

    if not compute_modes:
        return
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
        n_step=n_step,
        itr_i=initial_itr,
        itr_f=final_itr
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

    if compute_anti_symmetric:
        solver.add_modes(
            n_computed_mode=n_sorted_mode + 10,
            n_sorted_mode=n_sorted_mode,
            auto_labeling=False,
            boundaries={
                'right': 'anti-symmetric',
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

    if filename == 'auto':
        filename = "_".join(
            [clad_structure.__name__] +
            [fiber.__name__ for fiber in fibers_model] +
            [str(resolution)] +
            [f'wavelength_{wavelength}']
        )

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
