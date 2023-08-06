#includes
import numpy as np
from matplotlib.widgets import Slider
import sys
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R
from scipy.ndimage import affine_transform
from scipy import interpolate
from scipy.ndimage import measurements
from scipy.fftpack import fft2
from scipy.fftpack import ifft2
from scipy.fftpack import fftshift
from scipy.fftpack import ifftshift
from scipy.fftpack import fftfreq
import scipy as sc
from PIL import Image
from scipy.ndimage.interpolation import rotate
import textwrap
import periodictable as pt

from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))

import os
import sys
from contextlib import contextmanager

import openpmd_api as io
from matplotlib.colors import LogNorm

#import warnings
#warnings.filterwarnings("ignore")
#import shutup; shutup.please()

def get_globals():
    return vars()

@contextmanager
def stdout2devnull():
    old_target = sys.stdout
    old_target_err = sys.stderr
    try:
        with open(os.devnull, "w") as new_target:
            #sys.stdout = new_target
            #sys.stderr = new_target
            #yield new_target
            yield sys.stdout
    finally:
        sys.stdout = old_target
        sys.stderr = old_target_err

try:
    from tqdm.notebook import tqdm
except:
    import tqdm
    
from openpmd_viewer import OpenPMDTimeSeries
import openpmd_api as io

m = 1.
um=1e-6
mm=1e-3
cm=1e-2
nm=1.e-9
sec=1
fs=1e-15*sec
J = 1 # Joule
eV = 1*J/(6.2415e18)
keV = 1000 * eV
V=1 # Volt
T=1 #Tesla
TV=1e12*V/m
c=2e8*m/sec
e = 1.60217663e-19

def Open(results_path = ".",steps_per_wavelength=256):
    class simulation():
        def __init__(self,results_path="./",steps_per_wavelength=256):
            self._results_path = results_path
            self.wavelength = 0.8*um
            self.cells_per_wavelength = steps_per_wavelength
            self.steps_per_period = self.cells_per_wavelength*np.sqrt(2)
            self.period_SI = 3.33*fs*self.wavelength/um
            self.nc = 1.11485e21/cm**3 / ((self.wavelength/um)**2)
            self.a0 = 3.2*TV/((self.wavelength/um)**2)
            self.b0 = 3.2*TV/((self.wavelength/um)**2)/c
            self._d = io.Series(
                self._results_path + "/simOutput/openPMD/simData_%T.bp",
                io.Access.read_only)

            
        def _read_particle_energies(self,species="global", path="global"):
            return self._read_energies(species=species,fields=[])

        def _read_field_energies(self,fields="global",path="global"):
            return self._read_energies(species=[],fields=fields)

        def _read_energies(self,species="global",fields="all"):
            import pandas as pd

            path = self._results_path

            if not species == []:
                if isinstance(species,str): 
                    if species == "global" and "_species" in globals():
                        species = _species
                    elif not isinstance(species,(list,type(np.asarray([])))):
                        species=[]
                        files = os.listdir(path = path+"/simOutput/")
                        Z=[]
                        for i_,i in enumerate(files):
                            #get all species
                            if "_energy_all" in i and i[0] != "e":
                                Z.append(getattr(pt,i[0]).number)
                                species.append(i[0])
                        species = [x for _, x in sorted(zip(Z, species))]
                        species.append("e")

                particle_energies = {}
                for i,speci in enumerate(species):
                    particle_energies[speci] = pd.read_csv(path+"/simOutput/"+speci+"_energy_all.dat", header=0, sep=" ")
                    particle_energies[speci].rename({'Ekin_Joule': 'energy'}, axis=1, inplace=True)

            if not fields == []:
                field_energies = pd.read_csv(path+"/simOutput/fields_energy.dat", header=0, sep=" ")
                field_energies.rename({'total[Joule]': 'energy'}, axis=1, inplace=True)

            if fields != [] and species != []:
                return particle_energies, field_energies
            if species != []: return particle_energies
            return field_energies

##################################################################################################################################### 
#####################################################################################################################################    
#####################################################################################################################################    
        def Energy(self, scalars=None, timesteps_SI=None, units=[''], data_log=False, data_transform=None, **kwargs):
            class _energy():
                def __init__(s,scalars=None, timesteps_SI=None, units=['J',"steps"], data_log=False, data_transform=None, self = None,**kwargs):
                    s._self = self
                    s._units = units
                    if scalars == None:
                        # read all
                        scalars = []
                        Z=[]
                        files = os.listdir(s._self._results_path+"/simOutput/")
                        for i_,i in enumerate(files):
                            #get all species
                            if "_energy_all" in i and i[0] != "e":
                                Z.append(getattr(pt,i[0]).number)
                                scalars.append("Ukin_"+i[0])
                        scalars = [x for _, x in sorted(zip(Z, scalars))]
                        scalars.append("Ukin_e")
                        scalars.append("Uelm")

                    s._scalars = {}
                    for scalar in scalars: 
                        s._scalars[scalar] = s._self.Scalar(scalar=scalar, timesteps_SI=timesteps_SI, units=units, data_log=data_log, data_transform=data_transform, **kwargs)
                      
                def getData(s):
                    return s._scalars
                    
                def plot(s):              
                    plt.figure()
                    for i,speci in enumerate(s._scalars):
                        try:
                            x=x
                            x_=s._scalars[speci].getAxis("t")
                        except:
                            x = s._scalars[speci].getAxis("t")
                            l=len(x)-2; x=x[0:l]
                        if speci != "Uelm":
                            plt.plot(x,s._scalars[speci].getData()[0:l],label=speci,linestyle="--")
                            if i == 0:
                                totalp = s._scalars[speci].getData()[0:l]
                            else:
                                try:
                                    totalp += s._scalars[speci].getData()[0:l]
                                except:
                                    totalp=-1
                        else:
                            try:
                                plt.plot(x,totalp[0:l],label="particles",color="tab:orange")
                            except:
                                None
                            plt.plot(x,s._scalars["Uelm"].getData()[0:l],label="fields",color="tab:blue")
                            #try:
                            totalp += s._scalars["Uelm"].getData()[0:l]
                            plt.plot(x[0:l],totalp[0:l],label="total",color="black")
                            #except:
                            #    None

                    plt.xlabel("t ("+str(s._scalars[speci]._unitx)+")")
                    plt.ylabel("E ("+s._scalars[speci]._unity+")")
                    plt.legend()
                    plt.title(s._self._results_path.split("/bigdata/hplsim/")[1])
                             
                             
            return _energy(scalars=scalars, timesteps_SI=timesteps_SI, units=units, data_log=data_log, data_transform=data_transform, self=self,**kwargs)
                             ##################################################################################################################################### 
#####################################################################################################################################    
#####################################################################################################################################    
        def Scalar(self,scalar=None, timesteps_SI=None, units=[''], data_log=False, data_transform=None, **kwargs):
            class _scalar():
                def __init__(s,scalar=None, timesteps_SI=None, units=['J',"steps"], data_log=False, data_transform=None, self = None,**kwargs):
                    if timesteps_SI == None:
                        # read all
                        s._units=units
                        s._self=self
                        s._label = scalar
                        s._unitx = 1
                        s._data_log = data_log
                        if "Ukin" in scalar:
                            species = scalar.split("Ukin_")[1]
                            s._scalar=s._self._read_particle_energies(species=species)[species]
                        if scalar == "Uelm":
                            s._scalar = s._self._read_field_energies()
                        if scalar=="Utot":
                            s._scalar =  1
                            
                def getData(s):
                    if "J" in s._units: 
                        cv = 1*J
                        s._unity = "J"
                    if "eV" in s._units: 
                        cv = 1*eV
                        s._unity = "eV"
                    if "keV" in s._units: 
                        cv = keV
                        s._unity = "eV"
                    if "me" in s._units: 
                        cv = 511*keV
                        s._unity = "$m_e$"
                    return s._scalar["energy"]/cv
                
                def getAxis(s,ax="t"):
                    if ax == "t":
                        s._unitx = "steps"
                        cv = 1
                        if "fs" in s._units:
                            cv = 1/s._self.steps_per_period*s._self.period_SI/fs
                            s._unitx = "fs"
                        if "s" in s._units:
                            cv = 1/s._self.steps_per_period*s._self.period_SI/sec
                            s._unitx = "s"
                        if "periods" in s._units:
                            cv = 1/s._self.steps_per_period
                            s._unitx = "periods"
                        return s._scalar["#step"]*cv
                    
                def plot(s):
                    plt.figure()
                    if s._data_log:
                        plt.semilogy(s.getAxis(),s.getData(),label=s._label)
                    else:
                        plt.plot(s.getAxis(),s.getData(),label=s._label)
                    plt.xlabel("t ("+str(s._unitx)+")")
                    plt.ylabel("energy ("+str(s._unity)+")")
                    plt.legend()
                    plt.title(s._self._results_path.split("/bigdata/hplsim/")[1])
                    plt.tight_layout()
                    plt.show()
                    
            return _scalar(scalar=scalar, timesteps_SI=timesteps_SI, units=units, data_log=data_log, data_transform=data_transform, self=self,**kwargs)

        #####################################################################################################################################    
        #####################################################################################################################################    
        #####################################################################################################################################    
        class _field():
            def __init__(s, self=None,species=None,field=None, timesteps_SI=None, timesteps = None, average=None, units=[''], data_log=False, data_transform=None, moving=False, export_dir=None,export_format=None, verbose=True,**kwargs):
                s._units=units
                s._self=self
                s._verbose = verbose
                if species == None:
                    s._field = field[0]
                    s._dimension = field[1]
                    s._label = field
                else:
                    s._field = species+"_all_"+field
                    s._dimension = io.Mesh_Record_Component.SCALAR
                    s._label = species+" "+field
                s._species = species
                s._average = average
                if "x" in average:
                    s._ax = "y"
                else:
                    s._ax = "x"
                
                times = os.listdir(path = s._self._results_path +"/simOutput/openPMD/")
                for i,t in enumerate(times):
                    t = t.split("simData_")[1]
                    t = t.split(".")[0]
                    times[i] = int(t)
                times=sorted(times)
                s._max_time = np.max(times)
                
                if timesteps_SI != None and timesteps != None: 
                    print("Error: You can only set the time in SI units OR in steps!")
                else:
                    if type(timesteps_SI) == type(None) and type(timesteps) == type(None):
                        timesteps == "all"

                    if type(timesteps_SI) != type(None):
                        timesteps = np.asarray(timesteps_SI)/s._self.period_SI * s._self.steps_per_period
                        timesteps = timesteps.astype(int,)
                    if type(timesteps) == str or type(timesteps_SI) == str:
                        if timesteps == "all" or timesteps_SI == "all": 
                            timesteps = times

                    for i, time in enumerate(timesteps):
                        #check if time is on disk
                        if not time in times:
                            timesteps[i] = times[np.max(np.where(np.asarray(times) <= time))]
                    s._timesteps = timesteps

                    s._unitT = "steps"
                    s._timesteps_unit = s._timesteps
                    if "fs" in units:
                        s._unitT = "fs"
                        s._timesteps_unit = s._timesteps/s._self.steps_per_period*s._self.period_SI/fs
                    if "s" in units:
                        s._unitT = "s"
                        s._timesteps_unit = s._timesteps/s._self.steps_per_period*s._self.period_SI/sec
                    if "periods" in units:
                        s._unitT = "periods"
                        s._timesteps_unit = s._timesteps/s._self.steps_per_period
                    if "steps" in units:
                        s._unitT = "steps"
                        s._timesteps_unit = s._timesteps
                        
                    #s._read_data()

            def _read_data(s,ti=None):
                    field = s._field
                    dimension = s._dimension
                    s._dim = 2 # for now we only support 2D data
                    
                    if not hasattr(s,"_field_data"):
                        s._field_data = []
                        for i,time in enumerate(s._timesteps):
                            if ti == None or ti==i:
                                if s._verbose: print("Reading data at time",time/s._self.steps_per_period*s._self.period_SI/fs,"fs", "(t_max = ",np.max(s._max_time)/s._self.steps_per_period*s._self.period_SI/fs,"fs)...")
                                # opening the file
                                with stdout2devnull():
                                    data = s._self._d.iterations[time]   
                                    field_data = data.meshes[field][dimension][:]
                                    s._self._d.flush()
                                    field_data *= data.meshes[field][dimension].unit_SI

                                s._field_data.append(field_data)

                        if s._verbose:print("...done reading.")
                    return s._field_data

            def getAxis(s,ax=None):
                unit = "cells"
                cv = 1
                if "nm" in s._units:
                    cv = 1/s._self.cells_per_wavelength*s._self.wavelength/nm
                    unit = "nm"
                if "um" in s._units:
                    cv = 1/s._self.cells_per_wavelength*s._self.wavelength/um
                    unit = "um"
                if "m" in s._units:
                    cv = 1/s._self.cells_per_wavelength*s._self.wavelength/m
                    unit = "m"
                if "wavelength" in s._units:
                    cv = 1/s._self.cells_per_wavelength
                    unit = "wavelength"
                if ax == None:
                    ax = s._ax
                    setattr(s,"_cvx",cv)
                else:
                    setattr(s,"_cv"+ax,cv)
                d=s.getData()[0]
                if ax == "x":
                    if s._dim == 2:
                        dat = d[:,0]
                    if s._dim == 1:
                        dat = d
                    s._unitx = unit
                if ax == "y":
                    if s._dim == 2:
                        dat = d[0,:]
                    if s._dim == 1:
                        dat = d
                    s._unity = unit
                return np.arange(len(dat))*cv

            def getData(s,ti=None):

                if s._field == "E":
                    #default SI unit:
                    cv = 1*V/m
                    s._unitd = "V/m"
                    #other units:
                    if "a0" in s._units:
                        cv = s._self.a0
                        s._unitd = "$a_0$"
                if s._field == "B":
                    #default SI unit:
                    cv = 1*T#*V/m/c # not sure here !!!
                    s._unitd = "Tesla"
                    #other units:
                    if "a0" in s._units or "b0" in s._units:
                        cv = s._self.a0/c
                        s._unitd = "$a_0$"
                if "chargeDensity" in s._field:
                    #default SI unit:
                    cv = 1
                    s._unitd = "$(C/m^3)$"
                    #other units:
                    if "enc" in s._units: 
                        cv = 1*e*s._self.nc
                        s._unitd = "$(e \cdot n_c)$"
                    if "C/cm3" in s._units:
                        cv = 1e-6
                        s._unitd = "$(C/cm^3)$"
                elif "density" in s._field:
                    cv = 1/m
                    s._unitd = "$m^{-3}$"
                    if "nc" in s._units: 
                        cv = 1*s._self.nc
                        s._unitd = "$n_c$"
                    if "1/cm3" in s._units:
                        cv = 1/cm**3
                        s._unitd = "$cm^{-3}$"

                s._cv = cv
                average = s._average
                if not hasattr(s,"_results"):
                    s._results=[]
                    if not hasattr(s,"_field_data"):
                        s._read_data(ti=ti)
                    for i_,field_data in enumerate(s._field_data):
                        if not average == None:
                            for dim in average:
                                if i_ == 0: s._dim -= 1
                                if dim == "y":
                                    if average[dim] == "all":
                                        s._results.append(field_data.mean(0)/cv)
                                    elif isinstance(average[dim],(float,int)):
                                        s._results.append(field_data[int(average[dim]/s._self.wavelength*s._self.cells_per_wavelength),:]/cv)
                                    else:
                                        s._results.append(field_data[int(average[dim][0]/s._self.wavelength*s._self.cells_per_wavelength):int(average[dim][1]/s._self.wavelength*s._self.cells_per_wavelength),:].mean(0)/cv)
                                if dim == "x":
                                    if average[dim] == "all":
                                        s._results.append(field_data.mean(1)/cv)
                                    elif isinstance(average[dim],(float,int)):
                                        s._results.append(s._field_data[:,int(average[dim]/s._self.wavelength*s._self.cells_per_wavelength)]/cv)
                                    else:
                                        s._results.append(field_data[:,int(average[dim][0]/s._self.wavelength*s._self.cells_per_wavelength):int(average[dim][1]/s._self.wavelength*s._self.cells_per_wavelength)].mean(1)/cv)
                        else:
                            s._results.append(field_data/cv)

                return s._results
            
            def clear(s):
                try:
                    delattr(s,"_field_data")
                except:
                    #nothing to remove
                    None
                try:
                    delattr(s,"_results")
                except:
                    #nothing to remove
                    None

            def plot(s):
                dat = s.getData()
                if s._dim == 2:
                    for i,d in enumerate(dat):
                        plt.figure()
                        plt.contourf(s.getAxis("y"),s.getAxis("x"),d,levels=5)
                        plt.xlabel("x ("+s._unitx+")")
                        plt.ylabel("y ("+s._unity+")")
                        clb = plt.colorbar()
                        clb.ax.set_ylabel(s._label+" ("+s._unitd+")")
                        plt.title(s._self._results_path.split("/bigdata/hplsim/")[1]+" | time: "+str(np.round(s._timesteps_unit[i],2))+" "+s._unitT)
                        plt.show()
                elif s._dim == 1:
                    plt.figure()
                    ax = list(s._average)[0]
                    x = s.getAxis(ax)
                    for i,d in enumerate(dat):
                        plt.plot(x,d,label=s._label+" | " + str(np.round(s._timesteps_unit[i],2))+" "+s._unitT)
                    if ax == "x": unit = s._unitx
                    if ax == "y": unit = s._unity
                    plt.xlabel(ax+" ("+unit+")")
                    plt.ylabel(s._label+" ("+s._unitd+")")
                    plt.title(s._self._results_path.split("/bigdata/hplsim/")[1])
                    plt.legend()
                    plt.show()
                    
        def Field(self,field=None, timesteps_SI=None, timesteps = None, average=None, units=['V/m',"steps"], data_log=False, data_transform=None, moving=False, export_dir=None, verbose = True,**kwargs):

            return self._field(self=self,field=field, timesteps_SI=timesteps_SI, timesteps = timesteps, average=average, units=units, data_log=data_log, data_transform=data_transform, moving=moving, export_dir=export_dir, verbose=verbose, **kwargs)

                        #####################################################################################################################################    
        #####################################################################################################################################    
        #####################################################################################################################################    
        def ParticleBinning(self,species=None, field=None, timesteps_SI=None, timesteps = None, average=None, units=['V/m',"steps"], data_log=False, data_transform=None, moving=False, export_dir=None,verbose=True, **kwargs):
            return self._field(self=self,species = species, field=field, timesteps_SI=timesteps_SI, timesteps = timesteps, average=average, units=units, data_log=data_log, data_transform=data_transform, moving=moving, export_dir=export_dir,export_format=None, verbose=verbose, **kwargs)

        def ParticleFieldSummary(self,read_species="all",quantity="chargeDensity",read_fields=["E","B"],timesteps_SI=-1, timesteps = -1, average={"x":"all"}, units=['V/m',"steps"], data_log=False, data_transform=None, moving=False, export_dir=None,export_format="pdf", verbose=True,**kwargs):
            
            class _summary():
                def __init__(s,self,quantity=None,timesteps_SI=-1, timesteps = -1, average="all", units=['V/m',"steps"], data_log=False, data_transform=None, moving=False, export_dir=None,export_format=None, read_species="all",read_fields=["E","B"],verbose=True,**kwargs):

                    s._self=self
                    s._quantity = quantity
                    s._data_log = data_log
                    s._average = average
                    s._units = units,
                    s._data_transform=data_transform
                    s._moving=moving
                    s._export_dir=export_dir
                    s._export_format=export_format
                    s._verbose=verbose
                    s._kwargs=kwargs
                    
                    #get all timesteps
                    times = os.listdir(path = s._self._results_path +"/simOutput/openPMD/")
                    for i,t in enumerate(times):
                        t = t.split("simData_")[1]
                        t = t.split(".")[0]
                        times[i] = int(t)
                    times=sorted(times)
                    s._max_time = np.max(times)
                    if timesteps == "all" or timesteps_SI == "all": 
                        timesteps = times
                    else:
                        if timesteps_SI != None:
                            timesteps = np.asarray(timesteps_SI)/s._self.period_SI * s._self.steps_per_period
                            timesteps = timesteps.astype(int,)

                    for i, time in enumerate(timesteps):
                        #check if time is on disk
                        if not time in times:
                            timesteps[i] = times[np.max(np.where(np.asarray(times) <= time))]
                    s._timesteps = timesteps

                    #get all particles
                    # opening the file
                    data = s._self._d.iterations[0]   

                    if isinstance(read_species,str): 
                        if read_species == "all":                                
                            Z=[]
                            read_species=[]
                            for i_,i in enumerate(data.meshes):
                                #get all species
                                if "_"+quantity in i:
                                    if i[0] != "e":
                                        read_species.append(i[0])
                                        Z.append(getattr(pt,i[0]).number)
                            read_species = [x for _, x in sorted(zip(Z, read_species))]
                            read_species.append("e")
                        else:
                            read_species = [read_species]

                    s._particles = {}                       
                    #read all particles
                    with tqdm(total=(len(read_species))+3,leave=False) as pbar:
                        pbar.set_description("Reading particle fields")
                        # read particle fields
                        for i in read_species:
                            pbar.set_description("Reading " + i + " " + quantity)
                            s._particles[i] = s._self.ParticleBinning(i,quantity,timesteps=timesteps,average=average, units=units, data_log=data_log, data_transform=data_transform, moving=moving, export_dir=export_dir,verbose=False, **kwargs)
                            pbar.update(1)

                        #get all fields
                        s._fields={}
                        s._fields["E"]={}
                        pbar.set_description("Reading Ex")
                        s._fields["E"]["x"] = s._self.Field("Ex",timesteps = timesteps,average=average, units=units, data_log=data_log, data_transform=data_transform, moving=moving, export_dir=export_dir,verbose=False, **kwargs)
                        pbar.update(1)
                        pbar.set_description("Reading Ey")
                        s._fields["E"]["y"] = s._self.Field("Ey",timesteps = timesteps,average=average, units=units, data_log=data_log, data_transform=data_transform, moving=moving, export_dir=export_dir,verbose=False, **kwargs)
                        pbar.update(1)
                        s._fields["B"]={}
                        pbar.set_description("Reading Bz")
                        s._fields["B"]["z"] = s._self.Field("Bz",timesteps = timesteps,average=average, units=units, data_log=data_log, data_transform=data_transform, moving=moving, export_dir=export_dir,verbose=False, **kwargs)
                        pbar.update(1)
                        
                    s._read_species = read_species
                    
                def plot(s,
                         yrange=[None,None],yrange_SI=[None,None],
                         erange=[None,None],erange_SI=[None,None],
                         xrange=[None,None],xrange_SI=[None,None],
                         field_scaling="auto",
                         slide=False,
                         ax=None,
                         single_time=None,
                         export=None,
                         **kwargs
                        ):  
                    ptcl = list(s._particles)
                    if single_time != None:
                        timesteps=[s._timesteps[single_time]]         
                    else:
                        single_time=0
                        timesteps=s._timesteps
                    with tqdm(total=len(timesteps)*((len(s._read_species))+3),leave=False) as pbar:
                        for ti_,timestep in enumerate(timesteps):
                            ti = ti_ + single_time
                            if not export or ti_==0:
                                fig, ax1 = plt.subplots()

                                ax2 = ax1.twinx()
                            else:
                                ax1.clear();ax2.clear()
                            
                            if not (export and os.path.isfile(s._self._results_path+"/temp/summary_"+str(timestep)+".tif")):
                                #if export and file exists: skip
                                a=[]

                                for i_,i in enumerate(s._particles):
                                    pbar.set_description("Reading " + i + " " + s._quantity + " of timestep "+str(timestep))
                                    #if ti_ > 0 or slide:
                                    s._particles[i].clear()
                                    if not i == "e" and not i == "t":
                                        try:
                                            b=a*1
                                            a+=s._particles[i].getData(ti=ti)[0]
                                        except:
                                            b=1e-10
                                            a=s._particles[i].getData(ti=ti)[0]
                                            x=s._particles[ptcl[0]].getAxis()
                                        ax1.fill_between(x,(a),(b),label=i,linewidth=0)
                                    pbar.update(1)

                                if "e" in ptcl:
                                    #if ti_ > 0 or slide:
                                    s._particles["e"].clear()
                                    ax1.plot(x,(np.abs(s._particles["e"].getData(ti=ti)[0])),color="r",label="e")
                                    pbar.update(1)
                                if s._data_log: ax1.set_yscale('log')
                                if yrange_SI[0] != None and yrange_SI[1] != None:
                                    yrange = np.asarray(yrange_SI)/s._particles[ptcl[0]]._cv
                                if yrange[0] != None and yrange[1] != None:
                                    ax1.set_ylim(yrange)
                                if xrange_SI[0] != None and xrange_SI[1] != None:
                                    xrange = np.asarray(xrange_SI)*s._particles[ptcl[0]]._cvx
                                if xrange[0] != None and xrange[1] != None:
                                    ax1.set_xlim(xrange)

                                if True:#not fields=={}: 
                                    pbar.set_description("Reading Ex" + " of timestep "+str(timestep))
                                    #if ti_ > 0 or slide: 
                                    s._fields["E"]["x"].clear()
                                    ax2.plot(x,s._fields["E"]["x"].getData(ti=ti)[0],label="Ex",color="b")
                                    pbar.update(1)
                                    pbar.set_description("Reading Ey" + " of timestep "+str(timestep))
                                    #if ti_ > 0 or slide: 
                                    s._fields["E"]["y"].clear()
                                    ax2.plot(x,s._fields["E"]["y"].getData(ti=ti)[0],label="Ey",color="orange")
                                    pbar.update(1)
                                    pbar.set_description("Reading Bz" + " of timestep "+str(timestep))
                                    #if ti_ > 0 or slide: 
                                    s._fields["B"]["z"].clear()
                                    ax2.plot(x,s._fields["B"]["z"].getData(ti=ti)[0],label="Bz",color="black")
                                    pbar.update(1)
                                ax1.set_xlabel('x ($\mu m$)')
                                ax1.set_ylabel(s._quantity+' '+s._particles[ptcl[0]]._unitd)
                                ax2.set_ylabel('$E_{x,y}$ ('+s._fields["E"]["x"]._unitd+'), $B_{z}$ ('+s._fields["B"]["z"]._unitd+')', color='orange')
                                if isinstance(erange_SI,list) or isinstance(erange_SI,type(np.asarray([1,19]))):
                                    if erange_SI[0] != None and erange_SI[1] != None:
                                        erange = np.asarray(erange_SI)/s._fields["E"]["x"]._cv
                                    if erange[0] != None and erange[1] != None:
                                        ax2.set_ylim(erange)
                                if field_scaling=="auto":
                                    fm1 = np.max(np.abs(s._fields["E"]["x"].getData(ti=ti)[0]))*s._fields["E"]["x"]._cv/s._self.a0+1e-9
                                    fm2 = np.max(np.abs(s._fields["E"]["y"].getData(ti=ti)[0]))*s._fields["E"]["x"]._cv/s._self.a0
                                    fm =np.max([fm1,fm2])
                                    if isinstance(erange_SI,int) or isinstance(erange_SI,float):
                                        fm_plt = erange_SI/s._fields["E"]["x"]._cv
                                    else:
                                        fm_plt = fm/s._fields["E"]["x"]._cv*s._self.a0
                                    if s._data_log:
                                        pos_nc = (np.log10(np.sqrt(1+fm1**2/2))-np.log10(ax1.get_ylim()[0]))/(np.log10(ax1.get_ylim()[1])-np.log10(ax1.get_ylim()[0]))
                                    else:
                                        pos_nc = (np.sqrt(1+fm1**2/2)-(ax1.get_ylim()[0]))/((ax1.get_ylim()[1])-(ax1.get_ylim()[0]))
                                    if pos_nc  < 0.5:
                                        ax2.set_ylim([-fm_plt,(1-pos_nc)/pos_nc*fm_plt])
                                    else:
                                        ax2.set_ylim([-fm_plt*pos_nc/(1-pos_nc),fm_plt])

                                ax1.legend(loc=2)
                                ax2.legend(loc=1)                            
                                plt.title(s._self._results_path.split("/bigdata/hplsim/")[1]+" | time: "+str(np.round(s._fields["E"]["x"]._timesteps_unit[ti],2))+" "+s._fields["E"]["x"]._unitT)
                                plt.tight_layout()

                                if export:
                                    path = s._self._results_path+"/temp/"
                                    try:
                                        os.mkdir(path)
                                    except:
                                        None
                                    plt.savefig(path+"/summary_"+str(timestep)+".tif")
                                else:
                                    if (s._export_dir != None):
                                        if s._export_dir == True:
                                            s._export_dir = s._self._results_path+"/results"
                                        try:
                                            os.mkdir(s._export_dir)
                                        except:
                                            None
                                        plt.savefig(s._export_dir+"/summary_"+str(timestep)+"."+s._export_format)
                            else:
                                pbar.set_description("Skipping already existing preview "+str(timestep))
                                pbar.update(3+len(s._particles))

                            if slide:
                                plt.close(fig)
                            elif not export:
                                plt.show()
                    if export: plt.close(fig)

                def slide(s,clear_cache=False,cache=False,**kwargs):
                    # Create subplot
                    fig, ax = plt.subplots()
                    path = s._self._results_path+"/temp/"
                    if clear_cache==True:
                        try:
                            files = os.listdir(path)
                            for file in files:
                                os.remove(path+file)
                            os.rmdir(path)
                        except:
                            None
                    if cache:
                        try:
                            os.mkdir(path)
                        except:
                            None

                        s.plot(export=True,**kwargs)
                    # Hide X and Y axes label marks
                    ax.xaxis.set_tick_params(labelbottom=False)
                    ax.yaxis.set_tick_params(labelleft=False)
                    # Hide X and Y axes tick marks
                    ax.set_xticks([])
                    ax.set_yticks([])                    
                    plt.subplots_adjust(bottom=0.35)
                    
                    # Create and plot
                    file = path+'summary_0.tif'
                    if not os.path.exists(file):
                        s.plot(single_time=0,
                               export=True,
                               slide=True,
                               **kwargs
                              )
                    a=plt.imread(file)
                    ax.imshow(a)
                    plt.tight_layout()
                    # Create axes for frequency and amplitude sliders
                    axfreq = plt.axes([0.15, 0.005, 0.65, 0.03])

                    # Create a slider from 0.0 to 20.0 in axes axfreq
                    # with 3 as initial value
                    dt = s._timesteps[1]-s._timesteps[0]
                    if len(s._timesteps) > 1:
                        freq = Slider(axfreq, 'Timestep', s._timesteps[0], s._timesteps[-1], 0, valstep=dt)

                    # Create function to be called when slider value is changed

                        def update(val):
                            time = int(freq.val)
                            file = path+'/summary_'+str(time)+'.tif'
                            if not os.path.exists(file):
                                s.plot(single_time=int(time/dt),
                                       export=True,
                                       slide=True,
                                       **kwargs
                                      )
                            a=plt.imread(file)
                            ax.imshow(a)

                        # Call update function when slider value is changed
                        freq.on_changed(update)


                    # display graph
                    plt.show()            
            
            return _summary(self=self,
                            read_species=read_species,
                            quantity=quantity,
                            read_fields=read_fields,
                            timesteps_SI=timesteps_SI, 
                            timesteps = timesteps, 
                            average=average, 
                            units=units, 
                            data_log=data_log, 
                            data_transform=data_transform, 
                            moving=moving, 
                            export_dir=export_dir, 
                            export_format=export_format, 
                            verbose=verbose, 
                            **kwargs)

    return simulation(results_path,steps_per_wavelength)









#######################################################
##########----------//Phase Space\\----------##########        
#######################################################

class PhaseSpace():

    dataDict = dict()

    def __init__(self, phaseSpacePath):
        '''
        opens the output file of the sim and saves its important variables
        
        --------------------
        phaseSpaceData (string): path to .bp file in /simOutput/phaseSpace/*
                                 i.e.: /bigdata/hplsim/production/dispersion_ions/5/simOutput/phaseSpace/PhaseSpace_e_all_ypy_40830.bp
        '''
        series = io.Series(phaseSpacePath, io.Access.read_only)

        #get snapshot frame number
        for frameNumber, i in series.iterations.items(): pass

        i = series.iterations[frameNumber]

        #prepare/get attributes for extracting data out of i.meshes
        attributes = []
        for items in i.meshes.items():
            for string in items:
                for thing in string:
                    attributes.append(thing)

        #get phase space data
        self.dataDict.update({'mesh' : i.meshes[ ''.join( attributes[ : len( attributes ) - 1])][attributes[ len( attributes ) - 1]]})
        self.dataDict.update({'plotDataRaw' : self.dataDict.get('mesh')[ : ]})
        series.flush()
        
        self._appendCleanedValues(self.dataDict.get('plotDataRaw'))
    
    
    def getDataDictionary(self):
        return self.dataDict
        
    
    
    def _appendCleanedValues(self, valuesToClean):
        nonzeroIndices = np.nonzero(valuesToClean)
        
        try:
            xMin = np.min(nonzeroIndices[0])
            xMax = np.max(nonzeroIndices[0])
            yMin = np.min(nonzeroIndices[1])
            yMax = np.max(nonzeroIndices[1])
            
            #print(f'xMin: {xMin} xMax: {xMax} yMin: {yMin}yMax: {yMax}')
        
            trimmedData = valuesToClean[xMin:xMax+1, yMin:yMax+1]

        except:
            trimmedData = valuesToClean[:]
            print('PhaseSpace data cleaning did not work!!! pls check for reason')
        
        
        self.dataDict.update({'plotDataClean' : trimmedData})
    
    
    
    def drawPlotClean(self):
        im = plt.pcolormesh(-self.dataDict.get('plotDataClean'),  norm=LogNorm())
        plt.colorbar(im)
        plt.xlabel(self.getDataDictionary().get('mesh').get_attribute('axisLabels')[0])
        plt.ylabel(self.getDataDictionary().get('mesh').get_attribute('axisLabels')[1])
        plt.title('Phase Space Plot')
        
        '''
        xticks = np.arange(0, len(self.getDataDictionary().get('plotDataRaw')), self.getDataDictionary().get('mesh').get_attribute('dr'))
        plt.xticks(ticks=xticks)
        
        yticks = np.arange(0, self.getDataDictionary().get('mesh').get_attribute('dV'))
        plt.yticks(ticks=yticks)
        
        print(self.getDataDictionary().get('mesh').get_attribute('p_max'))
        '''
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
def Multiplot(*args,stack=False):
    plt.figure()
    for i,s in enumerate(args):
        if stack:
            if i == 0:
                plt.fill_between(s.getAxis(),s.getData(),0,label=s._label)
                total = s.getData()
            else:
                plt.fill_between(s.getAxis(),total+s.getData(),total,label=s._label)
                total += s.getData()
        else:
            plot = plt.plot(s.getAxis(),s.getData(),label=s._label)
  
    plt.xlabel("t ("+str(s._unitx)+")")
    plt.ylabel("energy ("+str(s._unity)+")")
    plt.legend()
    plt.tight_layout()
    plt.show()