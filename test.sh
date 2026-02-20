#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "==> Build wheel"
pip wheel . --no-build-isolation -w dist/

echo "==> Install wheel"
pip install dist/alayalite-*.whl --force-reinstall

echo "==> Install test dependencies"
pip install pytest pytest-asyncio pytest-cov httpx fastapi

echo "==> Run tests"
python -m pytest -v
