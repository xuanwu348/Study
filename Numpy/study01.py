import numpy as np
import numpy.random as rand


#  Creating  a  100-element  array  with  random  values
#  from  a  standard  normal  distribution  or,  in  other
#  words,  a  Gaussian  distribution.
a = rand.randn(100)
print("------ value of a-------\n")
print(a)

#  Here  we  generate  an  index  for  filtering
#  out  undesired  elements.
index = a > 0.2
b = a[index]
print("index:{}----\nb:{}\n".format(index, b))

#  We  execute  some  operation  on  the  desired  elements.
b = b ** 2 - 2

#  Then  we  put  the  modified  elements  back  into  the
#  original  array.
a[index] = b
print("-----\na[index] %s" % a)

