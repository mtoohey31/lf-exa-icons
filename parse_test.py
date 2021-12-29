import helper
import lf_exa_icons


def test_versions() -> None:
    for version in helper.get_supported_versions():
        source = lf_exa_icons.fetch_source(version)
        icons = lf_exa_icons.parse_source(source)
        lf_exa_icons.format_icons(icons)
