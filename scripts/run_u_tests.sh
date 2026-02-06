export PYTHONPATH="$(pwd)/src:${PYTHONPATH}"

python3 -m unittest discover \
    -s tests/unit \
    -p "*.py" \
    -t "$(pwd)" \
    -v
