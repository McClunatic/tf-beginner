# Tensorflow Beginner

A simple demo of TensorFlow's Keras model API.

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
