# SOLUTION.md — Monorepo & CI/CD Design

## Why **Pants** for Monorepo Management

- **Incremental builds out-of-the-box**: `--changed-since=<ref>` runs *only* affected tests/linters.
- **Hermetic, reproducible builds**: lockfile-based third‑party deps; deterministic PEX packaging (optional).
- **Dependency inference & graph awareness**: no hand-maintained requirements per module; fewer mistakes.
- **Unified developer UX**: one tool to run fmt, lint, test across the repo.
- **Scales**: As the monorepo grows (more services, libs, data jobs), Pants keeps CI fast via caching and invalidation.

Alternatives considered:
- **Poetry workspaces**: simple, but incremental builds and change detection would be DIY (paths-filter, Make scripts).
- **Bazel**: extremely performant but heavy to bootstrap for a small Python-only stack.
- **Nx**: great for JS; Python plugins exist but are less mature for the ML/py ecosystem.

Given Python microservices + shared library + need for incremental CI, **Pants** is the best fit.

---

## Dependency Resolution (Unified)

To avoid conflicts and ensure consistent behavior, both services share a single resolved set (see `3rdparty/python/requirements.txt`):
- `fastapi==0.110.2` (Pydantic v2 series)
- `pandas==2.2.2`
- `uvicorn[standard]==0.29.0`
- `scikit-learn==1.5.1`
- Test/lint stack is unified: `pytest`, `ruff`, `black`, `mypy`, etc.

> If a future service **must** pin a conflicting version (e.g., incompatible FastAPI), Pants also supports *multiple resolves* per target. For this assignment we keep a single, coherent set to reduce complexity and speed up CI.

---

## Shared Code Organization

Duplicated `utils/` is replaced by `libs/common_utils/`:
- `logging.py`: `setup_logging()` + `get_logger()` with a consistent format
- `validation.py`: shared Pydantic models (`RecordIn`, `RecordOut`)

Both services depend on `libs/common_utils` (see each service `BUILD`).

---

## Build Orchestration

- `pants.toml` enables Python backends (fmt/lint/test/typecheck, docker).
- `./pants fmt|lint|test ::` runs across the monorepo.
- `./pants --changed-since=<ref> test ::` focuses only on affected code.
- Optional `pex_binary` per service for packaging into a single-file executable.
- Dockerfiles are provided for both services (simple and predictable base images).

---

## Dev Workflow

- Local dev runs services with `uvicorn --reload` via `make run-dp` / `make run-ml`.
- Pre-commit hooks enforce style/quality quickly before pushing.
- Pants handles dependency inference and cache to make everyday tasks fast.

---

## Configuration Management

Centralized configs in the repo root:
- `pyproject.toml` for `black`, `isort`, `ruff`, `pytest`, `mypy`
- `.pre-commit-config.yaml` for local quality gates
- Single `requirements.txt` for unified deps
- Per-service `BUILD` files declare sources, tests, and binaries

Service-specific overrides can be added with per-directory `pyproject.toml` fragments if ever needed.

---

## CI/CD Pipeline (GitHub Actions)

**Goals:** fast feedback, minimal setup overhead, heavy reuse of caches, incremental execution.

### Key Techniques
- **Caching**: pip wheels (`~/.cache/pip`) + Pants cache (`~/.cache/pants`), keyed by lockfiles.
- **Incremental**: `./pants --changed-since=$(git merge-base origin/main HEAD)` to limit fmt/lint/test to affected targets.
- **Parallelism**: separate jobs for (lint/test) and (docker build). Additional test shard strategies can be enabled via Pants.
- **Pre-commit in CI**: ensures local and CI match.
- **Runner image optimization**: `.ci/Dockerfile` pre-installs Pants and the toolchain. Push to GHCR and set `jobs.<job>.container.image` to eliminate bootstrap time entirely.

### Local CI Simulation
`make ci` runs the same changed‑since logic. You can also use `act` if preferred; this workflow sticks to Actions-native steps for portability.

### Deployment Readiness
Dockerfiles are provided for both services. In production, add a publish step to push to a registry (e.g., GHCR). You can also switch to Pants‑built PEXes for *very* small runtime containers.

---

## Commands

```bash
# Bootstrap
python -m pip install --upgrade pip pipx
pipx install pantsbuild.pants==2.22.0
pip install -r 3rdparty/python/requirements.txt

# All repo
./pants fmt ::
./pants lint ::
./pants test ::

# Incremental (only changed targets vs main)
BASE_REF=$(git merge-base origin/main HEAD)
./pants fmt --changed-since="$BASE_REF" ::
./pants lint --changed-since="$BASE_REF" ::
./pants test --changed-since="$BASE_REF" ::

# Run locally
make run-dp   # http://localhost:8001/health
make run-ml   # http://localhost:8002/health
```

---

## Performance Expectations

With Pants caching + incremental invalidation:

- Re-run after tiny change in one service: **<~20–40s** typical on a medium laptop, dominated by test startup.
- First cold CI run: depends on wheel downloads; subsequent runs reuse caches, cutting minutes off.
- Compared to two isolated repos with separate pipelines, this monorepo avoids duplicated setup and test execution, and scales better as shared libs and services grow.

---

## Trade-offs / Future Enhancements

- If *strict* isolation is required, add **multiple resolves** (per‑service) and ensure `libs/common_utils` stays compatible with both or split libs as needed.
- Introduce **remote cache** for Pants (e.g., S3/GCS) to share build/test results across CI runners.
- Use **Pants docker_image** targets to produce images directly from PEXes for smaller, faster deploys.
- Add **schema/versioned contracts** in `common_utils` (e.g., via `pydantic` models) to enable evolving APIs without breakage.
