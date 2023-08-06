#!/usr/bin/env

deactivate
pyenv shell 3.8.10
rmvirtualenv margo-parser-py-3.8.10
mkvirtualenv margo-parser-py-3.8.10
pip install -r requirements-dev.txt
tox