#!/usr/bin/env bash

# Unofficial bash strict mode thanks to http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail
IFS=$'\n\t'

source venv/bin/activate
export COMPOSE_PROFILE=develop
