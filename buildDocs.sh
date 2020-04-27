find docs/rst/ ! -name 'index.rst' ! -name '.gitignore' -type f -exec rm -f {} +
export PYTHONPATH=$PYTHONPATH:$PWD/src
sphinx-apidoc -f -o docs/rst/ src/
sphinx-build -b html -c docs/ docs/rst/ docs/html/
