import pandas as pd

# Sample DataFrames
data1 = {'id': [1, 2, 3], 'name': ['A', 'B', 'C']}
data2 = {'id': [1, 2, 4], 'age': [30, 25, 22]}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Examples of merge operations
# Good examples (explicitly specify on, how, and validate parameters)
merged1 = df1.merge(df2, on='id', how='inner', validate='one_to_one')
merged2 = df1.merge(df2, on='id', how='left', validate='many_to_one')
merged3 = df1.merge(df2, on='id', how='right', validate='one_to_many')
merged4 = df1.merge(df2, on='id', how='outer', validate='many_to_many')

# Code Smell - Bad examples (using default parameters or not specifying all required parameters)
bad_merged1 = df1.merge(df2)  # Default parameters
bad_merged2 = df1.merge(df2, on='id')  # Missing how and validate
bad_merged3 = df1.merge(df2, how='inner')  # Missing on and validate
bad_merged4 = df1.merge(df2, validate='one_to_one')  # Missing on and how
