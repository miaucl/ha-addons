#!/bin/sh
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

INGRESS_ENTRY=${INGRESS_ENTRY:-/}

sed -i "s#websockify#${INGRESS_ENTRY#?}/novnc/websockify#g" /usr/share/novnc/vnc_lite.html
sed -i '/^\s*allow\s*172\.30\.32\.2\s*;/d; /^\s*deny\s*all\s*;/d' /etc/nginx/nginx.conf

exec supervisord -c /app/supervisord.conf