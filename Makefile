# Start the development environment
start-dev:
	docker-compose -f docker-compose.dev.yml up --build

# Start the production environment
start:
	docker-compose -f docker-compose.yml up --build

# Stop and remove containers, networks, images, and volumes
clean:
	docker-compose down -v

# Show help information
help:
	@echo "Usage:"
	@echo "  make start-dev   # Start the development environment"
	@echo "  make start       # Start the production environment"
	@echo "  make clean       # Stop and remove containers, networks, images, and volumes"

.PHONY: start-dev start clean help