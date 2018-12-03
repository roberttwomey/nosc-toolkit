# Flow LSL Interface

A python interface for various devices to the [labstreaminglayer](https://github.com/sccn/labstreaminglayer). Developed for the Arthur C. Clarke Center for Human Imagination and the Center for Human Transformation.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system. This project currently targets windows.

### Software Setup on Windows

Install git (with git bash): [download](https://git-scm.com/download/win)

Install the latest release of Python for Windows [download](https://www.python.org/downloads/windows/)

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
```

If you are unable to install python-opencv-contrib (for instance with 64 bit python), then you can install ```python-opencv``` instead.


A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds


## Authors

* **Xianhai Cao** - *Initial work*

* **Robert Twomey** - *current work* - [github.com/roberttwomey](https://github.com/roberttwomey)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
