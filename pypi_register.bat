pushd "%~dp0"
python3 setup.py register -r pypi
python3 setup.py sdist upload -r pypi