# 환경 설정
uv를 사용합니다.

```
uv sync && source .venv/bin/activate
```

# 포매팅
isort, ruff (black), ty, pyrefly를 사용합니다. uvx를 사용하여 실행가능합니다.

```
uvx isort --profile black -l 120 . && uvx ruff format .
uvx ruff check
uvx ty check
uvx pyrefly check .
```

# 감사합니다
기여해주시는 모든 분들에게 감사의 말씀을 전합니다! ⭐