# https://www.w3schools.com/python/scipy/scipy_constants.php

import numpy as np
from scipy import constants
from scipy.sparse import csr_matrix


def print_underscore(text: str):
    print(f"\n{text}")
    line = "".join("-" for c in text)
    print(line)


print("List of all units in constants. Everything is in terms of SI units.")
print(dir(constants))

print("Return the specified unit in metres")
print(constants.yotta)  # 1e+24
print(constants.zetta)  # 1e+21
print(constants.exa)  # 1e+18
print(constants.peta)  # 1000000000000000.0
print(constants.tera)  # 1000000000000.0
print(constants.giga)  # 1000000000.0
print(constants.mega)  # 1000000.0
print(constants.kilo)  # 1000.0
print(constants.hecto)  # 100.0
print(constants.deka)  # 10.0
print(constants.deci)  # 0.1
print(constants.centi)  # 0.01
print(constants.milli)  # 0.001
print(constants.micro)  # 1e-06
print(constants.nano)  # 1e-09
print(constants.pico)  # 1e-12
print(constants.femto)  # 1e-15
print(constants.atto)  # 1e-18
print(constants.zepto)  # 1e-21

print()

print(constants.kibi)  # 1024
print(constants.mebi)  # 1048576
print(constants.gibi)  # 1073741824
print(constants.tebi)  # 1099511627776
print(constants.pebi)  # 1125899906842624
print(constants.exbi)  # 1152921504606846976
print(constants.zebi)  # 1180591620717411303424
print(constants.yobi)  # 1208925819614629174706176

# https://www.w3schools.com/python/scipy/scipy_sparse_data.php
from scipy.sparse import csr_matrix

print("\nSparse data")
arr = np.array([0, 0, 0, 0, 0, 1, 1, 0, 2])

print(csr_matrix(arr))
print("The 1st non-zero item is in row 0 position 5 and has the value 1.")

print_underscore("Sparse Matrix Methods")

arr = np.array([[0, 0, 0], [0, 0, 1], [1, 0, 2]])
print("\narr")
print(arr)
print("View non-zero data in csr_matrix")
print(csr_matrix(arr).data)

print("View csr matrix")
print(csr_matrix(arr))

print("Eliminating duplicates by adding them:")
mat = csr_matrix(arr)
mat.sum_duplicates()

print(mat)

print_underscore("Connected Components")
# --------------------------------------

from scipy.sparse.csgraph import connected_components

arr = np.array([[0, 1, 2], [1, 0, 0], [2, 0, 0]])

newarr = csr_matrix(arr)

print(connected_components(newarr))


print('\nFind the shortest path from element 1 to 2:')

from scipy.sparse.csgraph import dijkstra

arr = np.array([
  [0, 1, 2],
  [1, 0, 0],
  [2, 0, 0]
])

newarr = csr_matrix(arr)

print(dijkstra(newarr, return_predecessors=True, indices=0))

print_underscore('SciPy Spatial Data')
# https://www.w3schools.com/python/scipy/scipy_spatial_data.php

print_underscore('SciPy Interpolation')
# https://www.w3schools.com/python/scipy/scipy_interpolation.php
print('Covers imputation')

print('\nFind univariate spline interpolation for 2.1, 2.2... 2.9 for the following non linear points:')
from scipy.interpolate import UnivariateSpline

xs = np.arange(10)
ys = xs**2 + np.sin(xs) + 1
print('xs')
print(xs)
print('ys')
print(ys)
interp_func = UnivariateSpline(xs, ys)

newarr = interp_func(np.arange(2.1, 3, 0.1))
print('newarr')
print(newarr)