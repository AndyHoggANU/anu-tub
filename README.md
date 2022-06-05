# anu-tub
A bathtub-sector ocean configuration for MOM6.
This configuration is designed primarily as a test case for implementing new vertical coordinate systems into MOM6, and to compare with existing vertical coordinate.
Thus, the design criteria is to produce the simplest configuration that incorporates buoyancy and wind forcing, gyre circulation, overturning circulation and topographically-constrained overflows.
The configuration includes the following features:
* The sector is 40° wide, and goes from ~70.3°S to ~70.3°N.
* It has a 1/4° nominal resolution and a Mercator grid refinement.
* the default vertical coordinate is ZSTAR with 75 vertical levels.
* The bathymetry is simple, with a vertical wall to the north, an "Antarctic shelf and slope" in the south and sloping sidewalls on the east and west.
* The domain is periodic in the east-west direction, allowing zonal flow in a narrow "Drake Passage" between ~65°S and ~52°S.
* Surface momentum forcing is via a prescribed zonal wind field that is constant, but varies with latitude.
* Thermal forcing is through relation to a latitude-dependent SST profile, and there is (currently) no freshwater forcing so that salinity is constant. 
* We use the WRIGHT equation of state, without frazil formation or sea ice.
* The model includes the PBL surface boundary layer scheme with a contant background diffusivity of $2 \times 10^{-5}$.
* The MEKE eddy parameterisation scheme is turned off, as is the mixed layer restratification scheme.

The model has $160 \times 800$ grid points, with a tile layout of $6 \times 40$ to run efficiently on 240 cores.
With a 900-second timestep, the standard ZSTAR case takes ~2 hours per year (12 years/day) and consumes ~500 SU per model year.
