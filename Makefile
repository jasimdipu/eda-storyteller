.PHONY: up down logs check_health e2e clean rebuild

# Start services (build + run + tail logs until healthy)
up: rebuild run logs

# Build images without using cache and pulling latest
rebuild:
	docker compose build --no-cache --pull

# Run services in detached mode
run:
	docker compose up -d

# Stop and remove all services and volumes
down:
	docker compose down -v

# Stream the last 120 lines of logs
logs:
	docker compose logs -f --tail=120

# Health check (wait until service responds OK on /health)
check_health:
	@echo "Checking service health..."
	@for i in `seq 1 15`; do \
		if curl -s http://localhost:8000/health | grep -q "ok"; then \
			echo "✅ Service is healthy!"; \
			exit 0; \
		fi; \
		echo "⏳ Waiting for service to be healthy... (attempt $$i/15)"; \
		sleep 2; \
	done; \
	echo "❌ Service did not become healthy within the timeout."; \
	exit 1

# End-to-end check (depends on health check)
e2e: check_health

# Clean up local build artifacts
clean:
	@echo "🧹 Cleaning up local build artifacts..."
	rm -rf node_modules build dist *.pyc __pycache__

