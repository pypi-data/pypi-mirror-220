import pandas as pd

# Example 1: No code smell - both usecols and dtype are explicitly set
data1 = pd.read_csv('data1.csv', usecols=['column1', 'column2'], dtype={'column1': 'float64', 'column2': 'int64'})

# Example 2: Code smell - usecols not explicitly set
data2 = pd.read_csv('data2.csv', dtype={'column1': 'float64', 'column2': 'int64'})

# Example 3: Code smell - dtype not explicitly set
data3 = pd.read_csv('data3.csv', usecols=['column1', 'column2'])

# Example 4: Code smell - both usecols and dtype not explicitly set
data4 = pd.read_csv('data4.csv')


def read_data(file_path, columns, dtypes):
    return pd.read_csv(file_path, usecols=columns, dtype=dtypes)


# Example 5: No code smell - columns and dtype passed through function parameters
data5 = read_data('data5.csv', ['column1', 'column2'], {'column1': 'float64', 'column2': 'int64'})


def read_data_without_dtype(file_path, columns):
    return pd.read_csv(file_path, usecols=columns)


# Example 6: Code smell - dtype not explicitly set, but usecols passed through function parameters
data6 = read_data_without_dtype('data6.csv', ['column1', 'column2'])


def read_data_with_dtype_inference(file_path, columns, dtypes=None):
    if dtypes is None:
        dtypes = {}
        for column in columns:
            dtypes[column] = 'float64'
    return pd.read_csv(file_path, usecols=columns, dtype=dtypes)


# Example 7: No code smell - columns and dtype inferred within the function
data7 = read_data_with_dtype_inference('data7.csv', ['column1', 'column2'])


# Example 8: No code smell - usecols and dtype set in a nested function call
def process_data(file_path):
    columns = ['column1', 'column2']
    dtypes = {'column1': 'float64', 'column2': 'int64'}
    return read_data(file_path, columns, dtypes)


data8 = process_data('data8.csv')


# Example 9: Code smell - usecols and dtype not set in a nested function call
def process_data_without_usecols_dtype(file_path):
    return pd.read_csv(file_path)


data9 = process_data_without_usecols_dtype('data9.csv')
