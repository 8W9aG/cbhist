#!/bin/sh

set -e

echo "Formatting..."
echo "--- Ruff ---"
ruff format cbhist
echo "--- isort ---"
isort cbhist

echo "Checking..."
echo "--- Flake8 ---"
flake8 cbhist
echo "--- pylint ---"
pylint cbhist
echo "--- mypy ---"
mypy cbhist
echo "--- Ruff ---"
ruff check cbhist
echo "--- pyright ---"
pyright cbhist
echo "--- pydocstyle ---"
pydocstyle cbhist
echo "--- bandit ---"
bandit -r cbhist
