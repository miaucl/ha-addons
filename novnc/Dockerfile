ARG BUILD_FROM
FROM $BUILD_FROM

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install noVNC dependencies
ARG BUILD_ARCH
RUN \
    set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        git \
        net-tools \
        nginx \
        novnc \
        xfonts-base \
        xfonts-scalable \
        x11vnc \
        xvfb \
        fluxbox \
        xterm \
        supervisor \
    && rm -rf /var/lib/apt/lists/*

ENV HOME=/root \
    DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    LC_ALL=C.UTF-8 \
    DISPLAY=:0.0 \
    DISPLAY_WIDTH=1024 \
    DISPLAY_HEIGHT=768

COPY rootfs /
COPY app /app
ENTRYPOINT "/app/entrypoint.sh"

CMD ["bash", "-c", "echo 'Running my app'; sleep infinity"]