#!/usr/bin/env bash
set -euo pipefail

DEBUG="${DEBUG:-false}"
DEBUG="${DEBUG,,}"

run() {
  if [[ "$DEBUG" == "true" ]]; then
    echo "+ $*"
  fi

  "$@"
}

if [[ $# -ne 1 ]]; then
  echo "Error: MODE is required."
  echo "Usage: $0 {dev|prod}"
  exit 1
fi

MODE="${1,,}"

if [[ "$MODE" != "dev" && "$MODE" != "prod" ]]; then
  echo "Error: Invalid mode '$MODE'"
  echo "Usage: $0 {dev|prod}"
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker not found"
  exit 1
fi

SCRIPT_DIR="$(realpath "$(dirname "${BASH_SOURCE[0]}")")"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose.$MODE.yml"

if [[ ! -f "$COMPOSE_FILE" ]]; then
  echo "Compose file not found: $COMPOSE_FILE"
  exit 1
fi

COMPOSE_UP_ARGS=(
  -d
  --build
)

if [[ "$MODE" == "prod" ]]; then
  COMPOSE_UP_ARGS+=(
    --force-recreate
    --pull
    always
  )
fi

COMPOSE_ARGS=(
  compose
  --project-directory
  "$SCRIPT_DIR"
  -f
  "$COMPOSE_FILE"
  up
  "${COMPOSE_UP_ARGS[@]}"
)

run docker "${COMPOSE_ARGS[@]}"