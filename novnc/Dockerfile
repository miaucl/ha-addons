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
    && rm -rf /var/lib/apt/lists/*

COPY rootfs /
