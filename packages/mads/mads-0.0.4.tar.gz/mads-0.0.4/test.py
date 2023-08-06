import numpy as np
from mads import mads

# Define objective function
def objective_function(d):
    f = (d[0] - 0.3)**2 + (d[1] - 0.7)**2
    
    return f

# Provide the problem configuration
design_variables = np.array([0.23, 0.97])   # Initial design variables
bounds_lower = np.array([0, 0])             # Lower bounds for design variables
bounds_upper = np.array([1, 1])             # Upper bounds for design variables
dp_tol = 1E-6                               # Minimum poll size stopping criteria
nitermax = 1000                             # Maximum objective function evaluations
dp = 0.1                                    # Initial poll size as percent of bounds
dm = 0.01                                   # Initial mesh size as percent of bounds

# Run the optimizer
orthomads(design_variables, bounds_upper, bounds_lower, objective_function, dp, dm, dp_tol, nitermax, True, True)