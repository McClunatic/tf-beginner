# Tensorflow Beginner

A simple demo of TensorFlow's Keras model API.

## Using MLEM

The `train.py` script supports a `save` option to save the model to a
local `models/` directory:

```sh
$ python train.py save
$ ls models/
model model.mlem
```

To generate input for the model when served, run `save_images.py`:

```sh
python save_images.py
```

With input ready, serve the model with Streamlit!

```sh
mlem serve streamlit \
    --model models/model \
    --ui_port 8082 \
    --request_serializer pil_numpy
```

Here we specify the model to use, a UI port instead of the
[default special port 80](https://mlem.ai/doc/user-guide/serving/streamlit#running-streamlit-model-server-from-code), and a
serializer to convert the input images to numpy array format.

Once the app is up and running, visit the web site and try dragging
and dropping images from our `images/` directory!

## Running pipelines

This repository is centralized in Bitbucket Data Center with pipeline
support via integration with Jenkins.

### Bitbucket integration

A *Project link* (see Project configuration page) is established between
Bitbucket and Jenkins to allow Jenkins to interact directly with Bitbucket
for the containing Bitbucket Project.

### Jenkins integration

The Atlassian official Bitbucket plugin is configured to watch this repository
with the following triggers:

* Pull request opened or source branch updated

### Commenting

The `comment.py` script is integrated with the `Jenkinsfile` pipeline to
enable adding simple comments associated pull requests when executed in the
scope of pull request continuous integration.

For example:

```shell
# Add comments written inline
python comment.py --comment "This is a smart and important comment."
# Add comments from `comment.md` files generated from `train.py`
python comment.py --file comment.md
```
