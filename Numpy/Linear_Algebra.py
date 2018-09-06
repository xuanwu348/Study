#_*_ encoding:utf-8 _*_
import numpy as np


"""
Some operations are easy and quick to do in linear algebra. A classic example is solving
a system of equations that we can express in matrix form:
    3x + 6y − 5z = 12
    x − 3y + 2z = −2
    5x − y + 4z = 10
    (2.1)

    
     3    6    −5     x      12
  [  1   −3     2 ] [ y ] = [ -2 ]
     5   −1     4     z       10

Now let us represent the matrix system as AX = B, and solve for the variables. This
means we should try to obtain X = A−1B. Here is how we would do this with NumPy
"""

A = np.matrix([[3, 6, -5],
              [1, -3, 2],
              [5, -1, 4]])
B = np.matrix([[12],
               [-2],
               [10]])
X = A ** (-1) * B
print(X)

"""
[[ 1.75]
 [ 1.75]
  [ 0.75]]
"""
#The same as below:
a = np.array([[3, 6, -5],
              [1, -3, 2],
              [5, -1, 4]])
b = np.array([12,-2,10])

#  Solving  for  the  variables,  where  we  invert  A
x = np.linalg.inv(a).dot(b)
print(x)


