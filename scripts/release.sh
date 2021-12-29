#!/bin/bash

set -e

existing_releases="$(gh release list | awk '{ print $1 }')"

for version in $(python3 -c 'from helper import get_supported_versions; print(" ".join(get_supported_versions()))'); do
  if test "${existing_releases#*$version}" == "$existing_releases"; then
    python3 -c "from lf_exa_icons import fetch_source, parse_source, format_icons; source = fetch_source(\"$version\"); icons = parse_source(source); print(format_icons(icons))" > icons
    gh release create "$version" icons
  fi
done

