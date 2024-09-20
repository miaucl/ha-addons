# Home Assistant Add-on: Chrome Runner

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg

## Base container

This addon repackages the image `ghcr.io/zenika/alpine-chrome` from [Zenika/alpine-chrome](https://github.com/Zenika/alpine-chrome) as a home assistant addon.

Since version `108` of chrome (as discussed in those issues [#253](https://github.com/Zenika/alpine-chrome/issues/253), [#225](https://github.com/Zenika/alpine-chrome/issues/225), [#158](https://github.com/Zenika/alpine-chrome/issues/158)), the debug port only accepts connections from localhost. There a nginx with websocket port forwarding has been packaged alongside to forward the traffic and make it available outside of the host (and thus accessible to the integrations).
