import numpy
import numpy as np

# Correct usage of np.matmul() for matrix multiplication
matrix_a = np.array([[1, 2], [3, 4]])
matrix_b = numpy.array([[5.5, 6.6], [7.7, 8.8]])
result_matmul = np.matmul(matrix_a, matrix_b)
print("Result of np.matmul():\n", result_matmul)

# CODE SMELL: Incorrect usage of np.dot() for matrix multiplication
result_dot = np.dot(matrix_a, matrix_b)
print("Result of np.dot():\n", result_dot)

# Correct usage of np.dot() for dot product of vectors
vector_a = np.array([1, 2, 3])
vector_b = np.array([4, 5, 6])
result_dot_vector = np.dot(vector_a, vector_b)
print("Result of np.dot() for vectors:\n", result_dot_vector)

# Aliasing the numpy import with a different name:
import numpy as npy

# CODE SMELL: Incorrect usage of npy.dot() for matrix multiplication
matrix_c = npy.array([[9, 10], [11, 12]])
result_dot_alias = npy.dot(matrix_a, matrix_c)
print("Result of npy.dot():\n", result_dot_alias)


# Matrix multiplication in a function scope:
# NOTE: Usage of np.dot() for matrix multiplication in a function can potentially be a code smell, especially if the
# function's arguments are expected to be 2D matrices. However, due to the dynamic typing in Python and the lack of
# explicit type hints in this case, static code analysis tools might not be able to reliably detect this issue.
# Always prefer using np.matmul() for matrix multiplications to avoid confusion and potential errors.
def multiply_matrices(m1, m2):
    return np.dot(m1, m2)


result_function_scope = multiply_matrices(matrix_a, matrix_b)
print("Result from function scope:\n", result_function_scope)

# Multidimensional arrays with dimensions higher than 2:
matrix_d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
matrix_e = np.array([[[9, 10], [11, 12]], [[13, 14], [15, 16]]])
result_dot_multidimensional = np.dot(matrix_d, matrix_e)
print("Result of np.dot() on multidimensional arrays:\n", result_dot_multidimensional)

# Usage of np.dot() where one or both arguments are not numpy arrays:
result_dot_non_np = np.dot([1, 2, 3], [4, 5, 6])
print("Result of np.dot() on non-numpy arrays:\n", result_dot_non_np)
