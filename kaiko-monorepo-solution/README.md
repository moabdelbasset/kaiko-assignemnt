# Kaiko Monorepo (Python / FastAPI / Pants)

This repository is a reference monorepo for two stateless services:

- `services/data_processor`: Data transformation API (FastAPI + pandas)
- `services/model_service`: Simple ML inference API (FastAPI + scikit-learn)

It uses **Pants** for monorepo orchestration (build, test, lint, package) and **GitHub Actions** for CI/CD.

## Quickstart

```bash
# 1) Install deps (one-off)
python -m pip install --upgrade pip pipx
pipx install pantsbuild.pants==2.22.0
pip install -r 3rdparty/python/requirements.txt

# 2) Run tests/lint across repo
./pants test ::
./pants lint ::

# 3) Run services locally
make run-dp   # http://localhost:8001
make run-ml   # http://localhost:8002
```

## Docker

```bash
make docker-dp
make docker-ml
```

## CI locally

```bash
make ci
```

See `SOLUTION.md` for rationale and trade-offs.
