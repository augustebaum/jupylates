### Conversion tests from cpp to jupyter

This repository contains some tests to automatically convert the C++
exercises from [info111](https://gitlab.dsi.universite-paris-saclay.fr/Info111/cpp-info111/-/tree/master/exercices_src)
into Jupyter Notebooks.

The notebookes are stored in [MyST](https://mystmd.org/) markdown format.
They can be translated in .ipynb format using [jupytext](https://jupytext.readthedocs.io/)
```
jupytext <name_of_the_notebook>.md --to ipynb
```

The notebooks are built to be graded via [nbgrader](https://nbgrader.readthedocs.io/),
once converted they can be validated via
```
nbgrader validate <name_of_the_notebook>.ipynb
```
