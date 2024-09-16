#!/usr/bin/with-contenv bashio
set -ex

RUN_FLUXBOX=${RUN_FLUXBOX:-yes}
RUN_XTERM=${RUN_XTERM:-yes}

case $RUN_FLUXBOX in
  false|no|n|0)
    rm -f /app/conf.d/fluxbox.conf
    ;;
esac

case $RUN_XTERM in
  false|no|n|0)
    rm -f /app/conf.d/xterm.conf
    ;;
esac

declare ingress_entry
ingress_entry=$(bashio::addon.ingress_entry)
echo $ingress_entry
sed -i "s#websockify#${ingress_entry#?}/novnc/websockify#g" /usr/share/novnc/vnc_lite.html
cat /usr/share/novnc/vnc_lite.html

exec supervisord -c /app/supervisord.conf