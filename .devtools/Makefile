# Single entry point for local development. Run from the repo root with
#   make -C .devtools <target>
# CI runs the same hooks `check` runs, so local and CI results match.

ROOT := $(abspath ..)
UV := uv --project $(CURDIR)
PRE_COMMIT := $(UV) run pre-commit
PYTHON := $(UV) run --frozen python
# python.org Python builds on macOS ship without a CA bundle until "Install
# Certificates" is run; hook installs download toolchains over HTTPS, so fall back
# to certifi's bundle unless one is already configured.
export SSL_CERT_FILE ?= $(shell $(UV) run --frozen python -c 'import certifi; print(certifi.where())' 2>/dev/null)

.DEFAULT_GOAL := help
.PHONY: help setup lint validate build check scan lock clean

help: ## List targets
	@grep -hE '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Install pinned tools and git hooks (pre-commit, commit-msg, pre-push)
	$(UV) sync --frozen
	cd $(ROOT) && $(PRE_COMMIT) install --install-hooks \
		--hook-type pre-commit --hook-type commit-msg --hook-type pre-push

lint: ## Run every pre-commit hook on all files (includes validate)
	cd $(ROOT) && $(PRE_COMMIT) run --all-files

validate: ## Check every pack's layout, namespaces, JSON and references
	$(PYTHON) $(CURDIR)/scripts/check-packs.py

build: ## Package every pack into dist/ (PACK=<slug> for one)
	$(PYTHON) $(CURDIR)/scripts/build.py $(PACK)

check: lint build ## Everything CI runs, plus a build

scan: ## Secret and workflow security scans
	cd $(ROOT) && $(PRE_COMMIT) run gitleaks --all-files
	cd $(ROOT) && $(PRE_COMMIT) run zizmor --all-files

lock: ## Refresh uv.lock after changing a tool version in pyproject.toml
	$(UV) lock

clean: ## Remove build outputs
	rm -rf $(ROOT)/dist
