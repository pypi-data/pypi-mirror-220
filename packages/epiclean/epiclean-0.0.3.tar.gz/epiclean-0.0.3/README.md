# epiclean

This is the package for the module clean_epigraphia at https://github.com/ShreyasKolpe/epigraphia-data-cleaning/tree/main/automation

Find it on PyPi at https://pypi.org/project/epiclean/

Instructions for Python packaging: https://packaging.python.org/en/latest/

Summarizing these instructions:

* Change source code in `src/` directory
* Make sure to have the latest build package with
```python3 -m pip install --upgrade build```
* From the directory where `pyproject.toml` is located, run
```python3 -m build```
* The `.tar.gz` and `.whl` files are generated in the `dist/` directory. These need to be uploaded to the PyPi distribution
* First, update twine with
```python3 -m pip install --upgrade twine```
* Then, run
```python3 -m twine upload dist/*```