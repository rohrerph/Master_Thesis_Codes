import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

# Create the range of AR values
ARs = np.arange(6, 40, 0.1)

# Create empty lists to store e and k values
e_values = []
k_values = []

# Calculate e and k values for each AR value and store them in the lists
for AR in ARs:
    e = 1.78*(1-0.045*AR**0.68)-0.64
    k = 1 / (math.pi * AR * e)
    e_values.append(e)
    k_values.append(k)

# Create a pandas DataFrame to store the e and k values
df = pd.DataFrame({'AR': ARs, 'e': e_values, 'k': k_values})

smallest_k = df['k'].min()
print('The smallest value of k is:', smallest_k)

# Plot k vs AR using matplotlib
plt.plot(df['AR'], df['k'])
plt.xlabel('AR')
plt.ylabel('k')
plt.title('k vs AR')
plt.show()

#smallest k appears to be at an aspect ratio of around 22-23 which is not possible due to structural limitations so what is the closest to it?


