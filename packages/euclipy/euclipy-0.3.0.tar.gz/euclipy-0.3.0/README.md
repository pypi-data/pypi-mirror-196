
# Euclipy

  

[![PyPI version](https://img.shields.io/pypi/v/euclipy.svg?color=dodgerblue&label=%20latest%20version)](https://pypi.org/project/euclipy/)

[![PyPI downloads](https://img.shields.io/pypi/dm/euclipy.svg?color=limegreen&label=PyPI%20downloads)](https://pypi.org/project/euclipy/)

  

### A library used to create, model, and solve figures in Euclidean Geometry.

## Features:

  

- Create symbolic geometric objects (Triangle(), Segment(), Angle(), etc.)

- Implicitly defines segments and angles created by polygon constructions

- Keeps a log of steps taken to prove distinct facts


![Sample Output](https://github.com/joshuavaron/euclipy/blob/main/tests/proof_output_framework.png?raw=true)

  

## Installation

```sh

# PyPi Installation

pip install euclipy

```

## Sample Code (With Comments):

```py

from euclipy.geometric_objects import Point

from euclipy.polygon import Triangle

from euclipy.theorems import isosceles_triangle_theorem

from euclipy.registry import Registry

  

if  __name__ == '__main__':

  

# Pretty print for registry

import pprint

pp = pprint.PrettyPrinter(indent=4)

  

# Define points

A = Point('A')

B = Point('B')

C = Point('C')

  

T1 = Triangle([A, B, C])

T2 = Triangle([B, C, A]) # Test for identity of two triangles expressed in different point

try:

T3 = Triangle([B, A, C]) # Test for inconsistent triangle

except:

print('Inconsistent triangle')

# Assign angle values

T1.angles[0].measure.value = 60

T1.angles[1].measure.value = 60

T1.angles[2].measure.value = 60

  

# Assign side values

T1.edges[2].measure.value = 1

  

# Apply theorem

theorem_applied = isosceles_triangle_theorem(T1)

  

# Print results

print(f'isosceles_triangle_theorem ran: {theorem_applied}')

  

# Print registry

pp.pprint(Registry().entries)

```
