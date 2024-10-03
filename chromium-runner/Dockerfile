# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM="alpine:3.20"
ARG BUILD_ARCH=unknown
ARG BUILD_VERSION=dev

FROM ${BUILD_FROM}

LABEL \
  io.hass.version="${BUILD_VERSION}" \
  io.hass.type="addon" \
  io.hass.arch="${BUILD_ARCH}"

# Installs latest Chromium package.
RUN apk upgrade --no-cache --available \
    && apk add --no-cache \
      chromium-swiftshader \
      ttf-freefont \
      font-noto-emoji \
      socat \
    && apk add --no-cache \
      --repository=https://dl-cdn.alpinelinux.org/alpine/edge/community \
      font-wqy-zenhei

COPY local.conf /etc/fonts/local.conf

# Add Chromium as a user
RUN mkdir -p /usr/src/app \
    && adduser -D chromium \
    && chown -R chromium:chromium /usr/src/app
# Run Chromium as non-privileged
USER chromium
WORKDIR /usr/src/app

ENV CHROME_BIN=/usr/bin/chromium-browser \
    CHROME_PATH=/usr/lib/chromium/


COPY ./entrypoint.sh /entrypoint.sh

ENTRYPOINT /entrypoint.sh
    