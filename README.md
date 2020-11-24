# FlappyBird GANN

### General
**FlappyBird-GANN** (Flappy Bird - Genetic Algorithm Neural Network) is application based on Python 3.8. 

The settings window made using **PyQt5**, where we can configure variables that affect the gameplay and the Genetic Algorithm.
The game itself is based on the PyGame library. 
All variables contains in **Data.рy** file.

### Neural Network (NN)
Each bird has its own **.npy** files containing weight coefficients.
The input of the neural network receives the normalized values distanse from bird to:
* Nearest top and bottom towers (on X Axis)
* Nearest top tower (on Y Axis)
* Nearest bottom tower (on Y Axis)

### Genetic Algorithm (GA)
A Genetic Algorithm is a class that contains 2 main functions:
* **Cross(*father, mother*)** - Сrossing between 2 individuals
* **New_Generation(*all_population*)** - Creation of new generation

And 1 auxiliary:
* **Save_Weights(*folder, inp_hid_weights, hid_out_weights*)** - Saves the weights coefficients to the appropriate folder

***
### Tech

Application uses a number of python libraries:

* **[NumPy](https://numpy.org/install/)** - is the fundamental package needed for scientific computing with Python
* **[SciPy](https://www.scipy.org/install.html)** - is a free and open-source Python library used for scientific computing and technical computing
* **[PyGame](https://pypi.org/project/pygame/)** - is a cross-platform set of Python modules designed for writing video games
* **[PyQt5](https://pypi.org/project/PyQt5/)** - is a Python binding of the cross-platform GUI toolkit Qt, implemented as a Python plug-in.


### Installation

This application requires [Python](https://www.python.org/downloads/release/python-380/) 3.8 to run.


```sh
pip install numpy
pip install scipy
pip install pygame
pip install PyQt5
```
You can also install [PyCharm (Community edition)](https://www.jetbrains.com/pycharm/download/#section=windows), because it is quite convenient to work with the Python language

