# rastro

projeto experimental para testar a instrumentação do django com opentelemetry.
project to experiment setting up the complete grafana stack + opentelemetry with django.

## checking

```sh
uv run ruff check src/
uv run mypy src/
uv run pytest --cov=src/
uv run python manage.py check
```
