FROM python:3.11-slim-bookworm
WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive

# Use HTTPS mirrors; remove default deb822 to avoid duplicate/stale entries
RUN set -eux; \
  rm -rf /var/lib/apt/lists/*; \
  rm -f /etc/apt/sources.list.d/debian.sources; \
  printf 'deb https://deb.debian.org/debian bookworm main\n\
deb https://deb.debian.org/debian bookworm-updates main\n\
deb https://security.debian.org/debian-security bookworm-security main\n' > /etc/apt/sources.list; \
  # (Optional) work around expired metadata / bad proxies. Remove if not needed.
  printf 'Acquire::Retries "5";\nAcquire::Check-Valid-Until "false";\nAcquire::Check-Date "false";\nAcquire::http::No-Cache "true";\nAcquire::https::No-Cache "true";\n' \
    > /etc/apt/apt.conf.d/99apt-net; \
  apt-get update; \
  apt-get install -y --no-install-recommends build-essential ca-certificates; \
  rm -rf /var/lib/apt/lists/*

COPY shared /app/shared
RUN pip install -e /app/shared
COPY worker /app/worker
RUN pip install -e /app/worker
