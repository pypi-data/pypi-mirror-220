from es.atp.app0aeamp.lib.cor.jsonutils import *

import numpy as np

def printInfo(array):
    
    print(array)
    print()
    print("No. Dimension's: " + str(array.ndim))
    print("No. Shape's: " + str(array.shape))
    print()

createJsonFile()

print()
print(' -- NUMPY COURSE -- ')

plain_array_unidimensional = [1,2,3,4,5]

print()
print(plain_array_unidimensional)
print()
array_unidimiensional = np.array(plain_array_unidimensional)

printInfo(array_unidimiensional)

deleteJsonFile()