# Home Assistant Add-on: Chrome Runner

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg

This addons lets you use a headless chrome browser for automation, through the debugging port `9222`.

**! As it is for testing and automation, this addons does NOT persist your chrome settings and profiles !**

If you need to see live what is happening in the chrome browser, have a look at the [chrome addon](https://github.com/miaucl/ha-addons/tree/main/chrome), which is a lot heavier, but provides a graphical view.

## Credits

The `Dockerfile` of the image to run this Chrome runner addon is heavily based on <https://github.com/Zenika/alpine-chrome> by [@Zenika](https://github.com/Zenika), but has been decoupled and aligned with the [Chrome addon](./chrome). A huge thank to him for the great work.

Since version `108` of chrome (as discussed in those issues [#253](https://github.com/Zenika/alpine-chrome/issues/253), [#225](https://github.com/Zenika/alpine-chrome/issues/225), [#158](https://github.com/Zenika/alpine-chrome/issues/158)), the debug port only accepts connections from localhost. Therefore, `socat` has been packaged alongside to forward the traffic and make it available outside of the host (and thus accessible to the integrations).

### IP-Only

The chrome debugging port accepts only IP host headers and no DNS. Therefore, requests must be of the following form `ws://<X.X.X.X>:9222`.
