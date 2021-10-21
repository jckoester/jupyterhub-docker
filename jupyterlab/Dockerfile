FROM jupyter/scipy-notebook:latest

LABEL maintainer="Jan Köster <https://www.gymnasium-ditzingen.de/>"

USER root

# APT packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-dejavu \
    tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER $NB_UID

# RUN pip install \
    # jupyterlab-language-pack-de-DE

# Conda installs
RUN conda install --quiet --yes \
    jupyterhub \
    jupyterlab
# Install German language pack for jupyterlab
RUN conda install -c conda-forge jupyterlab-language-pack-de-DE


# We create a complete environment for chatterbot, it will appear in jupyterlab as a separate notebook type
# That way we can add different environments later without dependecy problems!


# Create a conda/python environment for chatterbot as it requires python 3.7
RUN conda create -n chatterbot_py37 --yes python=3.7
# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "chatterbot_py37", "/bin/bash", "-c"]
# Install chatterbot and spacy 2.3.5 (as chatterbot 1.0.8 is incompatible with spacy 3.x)
RUN pip install \
     chatterbot \
     chatterbot-corpus \
     spacy==2.3.5
# Install spacy language models
RUN  python -m spacy download en
RUN  python -m spacy download de

# Install ipykernel
RUN conda install --quiet --yes \
    ipykernel
# and create the new environment for jupyterlab
RUN python -m ipykernel install --user --name chatterbot_py37 --display-name="Chatterbot (Python 3.7)"

# Add hook to load environments
COPY ./activate_envs.sh /usr/local/bin/before-notebook.d/