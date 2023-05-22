# Tensorflow Beginner

A simple demo of TensorFlow's Keras model API.

## Python requirements

Install the following:

* `tensorflow`
* `mlem[streamlit,docker,fastapi]`

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

### Streamlit for serving

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

### Streamlit for deployment

The same Streamlit application can be deployed as a Docker container
running the following:

```sh
# If you're using Podman, set this and also patch
# mlem.contrib.docker.utils:create_docker_client to not override it
# I need to open an issue about this!
$ export DOCKER_HOST='unix:///run/user/1000/podman/podman.sock'
$ mlem deploy run docker_container docker.mlem \
    --model models/model \
    --server streamlit \
    --server.ui_port 8082 \
    --server.request_serializer pil_numpy \
    --ports.0 8082:8082 --ports.1 8081:8081
⏳️ Loading deployment from docker.mlem
⏳️ Loading model from models/model.mlem
🛠 Creating docker image mlem-deploy-1684781576
  💼 Adding model files...
  🛠 Generating dockerfile...
  💼 Adding sources...
  💼 Generating requirements file...
  🛠 Building docker image mlem-deploy-1684781576:latest...
  ✅  Built docker image mlem-deploy-1684781576:latest
✅  Container mlem-deploy-1684781985 is up
```

### Interacting with FastAPI backend

Below is a quick example for interacting with the backend. You
can check out the API documentation by visiting <http://localhost:8081>.

```python
>>> def ask_for(num: int):
...  payload = {'file': (f'test_{num:02d}.jpg', open(f'images/test_{num:02d}.jpg', 'rb'), 'image/jpeg')}
...  return requests.post('http://localhost:8081/__call__', files=payload).json()
>>> ask_for(15)
5
```

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
