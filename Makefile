.PHONY: up down logs e2e clean

# Start Docker Compose services, build images if necessary, and stream logs.
up:
	docker compose build --no-cache --pull
	docker compose up -d
	docker compose logs -f --tail=120

# Stop and remove Docker Compose services and their volumes.
down:
	docker compose down -v

# Stream the last 100 lines of Docker Compose logs.
logs:
	docker compose logs -f --tail=100

# Perform a basic end-to-end health check.
check_health:
	@for i in `seq 1 10`; do \
		curl -s http://localhost:8000/health && echo "Service is up!" && exit 0; \
		echo "Waiting for service to be up... (attempt $$i/10)"; \
		sleep 2; \
	done; \
	echo "Service did not become healthy within the timeout."; \
	exit 1

e2e: check_health

# Remove any build artifacts or temporary files.
clean:
	@echo "Cleaning up local build artifacts..."
	# Add commands here to remove specific files or directories, e.g.,
	 rm -rf node_modules build dist *.pyc