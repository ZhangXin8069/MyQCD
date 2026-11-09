# API reference

Public names are taken from each module's `__all__`; this page is generated
from the installed package to avoid drift.

## `myqcd.color`

Su(3) generators, structure constants and color fierz.

- `N_COLORS`
- `N_GENERATORS`
- `adjoint_trace`
- `casimir_adjoint`
- `casimir_fundamental`
- `color_fierz_residual`
- `color_fierz_tensor`
- `epsilon_tensor`
- `fundamental_trace`
- `gell_mann_matrices`
- `generators`
- `quark_gluon_vertex`
- `structure_constants`
- `symmetric_constants`

## `myqcd.color_traces`

Su(3) traces, f/d contractions and casimirs.

- `casimir_generic`
- `d_contract`
- `f_contract`
- `f_d_contract`
- `jacobi_residual`
- `su3_casimirs`
- `trace_four`
- `trace_table`
- `trace_three`
- `trace_two`

## `myqcd.gamma`

Degrand--rossi gamma basis, traces and dirac structures.

- `EUCLIDEAN_DIM`
- `GAMMA_INDEX_MAX`
- `SPINOR_DIM`
- `charge_conjugation_matrix`
- `charge_conjugation_sign`
- `chiral_projectors`
- `clifford_residual`
- `dirac_adjoint`
- `dirac_slash`
- `dirac_trace`
- `gamma`
- `gamma5`
- `gamma_basis`
- `gamma_basis_gram`
- `gamma_basis_rank`
- `gamma_matrices`
- `gamma_properties`
- `hermiticity_sign`
- `identity`
- `parity_projectors`
- `parity_sign`
- `sigma`
- `trace_gamma_product`
- `transpose_sign`

## `myqcd.gamma_traces`

Gamma5 traces and chiral projector traces.

- `gamma5_anticommutator_residual`
- `trace_gamma5`
- `trace_gamma5_four`
- `trace_gamma5_four_residual`
- `trace_gamma5_table`
- `trace_left_projector`
- `trace_projector_orthogonality`
- `trace_right_projector`

## `myqcd.operators`

Dirac bilinears and pyqcd index mapping.

- `BilinearOperator`
- `COLOR_REPRESENTATIONS`
- `DIRAC_STRUCTURE_LABELS`
- `decompose_dirac_bilinear`
- `dirac_bilinear_structures`
- `enumerate_bilinear_operators`
- `operator_mass_dimension`
- `pyqcd_gamma_index`
- `reconstruct_dirac_bilinear`
- `structure_label`
- `structure_matrix`
- `structure_summary`

## `myqcd.operator_basis`

Derivative operators, chiral and color structures.

- `COLOR_REPRESENTATIONS`
- `DerivativeOperator`
- `chiral_bilinear_structures`
- `chiral_projector_identities`
- `color_factor`
- `enumerate_derivative_operators`
- `fierz_rearrangement`
- `operator_table`
- `quantum_number_summary`
- `vector_axial_combinations`

## `myqcd.fierz`

General 16-basis fierz transformations.

- `BASIS_NAMES`
- `basis_matrix`
- `common_identities`
- `dual_basis_matrix`
- `expand_in_basis`
- `fierz_residual`
- `fierz_table`
- `fierz_terms`
- `fierz_transform`

## `myqcd.lorentz`

Epsilon contractions, schouten identity and projectors.

- `DIM`
- `contract_vectors`
- `epsilon_four_contract`
- `epsilon_square`
- `epsilon_tensor`
- `epsilon_two_contract`
- `epsilon_two_contract_residual`
- `longitudinal_projector`
- `metric`
- `schouten_residual`
- `spin2_dimension`
- `spin2_traceless_check`
- `transverse_projector`
- `transverse_traceless_spin2`
- `vector_components`

## `myqcd.qcd_rules`

Qcd propagators, ward identities and vertices.

- `CONVENTION`
- `VertexFactor`
- `four_gluon_color_structures`
- `ghost_propagator`
- `gluon_propagator`
- `gluon_transversality`
- `gluon_vertex_factors`
- `propagator_mass_dimensions`
- `quark_propagator`
- `quark_propagator_inverse`
- `quark_propagator_residual`
- `rule_audit`
- `three_gluon_lorentz`
- `ward_identity_residual`

## `myqcd.feynman`

Diagram structures and rule catalogs.

- `Diagram`
- `Edge`
- `PARTICLE_STYLES`
- `PropagatorRule`
- `VertexRule`
- `diagram_from_edges`
- `qcd_propagator_rules`
- `qcd_vertex_rules`
- `rule_audit`
- `wick_pairing_diagram`

## `myqcd.topology`

Graph invariants, isomorphism and enumeration.

- `MAX_PERMUTATION_VERTICES`
- `build_chain`
- `build_cycle`
- `build_self_energy`
- `build_sunset`
- `canonical_signature`
- `degree_sequence`
- `enumerate_connected_topologies`
- `external_leg_count`
- `internal_edges`
- `is_cycle`
- `is_isomorphic`
- `is_tree`
- `topology_table`

## `myqcd.diagram_export`

Json, mermaid, latex, tikz, dot and svg export.

- `export_audit`
- `render`
- `to_dot`
- `to_json`
- `to_latex_table`
- `to_mermaid`
- `to_svg`
- `to_tikz`

## `myqcd.lattice`

Lattice momenta, phases and dispersion.

- `TAU`
- `continuum_dispersion`
- `fourier_phase`
- `lattice_dispersion`
- `momentum_from_indices`
- `momentum_permutations`
- `momentum_squared`
- `spatial_momenta`

## `myqcd.statistics`

Jackknife, bootstrap and effective mass.

- `bootstrap_indices`
- `bootstrap_mean`
- `effective_mass`
- `jackknife_covariance`
- `jackknife_mean`
- `jackknife_samples`

## `myqcd.wick`

Exact flavor-respecting wick pairings.

- `FermionField`
- `WickPairing`
- `count_wick_pairings`
- `enumerate_wick_pairings`
- `fermion_fields`

## Audit entry points

- `python -m myqcd`
- `python -m myqcd.operator_audit`
- `python -m myqcd.pyqcd_theory_audit`
