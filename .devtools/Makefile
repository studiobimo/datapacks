include base.mk

PYTHON := $(UV) run --frozen python

.PHONY: validate build check lock clean

validate: ## Check every pack's layout, namespaces, JSON and references
	$(PYTHON) $(CURDIR)/scripts/check-packs.py

build: ## Package every pack into dist/ (PACK=<slug> for one)
	$(PYTHON) $(CURDIR)/scripts/build.py $(PACK)

check: lint build ## Everything CI runs (lint includes validate), plus a build

lock: lock-tools ## Refresh every lockfile after a version change

clean: ## Remove build outputs
	rm -rf $(ROOT)/dist
