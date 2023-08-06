from cloud_geodesic import FastMarchingTree
import numpy as np
import matplotlib.pyplot as plt
from sklearn import manifold, datasets

X, _ = datasets.make_swiss_roll(n_samples=10000, random_state=0)
idx = np.argmax(X[:, 2])
X[0] = X[idx]

tree = FastMarchingTree(X.tolist(), 1)
tree.span_tree();

idx_dst = np.argmin(X[:, 2])
path = tree.get_geodesic_path(idx_dst)
costs = tree.get_costs()

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=costs, s=1)
ax.scatter(path[:, 0], path[:, 1], path[:, 2], c="red", s=20)
plt.show()
