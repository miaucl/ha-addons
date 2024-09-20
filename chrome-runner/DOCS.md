# Home Assistant Add-on: Chrome Runner

Source Documentation is found here: <https://github.com/Zenika/alpine-chrome>

## How to use

--> Using the devtools setup of the [Zenika/alpine-chrome README.md](https://github.com/Zenika/alpine-chrome?tab=readme-ov-file#use-the-devtools).

An equivalent of following command is launched: `docker container run -d -p 9222:9222 zenika/alpine-chrome --no-sandbox --remote-debugging-address=0.0.0.0 --remote-debugging-port=9222 https://www.chromestatus.com/`

Open your browser to: `http://localhost:9222` and then click on the tab you want to inspect. Replace the beginning
`https://chrome-devtools-frontend.appspot.com/serve_file/@.../inspector.html?ws=localhost:9222/[END]`
by
`chrome-devtools://devtools/bundled/inspector.html?ws=localhost:9222/[END]`
