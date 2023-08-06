import pandas as pd
import numpy as np

data = {
    "A": [1, 2, 3],
    "B": [4, 5, 6],
    "C": [7, 8, 9],
}

df = pd.DataFrame(data)
# Correct usage - df.to_numpy()
array1 = df.to_numpy()
print("Array1 (using to_numpy()):")
print(array1)

# Code smell - df.values
array2 = df.values
print("Array2 (using values):")
print(array2)

# Some other operations on the DataFrame
df["D"] = df["A"] + df["B"]
df["E"] = df["C"] - df["B"]

# Correct usage - df.to_numpy()
array3 = df.to_numpy()
print("Array3 (using to_numpy()):")
print(array3)

# Code smell - df.values
array4 = df.values
print("Array4 (using values):")
print(array4)
