from mip import *


class BranchAndBound(object):
    def __init__(
        self,
        model=None,
        filename=None,
    ):
        self.model = model
        if filename:
            model_data = self.read_file(filename)
            self.model = self.init_model(*model_data)
        self.model.verbose = 0

    def read_file(self, filename):
        with open(filename) as filename:
            restrictions = []
            vars_count, restrictions_count = filename.readline().strip().split(" ")
            vars_count = int(vars_count)
            restrictions_count = int(restrictions_count)
            coefficients = filename.readline().strip().split(" ")
            coefficients = list(map(int, coefficients))
            for line in filename.readlines():
                restrictions.append(list(map(int, line.strip().split(" "))))

        return (vars_count, restrictions_count, coefficients, restrictions)

    def init_model(self, vars_count, restrictions_count, coefficients, restrictions):
        model = Model(sense=MAXIMIZE, solver_name=CBC)
        x = [
            model.add_var(var_type=CONTINUOUS, name=f"x_{i}", lb=0, ub=1)
            for i in range(vars_count)
        ]

        model.objective = xsum(x[i] * coefficients[i] for i in range(len(coefficients)))
        for restriction in restrictions:
            coeff = restriction.pop(-1)
            model += (
                xsum(x[i] * restriction[i] for i in range(len(restriction))) <= coeff
            )
        return model

    def solve(self):
        status = self.model.optimize()

        return status, self.model.objective_value

    def find_closest_value(self):
        vars_values = {var: var.x for var in self.model.vars}
        break_var = min(vars_values.items(), key=lambda x: abs(x[1] - 0.5))
        return break_var[0]

    def add_restriction(self, var, value):
        self.model += var == value

    def check_integrality(self, epsilon=1e-6):
        # < epsilon >= 1- epsilon
        for v in self.model.vars:
            if v.x > epsilon and v.x <= 1 - epsilon:
                # if v.x % 1 != 0:
                return False

        return True
