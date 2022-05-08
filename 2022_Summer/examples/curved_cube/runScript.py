#!/usr/bin/env python

from mpi4py import MPI
from dafoam import PYDAFOAM

# Set the parameters for optimization
daOptions = {
    "solverName": "DASimpleFoam",
    "primalMinResTol": 1.0e-8,
    "useAD": {"mode": "fd"},
    "objFunc": {
        "CD": {
            "part1": {
                "type": "force",
                "source": "patchToFace",
                "patches": ["walls"],
                "directionMode": "fixedDirection",
                "direction": [1.0, 0.0, 0.0],
                "scale": 1.0,
                "addToAdjoint": True,
            }
        },
    },
}

DASolver = PYDAFOAM(options=daOptions, comm=MPI.COMM_WORLD)
DASolver()
funcs = {}
evalFuncs = ["CD", "CL"]
DASolver.evalFunctions(funcs, evalFuncs)
