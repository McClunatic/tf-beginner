"""Simple train script.

See: https://www.tensorflow.org/tutorials/quickstart/beginner
"""

import sys

import tensorflow as tf


def train():
    """Trains a simple model against the MNIST dataset."""

    mnist = tf.keras.datasets.mnist

    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10),
    ])

    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

    model.compile(
        optimizer='adam',
        loss=loss_fn,
        metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=5)

    if len(sys.argv) > 1 and sys.argv[1] == 'comment':
        loss, accuracy = model.evaluate(x_test,  y_test)
        with open('comment.md', 'w') as md:
            md.write('## Training results \n\n')
            md.write('Summary of metrics for training on MNIST dataset: \n\n')
            md.write('| Statistic | Value |\n|--|--|\n')
            md.write(f'| loss | {loss} |\n')
            md.write(f'| accuracy | {accuracy} |\n')


if __name__ == '__main__':
    train()
