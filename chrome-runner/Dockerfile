# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM="zenika/alpine-chrome:latest"
ARG BUILD_ARCH=unknown
ARG BUILD_VERSION=dev

FROM ${BUILD_FROM}

LABEL \
  io.hass.version="${BUILD_VERSION}" \
  io.hass.type="addon" \
  io.hass.arch="${BUILD_ARCH}"


CMD ["--no-sandbox", "--remote-debugging-address=0.0.0.0", "--remote-debugging-port=9222"]