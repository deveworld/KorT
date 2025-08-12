.PHONY: format check requirements test

format:
	uvx ruff format .

check:
	uvx ruff check . --fix; \
	uvx ty check .; \
	uvx pyrefly check

requirements:
	uv export -o requirements.txt --without-hashes --without dev
	uv export -o requirements-dev.txt --without-hashes

test:
	uv run pytest -v
