ESA Planning Timeline Request (PTR) Python package
==================================================
<img src="https://esa-ptr.readthedocs.io/en/1.3/_static/ptr-logo.svg" align="right" hspace="50" vspace="50" height="100" alt="ESA PTR logo">

Since the [Rosetta mission](https://www.esa.int/Science_Exploration/Space_Science/Rosetta),
ESA developed an XML-like syntax to create Planning Timeline Request (PTR) files.
These files allow the mission team member to design custom attitude spacecraft pointing.
It is readable by `AGM` and `MAPPS` softwares to detect spacecraft constrains violations,
power conception and surface coverage. It can also be used to compute custom spacecraft
attitude: quaterions, camera kernels (`ck`) and resolved PTR.
This format is used for the [JUICE mission](https://sci.esa.int/web/juice),
and can be tested on the [JUICE pointing tool](https://juicept.esac.esa.int).

This python package implements an object oriented approach to help the creation and parsing
of PTR files for the user, as well an interface to check JUICE PTR validity with AGM.

> 🚧 **Disclaimer:** This package is in beta stage and does not support all PTR implementations.
> Please, open an issue to report any issue you may accounter.
> ⚠️ Currently this tool in **beta stage**, **do not** use it in critical environments.

📚 Documentation
----------------
A detailed documentation can be found here: [esa-ptr.readthedocs.io](https://esa-ptr.readthedocs.io/)

🐍 Installation
---------------

This package is available on [PyPI](https://pypi.org/project/esa-ptr/) and could be installed with the python package manager `pip`:

```bash
python -m pip install esa-ptr
```

Even if this tool does not have any external dependencies, we recommend to use it in an isolated virtual environment (`venv` or `conda env`).


🐛 Development and testing
--------------------------

If you want to contribute to the development and tests your changes before submitting a merge request,
you need to install [Poetry](https://python-poetry.org/docs/) and clone this repository:

```bash
git clone https://juigitlab.esac.esa.int/python/ptr.git esa-ptr ;
cd esa-ptr/
```

Install the package and its dependencies:
```
poetry install
```

Then, after your edits, you need to check that both linters are happy:
```bash
poetry run flake8
poetry run pylint src tests
```

and all the tests passed:
```bash
poetry run pytest
```

🎓 Ressources
-------------
* Rosetta Flight Dynamics: `RO-ESC-IF-5501_i3r4_RSGS_FD_ICD-2.pdf`
