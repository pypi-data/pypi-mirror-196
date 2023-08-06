# Python project boiler plate

This project aims to make the building, and deployment of python packages and docker containers using OneDev as simple as possible.

## Features

- publish to DockerHub
- publish to pypi
- sync with GitHub

## TODO
 
 - add shields.io
 - branch protection settings setup

## How to Setup

- Make a new OneDev repository and copy the contents of this repository into it. 
- Update the following values in setup.py:
    - name   
        - **note: this sets the name used on DockerHub, PyPI, and GitHub**
    - version
    - description
    - author
    - license
    - classifiers
    - install requires
    - extras_require
- Update the docker file:
    - add your contact info to the `MAINTAINER` line
    - `CMD` to whatever command starts your app
- Create a Repository on GitHub with the same name as your OneDev project
- In OneDev:
    - Edit step templates in the `.onedev-buildspec.yaml` file::
        - Execute tests:Run Pytest:
            - add command to run test suite(s) if not pytest
        - Publish Docker Container to Dockerhub: publish to dockerhub:
            - update username to your dockerhub username
    - Under `Settings > Build > Job Secrets` add
      - your DockerHub password as `dockerhub_password`
      - your DockerHub password as `dockerhub_user`
      - your PyPI password as `pypi_password`
      - your PyPI user as `pypi_user`
      - your GitHub user as `github_user`
      - your [GitHub token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) as `github_token`
    - If there isn't already, make a 'Server Docker Executor' called `docker-executor` under `Administration > Job Executors`
- fill in your `README.md` and remove this section

## Contibuting

Contributions are welcome, this project is developed at [dev.doze.dev](https://dev.doze.dev/onedev-python-project-boilerplate/) where you can submit issues and open pull requests.

----

# My Project

Describe what your package is about

## Package Distribution

### Installation

`pip install my-project`

### Use

`python ./src/main.py`

## Docker Distibution

### Installation

`docker pull docker_user/project_name:latest`

### Use

`docker run -p 5000:5000 project_name`

or for detached mode:

`docker run -d -p 5000:5000 project_name`

