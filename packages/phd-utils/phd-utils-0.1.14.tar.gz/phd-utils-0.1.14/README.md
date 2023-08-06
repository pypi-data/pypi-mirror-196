# phd-utils

# to publish to pypi
python setup.py sdist 
twine upload dist/*

# to configure the pypi token
nano ~/.pypirc
then add the following:
[pypi]
username = __token__
password = <PyPI token>