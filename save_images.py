"""Simple script to dump test MNIST images to ``images/``."""

import pathlib

import tensorflow as tf
from PIL import Image


def main():
    """Saves 100 test images to the ``images/`` directory."""

    images = pathlib.Path(__file__).parent.joinpath('images')
    images.mkdir(exist_ok=True)

    mnist = tf.keras.datasets.mnist
    (_, _), (x_test, _) = mnist.load_data()
    for i, arr in enumerate(x_test[:100]):
        Image.fromarray(arr).save(f'images/test_{i:02d}.jpg')


if __name__ == '__main__':
    main()
