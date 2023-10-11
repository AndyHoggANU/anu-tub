import toml
import sys
sys.path = ["/g/data/x77/ahg157/python-ale/build/lib.linux-x86_64-cpython-310"] + sys.path
import pyale

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import cmocean as cm

## Do something like
## export OMP_NUM_THREADS=16
## to use OpenMP

iter=1
dt=3600
vlev = np.linspace(-2,30,35)

def tpplot(field,h,vlev=50,cmap=cm.cm.thermal):
    plt.figure(figsize=(12,6))
    plt.subplot(211)
    p1 = field.plot(y = "depth",add_colorbar=False,levels=vlev,cmap=cmap)
    for ii in range(75):
        if np.mod(ii,10)==5:
            plt.plot(field.yh.values,h[:,ii],'m',linewidth=0.6)
        else:
            plt.plot(field.yh.values,h[:,ii],'w',linewidth=0.3)
    plt.ylim([0,500])
    plt.gca().invert_yaxis()
    plt.subplot(212)
    p1 = field.plot(y = "depth",add_colorbar=False,levels=vlev,cmap=cmap)
    for ii in range(75):
        if np.mod(ii,10)==5:
            plt.plot(field.yh.values,h[:,ii],'m',linewidth=0.6)
        else:
            plt.plot(field.yh.values,h[:,ii],'w',linewidth=0.3)
    plt.ylim([500,4000])
    plt.gca().invert_yaxis()
    plt.subplots_adjust(hspace=0)
    ax_c = plt.axes([0.92,0.3,0.01,0.4])
    plt.colorbar(p1,ax_c)


params = toml.load("params_adapt.toml")
params["ADAPT_RESTORING_TIMESCALE"] = 50*86400        # default was 10 days
params["ADAPT_SMOOTH_MIN"] = 0.2                      # default is 0.1
cs = pyale.mom_init_cs(params)
restart_filename = 'INPUTS/MOM.res.nc' 
pyale.load_mom_restart(cs, restart_filename)
adapt_cs = pyale.mom_init_regrid(cs, params, "ADAPTIVE")


ds2 = xr.open_dataset(restart_filename)

state = pyale.accelerate_ale(cs, adapt_cs, iter=1, dt=3600)
h_depth = np.cumsum(state[0][39,:,:],1)
new_temp = xr.DataArray(data=np.transpose(state[1][39,:,:]),dims=["zl", "yh"],
            coords=dict(yh=(["yh"], ds2.lath.values),depth=(["zl", "yh"], np.transpose(h_depth))))    
tpplot(new_temp,h_depth,vlev=vlev,cmap=cm.cm.thermal)
plt.title('Iteration '+str(1))
plt.show()

for ii in range(2,10):
    state = pyale.resume_ale(cs, adapt_cs, state, 1, dt=3600)
    h_depth = np.cumsum(state[0][39,:,:],1)
    new_temp = xr.DataArray(data=np.transpose(state[1][39,:,:]),dims=["zl", "yh"],
                coords=dict(yh=(["yh"], ds2.lath.values),depth=(["zl", "yh"], np.transpose(h_depth))))    
    tpplot(new_temp,h_depth,vlev=vlev,cmap=cm.cm.thermal)
    plt.title('Iteration '+str(ii))
    plt.show()