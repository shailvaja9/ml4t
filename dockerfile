# Use an official Ubuntu image as a parent image
# Use an official Miniconda base image
FROM continuumio/miniconda3:latest

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the environment.yml file into the container at /usr/src/app
COPY environment.yml ./

# Create the environment using the environment.yml file
RUN conda env create --file environment.yml

# Make RUN commands use the new environment
RUN echo "source activate ml4t" > ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Command to run on container start
CMD ["conda", "run", "-n", "ml4t", "python", "./marketism/marketism.py"]


