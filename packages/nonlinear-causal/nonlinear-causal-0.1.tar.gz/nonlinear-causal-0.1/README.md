![Pypi](https://badge.fury.io/py/nl-causal.svg)
[![Python](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/)
[![MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- [![Youtube](https://img.shields.io/badge/YouTube-Channel-red)]()
![Downloads](https://static.pepy.tech/badge/nl-causal)
![MonthDownloads](https://pepy.tech/badge/nl-causal/month)
[![Conda](https://img.shields.io/conda/vn/conda-forge/???.svg)]() -->
<!-- [![image](https://pepy.tech/badge/leafmap)](https://pepy.tech/project/leafmap) -->
<!-- [![image](https://github.com/giswqs/leafmap/workflows/build/badge.svg)](https://github.com/giswqs/leafmap/actions?query=workflow%3Abuild) -->

# 🧬 nonlinear-causal

<!-- <img style="float: left; max-width: 10%" src="./logo/logo_transparent.png"> -->

![logo](./logo/logo_cover_transparent.png)

**nonlinear-causal** is a Python module for nonlinear causal inference, including **hypothesis testing** and **confidence interval** for causal effect, built on top of two-stage methods. 

- GitHub repo: [https://github.com/nl-causal/nonlinear-causal](https://github.com/nl-causal/nonlinear-causal)
<!-- - Documentation: [https://nonlinear-causal.readthedocs.io](https://nonlinear-causal.readthedocs.io/en/latest/) -->
- PyPi: [https://pypi.org/project/nl-causal](https://pypi.org/project/nonlinear-causal)
- Open Source: [MIT license](https://opensource.org/licenses/MIT)
<!-- - Paper: [pdf]() -->


<!-- <script type="text/javascript" charset="utf-8" 
src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML,
https://vincenttam.github.io/javascripts/MathJaxLocal.js"></script> -->

The proposed model is:
![model](.figs/../logo/nl_causal.png)

<p align="center">
<img src="https://latex.codecogs.com/svg.image?{\centering&space;\color{RedOrange}&space;\phi(x)&space;=&space;\mathbf{z}^\prime&space;\boldsymbol{\theta}&space;&plus;&space;w,&space;\quad&space;y&space;=&space;\beta&space;\phi(x)&space;&plus;&space;\mathbf{z}^\prime&space;\boldsymbol{\alpha}&space;&plus;&space;\epsilon}"" width="350">
</p>

<!-- $$
\phi(x) = \mathbf{z}^\prime \mathbf{\theta} + w, \quad y = \beta \phi(x) + \mathbf{z}^\prime \mathbf{\alpha} + \epsilon
$$ -->

- <img src="https://latex.codecogs.com/svg.image?\color{RedOrange}&space;\beta" title="\color{RedOrange} \beta" />: marginal causal effect from X -> Y;
- <img src="https://latex.codecogs.com/svg.image?\color{RedOrange}&space;\phi(\cdot)" tilte="\phi"/>: nonlinear causal link;

<!-- ![logo](./logo/model_black.gif) -->


## What We Can Do:
- Estimate <img src="https://latex.codecogs.com/svg.image?\color{RedOrange}&space;\theta" title="\color{RedOrange} \theta" /> and <img src="https://latex.codecogs.com/svg.image?\color{RedOrange}&space;\beta" title="\color{RedOrange} \beta" />.
- Hypothesis testing (HT) and confidence interval (CI) for marginal causal effect $\beta$.
- Estimate nonlinear causal link <img src="https://latex.codecogs.com/svg.image?\color{RedOrange}&space;\phi(\cdot)" tilte="\phi"/>.


## Installation

### Dependencies

`nonlinear-causal` requires:

| | | | | | |
|-|-|-|-|-|-|
| Python>=3.8 | numpy | pandas | sklearn | scipy | sliced |

### User installation

Install `nonlinear-causal` using ``pip``

```bash
pip install nl_causal
pip install git+https://github.com/nl-causal/nonlinear-causal
```
### Source code

You can check the latest sources with the command::

```bash
git clone https://github.com/nl-causal/nonlinear-causal
```

## Examples and notebooks

- [User Guide](user_guide.md)

- [Simulation for HT and CI with standard setup](sim_main.ipynb)
- [Simulation for HT and CI with invalid IVs](sim_invalid_IVS.ipynb)
- [Simulation for HT and CI with categorical IVs](sim_cate.ipynb)
- [Real application](app_test.ipynb)
<!-- - [Pipeline for plink data](user_guide.md) -->