import numpy as np

array = np.array([[2, 4, 9, 5, 8, 5]])

print(np.amax(array))
print("Hightest index:")
highest = np.where(array == np.amax(array))
print(highest)
print(highest[1][0])
