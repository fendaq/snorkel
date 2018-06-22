FROM continuumio/anaconda

RUN apt-get update -y
RUN apt-get install --reinstall build-essential -y
RUN apt-get install libgl1-mesa-glx -y

RUN conda install --yes numpy scipy matplotlib pip
RUN conda install --yes numba

COPY python-package-requirement.txt .
RUN pip install -r python-package-requirement.txt