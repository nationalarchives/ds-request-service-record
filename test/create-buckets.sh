#!/usr/bin/env bash

set -euo pipefail

# Compatibility shim: keep existing CI/local command unchanged while delegating
# the real implementation to Python in the app container.
docker compose exec -T app poetry run python /app/test/create_buckets.py
