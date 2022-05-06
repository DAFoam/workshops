"""
A pyXDSM script to generate the design structure matrix 
Run `pip install pyxdsm` before running this script
"""

from pyxdsm.XDSM import XDSM, FUNC, IFUNC

# Change `use_sfmath` to False to use computer modern
x = XDSM(use_sfmath=False)

x.add_input("ImplicitEqn", "x")

x.add_system("ImplicitEqn", IFUNC, "\\textrm{ImplicitEqn:}~ e^{-xy}-y=0")
x.add_system("Objective", FUNC, "\\textrm{Objective:}~ f=2y^2-y")

x.connect("ImplicitEqn", "Objective", "y")

x.add_process(["ImplicitEqn", "Objective"],arrow=True)

x.add_output("Objective", "f", side="right")

x.write("example_xdsm")
