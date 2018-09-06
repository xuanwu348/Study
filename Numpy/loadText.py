import numpy as np

table = np.loadtxt("example.txt", dtype={"names" : ("ID","Result","Type"), 'formats':("S4","f4","i2")})
print(table)
#[('xr21',  32.78900146, 1) ('xr22',  33.90999985, 2)]
print(table["ID"])
#['xr21' 'xr22']
