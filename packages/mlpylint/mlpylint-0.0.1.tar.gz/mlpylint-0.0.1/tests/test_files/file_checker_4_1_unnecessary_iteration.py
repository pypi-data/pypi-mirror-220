import numpy as np
import pandas as pd
import tensorflow as tf

# create a pandas dataframe
df = pd.DataFrame({
    'A': np.random.rand(10),
    'B': np.random.rand(10),
    'C': np.random.rand(10),
})

# Unnecessary pandas iteration with a for loop
for index, row in df.iterrows():  # CODE SMELL
    df.loc[index, 'A'] = row['A'] + row['B']
# Code smell: Looping through pandas DataFrame using iterrows is inefficient
# Suggested improvement:
df['A'] = df['A'] + df['B']  # Vectorized operation, much more efficient

for i in df.index:  # CODE SMELL
    df.loc[i, 'C'] = df.loc[i, 'A'] * df.loc[i, 'B']
# Code smell: Looping through pandas DataFrame using index is inefficient
# Suggested improvement:
df['C'] = df['A'] * df['B']  # Vectorized operation, much more efficient

# Unnecessary pandas iteration with a while loop
i = 0
while i < len(df):  # CODE SMELL
    df.loc[i, 'B'] = df.loc[i, 'A'] * 2
    i += 1
# Code smell: Looping through pandas DataFrame using while loop is inefficient
# Suggested improvement:
df['B'] = df['A'] * 2  # Vectorized operation, much more efficient

# create a tensorflow tensor
tensor = tf.constant([[1, 2], [3, 4]])  # Unable to infer variable after assignment

# Unnecessary tensorflow iteration with a for loop
output_tensor_for = tf.Variable(tf.zeros(tensor.shape))
for i in range(tensor.shape[0]):  # UNABLE TO DETECT CODE SMELL
    for j in range(tensor.shape[1]):
        output_tensor_for[i, j].assign(tensor[i, j] + 1)
# Code smell: Looping through TensorFlow tensors is inefficient
# Suggested improvement:
output_tensor_for = tensor + 1  # Vectorized operation, much more efficient

# Unnecessary tensorflow iteration with a while loop
output_tensor_while = tf.Variable(tf.zeros(tensor.shape))
i = tf.constant(0)
while i < tf.constant([[1, 2], [3, 4]]).shape[0]:  # CODE SMELL
    j = tf.constant(0)
    while j < tensor.shape[1]:
        output_tensor_while[i, j].assign(tensor[i, j] + 2)
        j += 1
    i += 1
# Code smell: Looping through TensorFlow tensors using while loop is inefficient
# Suggested improvement:
output_tensor_while = tensor + 2  # Vectorized operation, much more efficient

print(df)
print(output_tensor_for)
print(output_tensor_while)
