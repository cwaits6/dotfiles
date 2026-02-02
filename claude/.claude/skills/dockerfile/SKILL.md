---
name: dockerfile
description: Creates production-ready Dockerfiles following strict security, size, and caching best practices. Use when the user asks to containerize an application, create a Dockerfile, or optimize an existing Dockerfile.
allowed-tools: Read, Grep, Glob, Bash(cat *), Bash(ls *)
argument-hint: "[project-path]"
---

# Production Dockerfile Skill

Generate production-ready, multi-stage Dockerfiles. Follow every rule below — no exceptions.

## Base Image Rules

- **Never use `latest` tags** except for `cgr.dev/chainguard/wolfi-base:latest`, which is the only permitted `latest` image.
- **Pin versions** derived from the project's config files (`package.json`, `go.mod`, `pyproject.toml`, `.python-version`, `Cargo.toml`, `pom.xml`).
- Pin to at least the minor version (e.g., `node:22-alpine`, `python:3.12-slim`).
- Use only official Docker images or Verified Publishers.
- Prefer minimal base images: Alpine, slim variants, distroless, scratch, or Chainguard images.
- Containers are not VMs — never use full distributions like `ubuntu` or `debian` as runtime bases.

## Multi-Stage Builds (mandatory)

Every Dockerfile MUST use multi-stage builds:

1. **Builder stage**: install dependencies, compile/build the application.
2. **Runtime stage**: copy only the built artifacts into a minimal base image.

Build tools, dev dependencies, package caches, and source code must never appear in the final image.

## Layer Ordering and Caching

Order layers from least to most frequently changed:

1. Base image
2. System packages (if any)
3. Dependency manifests (lock files)
4. Install dependencies
5. Configuration files
6. Application source code

**Combine RUN instructions** — cache cleanup must happen in the same `RUN` as installation so intermediate layers never contain caches.

**Never use `COPY . .`** in any stage. Always use explicit COPY statements:
```dockerfile
COPY package.json bun.lock ./
COPY src ./src
```
This prevents leaking secrets, `.git/`, and unnecessary files, and improves cache hit rates.

## Security Hardening

### Non-root execution (mandatory)
Create a dedicated user and group with UID/GID >= 10001 to avoid conflicts with system-reserved IDs:
```dockerfile
RUN addgroup --gid 10001 appgroup && \
    adduser --uid 10001 --ingroup appgroup --disabled-password --gecos "" appuser
USER appuser
```
If the base image provides a non-root user (e.g., `nginxinc/nginx-unprivileged`), use it.

### Binary ownership
Application binaries should be owned by root but executed by the non-root user. Use `COPY --chown=root:root` for binaries so compromised processes cannot modify them.

### No secrets in images
Never put credentials, API keys, tokens, or passwords in `ENV`, `ARG`, or `COPY` instructions. Use runtime secrets injection (mounted secrets, env vars from orchestrator, etc.).

### Forbidden in production images
- `sudo` — never install it
- Debug/network tools (`curl`, `wget`, `vim`, `netcat`, `telnet`) — use ephemeral debug containers instead
- Any package not strictly required to run the application

### Other security rules
- Always use `COPY`, never `ADD` (unless tar extraction is specifically required, and never with URLs).
- Use `--no-install-recommends` with `apt-get`.
- When installing system packages, alphabetize the list for clean diffs.

## CMD Format

Always use exec form (JSON array):
```dockerfile
CMD ["node", "server.js"]
```
Never use shell form — it wraps the process in `/bin/sh` which swallows SIGTERM and prevents graceful shutdown.

## Other Required Practices

- Always set `WORKDIR` — never use `RUN cd`.
- Add OCI labels: `org.opencontainers.image.source`, `org.opencontainers.image.description`.
- Comment non-obvious decisions (explain *why*, not *what*).
- Install only production dependencies — never include dev dependencies in the final image.
- Use `.dockerignore` if one doesn't exist — exclude `.git/`, `node_modules/`, `__pycache__/`, `.env`, etc.

---

## Language-Specific Defaults

Before generating a Dockerfile, detect the project type by looking for config files. Apply the matching language section below.

### Python (uv)

- **Package manager**: `uv` (always, no pip/poetry/pipenv)
- **Builder base**: `python:<version>-slim` or `cgr.dev/chainguard/wolfi-base:latest`
- **Runtime base**: `python:<version>-slim` or `cgr.dev/chainguard/wolfi-base:latest`
- **Version source**: `.python-version` or `pyproject.toml`

```dockerfile
# --- Builder ---
FROM python:3.12-slim AS builder
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src ./src
RUN uv sync --frozen --no-dev

# --- Runtime ---
FROM python:3.12-slim AS runtime
WORKDIR /app

RUN addgroup --gid 10001 appgroup && \
    adduser --uid 10001 --ingroup appgroup --disabled-password --gecos "" appuser

COPY --from=builder --chown=root:root /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

USER appuser
CMD ["python", "-m", "myapp"]
```

### Node.js (bun)

- **Package manager**: `bun` (always, no npm/yarn/pnpm)
- **Builder base**: `oven/bun:<version>-alpine`
- **Runtime base**: depends on output — `oven/bun:<version>-alpine` for server apps, `nginxinc/nginx-unprivileged:alpine` for static sites
- **Version source**: `package.json`, `.nvmrc`, `.node-version`

```dockerfile
# --- Builder ---
FROM oven/bun:1-alpine AS builder
WORKDIR /app

COPY package.json bun.lock ./
RUN bun install --frozen-lockfile --production

COPY src ./src
COPY tsconfig.json ./
RUN bun build ./src/index.ts --target=bun --outdir=./dist

# --- Runtime ---
FROM oven/bun:1-alpine AS runtime
WORKDIR /app

RUN addgroup --gid 10001 appgroup && \
    adduser --uid 10001 -G appgroup --disabled-password --gecos "" appuser

COPY --from=builder --chown=root:root /app/dist ./dist
COPY --from=builder --chown=root:root /app/node_modules ./node_modules

USER appuser
EXPOSE 3000
CMD ["bun", "run", "./dist/index.js"]
```

### Go

- **Package manager**: Go modules
- **Builder base**: `golang:<version>-alpine`
- **Runtime base**: `cgr.dev/chainguard/static:latest` or `scratch`
- **Version source**: `go.mod`
- Build with `CGO_ENABLED=0` for static binaries.

```dockerfile
# --- Builder ---
FROM golang:1.23-alpine AS builder
WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app/server ./cmd/server

# --- Runtime ---
FROM cgr.dev/chainguard/static:latest AS runtime

COPY --from=builder --chown=root:root /app/server /server

USER nonroot
EXPOSE 8080
CMD ["/server"]
```

### Rust

- **Package manager**: Cargo
- **Builder base**: `rust:<version>-slim` or `rust:<version>-alpine`
- **Runtime base**: `cgr.dev/chainguard/static:latest` or `scratch`
- **Version source**: `Cargo.toml`, `rust-toolchain.toml`
- Use `--release` and strip debug symbols.

```dockerfile
# --- Builder ---
FROM rust:1.83-slim AS builder
WORKDIR /app

COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs && \
    cargo build --release && \
    rm -rf src target/release/deps/myapp*

COPY src ./src
RUN cargo build --release --locked && \
    strip target/release/myapp

# --- Runtime ---
FROM cgr.dev/chainguard/static:latest AS runtime

COPY --from=builder --chown=root:root /app/target/release/myapp /myapp

USER nonroot
EXPOSE 8080
CMD ["/myapp"]
```

### Java

- **Build tool**: detect Maven (`pom.xml`) or Gradle (`build.gradle`/`build.gradle.kts`)
- **Builder base**: `eclipse-temurin:<version>-jdk-alpine`
- **Runtime base**: `eclipse-temurin:<version>-jre-alpine` or `cgr.dev/chainguard/jre:latest`
- **Version source**: `pom.xml`, `build.gradle`, `.java-version`, `.sdkmanrc`

```dockerfile
# --- Builder ---
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app

COPY pom.xml ./
COPY .mvn .mvn
COPY mvnw ./
RUN chmod +x mvnw && ./mvnw dependency:resolve

COPY src ./src
RUN ./mvnw package -DskipTests -q && \
    cp target/*.jar app.jar

# --- Runtime ---
FROM eclipse-temurin:21-jre-alpine AS runtime
WORKDIR /app

RUN addgroup --gid 10001 appgroup && \
    adduser --uid 10001 -G appgroup --disabled-password --gecos "" appuser

COPY --from=builder --chown=root:root /app/app.jar ./app.jar

USER appuser
EXPOSE 8080
CMD ["java", "-jar", "app.jar"]
```

---

## Workflow

1. Detect the project language from config files in the working directory.
2. Read the relevant config files to determine versions.
3. Generate the Dockerfile following all rules above with the matching language template.
4. Generate a `.dockerignore` if one does not already exist.
5. Explain any non-obvious decisions made.
