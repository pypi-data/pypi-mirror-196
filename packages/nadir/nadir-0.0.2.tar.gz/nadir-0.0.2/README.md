![NADIRbanner2](https://user-images.githubusercontent.com/11348086/221370644-fcc05274-eb99-4237-a270-60dafd5ab69d.png)

# Nadir


![PyPI - Downloads](https://img.shields.io/pypi/dm/nadir)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/Dawn-Of-Eve/nadir)
![GitHub Repo stars](https://img.shields.io/github/stars/Dawn-Of-Eve/nadir?style=social)
![Twitter Follow](https://img.shields.io/twitter/follow/dawnofevehq?style=social)

**Nadir** (pronounced _nay-di-ah_) is derived from the arabic word _nazir_, and means "the lowest point of a space". In optimisation problems, it is equivalent to the point of minimum. If you are a machine learning enthusiast, a data scientist or an AI practitioner, you know how important it is to use the best optimization algorithms to train your models. The purpose of this library is to help optimize machine learning models and enable them to reach the point of nadir in the appropriate context.

PyTorch is a popular machine learning framework that provides a flexible and efficient way of building and training deep neural networks. This library, Nadir, is built on top of PyTorch to provide high-performing general-purpose optimisation algorithms.  

:warning: ***Currently in Developement Beta version with every update having breaking changes; user discreation and caution advised!*** :warning:

## Supported Optimisers

| Optimiser 	| Paper 	                                            |
|:---------:	|:-----:	                                            |
|  **SGD**  	| https://paperswithcode.com/method/sgd                 |
|  **Momentum** | https://paperswithcode.com/method/sgd-with-momentum   |
|  **Adagrad** 	| https://www.jmlr.org/papers/volume12/duchi11a/duchi11a.pdf |
|  **RMSProp** 	| https://paperswithcode.com/method/rmsprop             |
|  **Adam**     | https://arxiv.org/abs/1412.6980v9                     |
|  **Adamax**   | https://arxiv.org/abs/1412.6980v9                     |
|  **Adadelta** | https://arxiv.org/abs/1212.5701v1                     |




## Installation

Nadir is on the PyPi packaging Index! :partying_face:

Simply run the following command on your terminal and start using Nadir now!

```bash
$ pip install nadir
```

## Usage

```python
import nadir as nd

# some model setup here...
model = ...

# set up your Nadir optimiser
config = nd.SGDConfig(lr=learning_rate)
optimizer = nd.SGD(model.parameters(), config)

```

