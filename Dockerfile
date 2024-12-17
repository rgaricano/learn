ARG UID=1000
ARG GID=1000

FROM --platform=$BUILDPLATFORM node:22-alpine3.20 AS build
ARG BUILD_HASH

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
ENV APP_BUILD_HASH=${BUILD_HASH}
RUN npm run build

######## WebUI backend ########
FROM python:3.11-slim-bookworm AS base


## Basis ##
ENV ENV=prod \
    PORT=13456 \
    DOCKER=true \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    OPENAI_API_KEY=""


WORKDIR /app/backend

# Install essential system dependencies for Python and cleanup afterward
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl jq && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


RUN pip3 install uv && \
    uv pip install --system -r requirements.txt --no-cache-dir

# copy built frontend files
COPY --from=build /app/build /app/build
COPY --from=build /app/CHANGELOG.md /app/CHANGELOG.md
COPY --from=build /app/package.json /app/package.json

# copy backend files
COPY ./backend .

EXPOSE 13456

HEALTHCHECK CMD curl --silent --fail http://localhost:${PORT:-13456}/health | jq -ne 'input.status == true' || exit 1

# Run the application as a non-root user
RUN groupadd --gid $GID appgroup && \
    useradd --uid $UID --gid $GID --no-log-init --create-home appuser
USER appuser


CMD [ "bash", "start.sh"]
