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
        dwm \
        iproute2 \
        iputils-ping \
        kmod \
        libcap2-bin \
        libqt5core5a \
        libqt5gui5 \
        libqt5network5 \
        libqt5serialport5 \
        libqt5sql5 \
        libqt5websockets5 \
        libqt5widgets5 \
        libqt5qml5 \
        lsof \
        netcat-traditional \
        nginx \
        novnc \
        sqlite3 \
        tigervnc-common \
        tigervnc-standalone-server \
        udev \
        wget \
        xfonts-base \
        xfonts-scalable \
        x11vnc \
        xvfb \
        xterm \
    && rm -rf /var/lib/apt/lists/*

COPY rootfs /
