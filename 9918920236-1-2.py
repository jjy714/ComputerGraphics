import numpy as np

# Questions 2 A ~ F

# A
M = np.arange(2, 27)
print(M)

# B
M2 = M.reshape(5, 5)
print(M2)

# C
for i in range(3):
    for j in range(3):
        M2[i + 1][j + 1] = 0
print(M2)

# D
M3 = np.arange(2, 27).reshape(5, 5)
powM3 = M3 @ M3
print(powM3)

# E
vector1 = powM3[0]
print(np.sqrt(vector1.dot(vector1)))
