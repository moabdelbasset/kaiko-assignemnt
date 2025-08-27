# Optional: a pre-baked CI image to speed up runs.
FROM python:3.11-slim
RUN python -m pip install --upgrade pip pipx
RUN pipx install pantsbuild.pants==2.22.0
RUN pip install pre-commit==3.7.0 ruff==0.5.0 black==24.4.2 isort==5.13.2 pytest==8.2.0
