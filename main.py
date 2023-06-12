from BranchAndBound import BranchAndBound
from queue import Queue
from mip import *
import sys

queue = Queue()
root = BranchAndBound(filename=sys.argv[1])
queue.put(root)
z_p = float("-inf")

while queue.qsize():
    root = queue.get()
    status, z = root.solve()

    if status != OptimizationStatus.INFEASIBLE:
        integrality = root.check_integrality()
        if z > z_p:
            if integrality:
                z_p = z
                print(z)

            else:
                branch_var = root.find_closest_value()
                new_branch = BranchAndBound(model=root.model.copy())
                new_branch.add_restriction(branch_var, 0)
                queue.put(new_branch)
                new_branch = BranchAndBound(model=root.model.copy())
                new_branch.add_restriction(branch_var, 1)
                queue.put(new_branch)
