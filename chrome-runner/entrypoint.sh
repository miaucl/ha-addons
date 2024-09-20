#!/bin/sh
socat TCP-LISTEN:9223,fork TCP:127.0.0.1:9222 &
chromium --headless --disable-gpu --no-sandbox --remote-debugging-port=9222