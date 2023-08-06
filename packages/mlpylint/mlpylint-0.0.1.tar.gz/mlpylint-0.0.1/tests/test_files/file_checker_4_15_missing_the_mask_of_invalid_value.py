import tensorflow as tf


def main():
    x = tf.constant([0.0, 1.0, 2.0, 3.0, 4.0])

    # Proper masking (no code smell)
    masked_log_x = tf.math.log(tf.clip_by_value(x, 1e-10, 1.0))
    print("Masked log output:", masked_log_x.numpy())

    # Code smell - Missing masking
    unmasked_log_x = tf.math.log(x)

    # Code smell - Missing masking with keyword
    unmasked_log = tf.math.log(x=x, name="bla")

    # Proper masking (no code smell)
    masked_log_x = tf.math.log(x=tf.clip_by_value(x, 1e-10, 1.0))

    print("Unmasked log output:", unmasked_log_x.numpy())


if __name__ == "__main__":
    main()
