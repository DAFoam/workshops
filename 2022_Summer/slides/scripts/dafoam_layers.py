"""
A pyXDSM script to generate the design structure matrix 
Run `pip install pyxdsm` before running this script
"""

from pyxdsm.XDSM import XDSM, FUNC, IFUNC

# Change `use_sfmath` to False to use computer modern
x = XDSM(use_sfmath=False)

x.add_input("OpenFOAM", "\\textrm{src/adjoint}")
x.add_input("Cython", "\\textrm{src/pyDASolvers}")
x.add_input("Python", "\\textrm{pyDAFoam.py}, \\textrm{mphys\_dafoam.py}")

x.add_system("OpenFOAM", FUNC, "\\textrm{OpenFOAM}")
x.add_system("Cython", FUNC, "\\textrm{Cython}")
x.add_system("Python", FUNC, "\\textrm{Python}")

x.connect("OpenFOAM", "Cython", "\\textrm{libDAFoam*.so}")
x.connect("Cython", "Python", "\\textrm{pyDASolver*.so}, \\textrm{pyColoring*.so}")

x.add_process(["OpenFOAM", "Cython", "Python"], arrow=True)

x.add_output("OpenFOAM", "\\textrm{OpenFOAM/sharedLibs/}", side="right")
x.add_output("Python", "\\textrm{site-packages/dafoam/}", side="right")

x.write("dafoam_layers")
