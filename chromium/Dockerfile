# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM="jlesage/baseimage-gui:alpine-3.20-v4"
ARG BUILD_ARCH=unknown
ARG BUILD_VERSION=dev

FROM ${BUILD_FROM}

LABEL \
  io.hass.version="${BUILD_VERSION}" \
  io.hass.type="addon" \
  io.hass.arch="${BUILD_ARCH}"

# Install chromium and socat
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

# Copy the start script.
COPY startapp.sh /startapp.sh

# Set the name of the application.
RUN set-cont-env APP_NAME "Chromium"