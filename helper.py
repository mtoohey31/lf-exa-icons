import requests
import re

def get_supported_versions() -> list[str]:
    tags = requests.get('https://api.github.com/repos/ogham/exa/tags').json()
    minimum_version = 'v0.9.0-pre'
    minimum_version_int = int(re.sub(r'[^\d]', '', minimum_version))
    return [tag['name'] for tag in tags
                if int(re.sub(r'[^\d]', '', tag['name'])) > minimum_version_int]
