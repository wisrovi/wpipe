# =============================================================================
# MAKEFILE TEMPLATE
# Copy to project root: cp references/makefile-template.mk Makefile
# =============================================================================

# Author: [Author]
# LinkedIn: https://[linkedin-url]

.PHONY: help install lint format security test clean docs run docker-build docker-run diagrams diagrams-render

# Variables
PYTHON := python3
PYTEST := pytest
PYLINT_ARGS := --disable=import-error,no-member,no-name-in-module
PYTEST_ARGS := --cov=. --cov-report=term-missing --cov-report=html --cov-branch -v
PROJECT_DIR := app
SKILL_DIR := .agents/skills/excalidraw-diagram/references

# =============================================================================
# HELP
# =============================================================================
help: ## Show this help message
	@echo ""
	@echo "========================================"
	@echo "  Project Makefile - Available Commands"
	@echo "========================================"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'
	@echo ""

# =============================================================================
# INSTALLATION
# =============================================================================
install: ## Install dependencies
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install -r requirements-dev.txt

# =============================================================================
# CODE QUALITY
# =============================================================================
lint: ## Run linters (pylint, target: ≥9.5)
	$(PYTHON) -m pylint $(PYLINT_ARGS) $(PROJECT_DIR)/

format: ## Format code (isort + black)
	isort $(PROJECT_DIR)/ tests/
	black $(PROJECT_DIR)/ tests/

security: ## Run security checks (bandit)
	bandit -r $(PROJECT_DIR)/

typecheck: ## Run type checking (mypy)
	mypy $(PROJECT_DIR)/

safety: ## Check dependencies for vulnerabilities
	safety check || true

# =============================================================================
# TESTING
# =============================================================================
test: ## Run tests with coverage (target: ≥85%)
	$(PYTEST) $(PYTEST_ARGS) tests/

test-unit: ## Run unit tests only
	$(PYTEST) tests/unit/ -v

test-integration: ## Run integration tests only
	$(PYTEST) tests/integration/ -v

# =============================================================================
# DIAGRAMS
# =============================================================================
diagrams: ## Create diagrams directory
	mkdir -p docs/diagrams

diagrams-render: diagrams ## Render all Excalidraw diagrams to PNG
	@echo "Rendering Excalidraw diagrams..."
	@for f in docs/diagrams/*.excalidraw; do \
		if [ -f "$$f" ]; then \
			name=$$(basename $$f .excalidraw); \
			echo "  Rendering $$name..."; \
			cd $(SKILL_DIR) && uv run python render_excalidraw.py ../../$$f --output ../../docs/diagrams/$$name.png --scale 2 && cd ../..; \
		fi \
	done
	@echo "Diagrams rendered successfully!"

# =============================================================================
# DOCKER
# =============================================================================
docker-build: ## Build Docker image
	docker build -t $(PROJECT_NAME):latest .

docker-run: ## Run Docker container
	docker run -p 8000:8000 --env-file .env $(PROJECT_NAME):latest

# =============================================================================
# DOCUMENTATION
# =============================================================================
docs: ## Build documentation
	cd docs && $(MAKE) html

docs-serve: ## Serve documentation locally
	cd docs && $(MAKE) html && $(PYTHON) -m http.server 8000 -d docs/_build/html

# =============================================================================
# CLEANING
# =============================================================================
clean: ## Clean temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -f .coverage
	rm -rf htmlcov/

clean-build: ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info/ .eggs/

clean-diagrams: ## Clean rendered diagram PNGs
	rm -f docs/diagrams/*.png

# =============================================================================
# RUN
# =============================================================================
run: ## Run the application
	$(PYTHON) -m $(PROJECT_DIR).main

# =============================================================================
# PRE-COMMIT
# =============================================================================
pre-commit: ## Run all checks before commit
	black --check $(PROJECT_DIR)/
	isort --check-only $(PROJECT_DIR)/
	mypy $(PROJECT_DIR)/
	bandit -r $(PROJECT_DIR)/

.DEFAULT_GOAL := help
