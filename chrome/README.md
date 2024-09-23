# Home Assistant Add-on: Chrome

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg

## Base container

The base container to run this Chrome addon is <https://github.com/jlesage/docker-baseimage-gui>, which allows to run (almost) any X capable application in a container and expose the gui via a noVNC int the browser. Props to [@jlesage](https://github.com/jlesage)!















This addon repackages the image `ghcr.io/zenika/alpine-chrome` from [Zenika/alpine-chrome](https://github.com/Zenika/alpine-chrome) as a home assistant addon.

Since version `108` of chrome (as discussed in those issues [#253](https://github.com/Zenika/alpine-chrome/issues/253), [#225](https://github.com/Zenika/alpine-chrome/issues/225), [#158](https://github.com/Zenika/alpine-chrome/issues/158)), the debug port only accepts connections from localhost. Therefore, `socat` has been packaged alongside to forward the traffic and make it available outside of the host (and thus accessible to the integrations).

### IP-Only

The chrome debugging port accepts only IP host headers and no DNS. Therefore, requests must be of the following form `ws://<X.X.X.X>:9222`.