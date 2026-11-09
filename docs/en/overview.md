# Overview

`myqcd` provides executable evidence for lattice-QCD formulas used by MyQCD.
It splits a physics report into three layers:

- SymPy derivations with explicit assumptions and pass/fail checks;
- a source registry that binds formulas to report line numbers;
- independent operator-construction and Feynman-diagram layers.

The package does not copy GPL-3.0 or unlicensed upstream source code. Reference
libraries are read-only Git submodules; every implemented identity is asserted
independently in the test suite.

## Module map

| Module | Purpose |
|---|---|
| `myqcd.audit` | Core formula checks and paper-formula inventory |
| `myqcd.pyqcd_theory_audit` | Gamma, vertex, Wilson-line, Clover, ratio and TMD boundary audits |
| `myqcd.derivations` | SymPy derivations for lattice gauge theory, flow, LaMET, PDF/TMD and statistics |
| `myqcd.formula_registry` | Formula-to-source-to-derivation registry |
| `myqcd.latex_inventory` | Display-formula inventory for paper sources |
| `myqcd.wick` | Exact flavor-respecting Wick pairings with Grassmann signs |
| `myqcd.gamma` | DeGrand--Rossi gamma basis, trace theorem and 16 Dirac structures |
| `myqcd.color` | SU(3) generators, structure constants, Casimirs and color Fierz identity |
| `myqcd.operators` | Dirac bilinear decomposition, parity/C classification and PyQCD index mapping |
| `myqcd.feynman` | Diagram data structures, QCD rule catalog and Wick pairing graphs |
| `myqcd.diagram_export` | Zero-dependency TikZ-Feynman, DOT and SVG export |

## Evidence boundary

`verified` covers only the algebra, dimensions, finite-dimensional proxies and
combinatorial identities that are actually checked. It does not claim loop
integrals, nonperturbative matrix elements, real ensembles, GPU numerics,
soft/rapidity closure or the continuum limit.
