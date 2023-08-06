# Graph Partition and Measures

Python3 code implementing 11 graph-aware measures (gam) for comparing graph partitions as well as a stable ensemble-based graph partition algorithm (ecg) all for networkx.

## Graph aware measures (gam)

The measures are respectively:
* 'rand': the RAND index
* 'jaccard': the Jaccard index
* 'mn': pairwise similarity normalized with the mean function
* 'gmn': pairwise similarity normalized with the geometric mean function
* 'min': pairwise similarity normalized with the minimum function
* 'max': pairwise similarity normalized with the maximum function

Each measure can be adjusted (recommended) or not, except for 'jaccard'.
Details can be found in: 

Valérie Poulin and François Théberge, "Comparing Graph Clusterings: Set partition measures vs. Graph-aware measures", https://arxiv.org/abs/1806.11494.

## Ensemble clustering for graphs (ecg)

This is a good, stable graph partitioning algorithm. Details for ecg can be found in: 

Valérie Poulin and François Théberge, "Ensemble clustering for graphs: comparisons and applications", Appl Netw Sci 4, 51 (2019). 
    https://doi.org/10.1007/s41109-019-0162-z

# Example

First, we need to import the supplied Python file partition_networkx.

```python
import networkx as nx
import community ## this is the python-louvain package which can be pip installed 
import partition_networkx
import numpy as np
```

Next, let's build a graph with communities (dense subgraphs):

```python
# Graph generation with 10 communities of size 100
commSize = 100
numComm = 10
G = nx.generators.planted_partition_graph(l=numComm, k=commSize, p_in=0.1, p_out=0.02)
## store groud truth communities as 'iterables of sets of vertices'
true_comm = [set(list(range(commSize*i, commSize*(i+1)))) for i in range(numComm)]
```

run Louvain and ecg:

```python
ml = community.best_partition(G)
ec = community.ecg(G, ens_size=32)
```

We show a few examples of measures we can compute with gam:

```python
# for 'gam' partition are either iterables of sets of vertices or 'dict'
print("Adjusted Graph-Aware Rand Index for Louvain:",G.gam(true_comm, ml))
print("Adjusted Graph-Aware Rand Index for ecg:",G.gam(true_comm, ec.partition))

print("\nJaccard Graph-Aware for Louvain:",G.gam(true_comm, ml, method="jaccard",adjusted=False))
print("Jaccard Graph-Aware for ecg:",G.gam(true_comm, ec.partition, method="jaccard",adjusted=False))
```

Next, we compare with some non graph-aware measure (the adjusted Rand index); note that a different format is required for this function, so we build a dictionary for the partitions.

```python
## adjusted RAND index requires iterables over the vertices:
from sklearn.metrics import adjusted_rand_score as ARI
tc = {val:idx for idx,part in enumerate(true_comm) for val in part}

## compute ARI
print("Adjusted non-Graph-Aware Rand Index for Louvain:",ARI(list(tc.values()), list(ml.values())))
print("Adjusted non-Graph-Aware Rand Index for ecg:",ARI(list(tc.values()), list(ec.partition.values())))
```


