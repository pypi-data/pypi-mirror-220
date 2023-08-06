from setuptools import setup
from setuptools import setup

setup(name= "Vpro",
      version= 0.27,
      description="This is a Machine Learning Module that grants one access to a Multilayer percepton with an adjustable number of hidden layers and neurons per each layer. It also includes functionality to train the network based on a database, and has adjustable innitialisation types, activation functions, and learning hyperparamters.", 
      author="Agastyaa Vishvanath",
      packages=["Vpro"],
      install_requires= ["numpy", "tqdm"])

