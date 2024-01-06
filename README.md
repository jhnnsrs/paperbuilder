# Paper Builder

This repository contains a the build modules for the "paper" builder,a  simple docker container that can be run to recreate the Arkitekt Deployment that is illustratedin the original publication. 

## What is a Builder

Builders are compact Docker containers crafted to initialize projects, like the "Arkitekt"'s Docker Compose Project, within a specified directory. They primarily aim to simplify and abstract away the complexities associated with project configuration. This includes tasks such as managing secrets, dynamically mounting volumes, configuring services, and handling conditional setups.

# Usage

The Paper builder is primarily intended for use within a Konstruktor deployment workflow. This workflow generates a "setup.yaml" file, which is essential for this container's operation. An example setup file can be found
in the init directory.

## Dev Usage

```python
docker run --rm -v PATH_TO_SETUP_DIR_WITH_SETUP_YAML:/app/init .
```
Replace PATH_TO_SETUP_DIR_WITH_SETUP_YAML with the actual path to your setup directory containing the 'setup.yaml' file. This command initiates the Docker container and mounts the specified directory for initialization.




