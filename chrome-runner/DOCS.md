# Home Assistant Add-on: Chrome Runner

Source Documentation is found here: <https://github.com/Zenika/alpine-chrome>

## How to use

--> Using the devtools setup of the [Zenika/alpine-chrome README.md](https://github.com/Zenika/alpine-chrome?tab=readme-ov-file#use-the-devtools).

An equivalent of following command is launched: `docker container run -d -p 9222:9222 zenika/alpine-chrome --no-sandbox --remote-debugging-address=0.0.0.0 --remote-debugging-port=9222 https://www.chromestatus.com/`

Open your browser to: `http://localhost:9222` and then click on the tab you want to inspect. Replace the beginning
`https://chrome-devtools-frontend.appspot.com/serve_file/@.../inspector.html?ws=localhost:9222/[END]`
by
`chrome-devtools://devtools/bundled/inspector.html?ws=localhost:9222/[END]`

### Example

Using python and playwright, following snippet leverages the addons capability to serve as a remote web runner. This functionality can be used ad hoc or within an integration of course. The addon requires to be addressed by its IP, which is why we pre-resolve it in this snipped.

`pip install playwright`

```python
import asyncio
import time
from playwright.async_api import async_playwright
import socket
import re

# Set the remote addr
remote = 'homeassistant.local'    # Use in case of mdns local domain
# remote = 'homeassistant.home'   # Use in case of private DNS server
# remote = '192.168.1.36'         # Use in case of direct IP
# remote = 'localhost'            # Use in case of running directly inside the addon

port = "9222"

# Regex match for IP address
ipv4_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')

def resolve_remote_addr(addr):
  """Resolve the DNS entries."""
  return addr if addr == 'localhost' or ipv4_pattern.match(addr) else socket.gethostbyname(addr)

async def main():
  async with async_playwright() as p:
    browser = await p.chromium.connect_over_cdp(f"http://{resolve_remote_addr(remote)}:{port}")
    page = await browser.new_page()
    await page.goto('http://playwright.dev')
    await page.screenshot(path=f'demo.png')
    await browser.close()

asyncio.run(main())
```
