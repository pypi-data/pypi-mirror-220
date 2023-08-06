import tensorflow as tf


def correct_usage():
    tensor_array = tf.TensorArray(dtype=tf.float32, size=0, dynamic_size=True)

    for i in range(5):
        tensor_array = tensor_array.write(i, tf.constant(i, dtype=tf.float32))

    tensor_array = tensor_array.stack()


def code_smell_constant_update():
    constant_array = tf.constant([1, 2, 3, 4])

    for i in range(1, 5):
        constant_array += 1


def code_smell_constant_assign():   # Unable to smell
    constant_array = tf.constant([1, 2, 3, 4])

    for i in range(1, 5):
        constant_array = constant_array + 1


def code_smell_constant_while_loop():
    constant_array = tf.constant([1, 2, 3, 4])
    i = 0

    while i < 5:
        constant_array += 1
        i += 1


def no_code_smell_not_constant():
    variable_array = tf.Variable([1, 2, 3, 4])

    for i in range(1, 5):
        variable_array += 1
