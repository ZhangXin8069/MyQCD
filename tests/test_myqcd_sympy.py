from __future__ import annotations

from pathlib import Path

import sympy as sp

from myqcd import derivations as derivation_module

from myqcd.derivations import (
    derive_collins_soper_evolution,
    derive_correlator_spectrum,
    derive_diffusion_processes,
    derive_gauge_flow_kernel,
    derive_generating_functional,
    derive_gradient_flow,
    derive_lamet_matching,
    derive_lattice_link,
    derive_mellin_convolution,
    derive_normalizing_flow,
    derive_pdf_moment_relations,
    derive_quasi_pdf_tmd_relation,
    derive_mcmc_autocorrelation,
    derive_pseudo_pdf_one_loop,
    derive_phi4_lattice_observables,
    derive_renormalization,
    derive_tmd_fourier,
    derive_wilson_area_law,
    run_core_checks,
)
from myqcd.formula_registry import CORE_FORMULAS
from myqcd.latex_inventory import extract_display_formulas, scan_refer_papers


ROOT = Path(__file__).resolve().parents[1]


def test_gaussian_generating_functional_variations_are_exact() -> None:
    result = derive_generating_functional()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert sp.simplify(result.equations["d_log_Z_dJ"] - result.symbols["J"] / result.symbols["K"]) == 0
    assert sp.simplify(result.equations["d2_log_Z_dJ2"] - 1 / result.symbols["K"]) == 0


def test_lattice_link_is_unitary_and_has_continuum_expansion() -> None:
    result = derive_lattice_link()

    assert result.status == "verified"
    assert result.checks["unitarity"]
    assert result.checks["series_through_a2"]
    assert result.equations["U_series_a2"] == (
        1
        + sp.I * result.symbols["a"] * result.symbols["g"] * result.symbols["A"]
        - (result.symbols["a"] * result.symbols["g"] * result.symbols["A"]) ** 2 / 2
    )


def test_wilson_area_law_gives_linear_static_potential() -> None:
    result = derive_wilson_area_law()

    assert result.status == "verified"
    assert result.checks["large_T_limit"]
    assert sp.simplify(result.equations["V_of_R"] - result.symbols["sigma"] * result.symbols["R"]) == 0


def test_gradient_flow_linearization_is_heat_kernel_evolution() -> None:
    result = derive_gradient_flow()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert sp.simplify(result.equations["fourier_flow_residual"]) == 0
    assert sp.simplify(result.equations["kernel_normalization"] - 1) == 0


def test_renormalization_factor_is_solved_without_extra_physics() -> None:
    result = derive_renormalization()

    assert result.status == "verified"
    assert result.checks["inverse_relation"]
    assert result.equations["Z_solved"] == result.symbols["O_R"] / result.symbols["O_bare"]


def test_mellin_moment_of_explicit_convolution_respects_fubini_reordering() -> None:
    result = derive_mellin_convolution()

    assert result.status == "verified"
    assert result.checks["fubini_polynomial_example"]
    assert result.equations["difference"] == 0


def test_lamet_power_correction_vanishes_at_infinite_momentum() -> None:
    result = derive_lamet_matching()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["power_correction_limit"] == 0


def test_collins_soper_evolution_solution_satisfies_both_scale_equations() -> None:
    result = derive_collins_soper_evolution()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["rapidity_evolution_residual"] == 0
    assert result.equations["mu_rge_residual"] == 0


def test_tmd_gaussian_fourier_transform_is_normalized() -> None:
    result = derive_tmd_fourier()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert sp.simplify(result.equations["F_of_b"] - sp.exp(-result.symbols["Lambda"] ** 2 * result.symbols["b"] ** 2 / 4)) == 0


def test_normalizing_flow_jacobian_matches_affine_coupling_map() -> None:
    result = derive_normalizing_flow()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["det_J"] == sp.exp(result.symbols["s"])


def test_correlator_effective_energy_converges_to_ground_state() -> None:
    result = derive_correlator_spectrum()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["effective_energy_limit"] == result.symbols["E0"]


def test_core_audit_has_no_failed_symbolic_checks() -> None:
    report = run_core_checks()

    assert report["status"] == "verified"
    assert report["failed_checks"] == []
    assert report["derivation_count"] >= 10


def test_formula_registry_covers_report_level_structural_formulas() -> None:
    expected = {
        "generating_functional",
        "lattice_link",
        "gradient_flow",
        "gradient_flow_energy_density",
        "heat_kernel_semigroup",
        "gradient_flow_pole_cancellation",
        "gauge_flow_kernel",
        "diffusion_processes",
        "phi4_lattice_observables",
        "mcmc_autocorrelation",
        "pseudo_pdf_one_loop",
        "target_mass_corrections",
        "qpdf_ppdf_fourier_inversion",
        "flow_mcmc_balance",
        "stout_smearing_su2",
        "quark_gaussian_smearing",
        "u1_gauge_invariance",
        "su3_generator_identities",
        "su3_cayley_hamilton",
        "correlated_chi_square_profile",
        "ising_mean_field",
        "wilson_smearing_kernel",
        "wilson_smearing_scaling",
        "ape_projection_su2",
        "wilson_eigenvalue_statistics",
        "wilson_fourier_endpoint",
        "wilson_continuum_scale",
        "two_dimensional_wilson_loop",
        "instanton_holonomy_su2",
        "flowed_propagators",
        "u1_topological_charge",
        "u1_compact_action",
        "lattice_dispersion_relations",
        "boosted_smearing_width",
        "u1_lattice_field_strength",
        "momentum_smearing_shift",
        "pseudo_pdf_ir_regulators",
        "renormalization",
        "lamet_matching",
        "euclidean_to_tmd",
        "normalizing_flow",
        "pseudo_itd",
        "pdf_moment_relations",
        "quasi_pdf_tmd_relation",
        "langevin_fokker_planck",
        "hmc_scalar",
        "trivializing_map",
    }

    assert expected <= set(CORE_FORMULAS)
    assert all(CORE_FORMULAS[key].source for key in expected)
    assert all(CORE_FORMULAS[key].status in {"verified", "structural"} for key in expected)


def test_new_derivations_are_exposed_by_the_package() -> None:
    import myqcd

    assert myqcd.derive_pseudo_itd is derivation_module.derive_pseudo_itd
    assert myqcd.derive_langevin_fokker_planck is derivation_module.derive_langevin_fokker_planck
    assert myqcd.derive_hmc_scalar is derivation_module.derive_hmc_scalar
    assert myqcd.derive_trivializing_map is derivation_module.derive_trivializing_map
    assert myqcd.derive_diffusion_processes is derivation_module.derive_diffusion_processes
    assert myqcd.derive_phi4_lattice_observables is derivation_module.derive_phi4_lattice_observables
    assert myqcd.derive_mcmc_autocorrelation is derivation_module.derive_mcmc_autocorrelation
    assert myqcd.derive_pseudo_pdf_one_loop is derivation_module.derive_pseudo_pdf_one_loop
    assert myqcd.derive_gauge_flow_kernel is derivation_module.derive_gauge_flow_kernel
    assert myqcd.derive_pdf_moment_relations is derivation_module.derive_pdf_moment_relations
    assert myqcd.derive_quasi_pdf_tmd_relation is derivation_module.derive_quasi_pdf_tmd_relation
    quark_smearing = getattr(derivation_module, "derive_quark_gaussian_smearing", None)
    assert callable(quark_smearing)
    assert getattr(myqcd, "derive_quark_gaussian_smearing", None) is quark_smearing
    u1_gauge = getattr(derivation_module, "derive_u1_gauge_invariance", None)
    assert callable(u1_gauge)
    assert getattr(myqcd, "derive_u1_gauge_invariance", None) is u1_gauge
    flowed_propagators = getattr(derivation_module, "derive_flowed_propagators", None)
    assert callable(flowed_propagators)
    assert getattr(myqcd, "derive_flowed_propagators", None) is flowed_propagators
    u1_topology = getattr(derivation_module, "derive_u1_topological_charge", None)
    assert callable(u1_topology)
    assert getattr(myqcd, "derive_u1_topological_charge", None) is u1_topology
    u1_action = getattr(derivation_module, "derive_u1_compact_action", None)
    assert callable(u1_action)
    assert getattr(myqcd, "derive_u1_compact_action", None) is u1_action
    lattice_dispersion = getattr(derivation_module, "derive_lattice_dispersion_relations", None)
    assert callable(lattice_dispersion)
    assert getattr(myqcd, "derive_lattice_dispersion_relations", None) is lattice_dispersion
    boosted_smearing = getattr(derivation_module, "derive_boosted_smearing_width", None)
    assert callable(boosted_smearing)
    assert getattr(myqcd, "derive_boosted_smearing_width", None) is boosted_smearing
    lattice_field_strength = getattr(derivation_module, "derive_u1_lattice_field_strength", None)
    assert callable(lattice_field_strength)
    assert getattr(myqcd, "derive_u1_lattice_field_strength", None) is lattice_field_strength
    su3_generators = getattr(derivation_module, "derive_su3_generator_identities", None)
    assert callable(su3_generators)
    assert getattr(myqcd, "derive_su3_generator_identities", None) is su3_generators
    su3_cayley_hamilton = getattr(derivation_module, "derive_su3_cayley_hamilton", None)
    assert callable(su3_cayley_hamilton)
    assert getattr(myqcd, "derive_su3_cayley_hamilton", None) is su3_cayley_hamilton
    chi_square_profile = getattr(derivation_module, "derive_correlated_chi_square_profile", None)
    assert callable(chi_square_profile)
    assert getattr(myqcd, "derive_correlated_chi_square_profile", None) is chi_square_profile
    ising_mean_field = getattr(derivation_module, "derive_ising_mean_field", None)
    assert callable(ising_mean_field)
    assert getattr(myqcd, "derive_ising_mean_field", None) is ising_mean_field
    wilson_smearing_kernel = getattr(derivation_module, "derive_wilson_smearing_kernel", None)
    assert callable(wilson_smearing_kernel)
    assert getattr(myqcd, "derive_wilson_smearing_kernel", None) is wilson_smearing_kernel
    wilson_smearing_scaling = getattr(derivation_module, "derive_wilson_smearing_scaling", None)
    assert callable(wilson_smearing_scaling)
    assert getattr(myqcd, "derive_wilson_smearing_scaling", None) is wilson_smearing_scaling
    ape_projection = getattr(derivation_module, "derive_ape_projection_su2", None)
    assert callable(ape_projection)
    assert getattr(myqcd, "derive_ape_projection_su2", None) is ape_projection
    eigenvalue_statistics = getattr(derivation_module, "derive_wilson_eigenvalue_statistics", None)
    assert callable(eigenvalue_statistics)
    assert getattr(myqcd, "derive_wilson_eigenvalue_statistics", None) is eigenvalue_statistics
    fourier_endpoint = getattr(derivation_module, "derive_wilson_fourier_endpoint", None)
    assert callable(fourier_endpoint)
    assert getattr(myqcd, "derive_wilson_fourier_endpoint", None) is fourier_endpoint
    continuum_scale = getattr(derivation_module, "derive_wilson_continuum_scale", None)
    assert callable(continuum_scale)
    assert getattr(myqcd, "derive_wilson_continuum_scale", None) is continuum_scale
    two_dimensional_loop = getattr(derivation_module, "derive_two_dimensional_wilson_loop", None)
    assert callable(two_dimensional_loop)
    assert getattr(myqcd, "derive_two_dimensional_wilson_loop", None) is two_dimensional_loop
    instanton_holonomy = getattr(derivation_module, "derive_instanton_holonomy_su2", None)
    assert callable(instanton_holonomy)
    assert getattr(myqcd, "derive_instanton_holonomy_su2", None) is instanton_holonomy


def test_refer_papers_formula_inventory_is_traceable_and_excludes_build_outputs() -> None:
    inventory = scan_refer_papers(ROOT)

    assert inventory.paper_count == 50
    assert inventory.formula_count > 1000
    assert inventory.records
    assert len({record.formula_id for record in inventory.records}) == inventory.formula_count
    assert all("/build/" not in record.source_file for record in inventory.records)
    assert all(record.source_file.startswith("refer/papers/") for record in inventory.records)
    assert any(record.status == "unparsed" for record in inventory.records)


def test_formula_inventory_handles_custom_display_environments_and_nested_aligned() -> None:
    source = r"""
% \begin{equation} this is a comment and must not count
\be
  x = 1
\ee
\bea
  y &= x + 1
\eea
\begin{equation}
  \begin{aligned}
    z &= x + y
  \end{aligned}
\end{equation}
"""

    records = extract_display_formulas(source, "sample.tex", "P99")

    assert len(records) == 3
    assert [record.environment for record in records] == ["be", "bea", "equation"]
    assert records[0].start_line == 3
    assert records[-1].start_line < records[-1].end_line


def test_pseudo_itd_fourier_moments_and_reduced_ratio_are_consistent() -> None:
    result = derivation_module.derive_pseudo_itd()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["itd_at_zero"] == 1
    assert result.equations["reduced_itd"] == result.equations["physical_ratio"]
    assert result.equations["uv_scale_product"] == 4 * sp.exp(-2 * sp.EulerGamma)


def test_langevin_fokker_planck_has_gaussian_equilibrium() -> None:
    result = derivation_module.derive_langevin_fokker_planck()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["fp_stationary_residual"] == 0
    assert result.equations["equilibrium_variance"] == (
        result.symbols["alpha"] / result.symbols["mass_squared"]
    )


def test_scalar_hmc_equations_conserve_transformed_hamiltonian() -> None:
    result = derivation_module.derive_hmc_scalar()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["hamiltonian_time_derivative"] == 0
    assert result.equations["canonical_momentum"] == (
        result.symbols["jacobian_scale"] * result.symbols["momentum"]
    )


def test_trivializing_flow_has_evolving_jacobian_and_constant_pullback_action() -> None:
    result = derivation_module.derive_trivializing_map()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["linear_jacobian"] == sp.exp(
        result.symbols["flow_rate"] * result.symbols["flow_time"]
    )
    assert result.equations["trivialized_action_residual"] == 0


def test_gradient_flow_energy_density_has_four_dimensional_scaling() -> None:
    result = derivation_module.derive_gradient_flow_energy_density()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["four_dimensional_kernel_normalization"] == 1
    assert result.equations["four_dimensional_kernel_second_moment"] == (
        8 * result.symbols["flow_time"]
    )
    assert result.equations["running_leading"] .subs(
        result.symbols["alpha"], result.symbols["coupling"] ** 2 / (4 * sp.pi)
    ) == result.equations["renormalized_leading"]


def test_target_mass_corrections_match_derivative_and_integral_limits() -> None:
    result = derivation_module.derive_target_mass_corrections()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["qpdf_parallel_endpoint_limit"] == -sp.Rational(3, 4)
    assert result.equations["target_mass_integral"] == (
        1 - result.symbols["x"] ** 2
    ) / 2
    assert result.equations["ppdf_endpoint_limit"] == (
        result.symbols["z"] ** 2 / 4
    )


def test_qpdf_and_ppdf_fourier_definitions_invert_a_normalized_gaussian() -> None:
    result = derivation_module.derive_qpdf_ppdf_fourier_inversion()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["qpdf_from_itd"] == result.equations["pdf"]
    assert result.equations["ppdf_from_itd"] == result.equations["pdf"]
    assert result.equations["pdf_normalization"] == 1


def test_gradient_flow_heat_kernel_has_semigroup_composition() -> None:
    result = derivation_module.derive_heat_kernel_semigroup()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["convolution_residual"] == 0
    assert result.equations["fourier_composition_residual"] == 0


def test_gradient_flow_energy_density_pole_cancellation_uses_the_beta_coefficient() -> None:
    result = derivation_module.derive_gradient_flow_pole_cancellation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["b0"] == result.equations["c1_pole_coefficient"]
    assert result.equations["g4_pole_residual"] == 0


def test_flow_mcmc_acceptance_preserves_a_two_state_target_and_kl_identity() -> None:
    result = derivation_module.derive_flow_mcmc_balance()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["detailed_balance_residual"] == 0
    assert result.equations["stationary_residual"] == sp.Matrix([[0, 0]])
    assert result.equations["kl_identity_residual"] == 0


def test_stout_su2_subgroup_update_preserves_group_properties() -> None:
    result = derivation_module.derive_stout_smearing_su2()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["q_trace"] == 0
    assert result.equations["smeared_unitarity_residual"] == sp.zeros(2)
    assert result.equations["smeared_determinant"] == 1


def test_momentum_smearing_phase_shifts_a_gaussian_fourier_kernel() -> None:
    result = derivation_module.derive_momentum_smearing_shift()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["shifted_fourier_residual"] == 0
    assert result.equations["plus_convention_residual"] == 0


def test_pseudo_pdf_ir_regulators_have_bessel_and_incomplete_gamma_limits() -> None:
    result = derivation_module.derive_pseudo_pdf_ir_regulators()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["bessel_identity_residual"] == 0
    assert result.equations["bessel_small_distance_constant"] == (
        2 * sp.log(2) - 2 * sp.EulerGamma
    )
    assert result.equations["sharp_cutoff_identity_residual"] == 0
    assert result.equations["sharp_cutoff_small_distance_constant"] == -sp.EulerGamma


def test_diffusion_processes_reproduce_sde_score_and_probability_flow_identities() -> None:
    result = derive_diffusion_processes()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["ve_variance"] == (
        result.symbols["sigma"] ** (2 * result.symbols["xi"]) - 1
    ) / (2 * sp.log(result.symbols["sigma"]))
    assert sp.simplify(
        result.equations["conditional_score"]
        + (result.symbols["phi_xi"] - result.symbols["phi_0"])
        / result.equations["ve_variance"]
    ) == 0
    assert result.equations["probability_flow_residual"] == 0
    assert result.equations["logdet_divergence_residual"] == 0


def test_phi4_lattice_action_and_observables_respect_symmetry_and_mass_limits() -> None:
    result = derive_phi4_lattice_observables()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["box_symmetric_residual"] == sp.zeros(4)
    assert result.equations["sign_flip_residual"] == 0
    assert result.equations["chi2_definition_residual"] == 0
    assert result.equations["effective_mass_cosh_residual"] == 0


def test_mcmc_autocorrelation_bound_and_integrated_time_are_exact_in_a_toy_model() -> None:
    result = derive_mcmc_autocorrelation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["tau_two_bound_gap"] == sp.Rational(1, 16)
    assert result.equations["geometric_tau_int"] == (
        1 / result.symbols["acceptance_rate"] - sp.Rational(1, 2)
    )


def test_pseudo_pdf_one_loop_plus_kernels_cancel_endpoint_and_rewrite_scale() -> None:
    result = derive_pseudo_pdf_one_loop()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["B_plus_on_constant"] == 0
    assert result.equations["B_plus_on_linear_test"] == -sp.Rational(4, 3)
    assert result.equations["kernel_rewrite_residual"] == 0
    assert result.equations["effective_scale_residual"] == 0


def test_gauge_flow_kernel_has_projector_semigroup_and_initial_condition() -> None:
    result = derive_gauge_flow_kernel()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["initial_kernel_residual"] == sp.zeros(2)
    assert result.equations["semigroup_residual"] == sp.zeros(2)
    assert result.equations["flow_equation_residual"] == sp.zeros(2)


def test_pdf_moment_extension_and_target_mass_polynomial_are_consistent() -> None:
    result = derive_pdf_moment_relations()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["moment_identity_n2_residual"] == 0
    assert result.equations["moment_identity_n3_residual"] == 0
    assert result.equations["K_2"] == 1 + result.symbols["target_mass_ratio"]
    assert result.equations["K_4"] == (
        1
        + 3 * result.symbols["target_mass_ratio"]
        + result.symbols["target_mass_ratio"] ** 2
    )


def test_tmd_to_quasi_pdf_relation_preserves_normalization_and_large_momentum_limit() -> None:
    result = derive_quasi_pdf_tmd_relation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["quasi_pdf_normalization"] == 1
    assert result.equations["interior_large_momentum_limit"] == sp.Rational(1, 2)
    assert result.equations["outside_large_momentum_limit"] == 0


def test_quark_gaussian_smearing_and_distillation_preserve_lattice_structure() -> None:
    derivation = getattr(derivation_module, "derive_quark_gaussian_smearing", None)
    assert callable(derivation)
    result = derivation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["plane_wave_residual"] == sp.zeros(8, 1)
    assert result.equations["gaussian_limit_residual"] == 0
    assert result.equations["distillation_projector_residual"] == sp.zeros(8)
    assert result.equations["distillation_rank"] == 2


def test_u1_gauge_transform_leaves_plaquette_and_wilson_action_invariant() -> None:
    derivation = getattr(derivation_module, "derive_u1_gauge_invariance", None)
    assert callable(derivation)
    result = derivation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["plaquette_phase_residual"] == 0
    assert result.equations["plaquette_residual"] == 0
    assert result.equations["action_residual"] == 0
    assert result.equations["density_residual"] == 0


def test_flowed_propagators_have_projector_initial_data_and_dirac_inverse() -> None:
    derivation = getattr(derivation_module, "derive_flowed_propagators", None)
    assert callable(derivation)
    result = derivation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["gluon_projector_completeness_residual"] == sp.zeros(2)
    assert result.equations["gluon_initial_feynman_residual"] == sp.zeros(2)
    assert result.equations["quark_inverse_residual"] == sp.zeros(2)
    assert result.equations["quark_flow_equation_residual"] == sp.zeros(2)


def test_u1_topological_charge_uses_principal_plaquette_angles() -> None:
    derivation = getattr(derivation_module, "derive_u1_topological_charge", None)
    assert callable(derivation)
    result = derivation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["topological_charge"] == 1
    assert result.equations["configuration_susceptibility"] == sp.Rational(1, 4)
    assert result.equations["wilson_loop_residual"] == 0


def test_u1_compact_action_has_periodicity_and_correct_weak_field_limit() -> None:
    derivation = getattr(derivation_module, "derive_u1_compact_action", None)
    assert callable(derivation)
    result = derivation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["periodicity_residual"] == 0
    assert result.equations["quadratic_limit"] == 1
    assert result.equations["quartic_series_residual"] == 0


def test_lattice_dispersion_relations_have_continuum_momentum_and_rest_limits() -> None:
    derivation = getattr(derivation_module, "derive_lattice_dispersion_relations", None)
    assert callable(derivation)
    result = derivation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["hat_momentum_continuum_residual"] == 0
    assert result.equations["bar_momentum_continuum_residual"] == 0
    assert result.equations["pion_rest_dispersion_residual"] == 0
    assert result.equations["wilson_rest_dispersion_residual"] == 0
    assert result.equations["hat_squared_periodicity_residual"] == 0


def test_boosted_smearing_width_keeps_transverse_variance_and_shrinks_parallel_one() -> None:
    derivation = getattr(derivation_module, "derive_boosted_smearing_width", None)
    assert callable(derivation)
    result = derivation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["boosted_laplacian_residual"] == 0
    assert result.equations["gamma_one_width_residual"] == 0
    assert result.equations["width_matching_residual"] == 0
    assert result.equations["parallel_width_ratio_residual"] == 0
    assert result.equations["boost_parameter_ordering_at_two"] is True


def test_u1_lattice_field_strength_is_invariant_under_discrete_gauge_shift() -> None:
    derivation = getattr(derivation_module, "derive_u1_lattice_field_strength", None)
    assert callable(derivation)
    result = derivation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["gauge_shift_cancellation"] == 0
    assert result.equations["gauge_invariant_field_strength_residual"] == 0
    assert result.equations["rescaled_field_strength_residual"] == 0


def test_su3_generators_reproduce_algebra_normalization_and_completeness() -> None:
    derivation = getattr(derivation_module, "derive_su3_generator_identities", None)
    assert callable(derivation)
    result = derivation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["trace_orthogonality_residual"] == sp.zeros(8)
    assert result.equations["commutator_residual_count"] == 0
    assert result.equations["anticommutator_residual_count"] == 0
    assert result.equations["completeness_residual_count"] == 0
    assert result.equations["f_reality_residual"] == 0
    assert result.equations["d_reality_residual"] == 0


def test_su3_cayley_hamilton_relation_and_hermitian_discriminant_are_exact() -> None:
    derivation = getattr(derivation_module, "derive_su3_cayley_hamilton", None)
    assert callable(derivation)
    result = derivation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["cayley_hamilton_residual"] == sp.zeros(3)
    assert result.equations["det_trace_cubic_residual"] == 0
    assert result.equations["c1_sum_of_squares_residual"] == 0
    assert result.equations["discriminant_negative_square_residual"] == 0


def test_correlated_chi_square_profile_matches_covariance_and_shifted_residual_forms() -> None:
    derivation = getattr(derivation_module, "derive_correlated_chi_square_profile", None)
    assert callable(derivation)
    result = derivation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["stationarity_residual"] == 0
    assert result.equations["A_definition_residual"] == 0
    assert result.equations["covariance_inverse_identity"] == sp.zeros(2)
    assert result.equations["profiled_chi_square_residual"] == 0
    assert result.equations["shifted_residual_relation"] == sp.zeros(2, 1)
    assert result.equations["lambda_covariance_relation"] == 0


def test_ising_mean_field_sum_gives_tanh_self_consistency_and_critical_slope() -> None:
    derivation = getattr(derivation_module, "derive_ising_mean_field", None)
    assert callable(derivation)
    result = derivation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["partition_function_residual"] == 0
    assert result.equations["magnetization_tanh_residual"] == 0
    assert result.equations["zero_field_solution_residual"] == 0
    assert result.equations["critical_slope_residual"] == 0


def test_wilson_smearing_kernel_preserves_longitudinal_mode_and_damps_transverse_mode() -> None:
    derivation = getattr(derivation_module, "derive_wilson_smearing_kernel", None)
    assert callable(derivation)
    result = derivation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["projector_completeness_residual"] == sp.zeros(2)
    assert result.equations["projector_transverse_residual"] == sp.zeros(2)
    assert result.equations["projector_longitudinal_residual"] == sp.zeros(2)
    assert result.equations["kernel_square_residual"] == sp.zeros(2)
    assert result.equations["kernel_cube_residual"] == sp.zeros(2)
    assert result.equations["weak_smearing_limit_residual"] == 0
    assert result.equations["max_momentum_parameter_bound"] is True


def test_wilson_smearing_scaling_keeps_physical_profiles_cutoff_consistent() -> None:
    derivation = getattr(derivation_module, "derive_wilson_smearing_scaling", None)
    assert callable(derivation)
    result = derivation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["bare_thooft_relation_residual"] == 0
    assert result.equations["physical_length_inverse_residual"] == 0
    assert result.equations["square_loop_n_residual"] == 0
    assert result.equations["physical_smearing_scale_residual"] == 0
    assert result.equations["physical_mass_combination_residual"] == 0
    assert result.equations["cutoff_profile_limit_residual"] == 0
    assert result.equations["scaling_line_substitution_residual"] == 0
    assert result.equations["scaling_line_slope_negative"] is True


def test_ape_projection_su2_normalizes_a_nonsingular_staple_combination() -> None:
    derivation = getattr(derivation_module, "derive_ape_projection_su2", None)
    assert callable(derivation)
    result = derivation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["ape_combination_residual"] == sp.zeros(2)
    assert result.equations["x_dagger_x_residual"] == sp.zeros(2)
    assert result.equations["inverse_square_root_residual"] == sp.zeros(2)
    assert result.equations["projected_unitarity_residual"] == sp.zeros(2)
    assert result.equations["projected_su2_residual"] == 0
    assert result.equations["zero_smearing_residual"] == sp.zeros(2)
    assert result.equations["singular_example_radius_squared"] == 0


def test_wilson_eigenvalue_statistics_reproduce_central_moments_and_edge_scaling() -> None:
    derivation = getattr(derivation_module, "derive_wilson_eigenvalue_statistics", None)
    assert callable(derivation)
    result = derivation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["variance_definition_residual"] == 0
    assert result.equations["skewness_definition_residual"] == 0
    assert result.equations["kurtosis_definition_residual"] == 0
    assert result.equations["edge_transform_inverse_residual"] == 0
    assert result.equations["edge_mean_residual"] == 0
    assert result.equations["edge_variance_residual"] == 0


def test_wilson_fourier_endpoint_matches_the_alternating_pi_evaluation() -> None:
    derivation = getattr(derivation_module, "derive_wilson_fourier_endpoint", None)
    assert callable(derivation)
    result = derivation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["endpoint_residual"] == 0
    assert result.equations["cutoff_periodicity_residual"] == 0
    assert result.equations["cutoff_below_half_N"] is True


def test_wilson_continuum_scale_keeps_dimensionless_lengths_and_cutoff_order() -> None:
    derivation = getattr(derivation_module, "derive_wilson_continuum_scale", None)
    assert callable(derivation)
    result = derivation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["b_improved_definition_residual"] == 0
    assert result.equations["temperature_reciprocal_residual"] == 0
    assert result.equations["lattice_spacing_temperature_residual"] == 0
    assert result.equations["dimensionless_length_residual"] == 0
    assert result.equations["continuum_extrapolation_limit_residual"] == 0
    assert result.equations["crossing_line_substitution_residual"] == 0


def test_two_dimensional_wilson_loop_is_a_laguerre_polynomial_times_an_exponential() -> None:
    derivation = getattr(derivation_module, "derive_two_dimensional_wilson_loop", None)
    assert callable(derivation)
    result = derivation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["n1_formula_residual"] == 0
    assert result.equations["n2_formula_residual"] == 0
    assert result.equations["n3_formula_residual"] == 0
    assert result.equations["zero_area_normalization_residual"] == 0
    assert result.equations["polynomial_exponential_residual"] == 0


def test_instanton_su2_parallel_transport_has_group_properties_and_limits() -> None:
    derivation = getattr(derivation_module, "derive_instanton_holonomy_su2", None)
    assert callable(derivation)
    result = derivation()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["U_unitarity_residual"] == sp.zeros(2)
    assert result.equations["U_su2_residual"] == 0
    assert result.equations["holonomy_unitarity_residual"] == sp.zeros(2)
    assert result.equations["holonomy_su2_residual"] == 0
    assert result.equations["small_instanton_limit_residual"] == sp.zeros(2)
    assert result.equations["large_instanton_limit_residual"] == sp.zeros(2)
