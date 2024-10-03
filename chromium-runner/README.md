# Home Assistant Add-on: Chromium Runner

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg

[![GitHub](https://img.shields.io/badge/sponsor-30363D?style=for-the-badge&logo=GitHub-Sponsors&logoColor=#EA4AAA)](https://github.com/sponsors/miaucl)
[![Patreon](https://img.shields.io/badge/Patreon-F96854?style=for-the-badge&logo=patreon&logoColor=white)](https://patreon.com/miaucl)
[![BuyMeACoffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/miaucl)
[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/sponsormiaucl)

This addons lets you use a headless chromium browser for automation, through the debugging port `9222`.

**! As it is for testing and automation, this addons does NOT persist your chromium settings and profiles !**

If you need to see live what is happening in the chromium browser, have a look at the [chromium addon](https://github.com/miaucl/ha-addons/tree/main/chromium), which is a lot heavier, but provides a graphical view.

## Credits

The `Dockerfile` of the image to run this Chromium runner addon is heavily based on <https://github.com/Zenika/alpine-chrome> by [@Zenika](https://github.com/Zenika), but has been decoupled and aligned with the [Chromium addon](./chromium). A huge thank to him for the great work.

Since version `108` of chromium (as discussed in those issues [#253](https://github.com/Zenika/alpine-chrome/issues/253), [#225](https://github.com/Zenika/alpine-chrome/issues/225), [#158](https://github.com/Zenika/alpine-chrome/issues/158)), the debug port only accepts connections from localhost. Therefore, `socat` has been packaged alongside to forward the traffic and make it available outside of the host (and thus accessible to the integrations).

### IP-Only

The chromium debugging port accepts only IP host headers and no DNS. Therefore, requests must be of the following form `ws://<X.X.X.X>:9222`.

### CPU-Only

This chromium installation uses `chromium-swiftshader` to emulate the GPU if required, as it is designed to be run in virtualized environments.
