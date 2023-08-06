python3.11 setup.py sdist

twine upload --repository dsutils_ms dist/dsutils_ms-1.1.tar.gz --verbose


pip3.11 install -e .

