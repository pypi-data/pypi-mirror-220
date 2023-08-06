import pandas as pd  # pandas imported

# Creating a simple DataFrame
df = pd.DataFrame({
    'A': ['foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo', 'foo'],
    'B': ['one', 'one', 'two', 'three', 'two', 'two', 'one', 'three'],
    'C': pd.np.random.randn(8),
    'D': pd.np.random.randn(8)
})

# Chain indexing examples
val = df['A']['B']  # Chain indexing, code smell
df['B']['A'] = 5  # Chain indexing for assignment, code smell
print(df['A']['B'])  # Chain indexing inside a function call, code smell

# Non-chain indexing examples
val = df.loc[:, 'A']  # Not chain indexing
df.loc[:, 'B'] = 5  # Not chain indexing
print(df.loc[:, 'A'])  # Not chain indexing

# More complex chain indexing examples
val = df[df['A'] == 'foo']['B']  # Chain indexing with boolean indexing, code smell
df[df['B'] == 'one']['C'] = 5  # Chain indexing for assignment with boolean indexing, code smell
print(df[df['A'] == 'bar']['B'])  # Chain indexing inside a function call with boolean indexing, code smell

# More complex non-chain indexing examples
print(df[df['A'] == 'bar'])  # Not chain indexing
