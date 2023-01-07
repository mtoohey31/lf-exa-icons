import lf_exa_icons
import requests
import re
from unittest import TestCase, main

def get_supported_versions() -> list[str]:
    tags = requests.get('https://api.github.com/repos/ogham/exa/tags').json()
    minimum_version = 'v0.9.0-pre'
    minimum_version_int = int(re.sub(r'[^\d]', '', minimum_version))
    return [tag['name'] for tag in tags
                if int(re.sub(r'[^\d]', '', tag['name'])) > minimum_version_int]

class VersionsTestCase(TestCase):
    def test_versions(self) -> None:
        for version in get_supported_versions():
            source = lf_exa_icons.fetch_source(version)
            icons = lf_exa_icons.parse_source(source)
            lf_exa_icons.format_icons(icons)
