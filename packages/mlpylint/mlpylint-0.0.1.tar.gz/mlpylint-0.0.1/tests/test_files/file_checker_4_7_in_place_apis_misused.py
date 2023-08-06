import pandas as pd
import numpy as np

# Create a Pandas DataFrame with some missing values
data = {
    "A": [1, 2, np.nan, 4],
    "B": [5, np.nan, np.nan, 8],
    "C": [9, 10, 11, 12]
}
df = pd.DataFrame(data)

# Code Smell - Misuse of df.dropna(): Developer assumes it's an in-place operation and doesn't assign result to variable
df.dropna()

# The correct way to use df.dropna(): Assign the result to a variable or set the in-place parameter to True
df_clean = df.dropna()
# or
df.dropna(inplace=True)

# Create a NumPy array with some values
arr = np.array([1, 5, 3, -2, 0, 6])

# Code Smell - Misuse of np.clip(): Developer assumes it's an in-place operation and doesn't assign result to variable
np.clip(arr, 0, 4)

# The correct way to use np.clip(): Assign the result to a variable
clipped_arr = np.clip(arr, 0, 4)
