
source ./.venv/bin/activate
export PYTHONPATH="$(pwd)/src:${PYTHONPATH}"
fastapi dev ./src/main.py