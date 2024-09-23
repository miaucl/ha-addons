#!/bin/sh

# Symbolic links for persistent storage on HA
if [ ! -d "/data" ]; then
  mkdir -p /data
fi

if [ ! -d "/data/profile" ]; then
  mv /config/profile /data
else
  rm -rf /config/profile
fi
ln -s /data/profile /config/profile

if [ ! -d "/share/chromium" ]; then
  mkdir -p /share/chromium
fi
rm -rf /config/downloads

ln -s /share/chromium /config/downloads

# Cleanup
if ! pgrep chromium > /dev/null;then
  rm -f $HOME/.config/chromium/Singleton*
fi

# Start port forwarding
socat TCP-LISTEN:9223,fork TCP:127.0.0.1:9222 &

# Start chromium
exec /usr/bin/chromium-browser --disable-software-rasterizer --disable-dev-shm-usage --disable-gpu --ignore-gpu-blocklist --no-first-run --password-store=basic --user-data-dir=/tmp/chromium-profile --start-maximized --remote-debugging-port=9222 --remote-debugging-address=0.0.0.0