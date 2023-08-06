# jolli
jolli is **j**ust an **o**penPMD **l**ow-**l**evel **i**nterface for reading and plotting PIConGPU output in python. It is a simple wrapper for the openPMD-api to read PIConGPU output

It is currently under development and not recommended for production! It currently obnoxious works for 2D data, is slow, and is not well written. But it might be already useful: You will find it very familiar if you are already used to the ```happi``` interface for ```SMILEI```. 

The following methods are already implemented, while not all arguments are funtioning, yet:

# Quickstart:
```
import jolli
S=jolli.Open("/bigdata/hplsim/scratch/kluget/PFT_2/")
units = ["eV","fs","nc","um","a0"]
jolli.Multiplot(
                S.Scalar(scalar="Uelm",units=["eV","fs"]),
                S.Scalar(scalar="Ukin_e",units=units),
                S.Scalar(scalar="Ukin_H",units=units),
                S.Scalar(scalar="Ukin_C",units=units),
                S.Scalar(scalar="Ukin_O",units=units),
               )
dY = S.Scalar(scalar="Ukin_e",units=["me","s"]).getData()
dX = S.Scalar(scalar="Ukin_e",units=["J","steps"]).getAxis()

S.Scalar(scalar="Uelm",units=units).plot()
d1 = S.Scalar(scalar="Uelm",units=units).getData()

S.Energy(units=units).plot()
d2 = S.Energy(units=units).getData()

Ex = S.Field("Ex",timesteps_SI = [80*jolli.fs], units=units)
S.Field("Ex",timesteps_SI = [80*jolli.fs], units=units,average={"x":"all"}).plot()

S.ParticleBinning("H","density",timesteps_SI = [80*jolli.fs], units=units).plot()
S.ParticleBinning("H","density",timesteps_SI = [80*jolli.fs], units=units,average={"x":"all"}).plot()
S.ParticleBinning("H","density",timesteps_SI = [80*jolli.fs], units=units,average={"x":[1*jolli.um,2*jolli.um]}).plot()
d3 = S.ParticleBinning("H","density",timesteps_SI = [80*jolli.fs], units=units).getData()
d3X = S.Scalar(scalar="Ukin_e",units=["J","steps"]).getAxis("x")

S.ParticleFieldSummary(quantity="density",timesteps_SI = [80*jolli.fs], data_log=True,units=units,average={"x":[1*jolli.um,2*jolli.um]}).plot(yrange=[0.01,200])
```