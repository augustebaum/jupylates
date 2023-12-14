---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.15.2
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Why JuPylates

- integrates in the users's environment (for Jupyter-based courses)
- easy to deploy (at least for training purposes)
- easy to extend  
  writing an exercise is (almost) no harder than writing a Jupyter notebook
- harness the full power of Jupyter and the underlying open source scientific computing ecosystem
    - rich authoring, computational (and visualization?) tools
    - multilanguage
- lean (1k lines of code), modular, interoperable
- flexible learning record managment: can e.g. be used purely locally

+++

# Démo

+++

L'application, en mode examen, sur une liste d'exercices (ici tous les exercices dans le dossier `for`):

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
---
import glob
from jupyter_exercizer import Exerciser
Exerciser(glob.glob("for/*.md"), mode="exam")
```

L'application, en mode debug, sur une liste d'exercices classés par thèmes:

```{code-cell} ipython3
thèmes = {
    'Variables': 'variable/*.md',
    'Arithmétique': 'arithmetic/*.md',
    'Expressions booléennes': 'bool/*.md',
    'Conditionnelles': 'if/*.md',
    'Conditionnelles filées': 'elseif/*.md',
    'Boucles for': 'for/*.md',
    'Boucles for imbriquées': 'fornested/*.md',
    'Boucles while': 'while/*.md',
    'Prototypes de fonctions': 'function_prototype/*.md',
    'Tests de fonctions': 'function_test/*.md',
    'Flux et fichiers': 'stream/*.md',
    'Tous les thèmes': '*/*.md',
}
Exerciser({thème: glob.glob(f)
           for thème, f in thèmes.items()},
          mode="debug")
```

```{code-cell} ipython3

```