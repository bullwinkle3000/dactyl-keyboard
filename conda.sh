#!/bin/bash

# exit on any errors
set -e

function inform() { echo -e "\n[INFO] $@\n"; }
function warn() { echo -e "\n[WARN] $@\n"; }
function error() { echo -e "\n[ERROR] $@\n"; }

# exit unless user responds with yes
function confirmContinue() {
  while true; do
    read -p "$@ [y/n]" yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit 0;;
        * ) error "Please answer yes or no.";;
    esac
  done
}

if ! which conda &> /dev/null; then
  error "Conda not found.\n\nVisit https://docs.anaconda.com/anaconda/install/index.html for more info."
  exit 1
fi

# Enable "conda activate" and "conda deactivate"
eval "$(conda shell.bash hook)"

envName=dactyl-keyboard

if [ "$1" = "--uninstall" ]; then
  confirmContinue "Would you like to remove the conda environment $envName?"
  conda deactivate
  conda env remove -n $envName
  inform "Conda environment removed!\n\n\tRun \"conda deactivate\" to ensure the environment has been properly deactivated."

  exit
fi

if conda info --envs | grep $envName &> /dev/null; then
  warn "Conda env \"$envName\" already exists."
  confirmContinue "Do you want to overwrite it?"
fi

inform "Creating conda environment: $envName..."

conda create --name=$envName python=3.8 -y

conda activate $envName

inform "Installing CadQuery..."

conda install -c conda-forge cadquery occt=7.7.0 -y

inform "Installing dataclasses-json..."

pip install dataclasses-json

inform "Installing numpy..."

pip install numpy

inform "Installing scipy..."

pip install scipy

inform "Installing solidpython..."

pip install solidpython

inform "Installing gitpython..."

pip install gitpython

inform "Updating conda dependencies..."

conda update --all -y

inform "Success!\n\n\tRun \"conda activate $envName\" to activate the environment."
