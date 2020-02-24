export PYTHONPATH=./src
sphinx-apidoc -f -o docs/rst/ src/
sphinx-build -b html -c docs/ docs/rst/ docs/html/
