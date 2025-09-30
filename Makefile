.PHONY: dev
dev:
	pip install -e .[dev,test]

.PHONY: install
install:
	pip install -e .

.PHONY: test
test:
	pytest .

.PHONY: clean
clean:
	find src/ -name "__pycache__" | xargs rm -r
	rm -r ./build/

.PHONY: install_precommit_hooks
install_precommit_hooks:
	pip install pre-commit
	pre-commit install
