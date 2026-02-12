#!/bin/bash
# Set base directory to script location
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$BASE_DIR"

source venv/bin/activate
# load .env and export variables
if [ -f .env ]; then
  set -o allexport
  . .env
  set +o allexport
fi

python3 src/run.py --config config_models --max-items 10 >> models.log 2>&1
