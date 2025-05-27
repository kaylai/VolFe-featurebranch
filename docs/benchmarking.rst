===================================================================================
Benchmarking
===================================================================================

There are many levels to benchmarking a numerical model! 

The simplest level for VolFe is “are the model dependent variables (i.e., the calculation of other people’s parameterisations) correct”. To address this, we have attempted to benchmark the models used for model dependent variables (e.g., solubility functions, fugacity coefficients, sulfur saturation conditions, etc.) wherever possible against results described in the text, shown in figures, or detailed in tables of the studies; calculations in supplementary spreadsheets; or from other Python packages and code.
These are shown in the following notebooks: 

- :doc:`Equilibrium constants <../benchmarking/equilibrium_constants>`

- :doc:`Fugacity coefficients <../benchmarking/fugacity_coefficients>`

- :doc:`Solubility functions <../benchmarking/fugacity_coefficients>`

- :doc:`Sulfide and anhydrite saturation <../benchmarking/sulfur_saturation>`

- :doc:`Sulfide and anhydrite saturation <../benchmarking/sulfur_saturation>`

- :doc:`Oxygen fugacity related variables <../benchmarking/oxygen fugacity>`

Benchmarking calculations is a few steps up from benchmarking model dependent variables and would answer “how do you know a correct solution is reached”. 
To benchmark a calculation like isobars or degassing, all the model dependent variables employed in the tool used as a benchmark must be the same as in VolFe (i.e., fugacity coefficients, solubility functions, equilibrium constants etc.). 
If they are not the same, the answer will not be the same even if the calculation is working. 
Unfortunately, no melt-vapor equilibria tools available use the exact same combination of species, solubility functions, fugacity coefficients, etc. as in VolFe and so the results for the same calculation will not produce the same results.
Therefore, unfortunately, we are not able to benchmark VolFe calculations against any other tools to check it produces the “right” answer.
However, we can still compare the results to see how similar/different they are - a few examples are shown in the following notebooks:

- :doc:`Isobars using Dixon model in VESIcal <../benchmarking/isobar_VESIcal-Dixon>`

- :doc:`Closed-system degassing using VESIcal, CHOSETTO, Sulfur_X, and Evo <Examples/5a. marianas>`

