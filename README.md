# Paper Builder

This repository contains a the build modules for the "paper" builder,a  simple docker container that can be run to recreate the Arkitekt Deployment that is illustratedin the original publication. 

# Usage

The intended usage of this builder, is inside a Konstruktor deployment,workflow, which will generate a "setup.yaml" that can be used withthis container.

## Dev Usage

```python
docker run -rm -v PATH_TO_SETUP_DIR_WITH_SETUP_YAML:/app/init python go.py
```


