import requests
import re


def test_versions() -> None:
    tags = requests.get('https://api.github.com/repos/ogham/exa/tags').json()
    minimum_version = 'v0.9.0-pre'
    minimum_version_int = int(re.sub(r'[^\d]', '', minimum_version))
    versions = [tag['name'] for tag in tags
                if int(re.sub(r'[^\d]', '', tag['name'])) > minimum_version_int]

    import lf_exa_icons

    for version in versions:
        source = lf_exa_icons.fetch_source(version)
        icons = lf_exa_icons.parse_source(source)
        lf_exa_icons.format_icons(icons)
