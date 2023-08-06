import pandas as pd
import numpy as np
from pandas import DataFrame

# Creating a DataFrame
data = {'A': [1, 2, 3], 'B': [4, 5, 6], 'C': 1}
df = DataFrame(data=data, columns=['A', 'B', 'C'])
df1, df2 = DataFrame(data=data, columns=['D', 'E', 'F'])
df3 = pd.DataFrame(data=data, columns=['H', 'I', 'J'])
df4, df5 = pd.DataFrame(data=data, columns=['X', 'Y', 'Z'])
# bla = bla.DataFrame(data=data, columns=['T', 'S', 'K'])

# Usage of .assign() method to assign value
df = df.assign(B=0, T="")  # Code smell 1 (Note: B is already in DataFrame)
df = df.assign(S=0, V="")  # Code smell 2

df['A'] = ""  # No code smell - col A already exists in df
df['D'] = ""  # Code smell - empty column misinitialization of col D

val = ""
df['D'] = val  # Code smell

# # Multiple assignment in a single statement
# # Misinitializing new empty columns with zeros and empty strings
df['A'], df['G'], df['R'] = 10, "", 1  # Code smell 1

# # This line assigns an empty string to columns 'F', 'G', and 'C'
df['X'] = df['A'] = df['C'] = ""  # Code smell 1

# Correctly initializing a new empty column with NaN values
df['E'] = np.nan
