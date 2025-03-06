==========
Code structure
==========

This is a brief overview of how the VolFe code is structured and broadly where to find different types of functions in VolFe (see API reference for more detail about these functions).
You don't need to understand this to run VolFe, but popped it here in case people are interested!
For instance, you could use VolFe functions in your code if they're helpful (particuarly model-dependent variables).


Melt gas
--------

"melt_gas.py" hosts functions for calculating properties of the melt and gas at a set of conditions (e.g., *P* and *T*): so these are the forward calculations. Broadly, this includes things like:

- Fugacities (*f*\ :sub:`i`), partial pressures (*p*\ :sub:`i`), and mole fraction in the vapor (*x*\ :sup:`g` \ :sub:`i`) of vapor species given *P*, *T* and volatile concentration in the melt.

- Coverting melt composition between mass and mole fractions, based on cations, oxides, single oxygen, etc.

- Calculating melt speciation for oxidised carbon, oxidised hydrogen, sulfur, and iron given *P*, *T*, dissovled volatile concentration, and *f*\ :sub:`O2`.


Model dependent variables
------

"model_dependent_variables.py" hosts the functions for calculating various model dependent variables given a set of conditions (e.g., *P* and *T*): so these are the forward calculations.
More information can be found on the :doc:`Options <current_mdv>` page, but the types of parameters calculated and stored here are:

- Element and species constants (e.g., atomic and molecular mass).

- Functions to build the models option dataframe, including the default options.

- Functions to calculate solubility functions and and equilibrium constants; fugacity coefficients; SCSS and SCAS; and melt density.

- Functions to convert between *f*\ :sub:`O2` and Fe\ :sup:`3+`/Fe\ :sub:`T`, and *f*\ :sub:`O2` buffers.


Equilibrium and differential equations
------

"equilibrium_equations.py" contains the functions to calculate the equilibrium concentration and speciation of volatiles in melt ± vapor and the proportions of melt and vapor given *P*, *T*, and the bulk composition of the system.
These are iterative calculations, which are solved using Jacobian matrix/Newton-Raphson approach (solvers and initial guesses are also in this file).

The associated differential equations required for the solver are contained in “differential_equations.py”, where the symbolic differentiation was done using SymPy (Meurer et al., 2017).
It is a long file because there are separate functions for different combinations of species in the melt and vapor (e.g., only carbon species in the system; the full COHS system; only H\ :sub:`2`O-CO\ :sub:`2` in the melt and vapor, etc.)

Calculations
-----

“calculations.py” contains broadly two types of functions.

Firstly, there are functions for calculating properties about the system, such as:

- Bulk composition given melt and vapor compositions.

- Is sulfur or graphite saturated at a given set of condition.

- Monte Carlo simulation of compositional errors.

Secondly, there are calculation types that do not necessarily have independent variables of *P*, *T*, and bulk composition (as in "equilibrium_equations.py"), such as:

- *T*, melt composition (including *f*\ :sub:`O2` estimate), vapor-saturated: calculate *P*\ :sup: `v`\ :sub: `sat` and the melt/vapor composition and speciation.

- *T*, melt composition, vapor+sulfide+anhydrite-saturated, ± *P*: calculate *f*\ :sub:`O2` ± *P* and the melt/vapor composition and speciation.

- *T*, melt composition, vapor+(sulfide or anhydrite)-saturated, ± *P*: calculate *f*\ :sub:`O2` ± *P* and the melt/vapor composition and speciation.

- *T*, *P*, *f*\ :sub:`O2`, CO\ :sub:`2`-eq, H\ :sub:`2`O-eq, vapor±(sulfide and/or anhydrite)-saturation: calculate how much sulfur can dissolve in the melt.

- *T*, *P*, volatile-free composition, assuming only H\ :sub:`2`O and CO\ :sub:`2`: calculate concentrations of H\ :sub:`2`O and CO\ :sub:`2` in the melt (i.e., isobars).


Batch calculations
-----

"batch_calculations.py" joins calculations together to enable them to be run for multiple conditions.
This might be to create a degassing calculations (i.e., run over multiple *P*) and or *P*\ :sup: `v`\ :sub: `sat` for a whole spreadsheet of melt compositions.
More details can be found in the Worked Examples.
