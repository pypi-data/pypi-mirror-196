## gemmi executable in a wheel

Packaging [gemmi](https://gemmi.readthedocs.io/en/latest/utils.html),
a command-line program from a crystallographic / structural biology project
also called [gemmi](https://gemmi.readthedocs.io/en/latest/utils.html),
as a python wheel that installable with pip.


### how to make wheels after gemmi release

* update `GIT_TAG` in CMakeLists.txt and `version` in pyproject.toml
* (optionally) update version of cibuildwheel in .github/workflows/wheels.yml
* test locally with `pip wheel .`
* make source distribution of this repo: `python -m build --sdist`
* build wheels in GitHub Actions
* download the wheels, check them, upload sdist and wheels to PyPI
