%matplotlib notebook
from importlib import reload  # Python 3.4+
import jolli as j
reload(j)
S=j.Open("/bigdata/hplsim/production/dispersion_ions/5/",steps_per_wavelength=256)
units = ["eV","fs","nc","um","a0","enc"]
#jolli.Multiplot(
#                S.Scalar(scalar="Uelm",units=["eV","fs"]),
#                S.Scalar(scalar="Ukin_e",units=units),
#                S.Scalar(scalar="Ukin_H",units=units),
#                S.Scalar(scalar="Ukin_C",units=units),
#                S.Scalar(scalar="Ukin_O",units=units),
#               )
#dY = S.Scalar(scalar="Ukin_e",units=["me","s"]).getData()
#dX = S.Scalar(scalar="Ukin_e",units=["J","steps"]).getAxis()#

S.Scalar(scalar="Uelm",units=units).plot()
#d1 = S.Scalar(scalar="Uelm",units=units).getData()

#S.Energy(units=units).plot()
#d2 = S.Energy(units=units).getData()

#Ex = S.Field("Ex",timesteps_SI = [80*jolli.fs], units=units)
#S.Field("Ex",timesteps_SI = [80*jolli.fs], units=units,average={"x":"all"}).plot()

#S.ParticleBinning("H","density",timesteps_SI = [80*jolli.fs], units=units).plot()
#S.ParticleBinning("H","density",timesteps_SI = [80*jolli.fs], units=units,average={"x":"all"}).plot()
#S.ParticleBinning("H","density",timesteps_SI = [80*jolli.fs], units=units,average={"x":[1*jolli.um,2*jolli.um]}).plot()
#d3 = S.ParticleBinning("H","density",timesteps_SI = [80*jolli.fs], units=units).getData()
#d3X = S.Scalar(scalar="Ukin_e",units=["J","steps"]).getAxis("x")

#S.ParticleFieldSummary(timesteps_SI = "all", 
#                       data_log=True,
#                       units=units,
#                       average={"x":[5*j.um,6*j.um]},
#                      ).slide(yrange_SI=[0.01*j.e*S.nc,200*j.e*S.nc],
#                             erange_SI=[-30*S.a0,30*S.a0],
#                             field_scaling="manual",
#                             cache=True,
                             #clear_cache=True
#                            )