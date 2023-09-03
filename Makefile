#--- SETUP --------------------------------#

SHELL := /bin/bash

# print env vars
# $(foreach v, $(.VARIABLES), $(info $(v) = $($(v))))

# get all positional arguments passed to make (except the first one, i.e the
# target) and passed them as arguments to the target
RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
# ...and turn them into do-nothing targets
$(eval $(RUN_ARGS):;@:)

.PHONY: echo
echo:
	echo '-> ' $(RUN_ARGS)

.PHONY: format
format:
	isort api/
	black api/


#--- TEST --------------------------------#

.PHONY: run-test
run-test: stop clean
	docker compose -f docker/docker-compose.local.test.yml up -d
	docker compose -f docker/docker-compose.local.test.yml logs -f


#--- LOCAL -------------------------------#

.PHONY: build
build:
	docker compose -f docker/docker-compose.local.yml build
	docker compose -f docker/docker-compose.local.test.yml build

.PHONY: run
run:
	docker compose -f docker/docker-compose.local.yml up -d

.PHONY: logs
logs:
	docker compose -f docker/docker-compose.local.yml logs -f

.PHONY: logs-api
logs-api:
	docker compose -f docker/docker-compose.local.yml logs -f api

.PHONY: stop
stop:
	docker compose -f docker/docker-compose.local.test.yml down || true
	docker compose -f docker/docker-compose.local.yml down || true

.PHONY: stop-api
stop-api:
	docker compose -f docker/docker-compose.local.yml rm -svf api

.PHONY: restart
restart: stop run logs



#--- DB -------------------------------#

.PHONY: alembic-revision
alembic-revision:
	docker compose -f docker/docker-compose.local.yml exec api python -m alembic.config revision --autogenerate -m '$(RUN_ARGS)'

.PHONY: alembic-upgrade-head
alembic-upgrade-head:
	docker compose -f docker/docker-compose.local.yml exec api python -m alembic.config upgrade head

.PHONY: alembic-upgrade
alembic-upgrade:
	docker compose -f docker/docker-compose.local.yml exec api python -m alembic.config upgrade +1

.PHONY: alembic-downgrade-base
alembic-downgrade-base:
	docker compose -f docker/docker-compose.local.yml exec api python -m alembic.config downgrade base

.PHONY: alembic-downgrade
alembic-downgrade:
	docker compose -f docker/docker-compose.local.yml exec api python -m alembic.config downgrade -1

.PHONY: alembic-current
alembic-current:
	docker compose -f docker/docker-compose.local.yml exec api python -m alembic.config current

.PHONY: alembic-history
alembic-history:
	docker compose -f docker/docker-compose.local.yml exec api python -m alembic.config history


#--- CLI -----------------------------#
.PHONY: fetch
fetch:
	cd api && python -m cli episode fetch

.PHONY: prune
prune:
	cd api && python -m cli episode prune --all

.PHONY: prune-cache
prune-cache:
	cd api && python -m cli episode prune --cache

.PHONY: prune-database
prune-database:
	cd api && python -m cli episode prune --database


#--- TEARDOWN -----------------------------#

.PHONY: clean
clean: clean-files clean-volumes

.PHONY: clean-files
clean-files:
	find . \( -name __pycache__ -o -name "*.pyc" -o -name .pytest_cache -o -name .mypy_cache \) -exec rm -rf {} +

.PHONY: clean-volumes
clean-volumes:
	docker volume rm -f docker_local_postgres_data docker_local_test_postgres_data
	docker volume rm -f docker_prod_postgres_data docker_prod_test_postgres_data
