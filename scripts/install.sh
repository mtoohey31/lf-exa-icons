#!/usr/bin/env bash

set -euo pipefail

if command -v curl; then
  curl -sSL "https://github.com/mtoohey31/lf-exa-icons/releases/download/$(exa --version | awk 'NR==2 { print $1 }')/icons" > ~/.config/lf/icons
elif command -v wget; then
  wget -qO ~/.config/lf/icons "https://github.com/mtoohey31/lf-exa-icons/releases/download/$(exa --version | awk 'NR==2 { print $1 }')/icons"
else
  1>&2 echo "could not find curl or wget, please install one and re-run"
  exit 1
fi

