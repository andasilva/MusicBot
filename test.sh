#!/bin/sh

set -xe

pycodestyle musicbot
pydocstyle --add-ignore=D401 musicbot
isort --check-only --diff --recursive musicbot
flake8 musicbot
