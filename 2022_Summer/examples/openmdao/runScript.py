"""
A simple OpenMDAO optimization with one implicit and one explicit components
For more tutorials, refer to OpenMDAO's documentation website at
https://openmdao.org/newdocs/versions/latest/main.html
"""

import openmdao.api as om
import numpy as np


class ImplicitEqn(om.ImplicitComponent):
    """
    Define the implicit component, its governing equation is:
    e^(-x * y) - y = 0
    Here x is the input and y is the output
    """

    def setup(self):

        # define input
        self.add_input("x", val=1.0)

        # define output
        self.add_output("y", val=1.0)

    def setup_partials(self):
        # Finite difference all partials.
        self.declare_partials("*", "*", method="fd")

    def apply_nonlinear(self, inputs, outputs, residuals):
        # get the input and output and compute the residual
        # R = e^(-x * y) - y

        # NOTE: we use [0] here because OpenMDAO assumes all inputs
        # and outputs are arrays. If the input is a scalar, OpenMDAO
        # will create an array that has size 1, so to get its value
        # we have to use [0]
        x = inputs["x"][0]
        y = outputs["y"][0]

        residuals["y"] = np.exp(-x * y) - y


class Objective(om.ExplicitComponent):
    """
    Define the explicit component f = 2*y^2 - y + 1
    Here x is the input and y is the output
    """

    def setup(self):

        # define input
        self.add_input("y", val=1.0)

        # define output
        self.add_output("f", val=1.0)

    def setup_partials(self):
        # Finite difference all partials.
        self.declare_partials("*", "*", method="fd")

    def compute(self, inputs, outputs):
        # compute the output based on the input
        y = inputs["y"][0]

        outputs["f"] = 2 * y * y - y + 1


# create an OpenMDAO problem object
prob = om.Problem()

# now add the implicit component defined above to prob
# NOTE: we use "promotes" to facilitate the linking of components' inputs and outputs. Refer to the detailed explanation from
# https://openmdao.org/newdocs/versions/latest/basic_user_guide/multidisciplinary_optimization/linking_vars.html
prob.model.add_subsystem(
    "ImplicitEqn",
    ImplicitEqn(),
    promotes=["*"],
)

# add the objective explicit component defined above to prob
prob.model.add_subsystem(
    "Objective",
    Objective(),
    promotes=["*"],
)

# setup the linear and nonlinear equation solution methods for the implicit component
prob.model.nonlinear_solver = om.NewtonSolver(solve_subsystems=False, iprint=-1)
prob.model.linear_solver = om.ScipyKrylov()

# set the design variable and objective function
prob.model.add_design_var("x", lower=-10, upper=10)
prob.model.add_objective("f", scaler=1)

# setup the optimizer
prob.driver = om.ScipyOptimizeDriver()
prob.driver.options["optimizer"] = "SLSQP"

# setup the problem
prob.setup()

# write the n2 diagram
om.n2(prob, show_browser=False, outfile="n2.html")

# run the optimization
prob.run_driver()

# get the optimal solution after the optimization
f_opt = prob.get_val("f")
x_opt = prob.get_val("x")
print("f_opt:", f_opt)
print("x_opt:", x_opt)
