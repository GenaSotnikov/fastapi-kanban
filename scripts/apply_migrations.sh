set -e
export PYTHONPATH="$(pwd)/src:${PYTHONPATH}"

alembic upgrade head