# Home Assistant Add-on: Chrome

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg

[![GitHub](https://img.shields.io/badge/sponsor-30363D?style=for-the-badge&logo=GitHub-Sponsors&logoColor=#EA4AAA)](https://github.com/sponsors/miaucl)
[![Patreon](https://img.shields.io/badge/Patreon-F96854?style=for-the-badge&logo=patreon&logoColor=white)](https://patreon.com/miaucl)
[![BuyMeACoffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/miaucl)
[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/sponsormiaucl)

This addons lets you open a Chrome browser inside Home Assistant using ingress [see limitations](#ingress-ssl-only). It is intended for testing and automation, which is why there is a debugging port `9222` which can be opened in the configuration panel and also ports for direct access to the noVNC `5800` and xVNC `5900` services.

**! As it is for testing and automation, this addons does NOT persist your chrome settings and profiles !**

If you are developing web automation, this is a great tool. But once you are done, you might be interested by the lighter [chrome runner addon](https://github.com/miaucl/ha-addons/tree/main/chrome), which provides simple a headless chrome browser with a debugging port.

## Credits

The base image to run this Chrome addon is <https://github.com/jlesage/docker-baseimage-gui> by [@jlesage](https://github.com/jlesage), which allows to run (almost) any X capable application in a container and expose the gui via noVNC in the browser. A huge thank to him for the great containers created and maintained. He's the real hero who needs to be [supported](https://github.com/sponsors/jlesage).

Since version `108` of chrome (as discussed in those issues [#253](https://github.com/Zenika/alpine-chrome/issues/253), [#225](https://github.com/Zenika/alpine-chrome/issues/225), [#158](https://github.com/Zenika/alpine-chrome/issues/158)), the debug port only accepts connections from localhost. Therefore, `socat` has been packaged alongside to forward the traffic and make it available outside of the host (and thus accessible to the integrations).

### Ingress SSL-Only

To access the ingress page for the GUI, `SSL` is **required** and your server should be accessible over `https`. If you do not have this option, there are two fallback ports which can be opened (go to the Configuration panel), and one for direct access to the noVNC via port `5800` and one for direct access to the xVNC `5900`.

### IP-Only

The chrome debugging port accepts only IP host headers and no DNS. Therefore, requests must be of the following form `ws://<X.X.X.X>:9222`.
