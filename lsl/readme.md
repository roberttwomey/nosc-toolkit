# Flow LSL Interface

A python interface for various devices to the [labstreaminglayer](https://github.com/sccn/labstreaminglayer). Developed for the Arthur C. Clarke Center for Human Imagination and the Center for Human Transformation.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system. This project currently targets windows.

### Software Setup on Windows

Install git (with git bash): [download](https://git-scm.com/download/win)

Install the latest release of Python for Windows [download](https://www.python.org/downloads/windows/)

When downloading Python, don't forget to check the box for "Add Python to environment variables".

In git bash, alias python to python.exe:

```
cd ~
touch .bashrc
echo "alias python='winpty python.exe'" >> .bashrc
```

Quit and restart git bash. Now you should be able to run python:
```
python
```
type ```exit()``` to quit.

Use pip to install a number of packages (including [pylsl](https://pypi.org/project/pylsl/#description)):

```
pip install pylsl
pip install numpy
pip install matplotlib
pip install python-opencv-contrib
pip install pillow
pip install python-osc
```

If you are unable to install python-opencv-contrib (for instance with 64 bit python), then you can install ```python-opencv``` instead.


## Using the programs

gui.py will only work if your recorded data includes reference webcam footage.

## Authors

* **Xianhai Cao** - *Initial work*

* **Robert Twomey** - *current work* - [github.com/roberttwomey](https://github.com/roberttwomey)
