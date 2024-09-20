#!/bin/sh
echo "Starting port forwarding"
nginx
echo "Starting chromium"
su chrome
chromium --headless=new --disable-gpu --no-sandbox --remote-debugging-port=9222