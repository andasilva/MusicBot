#!/bin/sh

set -xe

pycodestyle AutomaBot
pydocstyle --add-ignore=D401 AutomaBot
isort --check-only --diff --recursive AutomaBot
flake8 AutomaBot
rstcheck README.rst
