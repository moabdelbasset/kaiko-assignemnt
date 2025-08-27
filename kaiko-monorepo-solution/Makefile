.PHONY: bootstrap fmt lint typecheck test run-dp run-ml precommit docker-dp docker-ml ci

bootstrap:
	python -m pip install --upgrade pip pipx
	pipx install pantsbuild.pants==2.22.0 || true
	pip install -r 3rdparty/python/requirements.txt

fmt:
	./pants fmt ::

lint:
	./pants lint ::

typecheck:
	./pants typecheck ::

test:
	./pants test ::

# Run services locally (development)
run-dp:
	uvicorn services.data_processor.app.main:app --host 0.0.0.0 --port 8001 --reload

run-ml:
	uvicorn services.model_service.app.main:app --host 0.0.0.0 --port 8002 --reload

precommit:
	pre-commit install
	pre-commit run --all-files

docker-dp:
	docker build -f docker/data_processor.Dockerfile -t data-processor:dev .

docker-ml:
	docker build -f docker/model_service.Dockerfile -t model-service:dev .

ci:
	bash scripts/ci_local.sh
