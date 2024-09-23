# Home Assistant Add-on: Chrome

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg

## Base container

The base container to run this Chrome addon is <https://github.com/jlesage/docker-baseimage-gui> by [@jlesage](https://github.com/jlesage), which allows to run (almost) any X capable application in a container and expose the gui via noVNC in the browser. A huge thank to him for the great containers created and maintained. He's the real hero who needs to be [supported](https://github.com/sponsors/jlesage).

Since version `108` of chrome (as discussed in those issues [#253](https://github.com/Zenika/alpine-chrome/issues/253), [#225](https://github.com/Zenika/alpine-chrome/issues/225), [#158](https://github.com/Zenika/alpine-chrome/issues/158)), the debug port only accepts connections from localhost. Therefore, `socat` has been packaged alongside to forward the traffic and make it available outside of the host (and thus accessible to the integrations).

### Ingress SSL-Only

To access the ingress page for the GUI, `SSL` is **required** and your server should be accessible over `https`. If you do not have this option, there are two fallback ports which can be opened (go to the Configuration panel), and one for direct access to the noVNC via port `5800` and one for direct access to the xVNC `5900`.

### IP-Only

The chrome debugging port accepts only IP host headers and no DNS. Therefore, requests must be of the following form `ws://<X.X.X.X>:9222`.
