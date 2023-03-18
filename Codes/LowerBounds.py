import numpy as np    
from mst import MST

cost_matrix = [] # this is the cost_matrix of the graph that was used in Experiments
cost = 0 # this is taken from Experiments output

# 3. 1-TREE (MST) TO COMPARE ACCURACY OF SOLUTION
mst = MST(cost_matrix) 
parent = mst.primMST()
mst_cost = 0
for i in range(1, len(cost_matrix)):
    mst_cost += cost_matrix[i][parent[i]]

print(f'MST Cost (Lower Bound): {mst_cost}')
print(f'MST Performance Rate: {cost / mst_cost}')

# Improved Lower Bound with 1-Tree
one_tree_costs = []
for i in range(len(cost_matrix)):
    new_matrix = np.array(cost_matrix)
    new_matrix = np.delete(new_matrix, i, axis=0)   # Remove the i-th row
    new_matrix = np.delete(new_matrix, i, axis=1)   # Remove the i-th column
    mst = MST(new_matrix) 
    parent = mst.primMST()
    mst_cost = 0
    for j in range(1, len(new_matrix)):
        mst_cost += new_matrix[j][parent[j]]
    row_i = np.array(cost_matrix[i]) # costs from ith node to every other node
    row_i = np.delete(row_i, i) # diagonal element is excluded since it's 0 always
    pidx = np.argpartition(row_i, 2) # 3 first indexes correspond to the smallest elements
    closest = row_i[pidx[:2]] # we get the two closest distances to node i
    mst_cost += np.sum(closest) # we add this two our mst_cost (1-tree cost)
    one_tree_costs.append(mst_cost)

improved_lower_bound = np.max(one_tree_costs)

print(f'Max 1-Tree Cost (Improved Lower Bound): {improved_lower_bound}')
print(f'Max 1-Tree Performance Rate: {cost / improved_lower_bound}')  