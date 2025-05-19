# dojo

DOJO web site

## Used components

Pure HTML, Tailwind $ with a few CSS rules and a few lines of JavaScript for menu

## How to set up a project

Clone git repo
Install python
Install Tailwind. For example via [Standalone CLI: Use Tailwind CSS without Node.js](https://tailwindcss.com/blog/standalone-cli).

# Example for macOS arm64
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-arm64
chmod +x tailwindcss-macos-arm64
mv tailwindcss-macos-arm64 tailwindcss

## How to start locally

Use web server. Eg: Live server in VS Studio
In Live Server settings set root to /public
Access page on http://127.0.0.1:5500

### How to publish a page

chmod +x ./scripts/publish.py
./scripts/publish.py
