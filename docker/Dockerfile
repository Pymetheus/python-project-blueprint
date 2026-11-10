# This Dockerfile was generated for [[PACKAGE_NAME]]

FROM ghcr.io/astral-sh/uv:0.13.7-python3.15-trixie-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-install-project

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-editable


FROM python:3.15-slim-trixie AS runtime

RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

WORKDIR /app

COPY --from=builder --chown=nonroot:nonroot /app /app

ARG APP_ENV=DEV
ENV APP_ENV=$APP_ENV
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

USER nonroot

CMD ["DISTRIBUTION-NAME"]
