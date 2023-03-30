import toml
import sys
sys.path = ["/g/data/x77/ahg157/python-ale/build/lib.linux-x86_64-cpython-39"] + sys.path
import pyale
import numpy as np
import xarray as xr

## Do something like
## export OMP_NUM_THREADS=16
## to use OpenMP

iter=200
dt=3600
restore_ts = 864000.0

params = toml.load("params_adapt.toml")
params["ADAPT_RESTORING_TIMESCALE"] = restore_ts  # default is 864000
cs = pyale.mom_init_cs(params)
restart_filename = 'INPUTS/MOM.res.nc' 
pyale.load_mom_restart(cs, restart_filename)
adapt_cs = pyale.mom_init_regrid(cs, params, "ADAPTIVE")

(h, temp, salt) = pyale.accelerate_ale(cs, adapt_cs, iter=iter, dt=dt)

ds2 = xr.open_dataset(restart_filename)
depth = np.cumsum(h[39,:,:],1)
temp_depth = xr.DataArray(
    data=np.transpose(temp[39,:,:]),dims=["zl", "yh"],
    name="temp",
    coords=dict(
        yh=(["yh"], ds2.lath.values),
        depth=(["zl", "yh"], np.transpose(depth))
    ),
    attrs=dict(
        description="Temperature on coordinate depths.",
        units="degC",
    )
)

temp_depth.to_netcdf('OUTPUTS/vary_restore_ts/temp_restore_ts_'+str(restore_ts)+'.nc')
