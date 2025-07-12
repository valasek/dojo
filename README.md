# dojo

DOJO web site source files and assets.

## Used components

Pure HTML, Tailwind $ with a few CSS rules and a few lines of JavaScript for menu

## How to set up a project

Clone git repo

Install python

Install Tailwind. For example via [Standalone CLI: Use Tailwind CSS without Node.js](https://tailwindcss.com/blog/standalone-cli).

**Example for macOS arm64**
```bash
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-arm64
chmod +x tailwindcss-macos-arm64
```

*Note: Tailwind executable for macos is part of the repo and is used in `./scripts/publish.py` script. If use a diffrent Tailwind installation, update the script.*

Install any lite web server. Eg: Live server in VS Studio and in Live Server settings set root to `/public`

Set publish script as executable `chmod +x ./scripts/publish.py`

## Optimaze images

# Simple - process everything with defaults
./scripts/optimize.sh

# Custom quality (75 = smaller files)
./scripts/optimize.sh "" "" 75

# Different input folder
./scripts/optimize.sh /path/to/other/images

## How to start locally

Start live web server

Build all pages via `./scripts/publish.py`

Access page on http://127.0.0.1:5500
